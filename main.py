import sys
from typing import List, Dict, Set, Tuple, Optional


class SWESolver:
    """Optimized solver for SuperStringWithExpansion problem"""

    def __init__(self):
        self.k = 0
        self.s = ""
        self.patterns = []
        self.expansions = {}
        self.pattern_cache = {}  # Cache for pattern validation

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
                options = [opt.strip() for opt in parts[1].split(',') if opt.strip()]
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

    def get_pattern_symbols(self, pattern: str) -> Set[str]:
        """Get all uppercase symbols in a pattern"""
        return set(c for c in pattern if c.isupper())

    def filter_by_length(self, symbol: str, options: List[str], assignment: Dict[str, str]) -> List[str]:
        """
        OPTIMIZATION: Filter options that are too long
        For each pattern using this symbol, compute max allowed length
        """
        max_allowed = len(self.s)

        for pattern in self.patterns:
            if symbol not in pattern:
                continue

            # Calculate minimum length for this pattern
            fixed_len = sum(1 for c in pattern if not c.isupper())
            other_symbols = [c for c in pattern if c.isupper() and c != symbol and c not in assignment]

            if other_symbols:
                # Other unassigned symbols - use minimum lengths
                other_min = sum(min(len(opt) for opt in self.expansions.get(sym, ['']))
                               for sym in other_symbols)
            else:
                other_min = 0

            assigned_len = sum(len(assignment.get(c, '')) for c in pattern if c.isupper() and c in assignment)

            # Max length for current symbol to fit
            pattern_max = len(self.s) - fixed_len - other_min - assigned_len
            max_allowed = min(max_allowed, pattern_max)

        # Filter options
        return [opt for opt in options if len(opt) <= max_allowed]

    def check_assignment(self, assignment: Dict[str, str]) -> bool:
        """Check if an assignment makes all patterns substrings of s"""
        for pattern in self.patterns:
            expanded = self.expand_pattern(pattern, assignment)
            if not self.is_substring(expanded, self.s):
                return False
        return True

    def prune_early(self, partial_assignment: Dict[str, str]) -> bool:
        """
        Enhanced pruning: Check if current partial assignment can possibly work
        Returns True if we should continue, False if we can prune
        """
        assigned_symbols = set(partial_assignment.keys())

        for pattern in self.patterns:
            pattern_symbols = self.get_pattern_symbols(pattern)

            # If all symbols in pattern are assigned, check immediately
            if pattern_symbols.issubset(assigned_symbols):
                expanded = self.expand_pattern(pattern, partial_assignment)
                if not self.is_substring(expanded, self.s):
                    return False

            # Additional check: if partially expanded pattern is already too long
            elif pattern_symbols.intersection(assigned_symbols):
                # Get partially expanded pattern
                partial = pattern
                for sym in assigned_symbols:
                    if sym in partial:
                        partial = partial.replace(sym, partial_assignment[sym])

                # Count remaining symbols
                remaining_symbols = [c for c in partial if c.isupper()]
                if remaining_symbols:
                    min_remaining = sum(min(len(opt) for opt in self.expansions.get(c, ['']))
                                       for c in remaining_symbols)
                    min_total = len([c for c in partial if not c.isupper()]) + min_remaining

                    if min_total > len(self.s):
                        return False

        return True

    def solve_bruteforce(self) -> Optional[Dict[str, str]]:
        """
        Optimized solver with aggressive pruning
        """
        # Get all symbols that need assignment
        symbols = list(self.expansions.keys())

        if not symbols:
            # No symbols to expand, check if patterns are substrings
            for pattern in self.patterns:
                if not self.is_substring(pattern, self.s):
                    return None
            return {}

        # Check if any expansion set is empty
        for symbol in symbols:
            if not self.expansions[symbol]:
                return None

        # HEURISTIC 1: Variable ordering - most constrained first
        def symbol_priority(sym):
            # Count how many patterns use this symbol
            pattern_count = sum(1 for p in self.patterns if sym in p)
            # Number of options
            option_count = len(self.expansions.get(sym, []))
            # Prioritize: high constraint, few options
            return (-pattern_count, option_count)

        symbols = sorted(symbols, key=symbol_priority)

        # HEURISTIC 2: Check for trivially unsolvable cases
        for pattern in self.patterns:
            pattern_symbols = self.get_pattern_symbols(pattern)
            if not pattern_symbols:  # Fixed pattern
                if not self.is_substring(pattern, self.s):
                    return None

        # HEURISTIC 3: Length feasibility check
        min_pattern_len = float('inf')
        for pattern in self.patterns:
            pattern_chars = [c for c in pattern if not c.isupper()]
            symbol_chars = [c for c in pattern if c.isupper()]

            if symbol_chars:
                if not all(c in self.expansions for c in symbol_chars):
                    return None

                min_expansion = sum(min(len(opt) for opt in self.expansions.get(c, ['']))
                                    for c in symbol_chars)
                total_min = len(pattern_chars) + min_expansion
            else:
                total_min = len(pattern_chars)

            min_pattern_len = min(min_pattern_len, total_min)

        if len(self.s) < min_pattern_len:
            return None

        # Start backtracking
        return self.backtrack_solve(symbols, {}, 0)

    def backtrack_solve(self, symbols: List[str],
                        assignment: Dict[str, str],
                        depth: int) -> Optional[Dict[str, str]]:
        """Backtracking solver with aggressive pruning"""

        # Base case: all symbols assigned
        if depth == len(symbols):
            if self.check_assignment(assignment):
                return assignment.copy()
            return None

        # Prune if current partial assignment already fails
        if not self.prune_early(assignment):
            return None

        # Get current symbol to assign
        current_symbol = symbols[depth]
        options = self.expansions[current_symbol]

        # OPTIMIZATION: Filter options by length feasibility
        filtered_options = self.filter_by_length(current_symbol, options, assignment)

        if not filtered_options:
            return None  # No valid options

        # HEURISTIC: Try shorter options first (more likely to fit)
        sorted_options = sorted(filtered_options, key=len)

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
    # Read input from stdin as required by assignment
    lines = []
    try:
        for line in sys.stdin:
            lines.append(line.rstrip('\n\r'))
    except Exception:
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