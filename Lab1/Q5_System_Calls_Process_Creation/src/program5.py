import os
import time
import subprocess

# ---------------------------------------------------------
# 1. CREATE A CHILD PROCESS
# ---------------------------------------------------------

print("===== SYSTEM CALLS AND PROCESS CREATION =====")

pid = os.fork()

if pid == 0:
    # =====================================================
    # CHILD PROCESS
    # =====================================================

    print("\n--- CHILD PROCESS ---")
    print("Child Process ID (PID):", os.getpid())
    print("Parent Process ID (PPID):", os.getppid())

    # -----------------------------------------------------
    # 4. EXECUTE A HARMLESS LINUX COMMAND
    # -----------------------------------------------------

    print("\nExecuting harmless Linux command: pwd")

    try:
        subprocess.run(["pwd"], check=True)
        print("Command executed successfully.")
    except Exception as e:
        print("Command execution failed:", e)

    # -----------------------------------------------------
    # 5. CREATE, WRITE, READ AND CLOSE A TEST FILE
    # -----------------------------------------------------

    filename = "os_test_file.txt"

    print("\n--- FILE OPERATIONS ---")

    try:
        # Create and write
        with open(filename, "w") as file:
            file.write("This is a controlled OS Lab test file.\n")
            file.write("File creation, writing and reading successful.\n")

        print("File created and written:", filename)

        # Read
        with open(filename, "r") as file:
            data = file.read()

        print("File contents:")
        print(data)

        print("File read and closed successfully.")

    except OSError as e:
        print("File operation error:", e)

    # -----------------------------------------------------
    # 6. INSPECT /dev/null
    # -----------------------------------------------------

    print("\n--- DEVICE INTERFACE ---")

    try:
        with open("/dev/null", "w") as device:
            device.write("Test data sent to /dev/null\n")

        print("/dev/null opened, written and closed successfully.")

    except OSError as e:
        print("Device interface error:", e)

    # -----------------------------------------------------
    # 7. HANDLE INVALID FILE OPERATION
    # -----------------------------------------------------

    print("\n--- ERROR HANDLING ---")

    invalid_file = "/invalid/path/test.txt"

    try:
        with open(invalid_file, "r") as file:
            data = file.read()

    except FileNotFoundError:
        print("Error handled: File does not exist ->", invalid_file)

    except PermissionError:
        print("Error handled: Permission denied ->", invalid_file)

    except OSError as e:
        print("Error handled:", e)

    # Child exits
    print("\nChild process completed.")
    os._exit(0)


else:
    # =====================================================
    # PARENT PROCESS
    # =====================================================

    print("\n--- PARENT PROCESS ---")
    print("Parent Process ID (PID):", os.getpid())
    print("Created Child Process ID:", pid)

    # -----------------------------------------------------
    # 3. WAIT FOR CHILD PROCESS
    # -----------------------------------------------------

    print("\nWaiting for child process to complete...")

    child_pid, status = os.waitpid(pid, 0)

    print("Child process completed.")
    print("Child PID returned by waitpid():", child_pid)

    if os.WIFEXITED(status):
        print("Child exit status:", os.WEXITSTATUS(status))

    print("\n===== PROGRAM COMPLETED =====")