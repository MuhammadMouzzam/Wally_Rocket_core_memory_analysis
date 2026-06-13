# RISC-V Memory Hierarchy & Cache Performance Analysis

## Project Overview
This repository contains the evaluation framework, profiling tools, and analytical results for comparing the memory hierarchy and cache performance of two prominent open-source RISC-V processors: the CVW Wally core (Harvey Mudd College) and the Rocket Core (UC Berkeley). The primary workload used for this microarchitectural analysis is a 256x64 matrix transpose algorithm, compiled into a `.riscv` executable using the RISC-V GNU Toolchain.

## Methodology & Testing Strategy
The evaluation was conducted through a systematic profiling approach to isolate the impact of software optimizations and hardware configurations:

* **Ideal Baseline Simulation:** Initial execution of the workload was performed on the Spike ISA simulator to establish an ideal architectural baseline and gather fundamental instruction execution metrics without cache latency penalties.
* **Matrix Blocking Optimization:** To test spatial and temporal locality limits, the transpose algorithm was modified to use matrix blocking (tiling). 
* **Cache Associativity Sweeps:** The hardware parameters were modified to evaluate cache design impacts. The core tiles for both processors were repeatedly reconfigured and rebuilt to test varying set-associative cache configurations.

## Simulation Parameters & Experimental Workloads

### Benchmark Profile
* **Workload Application:** 256x64 Matrix Transpose Algorithm
* **Compilation Target:** 32-bit RISC-V ISA (`.riscv` binary format)
* **Execution Baseline:** Spike ISA Functional Simulator (Zero-cycle memory latency model)

### Parameterized Sweeps & Test Vectors
To comprehensively capture microarchitectural tradeoffs, the workload was profiled across explicit parameter sweeps:

* **Software-Level Blocking Sweep:** Execution was repeated across discrete block (tile) size variations: 1x1, 2x2, 4x4, 8x8, 16x16, and 32x32.
* **Hardware-Level Configuration Sweep:** The underlying memory subsystem of the CVW Wally and Rocket Core tiles were rebuilt to isolate structural associativity impacts, testing: 1-Way (Direct-Mapped), 2-Way, 4-Way, and 8-Way Set-Associative configurations.

## Performance Metrics & Visualization
During each hardware and software sweep, extensive data was collected to evaluate the processors. Every hardware-software configuration pair was evaluated based on the absolute collection of the following hardware performance counters:

* Total Clock Cycles
* Instruction Count (Retired Instructions)
* Cycles Per Instruction (CPI)
* L1 Data Cache Misses
* Memory Access Instructions: Load Word (`lw`) and Store Word (`sw`) frequencies

The repository includes a comprehensive set of comparative plots generated via Python, visualizing the performance differences between the Wally and Rocket cores. Key plots include:

* Block Size vs. Total Instructions
* Block Size vs. Clock Cycles
* Block Size vs. Cache Misses
* Block Size vs. CPI

## Technologies Used
* **Simulation & Compilation:** RISC-V GNU Toolchain, Spike ISA Simulator
* **Hardware Description:** SystemVerilog
* **Data Analysis & Plotting:** Python (Matplotlib)

## Repository Contents
This repository includes the C source code for the standard and blocked matrix transpose algorithms, the generated `.riscv` binaries, scripts used for automating the sweeps, all generated graphical plots, and the final analytical report detailing the comparative microarchitectural behavior of both cores.
