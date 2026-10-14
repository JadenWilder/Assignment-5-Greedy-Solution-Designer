# Greedy Solution Designer: Greedy Property Justification and Complexity Analysis

## Greedy Property Justification

### Part 1: Package Prioritization (Activity Selection)

For package prioritization, I used the strategy of selecting the delivery that finishes earliest. After sorting deliveries by their ending times, the algorithm chooses a delivery if it does not overlap with the previously selected delivery. This works because finishing earlier leaves more time for other deliveries. Choosing the earliest finishing delivery helps keep the schedule open for as many deliveries as possible. Choosing the shortest delivery or the one that starts earliest would not always produce the maximum number of deliveries because those choices do not guarantee that more time remains for other deliveries.

### Part 2: Truck Loading (Fractional Knapsack)

For truck loading, I sorted packages by their priority-to-weight ratio, from highest to lowest. This means the algorithm chooses packages that provide the most priority value for each pound of weight. If a package does not fit completely, the algorithm takes the fraction that fits in the remaining capacity. This strategy produces an optimal result for the fractional knapsack problem because the available space is used for the highest-value options first. In my test, the truck reached its 50-pound limit and achieved a total priority value of 240. If packages could not be divided, sorting by this ratio would not always guarantee the best solution because an entire package might need to be skipped to make room for a better combination.

### Part 3: Driver Assignment (Interval Scheduling)

For driver assignment, I sorted deliveries by their start times and reused the driver whose previous delivery finished earliest whenever that driver was available. If every driver was busy, the algorithm created a new driver. This minimizes the number of drivers because it reuses available drivers and only adds another driver when overlapping deliveries require one. This problem differs from package prioritization because the goal is not to maximize the number of deliveries selected. Instead, every delivery must be assigned while minimizing the number of drivers needed.

## Complexity Analysis

All three algorithms use sorting, which takes O(n log n) time for n deliveries or packages. In package prioritization, sorting by ending time dominates the runtime. The algorithm then scans the sorted deliveries once, taking O(n) additional time. Therefore, its overall time complexity is O(n log n).

Truck loading also takes O(n log n) time because packages are sorted by their priority-to-weight ratios. After sorting, the algorithm visits each package once and calculates how much can fit. This scan takes O(n) time, so sorting dominates the runtime.

Driver assignment sorts deliveries by starting time and uses a min-heap to track driver availability. Each delivery requires at most one heap removal and one heap insertion, each taking O(log n) time. Therefore, its overall time complexity is O(n log n).

Compared with brute-force methods that examine every possible delivery schedule or package combination, these greedy algorithms avoid exploring an enormous number of possibilities. Exhaustive approaches can take exponential or factorial time, depending on the problem and implementation, while these greedy implementations scale much better. My benchmarks processed 50 deliveries in 0.0186 milliseconds, loaded 100 packages in 0.0524 milliseconds, and assigned 60 deliveries using 19 drivers in 0.0407 milliseconds. These results show that the implementations ran quickly on the generated scenarios.