# SuperStringWithExpansion Solver

Course 02249, DTU Compute - Computationally Hard Problems – Fall 2025

## Problem Description

This project implements a solver for the **SuperStringWithExpansion** problem, an NP-complete problem involving string matching with variable expansions.

### Problem Definition

**Input:**
- Two disjoint alphabets Σ (lowercase letters) and Γ (uppercase letters)
- A target string `s ∈ Σ*`
- k pattern strings `t₁, ..., tₖ ∈ (Σ ∪ Γ)*`
- m expansion sets `R₁, ..., Rₘ ⊆ Σ*`

**Output:** YES if there exists a sequence of words `r₁ ∈ R₁, r₂ ∈ R₂, ..., rₘ ∈ Rₘ` such that for all i ∈ {1, ..., k}, the expansion e(tᵢ) is a substring of s. Otherwise, output NO.

## Project Structure

```
CHP_project/
├── main.py                 # Main solver implementation
├── data/                   # Test instances
│   ├── test01.swe
│   ├── test02.swe
│   └── ...
├── report.md              # Project report (theoretical parts)
├── assignment.pdf         # Original assignment description
├── README.md              # This file
├── requirements.txt       # Python dependencies
└── .gitignore            # Git ignore rules
```

## File Format (.SWE)

The input files follow the SWE format:

```
k                          # Number of patterns
s                          # Target string
t₁                         # Pattern 1
t₂                         # Pattern 2
...
tₖ                         # Pattern k
Γ₁:r₁,r₂,...              # Expansion set for symbol Γ₁
Γ₂:r₁,r₂,...              # Expansion set for symbol Γ₂
...
```

### Example (test01.swe)

```
4
abdde
ABD
DDE
AAB
ABd
A:a,b,c,d,e,f,dd
B:a,b,c,d,e,f,dd
C:a,b,c,d,e,f,dd
D:a,b,c,d,e,f,dd
E:aa,bd,c,d,e
```

## Installation

### Requirements

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd CHP_project

# Install dependencies (if any)
pip install -r requirements.txt
```

## Usage

The solver reads input from standard input in .SWE format:

```bash
# Run with standard input
python main.py < data/test01.swe

# Or use input redirection
cat data/test01.swe | python main.py
```

**Note:** The current version has `data/test01.swe` hardcoded for testing purposes. To use standard input, modify `main.py` line 177.

### Output Format

If a solution exists:
```
A:a
B:b
D:d
```

If no solution exists:
```
NO
```

## Algorithm

The solver uses a **backtracking algorithm with pruning heuristics**:

1. **Early Pruning**: Checks if partial assignments already violate constraints
2. **Length-based Heuristic**: Tries shorter expansions first
3. **Pattern Validation**: Validates fully-assigned patterns immediately

The algorithm explores the search space systematically while avoiding unnecessary branches.

### Complexity

- **Time Complexity**: O(2^p(n)) where n is input size and p is polynomial
- **Space Complexity**: O(n) for the recursion stack

## Implementation Details

### Main Components

- `SWESolver`: Main solver class
  - `parse_input()`: Parses .SWE format
  - `solve()`: Entry point for solving
  - `backtrack_solve()`: Recursive backtracking with pruning
  - `check_assignment()`: Validates complete assignments
  - `prune_early()`: Early pruning heuristic

## Testing

Test files are provided in the `data/` directory:

```bash
# Test individual files
python main.py < data/test01.swe
python main.py < data/test02.swe
```

## Division of Labor

- **Member 1**: [Name] - [Responsibilities]
- **Member 2**: [Name] - [Responsibilities]
- **Member 3**: [Name] - [Responsibilities]

## Submission Files

For submission, prepare:

1. `report-group-XX.pdf` - Theoretical solutions
2. `code-group-XX.zip` - Source code (zip the project root contents)
3. `readme-group-XX.txt` - Compilation and execution instructions

## References

- Course 02249, DTU Compute
- Carsten Witt
- Assignment Date: 07.10.2025
- Due Date: 03.11.2025, 21:00

## License

This project is for educational purposes as part of the DTU Compute course 02249.