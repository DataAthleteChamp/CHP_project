SuperStringWithExpansion Solver - Compilation and Execution Instructions
===========================================================================

Group Number: XX
Course: 02249, DTU Compute - Computationally Hard Problems
Date: 07.10.2025

===========================================================================
REQUIREMENTS
===========================================================================

Programming Language: Python 3.7 or higher
Dependencies: None (uses only Python standard library)

===========================================================================
COMPILATION
===========================================================================

No compilation is required. Python is an interpreted language.

===========================================================================
EXECUTION
===========================================================================

The program reads input from standard input (stdin) and outputs to standard
output (stdout) as required by the assignment specifications.

Basic usage:
    python main.py < input_file.swe

Or using pipe:
    cat input_file.swe | python main.py

Examples:
    python main.py < data/test01.swe
    python main.py < data/test02.swe

===========================================================================
INPUT FORMAT
===========================================================================

The program accepts input in .SWE format:
- Line 1: Number k (number of patterns)
- Line 2: Target string s (lowercase letters only)
- Lines 3 to k+2: Pattern strings (lowercase and uppercase letters)
- Remaining lines: Expansion sets in format "LETTER:option1,option2,..."

Example:
    4
    abdde
    ABD
    DDE
    AAB
    ABd
    A:a,b,c,d,e,f,dd
    B:a,b,c,d,e,f,dd
    D:a,b,c,d,e,f,dd

===========================================================================
OUTPUT FORMAT
===========================================================================

If a solution exists, the program outputs one line per symbol assignment:
    A:a
    B:b
    D:d

If no solution exists or input is malformed:
    NO

===========================================================================
TESTING
===========================================================================

Test files are provided in the data/ directory:
- test01.swe through test06.swe

To run all tests:
    for file in data/test*.swe; do
        echo "Testing $file"
        python main.py < "$file"
        echo
    done

===========================================================================
ALGORITHM
===========================================================================

The implementation uses a backtracking algorithm with pruning heuristics:

1. Early Pruning: Validates partial assignments before full exploration
2. Length Heuristic: Tries shorter expansions first
3. Feasibility Check: Quick rejection of impossible instances

Time Complexity: O(2^p(n)) where n is input size and p is polynomial
Space Complexity: O(n) for recursion stack

===========================================================================
PROJECT STRUCTURE
===========================================================================

main.py         - Main solver implementation
data/           - Test instance files
README.md       - Detailed project documentation
report.md       - Theoretical analysis and solutions
requirements.txt - Python dependencies (none required)

===========================================================================
NOTES
===========================================================================

- The program uses ONLY standard input/output (no command-line arguments)
- Malformed input is treated as a NO instance
- The algorithm always terminates with correct output
- Some large instances may take longer to solve due to exponential complexity

===========================================================================
CONTACT
===========================================================================

For questions about this implementation, please refer to the project report
or contact the group members listed in the report.

===========================================================================