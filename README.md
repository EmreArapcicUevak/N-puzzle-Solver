# 🧩 N-Puzzle Solver — Disjoint Pattern Database (PDB) Edition

A high-performance **N-Puzzle Solver** implemented in Python, powered by the **AIMA Toolkit** — a modular artificial intelligence framework I designed to re-create and extend the algorithms from *Artificial Intelligence: A Modern Approach* (AIMA).  

This solver supports both **Manhattan Distance** and **Disjoint Pattern Database (PDB)** heuristics and provides a clean, modern **command-line interface** for benchmarking and research.

---

## 🚀 Features

- 🔢 Supports any **N×N puzzle** (default: 3×3)  
- 🧮 Implements A\* search with modular heuristic selection  
- 💾 Automatically **generates & caches pattern databases** for fast reuse  
- 📊 Displays real-time **progress bars** during PDB generation  
- ✅ Prints full **step-by-step optimal solutions**

---

## 🧠 Project Overview

This repository demonstrates the **power of Disjoint Pattern Databases** — one of the most effective admissible heuristics in combinatorial search problems.  
Compared to traditional heuristics (like Manhattan distance), PDBs offer:
- Far stronger informedness  
- Fewer node expansions  
- Reduced runtime for complex instances  

The solver internally partitions the puzzle into disjoint subsets (e.g. `{1,2,3,4}` and `{5,6,7,8}` for the 8-puzzle), precomputes optimal subproblem costs, and stores them for reuse in future runs.

---

## 🧩 Example Usage

### 🔹 Solving a 3×3 puzzle with PDB heuristic

```bash
python3 solve_n_puzzle.py --dim 3 --state "1 2 0 7 6 5 4 3 8" --heuristic pdb
```

**Output:**
```
Dimension: 3x3
Initial state: (1, 2, 0, 7, 6, 5, 4, 3, 8)
Goal state:    (1, 2, 3, 4, 5, 6, 7, 8, 0)
Heuristic:     pdb
Solving...

[!] Pattern DB not found at Pattern_Databases/N9_tiles_1_2_3_4_goal_1_2_3_4_5_6_7_8_0.pkl. Generating...
[+] Saved pattern DB to Pattern_Databases/N9_tiles_1_2_3_4_goal_1_2_3_4_5_6_7_8_0.pkl
Generating adjoint patterns... ██████████ 100% 0:00:00
Generating adjoint patterns... ██████▏    40% 0:01:00

Step 0: down  
Step 1: left  
Step 2: down  
...  
Step 17: down  

Solution length: 18 moves.
```

---

## ⚙️ Command-Line Options

```bash
python3 solve_n_puzzle.py -h
```

```
usage: solve_n_puzzle.py [-h] [--dim DIM] --state STATE [--heuristic {pdb,manhattan}]

Solve the N-Puzzle from the command line.

options:
  -h, --help            show this help message and exit
  --dim, -d DIM         Board dimension N for an N×N puzzle (default: 3)
  --state, -s STATE     Initial state as a flat list, e.g. "1 2 0 7 6 5 4 3 8"
  --heuristic, -H       Heuristic to use (default: pdb for 3×3, otherwise manhattan)
```

---

## 🧮 Heuristics Overview

| Heuristic | Description | Admissible | Recommended For |
|------------|-------------|-------------|-----------------|
| **Manhattan Distance** | Sum of the tile distances from their goal positions | ✅ | Quick runs and simple puzzles |
| **Pattern Database (PDB)** | Precomputed subproblem costs stored in disjoint databases | ✅ | Optimal and large-scale solving |

---

## 📁 Repository Structure

```
N-puzzle-Solver/
│
├── solve_n_puzzle.py          # CLI entry point
├── n_puzzle_problem.py        # Puzzle state representation and logic
├── heuristics/                # PDB and Manhattan implementations
├── Pattern_Databases/         # Auto-generated .pkl databases
├── utils/                     # Conversion & helper utilities
└── README.md                  # You’re here
```

---

## 🧠 About the AIMA Toolkit

This solver is a demonstration project for the **[AIMA Toolkit](https://github.com/EmreArapcicUevak/aima-toolkit)** — a Python framework I created that re-implements and extends the algorithms described in *Artificial Intelligence: A Modern Approach (4th Ed.)* by Stuart Russell and Peter Norvig.  

---