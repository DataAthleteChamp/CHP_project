# Assignment Project Report
## Course 02249, DTU Compute - Computationally Hard Problems
**Group Number:** XX
**Date:** 07.10.2025
**Due Date:** 03.11.2025, 21:00

---

## Division of Labor

- **Member 1 (Name):** [Responsibilities - e.g., Parts b, c, implementation]
- **Member 2 (Name):** [Responsibilities - e.g., Parts d, e, testing]
- **Member 3 (Name):** [Responsibilities - e.g., Parts f, g, h, documentation]

---

## Part b) Solution for test01.swe

### Instance Analysis

The test01.swe file contains:
- k = 4 patterns
- Target string s = "abdde"
- Patterns: ABD, DDE, AAB, ABd
- Expansion sets:
  - A: {a, b, c, d, e, f, dd}
  - B: {a, b, c, d, e, f, dd}
  - D: {a, b, c, d, e, f, dd}
  - E: {aa, bd, c, d, e}

### Answer: [YES/NO]

**Justification:**

[Provide detailed analysis showing whether a valid expansion exists]

[If YES: Show the specific assignment of expansions and verify each pattern becomes a substring of s]

[If NO: Explain why no valid assignment can exist]

---

## Part c) Formal Language for .SWE Format

### Alphabet Definition

The alphabet Σ_SWE for the .SWE file format consists of:
```
Σ_SWE = {0-9, a-z, A-Z, :, ,, \n, <space>}
```

### Grammar Description

[Describe the formal language/grammar for .SWE files]

```
<SWE-file> ::= <k-value> <newline> <target-string> <newline> <patterns> <expansions>
<k-value> ::= <digit>+
<target-string> ::= <lowercase>*
<patterns> ::= <pattern> (<newline> <pattern>)*
<pattern> ::= (<lowercase> | <uppercase>)*
<expansions> ::= <expansion> (<newline> <expansion>)*
<expansion> ::= <uppercase> : <word-list>
<word-list> ::= <word> (, <word>)*
...
```

### Word Problem Solution

[Describe algorithm to determine if a given string w ∈ Σ_SWE* is a valid .SWE file]

**Algorithm:**
1. [Step-by-step process to validate the format]
2. [Parsing rules]
3. [Validation checks]

**Complexity:** [Time and space complexity analysis]

---

## Part d) Optimization Version Algorithm

### Problem Statement

Given: Algorithm A_d for decision version of SuperStringWithExpansion
Goal: Design algorithm A_o that outputs the actual solution (r₁, r₂, ..., r_m) or NO

### Algorithm Description

```
Algorithm A_o(s, t₁,...,t_k, R₁,...,R_m):
    [Pseudocode for optimization algorithm]

    1. If A_d returns NO, return NO
    2. For each symbol γ_i ∈ Γ:
        [Binary search or iterative approach to find r_i]
    3. Return (r₁, r₂, ..., r_m)
```

### Correctness Proof

**Theorem:** Algorithm A_o correctly computes a valid solution or returns NO.

**Proof:**
[Detailed proof of correctness]

### Running Time Analysis

**Theorem:** A_o runs in polynomial time (assuming A_d takes O(1) time).

**Proof:**
[Analysis showing polynomial number of calls to A_d and polynomial overhead]

---

## Part e) SuperStringWithExpansion ∈ NP

### Proof Strategy

To show SuperStringWithExpansion ∈ NP, we need:
1. Define a certificate
2. Show the certificate has polynomial size
3. Provide a polynomial-time verification algorithm

### Certificate Definition

**Certificate:** A sequence of words (r₁, r₂, ..., r_m) where r_i ∈ R_i

**Size:** [Analysis of certificate size in terms of input]

### Verification Algorithm

```
Algorithm Verify(Instance, Certificate):
    Input: Instance I = (Σ, Γ, s, t₁,...,t_k, R₁,...,R_m)
           Certificate C = (r₁, r₂, ..., r_m)

    1. Check r_i ∈ R_i for all i
    2. For each pattern t_j:
        a. Compute expansion e(t_j) using C
        b. Check if e(t_j) is substring of s
    3. Return YES if all checks pass, NO otherwise
```

### Complexity Analysis

[Show that verification runs in polynomial time]

**Conclusion:** SuperStringWithExpansion ∈ NP

---

## Part f) NP-Completeness Proof

### Selected Reference Problem

**Reference Problem:** [Choose one from: PartitionInto3-Sets, 1-In-3-Satisfiability, MinimumCliqueCover, Graph-3-Coloring, Longest-Common-Subsequence, MinimumRectangleTiling, Minimum Graph Transformation, MinimumDegreeSpanningTree]

### Reduction Strategy

We show [Reference Problem] ≤_p SuperStringWithExpansion

### Construction

Given an instance I of [Reference Problem], construct instance I' of SuperStringWithExpansion:

[Detailed construction mapping]

**Example:**
[Provide concrete example of the reduction]

### Correctness Proof

**Lemma 1:** If I is a YES-instance of [Reference Problem], then I' is a YES-instance of SuperStringWithExpansion.

**Proof:**
[Detailed proof]

**Lemma 2:** If I' is a YES-instance of SuperStringWithExpansion, then I is a YES-instance of [Reference Problem].

**Proof:**
[Detailed proof]

### Polynomial Time Analysis

[Show that the reduction can be computed in polynomial time]

**Conclusion:** SuperStringWithExpansion is NP-complete.

---

## Part g) Algorithm Design

### High-Level Description

The algorithm uses **backtracking with heuristic pruning** to explore the search space of possible expansions.

### Algorithm Pseudocode

```
Algorithm Solve(s, t₁,...,t_k, R₁,...,R_m):
    symbols ← sort(Γ)
    return Backtrack(symbols, {}, 0)

Algorithm Backtrack(symbols, assignment, depth):
    // Base case
    if depth = |symbols|:
        if CheckAssignment(assignment):
            return assignment
        return NO

    // Heuristic pruning
    if not PruneEarly(assignment, symbols[depth:]):
        return NO

    // Try each expansion option
    current_symbol ← symbols[depth]
    options ← R_current_symbol

    // Heuristic: try shorter options first
    sort options by length

    for each option in options:
        assignment[current_symbol] ← option
        result ← Backtrack(symbols, assignment, depth + 1)
        if result ≠ NO:
            return result
        remove assignment[current_symbol]

    return NO
```

### Heuristic Elements

1. **Early Pruning:** Check partially assigned patterns immediately
   - If a pattern uses only assigned symbols and doesn't match, prune branch

2. **Length-based Ordering:** Try shorter expansions first
   - Shorter strings more likely to fit in target string

3. **Length Feasibility Check:** Quick check if minimum pattern length exceeds target
   - Prune impossible instances early

### Correctness Proof

**Theorem:** The algorithm always returns the correct answer.

**Proof:**
[Prove completeness and soundness]

### Running Time Analysis

**Worst Case:** O(2^p(n)) where n is input size

[Detailed analysis showing exponential bound]

---

## Part h) Worst-Case Running Time Analysis

### Input Size Definition

Let n be the total input size:
```
n = |s| + Σ|t_i| + Σ_j(|R_j| + Σ_{r∈R_j}|r|)
```

### Detailed Complexity Analysis

1. **Search Space Size:** O(Π|R_i|) ≤ O(c^m) where c = max|R_i|

2. **Per-Node Work:**
   - Pattern expansion: O(k × max|t_i|)
   - Substring check: O(|s| × max_expanded_pattern_length)

3. **Total Time:** [Detailed calculation showing O(2^p(n))]

### Space Complexity

[Analysis of space requirements]

---

## Part i) Implementation Details

### Language and Libraries

- **Language:** Python 3.7+
- **Libraries:** Standard library only (sys, itertools, typing)

### Code Structure

```
SWESolver class:
- parse_input(): Parse .SWE format
- solve(): Main entry point
- backtrack_solve(): Recursive backtracking
- check_assignment(): Validate complete assignments
- prune_early(): Heuristic pruning
- expand_pattern(): Apply expansions
- format_solution(): Format output
```

### Testing Results

| Test File | Result | Time | Notes |
|-----------|--------|------|-------|
| test01.swe | [YES/NO] | [time] | [notes] |
| test02.swe | [YES/NO] | [time] | [notes] |
| test03.swe | [YES/NO] | [time] | [notes] |
| test04.swe | [YES/NO] | [time] | [notes] |
| test05.swe | [YES/NO] | [time] | [notes] |
| test06.swe | [YES/NO] | [time] | [notes] |

### Performance Observations

[Discuss where heuristics help and where they don't]

### Known Limitations

[Discuss any limitations or edge cases]

---

## References

1. Course materials, DTU Compute 02249
2. [Add any additional references used]

---

## Appendix

### Additional Test Cases

[Document any additional test cases created]

### Code Snippets

[Include key code snippets if helpful for the report]