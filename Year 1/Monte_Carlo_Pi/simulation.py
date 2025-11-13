import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.ticker import ScalarFormatter
import argparse

# Monte Carlo Main Function
def monte_carlo_pi(simulation_limit, update_interval, seed):
    
    if seed is not None:
        np.random.seed(seed)
        print(f"[INFO] Random seed set to {seed} for reproducibility.")
    else:
        print("[INFO] No seed provided. Using random initialization.")

    # Monte Carlo Sampling
    x = np.random.uniform(0, 1, simulation_limit)
    y = np.random.uniform(0, 1, simulation_limit)
    r = np.sqrt(x**2 + y**2)
    inside = r <= 1

    # Progressive π estimates and error values
    pi_estimates = 4 * np.cumsum(inside) / np.arange(1, simulation_limit + 1)
    error_values = 100 * np.abs(pi_estimates - np.pi) / np.pi  # Percent error

    # Setup of Plot
    plt.style.use("dark_background")
    fig, axis = plt.subplots(1, 2, figsize=(10, 5))
    fig.canvas.manager.set_window_title("Monte Carlo Simulation for Estimation of π")

    # Graph on the Left
    axis[0].set_title('Randomly Generated Dots')
    axis[0].set_aspect('equal', 'box')
    axis[0].set_xlim([0, 1])
    axis[0].set_ylim([0, 1])
    circle = Circle((0, 0), 1, fill=False, color="#000000", linewidth=1.5, linestyle="--")
    axis[0].add_patch(circle)

    # Graph on the Right
    axis[1].set_title('Approximating π')
    axis[1].set_xlim([0, update_interval])
    axis[1].set_ylim([2, 4])
    axis[1].grid(True)
    axis[1].axhline(np.pi, color="#A00000", linewidth=1.5, label="True π")
    axis[1].set_xlabel('Number of Points (N)')

    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-3, 4))
    axis[1].xaxis.set_major_formatter(formatter)

    scatter = axis[0].scatter([], [], s=0.5)
    plot, = axis[1].plot([], [], "#1A80BB", label="Estimate", linewidth=1)
    axis[1].legend()

    for n in range(update_interval, simulation_limit + 1, update_interval):
        scatter.set_offsets(np.column_stack((x[:n], y[:n])))
        scatter.set_facecolors(np.where(inside[:n], "#1A80BB", "#A00000"))
        plot.set_data(np.arange(1, n + 1), pi_estimates[:n])

        # Dynamic scaling
        if n > axis[1].get_xlim()[1] - update_interval:
            axis[1].set_xlim([0, n + update_interval])

        recent_slice = pi_estimates[max(0, n - update_interval):n]
        min_y, max_y = np.min(recent_slice), np.max(recent_slice)
        new_ylim = [min_y - 0.05, max_y + 0.05]
        prev_ylim = axis[1].get_ylim()
        smooth_ylim = [
            (1 - 0.2) * prev_ylim[0] + 0.2 * new_ylim[0],
            (1 - 0.2) * prev_ylim[1] + 0.2 * new_ylim[1],
        ]
        axis[1].set_ylim(smooth_ylim)

        current_pi = pi_estimates[n - 1]
        current_error = error_values[n - 1]
        axis[0].set_title(f"Dots in Circle: {inside[:n].sum()} / {n}")
        axis[1].set_title(f"π ≈ {current_pi:.6f}  |  Error: {current_error:.4f}%")

        plt.pause(0.001)

    plt.show()

    # Return data for reuse if needed
    return x, y, inside, pi_estimates

# Error Analysis Function
def error_analysis(seed, x, y, inside, pi_estimates):
    
    if seed is not None:
        np.random.seed(seed)
        print(f"[INFO] Random seed set to {seed} for reproducibility.")

    if x is not None and y is not None and inside is not None and pi_estimates is not None:
        print("[INFO] Reusing simulation data for error analysis.")
        # Create multiple sample sizes from the existing data
        N_values = np.logspace(2, np.log10(len(pi_estimates)), 20, dtype=int)
        errors = [abs(pi_estimates[n-1] - np.pi) for n in N_values]
    else:
        print("[INFO] Running new Monte Carlo error analysis...")
        # Multiple sample sizes from 1e2 to 1e7
        N_values = np.logspace(2, 7, 20, dtype=int)
        errors = []
        for N in N_values:
            x_sample = np.random.uniform(-1, 1, N)
            y_sample = np.random.uniform(-1, 1, N)
            inside_circle = x_sample**2 + y_sample**2 <= 1
            pi_est = 4 * np.mean(inside_circle)
            errors.append(abs(pi_est - np.pi))

    # Theoretical CLT reference: 1/sqrt(N), scaled to match first error
    ref_line = 1 / np.sqrt(N_values)
    ref_line *= errors[0] / ref_line[0]

    # Plot log-log
    plt.figure(figsize=(8, 6))
    plt.loglog(N_values, errors, 'o', label='Monte Carlo Error', linewidth=2)
    plt.loglog(N_values, ref_line, '--', label=r'$1/\sqrt{N}$ CLT Reference', linewidth=2)
    plt.title("Monte Carlo π Estimation Error vs Sample Size (CLT Comparison)", fontsize=14)
    plt.xlabel("Number of Samples (N)")
    plt.ylabel("Absolute Error |π_est - π|")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=25000, help="Total number of random points to simulate")
    parser.add_argument("--interval", type=int, default=1000, help="Update interval for visualization")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--analysis", action="store_true", help="Run error analysis instead of simulation")
    parser.add_argument("--reuse", action="store_true", help="Reuse simulation data for error analysis")

    args = parser.parse_args()

    if args.analysis and args.reuse:
        # Run simulation first and reuse data
        x, y, inside, pi_estimates = monte_carlo_pi(simulation_limit=args.limit,
                                                    update_interval=args.interval,
                                                    seed=args.seed)
        error_analysis(x=x, y=y, inside=inside, pi_estimates=pi_estimates, seed=args.seed)
    elif args.analysis:
        # Run error analysis independently
        error_analysis(seed=args.seed)
    else:
        # Run normal simulation
        monte_carlo_pi(simulation_limit=args.limit,
                       update_interval=args.interval,
                       seed=args.seed)

if __name__ == "__main__":
    main()
