import threading
import multiprocessing
import time
from dataclasses import dataclass
from collections import deque


# ============================================================
# PROCESS DATA
# ============================================================

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int


# ============================================================
# INPUT
# ============================================================

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
    print("PID Arrival_Time Burst_Time")
    print("Example: P1 0 5\n")

    used_ids = set()

    for i in range(n):

        while True:
            try:
                values = input(f"Process {i + 1}: ").split()

                if len(values) != 3:
                    print("Error: Enter exactly 3 values.")
                    continue

                pid = values[0]
                arrival = int(values[1])
                burst = int(values[2])

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
                    Process(pid, arrival, burst)
                )

                used_ids.add(pid)
                break

            except ValueError:
                print("Error: Arrival time and burst time must be integers.")

    return processes


# ============================================================
# ROUND ROBIN SCHEDULING
# ============================================================

def round_robin(processes, quantum):

    remaining = {
        p.pid: p.burst
        for p in processes
    }

    first_start = {
        p.pid: None
        for p in processes
    }

    completion = {}

    arrival_map = {
        p.pid: p.arrival
        for p in processes
    }

    process_map = {
        p.pid: p
        for p in processes
    }

    ordered = sorted(
        processes,
        key=lambda p: (p.arrival, p.pid)
    )

    ready_queue = deque()

    current_time = 0
    index = 0

    gantt = []

    while index < len(ordered) or ready_queue:

        # ----------------------------------------------------
        # CPU IDLE
        # ----------------------------------------------------

        if not ready_queue:

            if current_time < ordered[index].arrival:

                gantt.append(
                    ("IDLE", current_time, ordered[index].arrival)
                )

                current_time = ordered[index].arrival

            ready_queue.append(ordered[index].pid)
            index += 1

        # ----------------------------------------------------
        # EXECUTE PROCESS
        # ----------------------------------------------------

        pid = ready_queue.popleft()

        if first_start[pid] is None:
            first_start[pid] = current_time

        start = current_time

        execution_time = min(
            quantum,
            remaining[pid]
        )

        current_time += execution_time

        remaining[pid] -= execution_time

        gantt.append(
            (pid, start, current_time)
        )

        # ----------------------------------------------------
        # ADD NEWLY ARRIVED PROCESSES
        # ----------------------------------------------------

        while (
            index < len(ordered)
            and ordered[index].arrival <= current_time
        ):
            ready_queue.append(
                ordered[index].pid
            )
            index += 1

        # ----------------------------------------------------
        # RE-QUEUE CURRENT PROCESS
        # ----------------------------------------------------

        if remaining[pid] > 0:
            ready_queue.append(pid)
        else:
            completion[pid] = current_time

    return gantt, completion, first_start


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(processes, completion, first_start):

    results = []

    for p in processes:

        ct = completion[p.pid]

        turnaround = ct - p.arrival

        waiting = turnaround - p.burst

        response = first_start[p.pid] - p.arrival

        results.append({
            "pid": p.pid,
            "arrival": p.arrival,
            "burst": p.burst,
            "completion": ct,
            "turnaround": turnaround,
            "waiting": waiting,
            "response": response
        })

    return results


def display_metrics(results):

    print("\n" + "=" * 80)
    print("SCHEDULING METRICS")
    print("=" * 80)

    print(
        f"{'PID':<8}"
        f"{'AT':<8}"
        f"{'BT':<8}"
        f"{'CT':<8}"
        f"{'TAT':<8}"
        f"{'WT':<8}"
        f"{'RT':<8}"
    )

    print("-" * 80)

    for r in results:

        print(
            f"{r['pid']:<8}"
            f"{r['arrival']:<8}"
            f"{r['burst']:<8}"
            f"{r['completion']:<8}"
            f"{r['turnaround']:<8}"
            f"{r['waiting']:<8}"
            f"{r['response']:<8}"
        )

    avg_tat = sum(
        r["turnaround"] for r in results
    ) / len(results)

    avg_wt = sum(
        r["waiting"] for r in results
    ) / len(results)

    avg_rt = sum(
        r["response"] for r in results
    ) / len(results)

    print("-" * 80)

    print(f"Average Turnaround Time : {avg_tat:.2f}")
    print(f"Average Waiting Time    : {avg_wt:.2f}")
    print(f"Average Response Time   : {avg_rt:.2f}")


# ============================================================
# GANTT CHART
# ============================================================

def display_gantt(gantt):

    print("\n" + "=" * 80)
    print("ROUND ROBIN GANTT CHART")
    print("=" * 80)

    print("\nExecution:")
    
    for pid, start, end in gantt:
        print(
            f"| {pid:^7} ",
            end=""
        )

    print("|")

    # Exact time boundaries
    print(gantt[0][1], end="")

    for _, _, end in gantt:
        print(f"{'':>9}{end}", end="")

    print("\n")

    print("Execution intervals:")

    for pid, start, end in gantt:

        if pid == "IDLE":
            print(
                f"CPU IDLE : {start} -> {end}"
            )
        else:
            print(
                f"{pid:<8}: {start} -> {end}"
            )


# ============================================================
# THREADING
# ============================================================

def thread_work(name):

    print(
        f"\nThread {name} started"
    )

    print(
        f"Thread {name} ID: "
        f"{threading.get_ident()}"
    )

    for i in range(1, 4):

        print(
            f"Thread {name}: completed work {i}"
        )

        time.sleep(0.2)

    print(
        f"Thread {name} completed"
    )


def demonstrate_threads():

    print("\n" + "=" * 80)
    print("THREAD DEMONSTRATION")
    print("=" * 80)

    thread1 = threading.Thread(
        target=thread_work,
        args=("A",)
    )

    thread2 = threading.Thread(
        target=thread_work,
        args=("B",)
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("\nBoth threads completed.")


# ============================================================
# IPC USING PIPE
# ============================================================

def ipc_receiver(connection):

    print("\nChild process started.")
    print(
        f"Child process PID: "
        f"{multiprocessing.current_process().pid}"
    )

    message = connection.recv()

    print(
        f"Child process received message: {message}"
    )

    connection.send(
        "Message successfully received by child process."
    )

    connection.close()


def demonstrate_ipc():

    print("\n" + "=" * 80)
    print("INTER-PROCESS COMMUNICATION USING PIPE")
    print("=" * 80)

    parent_connection, child_connection = (
        multiprocessing.Pipe()
    )

    process = multiprocessing.Process(
        target=ipc_receiver,
        args=(child_connection,)
    )

    process.start()

    message = "Hello from parent process."

    print(
        f"Parent process PID: "
        f"{multiprocessing.current_process().pid}"
    )

    print(
        f"Parent process sent: {message}"
    )

    parent_connection.send(message)

    response = parent_connection.recv()

    print(
        f"Parent process received: {response}"
    )

    process.join()

    print("Child process completed.")

    parent_connection.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("SCHEDULING METRICS, THREADS AND IPC")
    print("=" * 80)

    processes = get_processes()

    while True:

        try:
            quantum = int(
                input("\nEnter Round Robin time quantum: ")
            )

            if quantum <= 0:
                print(
                    "Error: Time quantum must be greater than 0."
                )
                continue

            break

        except ValueError:
            print("Error: Enter a valid integer.")

    # --------------------------------------------------------
    # ROUND ROBIN
    # --------------------------------------------------------

    gantt, completion, first_start = round_robin(
        processes,
        quantum
    )

    display_gantt(gantt)

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    results = calculate_metrics(
        processes,
        completion,
        first_start
    )

    display_metrics(results)

    # --------------------------------------------------------
    # THREADS
    # --------------------------------------------------------

    demonstrate_threads()

    # --------------------------------------------------------
    # IPC
    # --------------------------------------------------------

    demonstrate_ipc()

    print("\n" + "=" * 80)
    print("LAB 1 Q4 DEMONSTRATION COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()