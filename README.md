# Python Scheduling Simulator

---

A basic python-based process scheduling simulator.

## Scheduling Algorithms

- **First-come first-served (FCFS):** Tasks are executed based on the order they were received.

- **Round-Robin (RR):** Each process is assigned a fixed time slice. Each process gets a turn to execute for its allotted time slice before being preempted to allow another process to run.

- **Shortest Job First (SJF):** The process with the shortest estimated run time is selected for execution next.

- **Priority Scheduling (PS):** Execution of processes is prioritized based on their relative priority

## Program Input

- **Simulation Mode:** 0 for auto, 1 for manual
  
  - **Auto:** Simulation steps are updated automatically
  
  - **Manual:** User input needed to progress to the next simulation step

- **Simulation Unit Time (ms):** The time between two simulation steps in auto mode

- **Quantum (Time Slice):** Only used in Round Robin. Maximum amount of time each process has with the CPU before proceeding to the next process 

## Simulation Input File

&lt;name&gt; &lt;s&gt; &lt;p&gt; &lt;C0&gt; &lt;I0&gt; ... &lt;Cn-1&gt; &lt;In-1&gt; &lt;Cn&gt;

- **name:** Name of the process (String with no spaces)

- **s:** Arrival time of the process

- **p:** Priority level of the process (0-9), in which 0 is the highest priority and 9 is the highest

- **C<sub>i</sub>:** The *i* <sup>th</sup> CPU burst time

- **I<sub>i</sub>:** The *i* <sup>th</sup> IO burst time
