RISC-V 5-Stage Pipeline Simulator
https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/GUI-Tkinter-orange.svg

A comprehensive educational simulator for the RISC-V 32-bit instruction set architecture with a 5-stage pipeline visualization. This tool helps students and developers understand pipeline hazards, forwarding, and the inner workings of a RISC-V CPU.

https://screenshot.png

✨ Features
🎯 Core Simulation
5-Stage Pipeline: IF (Instruction Fetch), ID (Decode), EX (Execute), MEM (Memory), WB (Write Back)

Full RV32I Support: Implements all base integer instructions (R, I, S, B, J, U types)

Visual Pipeline: Real-time visualization of instructions moving through pipeline stages

Step-by-Step Execution: Run instructions one cycle at a time or at adjustable speeds

Hazard Detection: Automatically detects and reports data and control hazards

📊 Visualizations
Register File: Live view of all 32 registers (x0-x31)

Memory View: Monitor memory contents during execution

Pipeline Stages: See current instruction in each stage with detailed information

Statistics Panel: Track cycles, instructions executed, hazards, and CPI

🛠️ Educational Tools
Hazard Explanations: Clear messages explaining detected hazards

Forwarding Visualization: See forwarding paths in action

Cycle Counting: Understand pipeline efficiency through CPI calculation

Instruction Table: View all loaded instructions with PC and type information

🏗️ Architecture
The simulator is built with a modular architecture:

text
riscv-simulator/
├── cpu.py              # CPU core with pipeline stages
├── memory.py           # Memory management
├── alu.py              # Arithmetic Logic Unit operations
├── hazard_detector.py  # Hazard detection and forwarding
├── opcode.py           # Instruction encoding and types
├── parser.py           # Assembly code parser
├── simulator.py        # Main simulator orchestrator
├── gui.py             # Tkinter-based user interface
└── README.md          # This file
Key Components:
CPU: Manages the pipeline stages (IF, ID, EX, MEM, WB) and register file

Memory: Simulates data memory with load/store operations

ALU: Performs all arithmetic and logical operations

Hazard Detector: Identifies data and control hazards, handles forwarding

Parser: Converts assembly code to internal instruction format

GUI: Provides visualization and user interaction

🚀 Installation
Prerequisites
Python 3.8 or higher

Tkinter (usually comes with Python)

Quick Start
Clone the repository:

bash
git clone https://github.com/yourusername/riscv-pipeline-simulator.git
cd riscv-pipeline-simulator
Run the simulator:

bash
python gui.py
💻 Usage
1. Writing Assembly Code
Enter your RISC-V assembly code in the text editor:

assembly
# Sample program with hazards
addi x1, x0, 10      # x1 = 10
addi x2, x0, 20      # x2 = 20
add  x3, x1, x2      # x3 = x1 + x2 (data hazard)
sub  x4, x3, x1      # x4 = x3 - x1 (data hazard)
sw   x4, 0(x0)       # Store x4 to memory
lw   x5, 0(x0)       # Load from memory (load-use hazard)
addi x6, x5, 5       # Use loaded value
beq  x3, x3, 8       # Branch (control hazard)
addi x7, x0, 100     # This may be skipped
2. Loading and Running
Load Program: Parses and loads the assembly code

Step: Execute one pipeline cycle at a time

Run: Execute continuously at adjustable speed

Reset: Clear all state and start over

3. Understanding the Display
Pipeline Stages: Each stage shows the current instruction and relevant data

Registers: Watch values change in real-time (x0 is always 0)

Memory: See stored values at different addresses

Statistics: Monitor performance metrics

Log: Detailed execution trace with hazard notifications

📚 Supported Instructions
R-Type (Register-Register)
add, sub, and, or, xor, sll, srl, sra, slt, sltu

I-Type (Immediate)
addi, andi, ori, xori, slti, sltiu

slli, srli, srai

Loads: lw, lb, lh, lbu, lhu

jalr

S-Type (Store)
sw, sb, sh

B-Type (Branch)
beq, bne, blt, bge, bltu, bgeu

J-Type (Jump)
jal

U-Type (Upper Immediate)
lui, auipc

🔍 Pipeline Hazards
The simulator detects and explains three types of hazards:

1. Data Hazards
RAW (Read After Write): When an instruction needs a value that hasn't been written yet

Load-Use: Special case where a load is followed by an instruction that uses the loaded value

2. Control Hazards
Branches and Jumps: Instructions that change the program counter

Pipeline Flush: Subsequent instructions are discarded when a branch is taken

3. Forwarding
The simulator implements forwarding (data bypassing) to handle many data hazards without stalling:

EX to EX forwarding for arithmetic operations

MEM to EX forwarding for memory results

🧪 Example Programs
The simulator comes with several built-in examples:

Basic Arithmetic
assembly
addi x1, x0, 5
addi x2, x0, 3
add x3, x1, x2
sub x4, x1, x2
Memory Operations
assembly
addi x1, x0, 42
sw x1, 0(x0)
lw x2, 0(x0)
addi x3, x2, 10
Control Flow
assembly
addi x1, x0, 10
addi x2, x0, 20
loop:
  addi x1, x1, -1
  bne x1, x0, loop
📊 Performance Metrics
The simulator tracks:

CPI (Cycles Per Instruction): Measure of pipeline efficiency

Total Cycles: Number of clock cycles executed

Instructions Executed: Count of completed instructions

Hazards Detected: Number of pipeline hazards encountered

🧠 Learning Outcomes
Using this simulator helps understand:

RISC-V instruction set architecture

Pipeline stage interactions

Hazard detection and resolution

Forwarding techniques

Control flow implications

Memory hierarchy basics

Performance measurement (CPI)

🐛 Known Limitations
Simplified Memory: Memory is word-addressable (not byte-addressable)

No Cache: Direct memory access without cache simulation

Basic Forwarding: Limited forwarding paths implemented

No Stalling: Pipeline doesn't stall for hazards (uses flushing for control hazards)

Instruction Limit: Programs limited to 256 instructions

🔮 Future Enhancements
Planned features:

Cache simulation

More sophisticated hazard handling (stalling)

Multi-cycle operations

Superscalar pipeline

Out-of-order execution

Branch prediction

Save/Load program state

Export execution traces

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
RISC-V International for the ISA specification

UC Berkeley for pioneering RISC architecture education

The open-source community for Python and Tkinter resources

📚 Resources
RISC-V Specification

Computer Organization and Design (Patterson & Hennessy)

RISC-V Green Card
