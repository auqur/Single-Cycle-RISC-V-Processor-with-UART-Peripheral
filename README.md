# Single-Cycle RISC-V Processor with UART Peripheral  

## Project Overview  
This project was developed as part of the **EE446 Computer Architecture Laboratory** at METU.  
Together with my teammate, we designed and implemented a **32-bit single-cycle RISC-V processor** in **Verilog HDL**, including a **custom UART peripheral** for serial communication.  

The processor supports the **RV32I Base Integer Instruction Set** (with one additional instruction extension) and was deployed on the **Nexys A7 FPGA** board.  

## Features  
- **Datapath & Controller** fully implemented in Verilog  
- Supports arithmetic, logic, shift, set, branch, jump, load/store, and immediate instructions  
- **UART peripheral** with memory-mapped I/O (0x00000400 for TX, 0x00000404 for RX)  
- **16-byte FIFO receive buffer** to prevent data loss  
- **Testbench** written in Python (cocotb-style), verifying correct execution of instructions  
- Demonstrated on FPGA with interactive UART communication via Tera Term  

## Tools & Technologies  
- **HDL**: Verilog  
- **Testbench**: Python (cocotb)  
- **Hardware**: Xilinx Nexys A7 FPGA  
- **Software**: Vivado, ModelSim, Tera Term  

## Instruction Set Implemented  
- **Arithmetic**: ADD[I], SUB  
- **Logic**: AND[I], OR[I], XOR[I]  
- **Shift**: SLL[I], SRL[I], SRA[I]  
- **Set if less than**: SLT[I][U]  
- **Branch**: BEQ, BNE, BLT[U], BGE[U]  
- **Jump**: JAL, JALR  
- **Load/Store**: LW, LH[U], LB[U], SW, SH, SB  
- **Others**: LUI, AUIPC  

## How to Run  
1. Clone this repository  
2. Open the project in Vivado / ModelSim  
3. Run the testbench:  
   ```bash
   make
4. Synthesize and upload the design to the Nexys A7 FPGA
5. Use Tera Term (9600 baud, 8N1) to interact with the UART peripheral

## Contributors

Mustafa Mert Mıhçı & Ahmet Uğur Akdemir
