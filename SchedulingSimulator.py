from collections import deque
import time


class Process:
    def __init__(self, pid, name, arrival_time, priority, cpu_bursts, io_bursts):
        self.pid = pid
        self.name = name
        self.arrival_time = arrival_time
        self.priority = priority
        self.cpu_bursts = cpu_bursts
        self.io_bursts = io_bursts
        self.state = "NEW"
        self.remaining_cpu_bursts = deque(cpu_bursts)
        self.remaining_io_bursts = deque(io_bursts)
        self.finish_time = 0
        self.turnaround_time = 0
        self.wait_time = 0
        self.io_wait_time = 0


class Scheduler:
    def __init__(self, simulation_mode, simulation_unit_time, quantum):
        self.simulation_mode = simulation_mode
        self.simulation_unit_time = simulation_unit_time
        self.quantum = quantum
        self.current_time = 0
        self.cpu = None
        self.ready_queue = deque()
        self.io_devices = []
        self.io_queues = []
        self.processes = []
        self.completed_processes = []
        self.event_log = []

    def load_processes(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                name = parts[0]
                arrival_time = int(parts[1])
                priority = int(parts[2])
                cpu_bursts = [int(parts[i]) for i in range(3, len(parts)) if i % 2 == 0]
                io_bursts = [int(parts[i]) for i in range(3, len(parts)) if i % 2 != 0]
                process = Process(len(self.processes), name, arrival_time, priority, cpu_bursts, io_bursts)
                self.processes.append(process)

    def add_io_device(self):
        self.io_devices.append("IDLE")
        self.io_queues.append(deque())

    def schedule_processes(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        while self.processes or any(self.io_queues) or self.cpu or self.ready_queue:
            print(f"Current time: {self.current_time}")
            if self.processes and self.processes[0].arrival_time <= self.current_time:
                process = self.processes.pop(0)
                self.ready_queue.append(process)
                print(f"Process {process.name} is newly created.")
            for io_device, io_queue in enumerate(self.io_queues):
                if io_queue:
                    process = io_queue[0]
                    if process.remaining_io_bursts[0] == 0:
                        io_queue.popleft()
                        process.state = "READY"
                        self.ready_queue.append(process)
                        print(f"Process {process.name} completes I/O and returns to the ready queue.")
                    else:
                        process.io_wait_time += 1
            if self.cpu:
                process = self.cpu
                if process.remaining_cpu_bursts[0] == 0:
                    process.remaining_cpu_bursts.popleft()
                    if process.remaining_cpu_bursts:
                        process.remaining_io_bursts.popleft()
                        process.state = "WAITING"
                        self.io_queues[process.pid].append(process)
                        self.cpu = None
                        print(f"Process {process.name} is put into I/O queue.")
                    else:
                        process.finish_time = self.current_time
                        process.turnaround_time = process.finish_time - process.arrival_time
                        self.completed_processes.append(process)
                        self.cpu = None
                        print(f"Process {process.name} terminates.")
            if not self.cpu and self.ready_queue:
                process = self.ready_queue.popleft()
                process.state = "RUNNING"
                self.cpu = process
                print(f"Process {process.name} is dispatched from the ready queue to use the CPU.")
            self.current_time += 1
            if self.simulation_mode == 0:
                time.sleep(self.simulation_unit_time)

            print("Current ready queue:")
            for process in self.ready_queue:
                print(f"Process {process.name} (PID: {process.pid})")

            print("Current IO queues:")
            for i, io_queue in enumerate(self.io_queues):
                print(f"I/O Device {i}:")
                for process in io_queue:
                    print(f"  Process {process.name} (PID: {process.pid})")

        print("Simulation completed.")





    def log_event(self, event):
        self.event_log.append(f"[{self.current_time}] {event}")

    def display_event_log(self):
        for event in self.event_log:
            print(event)

    def calculate_metrics(self):
        total_turnaround_time = sum(process.turnaround_time for process in self.completed_processes)
        total_wait_time = sum(process.wait_time for process in self.completed_processes)
        cpu_utilization = (self.current_time - total_wait_time) / self.current_time * 100
        average_turnaround_time = total_turnaround_time / len(self.completed_processes)
        average_wait_time = total_wait_time / len(self.completed_processes)
        throughput = len(self.completed_processes) / self.current_time
        print(f"CPU Utilization: {cpu_utilization}%")
        print(f"Average Turnaround Time: {average_turnaround_time}")
        print(f"Average Wait Time: {average_wait_time}")
        print(f"Throughput: {throughput}")


def main():
    simulation_mode = int(input("Enter simulation mode (0 for auto, 1 for manual): "))
    simulation_unit_time = int(input("Enter simulation unit time (ms): "))
    quantum = int(input("Enter quantum for round-robin scheduling: "))
    filename = input("Enter filename for process info: ")

    scheduler = Scheduler(simulation_mode, simulation_unit_time, quantum)
    scheduler.load_processes(filename)
    scheduler.add_io_device()

    scheduler.schedule_processes()

    scheduler.display_event_log()
    scheduler.calculate_metrics()


if __name__ == "__main__":
    main()
