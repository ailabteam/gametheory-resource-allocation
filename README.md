# Resource Allocation Simulation using Contract Theory

## Overview

This project is a Python-based simulation that models a resource allocation problem under asymmetric information, applying concepts from **Contract Theory**. It analyzes a scenario where a single provider (the "Principal") allocates a divisible resource (e.g., satellite bandwidth) to multiple consumers (the "Agents").

The core challenge is that the Principal does not know the "type" of each Agent. Agents can be of different types (e.g., high-efficiency or low-efficiency), and this private information may lead them to misrepresent their needs. The goal of this project is to design and evaluate a mechanism that incentivizes Agents to reveal their true type, allowing the Principal to make optimal allocation decisions.

The simulation compares the performance of the proposed **Contract Theory** model against two baseline scenarios: a **Centralized** (theoretically optimal) model and a naive **Equal Allocation** model.

**Note:** The source code and its internal comments are written in Vietnamese.

## The Scenario: Satellite Bandwidth Allocation

The simulation is framed within a techno-economic model of a satellite communications system:
-   **The Principal:** A satellite operator who possesses a certain amount of total bandwidth. The Principal incurs a quadratic cost for allocating more bandwidth.
-   **The Agents:** Terrestrial Operators (TOs) who want to purchase bandwidth from the satellite operator to serve their own users.
-   **Agent Types:** Each TO has an intrinsic "efficiency" (`theta`) in how effectively they can use the bandwidth. This `theta` is private information. In this simulation, there are two types: `high-efficiency` and `low-efficiency`.
-   **Utility:**
    -   An Agent's utility is based on a logarithmic function of the bandwidth they receive (`theta * log(1 + R)`) minus the payment (`P`) they make to the Principal.
    -   The Principal's utility is the payment received (`P`) minus the cost of providing the resource (`cost(R)`).

## Models & Scenarios Compared

The simulation implements and compares three different allocation mechanisms:

1.  **Contract Theory (Principal-Agent Model):** This is the core proposal. The Principal, knowing the possible Agent types and their probabilities but not the type of any specific agent, designs a "menu of contracts". Each contract is a pair of `(Resource, Payment)`. The menu is optimized to maximize the Principal's expected utility while satisfying two key constraints:
    -   **Individual Rationality (IR):** Agents must have a non-negative utility from accepting the contract designed for their type.
    -   **Incentive Compatibility (IC):** Agents must prefer the contract designed for their own type over any other contract on the menu.

2.  **Centralized (Social Planner):** This is a theoretical benchmark that assumes a "first-best" world. A central planner, who knows the true type of every agent, allocates resources to maximize the *total social welfare* (sum of all agents' benefits minus the Principal's cost). This scenario is typically not achievable in practice due to information asymmetry but serves as an upper bound for system efficiency.

3.  **Equal Allocation (Naive Baseline):** This is a simple, naive approach where the Principal divides the total available bandwidth equally among all requesting agents, without any regard for their type or efficiency.

## Prerequisites

To run the simulation, you need Python 3 and the following libraries:
-   `numpy`
-   `pandas`
-   `matplotlib`
-   `scipy`

You can install them using pip:
```bash
pip install numpy pandas matplotlib scipy
```

## How to Run

You can run the entire simulation from the command line:

```bash
python main.py
```

The script will:
1.  Loop through a range of different numbers of Terrestrial Operators (TOs).
2.  For each number, run the simulation for all three scenarios (`Contract Theory`, `Centralized`, `Equal Allocation`).
3.  Average the results over multiple runs to ensure statistical significance.
4.  Print the final results to the console.
5.  Save the aggregated results to a CSV file.
6.  Generate and save a comparative plot.

## Results

The simulation produces two main outputs in the `results/` directory:

1.  **`simulation_results.csv`**: A CSV file containing the performance metrics for each scenario and for each number of agents, including:
    -   Principal Utility
    -   Agents Utility
    -   Social Welfare (Principal Utility + Agents Utility)

2.  **`performance_comparison.png`**: A plot visualizing the Social Welfare (and other metrics) of the three scenarios as the number of agents increases. This plot is the primary visual output for comparing the models.

Here is an example of the generated plot:

![Performance Comparison](results/performance_comparison.png)


## Code Structure

-   `main.py`: The main entry point of the simulation. It controls the simulation loops, calls the different models, and generates the final results and plots.
-   `config.py`: Contains all the key economic and physical parameters for the simulation, such as agent types, cost functions, and total available resources.
-   `contract_solver.py`: Implements the core logic for the **Contract Theory** model. It uses `scipy.optimize.minimize` to solve the constrained optimization problem and design the optimal contract menu.
-   `baselines.py`: Implements the logic for the **Centralized** and **Equal Allocation** scenarios.
-   `plotter.py`: Contains functions for plotting the results (Note: in the current version, plotting is handled directly in `main.py`).
-   `channel.py` & `geometry.py`: Contain helper functions for modeling the physical layer of the satellite link, which are used to inform the utility functions.
-   `results/`: The directory where all output files (CSV, plots) are saved.
