"""
Greedy Algorithms Assignment
Implement three greedy algorithms for delivery optimization.
"""

import json
import time
import heapq


# ============================================================================
# PART 1: PACKAGE PRIORITIZATION (Activity Selection)
# ============================================================================

def maximize_deliveries(time_windows):
    """
    Schedule the maximum number of compatible deliveries.

    Args:
        time_windows: List of dictionaries containing delivery_id, start, end.

    Returns:
        List of delivery IDs for the maximum number of deliveries.
    """
    if not time_windows:
        return []

    # Greedy choice: select the delivery that finishes earliest.
    sorted_deliveries = sorted(
        time_windows,
        key=lambda delivery: (
            delivery["end"],
            delivery["start"],
            str(delivery["delivery_id"])
        )
    )

    selected_deliveries = []
    last_end_time = None

    for delivery in sorted_deliveries:
        if last_end_time is None or delivery["start"] >= last_end_time:
            selected_deliveries.append(delivery["delivery_id"])
            last_end_time = delivery["end"]

    return selected_deliveries


# ============================================================================
# PART 2: TRUCK LOADING (Fractional Knapsack)
# ============================================================================

def optimize_truck_load(packages, weight_limit):
    """
    Maximize total package priority within the truck's weight limit.
    Packages may be divided into fractions.

    Args:
        packages: List of dictionaries containing package_id, weight, priority.
        weight_limit: Maximum weight the truck can carry.

    Returns:
        Dictionary containing total_priority, total_weight, and packages.
    """
    result = {
        "total_priority": 0.0,
        "total_weight": 0.0,
        "packages": []
    }

    if not packages or weight_limit <= 0:
        return result

    # Ignore packages with nonpositive weight or priority.
    valid_packages = [
        package for package in packages
        if package["weight"] > 0 and package["priority"] > 0
    ]

    # Greedy choice: highest priority-to-weight ratio first.
    sorted_packages = sorted(
        valid_packages,
        key=lambda package: (
            package["priority"] / package["weight"],
            str(package["package_id"])
        ),
        reverse=True
    )

    remaining_capacity = float(weight_limit)

    for package in sorted_packages:
        if remaining_capacity <= 0:
            break

        package_weight = float(package["weight"])
        package_priority = float(package["priority"])

        weight_taken = min(package_weight, remaining_capacity)
        fraction_taken = weight_taken / package_weight
        priority_taken = package_priority * fraction_taken

        result["packages"].append({
            "package_id": package["package_id"],
            "fraction": fraction_taken
        })

        result["total_weight"] += weight_taken
        result["total_priority"] += priority_taken
        remaining_capacity -= weight_taken

    return result


# ============================================================================
# PART 3: DRIVER ASSIGNMENT (Interval Scheduling)
# ============================================================================

def minimize_drivers(deliveries):
    """
    Assign deliveries to the minimum number of drivers.

    Args:
        deliveries: List of dictionaries containing delivery_id, start, end.

    Returns:
        Dictionary containing num_drivers and driver assignments.
    """
    if not deliveries:
        return {
            "num_drivers": 0,
            "assignments": []
        }

    # Process deliveries in ascending order of start time.
    sorted_deliveries = sorted(
        deliveries,
        key=lambda delivery: (
            delivery["start"],
            delivery["end"],
            str(delivery["delivery_id"])
        )
    )

    # Min-heap stores (driver's current finish time, driver index).
    available_drivers = []
    assignments = []

    for delivery in sorted_deliveries:
        start_time = delivery["start"]
        end_time = delivery["end"]
        delivery_id = delivery["delivery_id"]

        # Reuse the driver who finishes earliest if available.
        if available_drivers and available_drivers[0][0] <= start_time:
            _, driver_index = heapq.heappop(available_drivers)
        else:
            # All current drivers are busy, so create another driver.
            driver_index = len(assignments)
            assignments.append([])

        assignments[driver_index].append(delivery_id)

        # Update when this driver will become available.
        heapq.heappush(
            available_drivers,
            (end_time, driver_index)
        )

    return {
        "num_drivers": len(assignments),
        "assignments": assignments
    }


# ============================================================================
# TESTING & BENCHMARKING
# ============================================================================

def load_scenario(filename):
    """Load a scenario from JSON file."""
    with open(f"scenarios/{filename}", "r") as file:
        return json.load(file)


def test_package_prioritization():
    """Test package prioritization with small known cases."""
    print("=" * 70)
    print("TESTING PACKAGE PRIORITIZATION")
    print("=" * 70 + "\n")

    # Test 1: Non-overlapping deliveries.
    test1 = [
        {"delivery_id": "A", "start": 1, "end": 2},
        {"delivery_id": "B", "start": 3, "end": 4},
        {"delivery_id": "C", "start": 5, "end": 6}
    ]

    result1 = maximize_deliveries(test1)
    passed1 = len(result1) == 3

    print("Test 1: Non-overlapping")
    print("  Expected: 3 deliveries")
    print(f"  Got: {len(result1)} deliveries")
    print(f"  {'PASS' if passed1 else 'FAIL'}\n")

    # Test 2: Overlapping deliveries.
    test2 = [
        {"delivery_id": "A", "start": 1, "end": 5},
        {"delivery_id": "B", "start": 2, "end": 4},
        {"delivery_id": "C", "start": 3, "end": 6}
    ]

    result2 = maximize_deliveries(test2)
    passed2 = len(result2) == 1

    print("Test 2: All overlapping")
    print("  Expected: 1 delivery")
    print(f"  Got: {len(result2)} deliveries")
    print(f"  Result: {result2}")
    print(f"  {'PASS' if passed2 else 'FAIL'}\n")

    # Test 3: Mixed overlapping deliveries.
    test3 = [
        {"delivery_id": "A", "start": 1, "end": 3},
        {"delivery_id": "B", "start": 2, "end": 5},
        {"delivery_id": "C", "start": 4, "end": 7},
        {"delivery_id": "D", "start": 6, "end": 9}
    ]

    result3 = maximize_deliveries(test3)
    passed3 = len(result3) == 2

    print("Test 3: Mixed overlapping")
    print("  Expected: 2 deliveries")
    print(f"  Got: {len(result3)} deliveries")
    print(f"  Result: {result3}")
    print(f"  {'PASS' if passed3 else 'FAIL'}\n")

    # Test 4: Empty input.
    result4 = maximize_deliveries([])
    passed4 = result4 == []

    print("Test 4: Empty input")
    print(f"  {'PASS' if passed4 else 'FAIL'}\n")

    assert all([passed1, passed2, passed3, passed4]), (
        "Package prioritization tests failed."
    )


def test_truck_loading():
    """Test truck loading with small known cases."""
    print("=" * 70)
    print("TESTING TRUCK LOADING")
    print("=" * 70 + "\n")

    # Test 1: All packages fit.
    packages1 = [
        {"package_id": "A", "weight": 10, "priority": 60},
        {"package_id": "B", "weight": 20, "priority": 100}
    ]

    result1 = optimize_truck_load(packages1, 50)

    passed1 = (
        abs(result1["total_priority"] - 160) < 1e-9
        and abs(result1["total_weight"] - 30) < 1e-9
    )

    print("Test 1: All packages fit")
    print("  Expected: Priority = 160, weight = 30")
    print(
        f"  Got: Priority = {result1['total_priority']}, "
        f"weight = {result1['total_weight']}"
    )
    print(f"  {'PASS' if passed1 else 'FAIL'}\n")

    # Test 2: Fractional knapsack.
    packages2 = [
        {"package_id": "A", "weight": 10, "priority": 60},
        {"package_id": "B", "weight": 20, "priority": 100},
        {"package_id": "C", "weight": 30, "priority": 120}
    ]

    result2 = optimize_truck_load(packages2, 50)

    passed2 = (
        abs(result2["total_priority"] - 240) < 1e-9
        and abs(result2["total_weight"] - 50) < 1e-9
    )

    print("Test 2: Fractional knapsack")
    print("  Expected: Priority = 240, weight = 50")
    print(
        f"  Got: Priority = {result2['total_priority']}, "
        f"weight = {result2['total_weight']}"
    )
    print(f"  Packages: {result2['packages']}")
    print(f"  {'PASS' if passed2 else 'FAIL'}\n")

    # Test 3: Empty packages.
    result3 = optimize_truck_load([], 50)
    passed3 = result3["total_priority"] == 0

    print("Test 3: Empty packages")
    print(f"  {'PASS' if passed3 else 'FAIL'}\n")

    assert all([passed1, passed2, passed3]), (
        "Truck loading tests failed."
    )


def test_driver_assignment():
    """Test driver assignment with small known cases."""
    print("=" * 70)
    print("TESTING DRIVER ASSIGNMENT")
    print("=" * 70 + "\n")

    # Test 1: All non-overlapping deliveries.
    deliveries1 = [
        {"delivery_id": "A", "start": 1, "end": 2},
        {"delivery_id": "B", "start": 3, "end": 4},
        {"delivery_id": "C", "start": 5, "end": 6}
    ]

    result1 = minimize_drivers(deliveries1)
    passed1 = result1["num_drivers"] == 1

    print("Test 1: Non-overlapping")
    print("  Expected: 1 driver")
    print(f"  Got: {result1['num_drivers']} drivers")
    print(f"  {'PASS' if passed1 else 'FAIL'}\n")

    # Test 2: All deliveries overlap.
    deliveries2 = [
        {"delivery_id": "A", "start": 1, "end": 5},
        {"delivery_id": "B", "start": 2, "end": 6},
        {"delivery_id": "C", "start": 3, "end": 7}
    ]

    result2 = minimize_drivers(deliveries2)
    passed2 = result2["num_drivers"] == 3

    print("Test 2: All overlapping")
    print("  Expected: 3 drivers")
    print(f"  Got: {result2['num_drivers']} drivers")
    print(f"  {'PASS' if passed2 else 'FAIL'}\n")

    # Test 3: Mixed overlapping.
    deliveries3 = [
        {"delivery_id": "A", "start": 1, "end": 3},
        {"delivery_id": "B", "start": 2, "end": 4},
        {"delivery_id": "C", "start": 4, "end": 6},
        {"delivery_id": "D", "start": 5, "end": 7}
    ]

    result3 = minimize_drivers(deliveries3)
    passed3 = result3["num_drivers"] == 2

    print("Test 3: Mixed overlapping")
    print("  Expected: 2 drivers")
    print(f"  Got: {result3['num_drivers']} drivers")
    print(f"  Assignments: {result3['assignments']}")
    print(f"  {'PASS' if passed3 else 'FAIL'}\n")

    # Test 4: Empty input.
    result4 = minimize_drivers([])
    passed4 = result4["num_drivers"] == 0

    print("Test 4: Empty input")
    print(f"  {'PASS' if passed4 else 'FAIL'}\n")

    assert all([passed1, passed2, passed3, passed4]), (
        "Driver assignment tests failed."
    )


def benchmark_scenarios():
    """Benchmark all algorithms on realistic scenarios."""
    print("\n" + "=" * 70)
    print("BENCHMARKING ON REALISTIC SCENARIOS")
    print("=" * 70 + "\n")

    # Benchmark package prioritization.
    print("Scenario 1: Package Prioritization (50 deliveries)")
    print("-" * 70)

    data = load_scenario("package_prioritization.json")

    start = time.perf_counter()
    result = maximize_deliveries(data)
    elapsed = time.perf_counter() - start

    print(f"  Deliveries scheduled: {len(result)} out of {len(data)}")
    print(f"  Runtime: {elapsed * 1000:.4f} ms\n")

    # Benchmark truck loading.
    print("Scenario 2: Truck Loading (100 packages, 500 lb limit)")
    print("-" * 70)

    data = load_scenario("truck_loading.json")

    start = time.perf_counter()
    result = optimize_truck_load(
        data["packages"],
        data["truck_capacity"]
    )
    elapsed = time.perf_counter() - start

    print(f"  Total priority loaded: {result['total_priority']:.2f}")
    print(f"  Total weight loaded: {result['total_weight']:.2f} lbs")
    print(f"  Packages used: {len(result['packages'])}")
    print(f"  Runtime: {elapsed * 1000:.4f} ms\n")

    # Benchmark driver assignment.
    print("Scenario 3: Driver Assignment (60 deliveries)")
    print("-" * 70)

    data = load_scenario("driver_assignment.json")

    start = time.perf_counter()
    result = minimize_drivers(data)
    elapsed = time.perf_counter() - start

    print(f"  Drivers needed: {result['num_drivers']}")
    print(f"  Runtime: {elapsed * 1000:.4f} ms\n")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

if __name__ == "__main__":
    print("GREEDY ALGORITHMS ASSIGNMENT")
    print("Running all tests and performance benchmarks.\n")

    test_package_prioritization()
    test_truck_loading()
    test_driver_assignment()

    print("\nAll small test suites passed.")
    benchmark_scenarios()