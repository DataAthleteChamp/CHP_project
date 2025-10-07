import sys
from itertools import product
from typing import List, Dict, Set, Tuple, Optional


class SWESolver:
    """Solver for SuperStringWithExpansion problem"""

    def __init__(self):
        self.k = 0
        self.s = ""
        self.patterns = []
        self.expansions = {}

    def parse_input(self, lines: List[str]) -> bool:
        """Parse input in .SWE format"""
        try:
            idx = 0
            # Parse k
            self.k = int(lines[idx].strip())
            idx += 1

            # Parse string s
            self.s = lines[idx].strip()
            idx += 1

            # Parse k patterns
            self.patterns = []
            for i in range(self.k):
                self.patterns.append(lines[idx].strip())
                idx += 1

            # Parse expansion sets
            self.expansions = {}
            while idx < len(lines):
                line = lines[idx].strip()
                if not line:
                    idx += 1
                    continue

                if ':' not in line:
                    idx += 1
                    continue

                parts = line.split(':', 1)
                symbol = parts[0].strip()
                options = [opt.strip() for opt in parts[1].split(',')]
                self.expansions[symbol] = options
                idx += 1

            return True
        except Exception as e:
            print(f"Error parsing input: {e}", file=sys.stderr)
            return False

    def expand_pattern(self, pattern: str, assignment: Dict[str, str]) -> str:
        """Expand a pattern given symbol assignments"""
        result = pattern
        for symbol, replacement in assignment.items():
            result = result.replace(symbol, replacement)
        return result

    def is_substring(self, needle: str, haystack: str) -> bool:
        """Check if needle is substring of haystack"""
        return needle in haystack

    def check_assignment(self, assignment: Dict[str, str]) -> bool:
        """Check if an assignment makes all patterns substrings of s"""
        for pattern in self.patterns:
            expanded = self.expand_pattern(pattern, assignment)
            if not self.is_substring(expanded, self.s):
                return False
        return True

    def prune_early(self, partial_assignment: Dict[str, str],
                    remaining_symbols: List[str]) -> bool:
        """
        Heuristic: Check if current partial assignment can possibly work
        Returns True if we should continue, False if we can prune
        """
        # Check patterns that only use assigned symbols
        for pattern in self.patterns:
            # Check if pattern only uses assigned symbols
            pattern_symbols = set(c for c in pattern if c.isupper())
            if pattern_symbols.issubset(set(partial_assignment.keys())):
                expanded = self.expand_pattern(pattern, partial_assignment)
                if not self.is_substring(expanded, self.s):
                    return False
        return True

    def solve_bruteforce(self) -> Optional[Dict[str, str]]:
        """
        Brute force solver with pruning heuristics
        """
        # Get all symbols that need assignment
        symbols = sorted(self.expansions.keys())

        if not symbols:
            # No symbols to expand, check if patterns are substrings
            for pattern in self.patterns:
                if not self.is_substring(pattern, self.s):
                    return None
            return {}

        # Heuristic 1: Quick check for impossible cases
        # If target string is too short, impossible
        min_pattern_len = float('inf')
        for pattern in self.patterns:
            pattern_chars = [c for c in pattern if not c.isupper()]
            symbol_chars = [c for c in pattern if c.isupper()]
            min_expansion = sum(min(len(opt) for opt in self.expansions.get(c, ['']))
                                for c in symbol_chars)
            total_min = len(''.join(pattern_chars)) + min_expansion
            min_pattern_len = min(min_pattern_len, total_min)

        if len(self.s) < min_pattern_len:
            return None

        # Generate all possible assignments using backtracking with pruning
        return self.backtrack_solve(symbols, {}, 0)

    def backtrack_solve(self, symbols: List[str],
                        assignment: Dict[str, str],
                        depth: int) -> Optional[Dict[str, str]]:
        """Backtracking solver with pruning"""

        # Base case: all symbols assigned
        if depth == len(symbols):
            if self.check_assignment(assignment):
                return assignment.copy()
            return None

        # Prune if current partial assignment already fails
        if not self.prune_early(assignment, symbols[depth:]):
            return None

        # Try each option for current symbol
        current_symbol = symbols[depth]
        options = self.expansions[current_symbol]

        # Heuristic 2: Try shorter replacements first (often more likely to fit)
        sorted_options = sorted(options, key=len)

        for option in sorted_options:
            assignment[current_symbol] = option

            result = self.backtrack_solve(symbols, assignment, depth + 1)
            if result is not None:
                return result

            del assignment[current_symbol]

        return None

    def solve(self) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Main solve method"""
        solution = self.solve_bruteforce()
        if solution is not None:
            return True, solution
        return False, None

    def format_solution(self, solution: Dict[str, str]) -> str:
        """Format solution for output"""
        if solution is None:
            return "NO"

        lines = []
        for symbol in sorted(solution.keys()):
            lines.append(f"{symbol}:{solution[symbol]}")
        return '\n'.join(lines)


def main():
    """Main entry point"""
    # Read input from hardcoded file
    import os
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'test01.swe')

    try:
        with open(file_path, 'r') as f:
            lines = [line.rstrip('\n\r') for line in f]
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        print("NO")
        return

    if not lines:
        print("NO")
        return

    # Create solver and parse input
    solver = SWESolver()
    if not solver.parse_input(lines):
        print("NO")
        return

    # Solve
    is_yes, solution = solver.solve()

    # Output result
    if is_yes:
        print(solver.format_solution(solution))
    else:
        print("NO")


if __name__ == "__main__":
    main()