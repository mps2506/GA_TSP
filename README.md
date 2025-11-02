# 🧬 Genetic Algorithm for the Traveling Salesman Problem (TSP)

## 📘 Introduction
This project implements a **Genetic Algorithm (GA)** to solve the **Traveling Salesman Problem (TSP)** — finding the shortest possible route that visits every city exactly once and returns to the starting point.

The program is written in **Python** and provides an **interactive graphical user interface (GUI)** to configure parameters and visualize the optimization process in real time.

---

## ⚙️ Features
- **Interactive parameter input** using `tkinter`:
  - Number of cities
  - Population size
  - Number of generations
  - Starting city index
- **Dynamic visualization** using `matplotlib`:
  - Real-time evolution of the best and average route length
  - Animated route optimization process
- **Control panel**:
  - ⏩ Next / Prev generation navigation  
  - ▶️ Auto Play / Pause simulation  
  - 🔄 Restart and reconfigure parameters  
  - ⤴ Go to a specific generation index  

---

## 💻 Installation Guide

### 1️⃣ Requirements
- **Python 3.8+**

### 2️⃣ Install dependencies
Run the following command in your terminal or command prompt:
```bash
pip install numpy matplotlib
Modules such as math, random, and tkinter are included in the Python standard library.

🚀 How to Run
Download or clone this repository.

Open a terminal in the directory containing ga_tsp_animation.py.

Run the program:

bash
Sao chép mã
python ga_tsp_animation.py
A configuration window will appear. Enter:

Number of cities – total number of cities to visit (e.g., 20)

Population size – number of candidate routes in the population (e.g., 200)

Generations – number of evolutionary iterations (e.g., 100)

Start city (index) – index of the first city (e.g., 0)

Click Start Simulation to launch the genetic algorithm and visualization.

🖥️ User Interface Overview
Once started, two panels will appear:

Left Panel: Current best route connecting all cities

Right Panel: Convergence chart showing best and average route lengths across generations

Control Buttons
Button	Description
← Prev	Move to the previous generation
Next →	Move to the next generation
Auto Play / Pause	Automatically iterate generations
Go to	Jump to a specific generation number
Restart	Restart simulation and re-enter parameters

🧠 Algorithm Workflow
City generation:
Random coordinates are generated to represent cities.

Distance matrix computation:
Euclidean distance between every pair of cities is calculated and stored.

Population initialization:
Random routes are created as chromosomes (each representing a complete tour).

Fitness evaluation:
Each route is scored by total distance — shorter routes yield higher fitness.

Selection:
Individuals with better fitness are selected using Tournament Selection to reproduce.

Crossover (Ordered Crossover - OX):
Combines genetic material from two parents to form a valid child route.

Mutation (Swap Mutation):
Randomly swaps two cities in a route to preserve diversity and avoid local minima.

Replacement:
The next generation replaces the previous population, keeping the best route found so far.

Visualization:
The evolution of routes and convergence metrics are updated in real time via matplotlib.

Termination:
When the defined number of generations is reached, the best route is displayed along with convergence statistics.

🧩 File Structure
Function / Component	Description
euclidean(a, b)	Calculates Euclidean distance between two points
make_distance_matrix(cities)	Builds the pairwise distance matrix
genetic_algorithm_tsp()	Core genetic algorithm implementation
ordered_crossover()	Ordered crossover operation for permutations
swap_mutation()	Swaps two cities with a small mutation probability
get_parameters()	Opens GUI window to input parameters
animate_ga_tsp()	Manages main simulation loop and visualization

📊 Example Output
After running the program, you will see:

A plotted route connecting all cities (optimized over generations)

A graph showing how the best and average route lengths converge over time

Each run generates a different random city layout, allowing you to experiment with various settings.

🧩 Tips for Experimentation
Try increasing population size or generations to improve accuracy.

Adjust mutation rate (inside the code) to observe convergence behavior.

Re-run the simulation with different random seeds for comparison.

👨‍💻 Author
Nguyễn Khắc Hoàng Anh
Project: Applying Genetic Algorithm to the Traveling Salesman Problem (TSP)
Year: 2025


