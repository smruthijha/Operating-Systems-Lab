from dataclasses import dataclass


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    input_order: int


def get_processes():
    processes = []

    while True:
        try:
            n = int(input("Enter number of processes: "))

            if n <= 0:
                print("Error: Number of processes must be greater than 0.")
                continue

            break

        except ValueError:
            print("Error: Enter a valid integer.")


    print("\nEnter process details:")
    print("Format: Process_ID Arrival_Time Burst_Time")
    print("Example: P1 0 5\n")

    used_ids = set()

    for i in range(n):

        while True:
            try:
                data = input(f"Process {i + 1}: ").split()

                if len(data) != 3:
                    print("Error: Enter exactly 3 values.")
                    continue

                pid = data[0]
                arrival = int(data[1])
                burst = int(data[2])

                if pid in used_ids:
                    print("Error: Process ID must be unique.")
                    continue

                if arrival < 0:
                    print("Error: Arrival time cannot be negative.")
                    continue

                if burst <= 0:
                    print("Error: Burst time must be greater than 0.")
                    continue

                processes.append(
                    Process(pid, arrival, burst, i)
                )

                used_ids.add(pid)
                break

            except ValueError:
                print("Error: Arrival time and burst time must be integers.")

    return processes


def fcfs(processes):
    # Sort by arrival time.
    # If arrival times are equal, original input order is used.
    ordered = sorted(
        processes,
        key=lambda p: (p.arrival, p.input_order)
    )

    current_time = 0
    schedule = []

    for p in ordered:

        # CPU is idle if the next process has not arrived.
        if current_time < p.arrival:
            schedule.append(
                ("IDLE", current_time, p.arrival)
            )
            current_time = p.arrival

        start = current_time
        end = start + p.burst

        schedule.append(
            (p.pid, start, end)
        )

        current_time = end

    return schedule


def sjf(processes):
    # Non-preemptive SJF
    # Tie-breaking:
    # 1. Shortest burst time
    # 2. Earlier arrival time
    # 3. Original input order

    remaining = processes.copy()

    current_time = 0
    schedule = []

    while remaining:

        # Find processes that have already arrived.
        available = [
            p for p in remaining
            if p.arrival <= current_time
        ]

        # If no process has arrived yet, CPU becomes idle.
        if not available:

            next_arrival = min(
                p.arrival for p in remaining
            )

            schedule.append(
                ("IDLE", current_time, next_arrival)
            )

            current_time = next_arrival
            continue

        # Select shortest available process.
        selected = min(
            available,
            key=lambda p: (
                p.burst,
                p.arrival,
                p.input_order
            )
        )

        start = current_time
        end = start + selected.burst

        schedule.append(
            (selected.pid, start, end)
        )

        current_time = end
        remaining.remove(selected)

    return schedule


def display_schedule(name, schedule):

    print("\n" + "=" * 55)
    print(name)
    print("=" * 55)

    print("\nExecution Sequence:")

    sequence = [
        item[0]
        for item in schedule
    ]

    print(" -> ".join(sequence))

    print("\nStart / End Intervals:")

    for pid, start, end in schedule:
        if pid == "IDLE":
            print(f"CPU IDLE : {start} -> {end}")
        else:
            print(f"{pid:8} : {start} -> {end}")


def main():

    print("=" * 55)
    print("       FCFS AND NON-PREEMPTIVE SJF SCHEDULING")
    print("=" * 55)

    processes = get_processes()

    # Original data is never modified.
    original_processes = processes.copy()

    fcfs_schedule = fcfs(original_processes)
    sjf_schedule = sjf(original_processes)

    display_schedule(
        "FCFS SCHEDULING",
        fcfs_schedule
    )

    display_schedule(
        "NON-PREEMPTIVE SJF SCHEDULING",
        sjf_schedule
    )


if __name__ == "__main__":
    main()