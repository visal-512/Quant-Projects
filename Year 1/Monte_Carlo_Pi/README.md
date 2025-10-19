# Monte Carlo Simulation to Estimate the Value of π

## Overview

This project demonstrates the estimation of π using a Monte Carlo simulation. The simulation randomly generates points in a unit square and calculates the proportion that fall inside a quarter circle.

## Features

- Interactive Visualisation:
  - Left plot: scatter of random points (inside/outside the circle).
  - Right plot: π estimate vs number of points, with dynamic scaling.
- Error Analysis with CLT Comparison:
  - Logarithmic Plot of absolute error vs. number of points.
  - Compares this plot to $\frac{1}{sqrt{N}}$ from the Central Limit Theorem
  - Supports reusing simulation data for analysis or randomly generates a plot.
- Reproducibility: Random Seed Support to Ensure Consistent Results if desired.
- Customisable Paramaters:
  - `--limit`: total number of points being simulated
  - `--interval`: visualisation update interval
  - `--seed`: random seed
  - `--analysis`: run error analysis only
  - `--reuse`: reuse simulation data for analysis

## Installation & Usage

This project requires Python 3.9+ and some packages which can be downloaded by running the code below in the terminal:

```bash
pip install numpy matplotlib
```

1. Run Simulation:

  ```bash
  python simulation.py --limit 50000 --interval 2000 --seed 42
  ```
  This command runs the simulation for a limit of 50000 points and updates the graph every 2000 points. It also sets the generated data to the seed 42.

2. Run Error Analysis & Simulation:

  ```bash
  python simulation.py --analysis --reuse --limit 50000 --interval 2000 --seed 42
  ```
  This command runs the simulation with the same paramters as the one above, and then runs the error analysis for the same set of data.

## Mathematics Behind the Code

### Simulation:

Consider a unit square in the first quadrant, i.e. for coordinates $(x,y)$:

$$
0 \le x \le 1, \text{ and } 0 \le y\le 1
$$

We draw a quarter circle in that square which has radius of one and one that is centered at the origin $(0,0)$.
The area of the square and the quarter cirlce are as follows:

$$
A_{square} = r^2 = 1, \text{ and } A_{circle} = \frac{\pi r^2}{4} = \frac{\pi}{4}
$$

and by geometric probability, we cam say that:

$$
p = \mathbb{P}(\text{generating a point inside the circle}) = \frac{A_{circle}}{A_{square}} = \frac{\pi}{4}
$$

and from this we can see that $\pi \sim 4p$ as $N \rightarrow \infty$.

## References

1. https://en.wikipedia.org/wiki/Monte_Carlo_method
2. https://en.wikipedia.org/wiki/Markov_chain_central_limit_theorem
3. https://www.youtube.com/watch?v=6QVksCZ0ml8
