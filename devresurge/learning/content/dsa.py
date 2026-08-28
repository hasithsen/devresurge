ROADMAP = {
    "slug": "dsa-interview",
    "title": "DSA for interviews",
    "tagline": "Patterns that win coding rounds at top companies.",
    "description": (
        "A pattern-first path through arrays, hashes, trees, graphs, DP, and "
        "complexity trade-offs — built for FAANG-style interviews and real code."
    ),
    "domain": "algorithms",
    "level": "intermediate",
    "icon": "π",
    "order": 20,
    "audience": "Grads preparing for coding interviews while building lasting skill.",
    "outcomes": (
        "Recognize the top interview patterns in under a minute",
        "Write correct solutions with clear complexity analysis",
        "Communicate approach before coding",
    ),
    "related_quiz_slugs": ("data-structures", "algorithms-patterns"),
    "lessons": [
        {
            "slug": "interview-operating-system",
            "title": "Interview operating system",
            "summary": "Clarify → examples → brute force → optimize → code → test.",
            "minutes": 10,
            "outcomes": ("Run a repeatable interview script under time pressure",),
            "body": """## The 45-minute script

1. **Restate** the problem and constraints (n size, duplicates, sorted?).
2. **Examples** — normal, edge (empty, one element), adversarial.
3. **Brute force** — say it out loud; prove you understand.
4. **Optimize** — name the pattern (two pointers, sliding window, etc.).
5. **Complexity** — time and space before coding.
6. **Code** cleanly; narrate intent.
7. **Test** on your examples; fix bugs calmly.

## What interviewers score

- Problem solving process
- Code quality and correctness
- Communication
- Complexity awareness

Silent geniuses lose to clear, solid engineers.

## Habit

Every practice problem: speak the script aloud — even alone.
""",
        },
        {
            "slug": "arrays-hashes-pointers",
            "title": "Arrays, hashes, two pointers",
            "summary": "The bread-and-butter of easy/medium rounds.",
            "minutes": 16,
            "quiz_slug": "data-structures",
            "outcomes": (
                "Use hash maps for O(n) pair/complement problems",
                "Apply two pointers on sorted or partitioned arrays",
            ),
            "body": """## Hash map reflexes

- Two-sum / complements → value → index map
- Frequency counting → Counter / dict
- Grouping anagrams → sorted key or signature

Trade space for time deliberately.

## Two pointers

Use when:

- Array is sorted
- You shrink/expand a window from ends
- Partitioning (Dutch national flag)

## Sliding window

For contiguous subarrays/strings with a constraint (max sum, unique chars):

- Expand right; shrink left when invalid
- Maintain a running state (sum, counts)

## Pitfalls

- Off-by-one on inclusive bounds
- Mutating while iterating
- Forgetting empty-input behavior

## Drill

Solve: two-sum, longest substring without repeating chars, container with most water.
""",
        },
        {
            "slug": "trees-and-recursion",
            "title": "Trees, recursion, and DFS/BFS",
            "summary": "Binary trees, BST invariants, and traversal fluency.",
            "minutes": 16,
            "outcomes": (
                "Implement DFS/BFS without panic",
                "Use recursion with clear base cases",
            ),
            "body": """## Traversals

- **DFS**: preorder / inorder / postorder (recursion or explicit stack)
- **BFS**: level-order with a queue

BST: inorder yields sorted values — use it.

## Patterns

- Diameter / height: return multiple values from recursion
- Path sums: pass running state down; decide at leaves
- Serialize/deserialize: choose a clear encoding

## Recursion checklist

- Base case first
- Trust the recursive result
- Watch stack depth (prefer iterative for huge trees)

## Drill

Max depth, lowest common ancestor, level-order zigzag, validate BST.
""",
        },
        {
            "slug": "graphs-essentials",
            "title": "Graphs essentials",
            "summary": "Adjacency lists, BFS shortest path, DFS components, topo sort.",
            "minutes": 16,
            "quiz_slug": "algorithms-patterns",
            "outcomes": (
                "Model problems as graphs",
                "Choose BFS vs DFS vs topo correctly",
            ),
            "body": """## Representation

Prefer **adjacency list** for interviews unless dense matrix is natural (grid).

## Core algorithms

- **BFS** — shortest path in unweighted graphs
- **DFS** — components, cycle detection, flood fill
- **Topo sort** — course schedule / dependency order (Kahn or DFS)
- **Union-Find** — connected components / redundant edges (optional but strong)

## Grid graphs

Treat cells as nodes; edges to 4/8 neighbors. Visited set is mandatory.

## Complexity

V nodes, E edges: BFS/DFS are O(V+E). Say it.

## Drill

Number of islands, course schedule, clone graph, word ladder (BFS).
""",
        },
        {
            "slug": "heaps-intervals-binary-search",
            "title": "Heaps, intervals, binary search",
            "summary": "Priority queues, merge intervals, search on answer space.",
            "minutes": 14,
            "outcomes": (
                "Use heaps for top-k and scheduling",
                "Binary-search answers, not only arrays",
            ),
            "body": """## Heaps

- Top-k → size-k heap
- Merge k sorted lists
- Meeting rooms / CPU scheduling intuition

Know min-heap vs max-heap conventions in your language.

## Intervals

Sort by start (or end). Sweep line / greedy merge is common.

## Binary search beyond arrays

Search on **monotonic answer space**:

- "Minimum capacity to ship packages in D days"
- "Split array largest sum"

Invariant: keep a feasible half; prove monotonicity first.

## Drill

Kth largest, merge intervals, search in rotated array, koko eating bananas.
""",
        },
        {
            "slug": "dynamic-programming",
            "title": "Dynamic programming without fear",
            "summary": "State, transition, base case — the only DP recipe you need.",
            "minutes": 18,
            "outcomes": (
                "Define DP state clearly",
                "Convert recursion + memo to bottom-up",
            ),
            "body": """## DP recipe

1. **Define state** — what decisions remain? (`dp[i]`, `dp[i][j]`)
2. **Transition** — how do you build from smaller states?
3. **Base cases** — empty / zero / first element
4. **Order** — ensure dependencies computed first
5. **Answer location** — usually `dp[n]` or max over states

## Starter patterns

- 1D climb / rob house / coin change
- Knapsack / subset sum
- Grid paths
- LIS (patience / DP)
- String DP (edit distance, LCS) — later stage

## Interview tip

Start with **top-down memo** if stuck — clarity beats premature bottom-up.

## Drill

Climbing stairs, coin change, house robber, unique paths, longest increasing subsequence.
""",
        },
    ],
}
