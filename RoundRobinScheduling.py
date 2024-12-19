def round_robin_scheduling(processes, quantum):
    """This code implements round robin scheduling algorithm
    Author: Rahul Kumar
    Date: October 12, 2024
    """

    n = len(processes)
    rem_burst_times = [p[1] for p in processes]  # Remaining burst times for each process
    waiting_time = [0] * n  # Waiting times for each process
    turnaround_time = [0] * n  # Turnaround times for each process
    t = 0  # Current time

    # Loop until all processes are complete
    while any(rem_burst_times[i] > 0 for i in range(n)):
        for i in range(n):
            if rem_burst_times[i] > 0:  # If process has remaining burst time
                process_executed = False

                if rem_burst_times[i] > quantum:
                    # Process runs for the full quantum
                    t += quantum
                    rem_burst_times[i] -= quantum
                    process_executed = True
                else:
                    # Process finishes its execution
                    t += rem_burst_times[i]
                    waiting_time[i] = t - processes[i][1]  # Calculate waiting time
                    rem_burst_times[i] = 0  # Process completed
                    process_executed = True

                if process_executed:
                    print(f"Process {processes[i][0]} executed for {quantum if rem_burst_times[i] > 0 else processes[i][1]} units")

    # Calculate turnaround time for each process
    for i in range(n):
        turnaround_time[i] = processes[i][1] + waiting_time[i]  # Turnaround time = burst time + waiting time

    # Calculate average times
    avg_waiting = sum(waiting_time) / n
    avg_turnaround = sum(turnaround_time) / n

    # Display results
    print("\nProcess ID\tBurst Time\tWaiting Time\tTurnaround Time")
    for i in range(n):
        print(f"{processes[i][0]}\t\t\t{processes[i][1]}\t\t\t{waiting_time[i]}\t\t\t\t{turnaround_time[i]}")
    print(f"\nAverage Waiting Time: {avg_waiting}")
    print(f"Average Turnaround Time: {avg_turnaround}")

if __name__ == '__main__':
    while True:
        # Sample list of processes [process_id, burst_time]
        processes = [[1, 10], [2, 1], [3, 2], [4, 1], [5, 5]]
        quantum = int(input("Enter time quantum: "))
        round_robin_scheduling(processes, quantum)

        # Ask the user if they want to continue
        cont = input("Do you want to run again with a different quantum? (Y/N): ").strip()
        if cont != 'Y':
            break


