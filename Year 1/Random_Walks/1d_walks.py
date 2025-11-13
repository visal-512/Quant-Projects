import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import argparse

plt.style.use('dark_background')

## Algorithm for the position after n steps in the walk
def random_walk_1d(n_steps):
    # Generate random steps of ±1 with equal probability
    steps = np.random.choice([1, -1], size = n_steps)

    position = np.cumsum(steps) # cumulative sum gives final position after n steps
    position = np.insert(position, 0, 0)  # make starting point the origin

    return position

## Find the final positions of multiple walks
def end_positions(num_walks, n_steps):
    final_positions = []
    
    for _ in range(num_walks):
        walk = random_walk_1d(n_steps) # generate a random walk
        final_positions.append(walk[-1]) # find the last element in the position array and append to the final position array
    
    return np.array(final_positions) # return the final positions

## Plot the graphs
def plot_walks(num_walks, n_steps):
    # Generate data
    single_walk = random_walk_1d(n_steps)
    final_positions = end_positions(num_walks, n_steps)
    # Create plot
    plt.figure(figsize=(12,6)) # dimensions 12in x 5in
    # Plot the single walk
    plt.subplot(1, 2, 1) # plot the graph on the left
    plt.plot(single_walk, color="#1A80BB") # assign the data values the colour blue
    plt.title(f"Single 1D Random Walk ({n_steps} steps)")
    plt.xlabel("# Steps")
    plt.ylabel("Position")
    plt.grid(True)
    # Plot the Histogram
    plt.subplot(1, 2, 2) # plt the graph on the right
    plt.hist(final_positions,   # what data are we using
             bins = 50,         # how many bars are there
             density = True,    # area under the histogram = 1
             alpha = 1.00,      # opacity of the bars
             color = "#A00000", label = "Final Positions")
    # Overlap Normal Distribution Curve
    x_values = np.linspace(min(final_positions), max(final_positions), 250) # creates 250 evenly spaced points from the range of the final_positions
    pdf = norm.pdf(x_values, 0, np.sqrt(n_steps)) # P.D.F. with N(0, √N) for the data from x_values
    plt.plot(x_values, pdf, color = "#1A80BB", lw = 2.5, label = "N(0, √N)")
    plt.title(f"Distribution of End Positions of {num_walks} Random Walks")
    plt.xlabel("Final Positions")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True)

    plt.show() # Render graph

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_walks", type=int, default=1000, help="Number of Random Walks")
    parser.add_argument("--num_steps", type=int, default=2000, help="Number of Steps in Each Walk")

    args = parser.parse_args()
    print(f"Simulating {args.num_walks} walks, each with {args.num_steps} steps:")
    plot_walks(args.num_walks, args.num_steps)

if __name__ == "__main__":
    main()
