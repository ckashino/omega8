# Omega8 CPU
A simple RISC-V inspired 8-bit CPU and ISA with a main focus of simplicity and low resource usage. The main design includes three major components: an ALU, a register file, and the main core.

Simple test benches are written in Python with cocotb which test the main components individually. Within the *examples/* folder, there is a full design example which also provides
a simple RAM and instruction memory designs. Tests for this are also included. Additionally, a full example running on real hardware is available [here](https://github.com/ckashino/omega8_hardware_demo).

*assemble.py* contains a simple assembler to convert Omega8 assemble code into machine code. It can be ran simply through:

```
python assemble.py filename [verilog]
```

The 'verilog' argument can be included to help with formatting Verilog case statements. A sample assembly file can be found at examples/fib.omega

The simple ISA specs can also be found within specs.txt.

# Positives
- Machine codes are simple and easy decipher, bit positions always mean the same thing
- Very low resource usage in hardware, as can be seen within the hardware exmaple.
- While only an 8-bit CPU, 16-bit operations can be easily performed using the supplied ADDC and SUBB instructions.

# Negatives
- Simple machine code format means many don't care bits within each instruction, wasting memory/resources.
- Not pipelined.

# Example Walkthrough

The supplied example calculates the 7th Fibonacci number.

```
0x0: ldi r0, 6        # counter
0x1: ldi r1, 0        # f0
0x2: ldi r2, 1        # f1
0x3: ldi r3, 0        # f(n)
0x4: add r3, r1, r2
0x5: mov r1, r2
0x6: mov r2, r3
0x7: addi r0, r0, -1
0x8: jnz 0x4
0x9: push r3
0xA: nop
0xB: pop r4
```
It starts off by initializing the relevant registers, zeroing r1 and r3, setting r2 to 1 (f(1)) and setting r0 to 6 ('loop' variable).
Then performs the standard sequence of f(n) = f(n - 1) + f(n - 2), equivalent to r3 = r2 + r1. After, it moves f(n) into r2 (the new
f(n-1)) and moves r2 into r1 (the new f(n-2)). The loop variable is then decremented, if there is still iterations remaining it jumps
back to the start of the iteration calculation steps, otherwises moves on. Once the 'loop' is done, the final f(n) is pushed to the memory
at the current stack address, the CPU arbitrarily waits a cycle, then the result is popped from the stack into r4 for testing purposes.

# TODO
- (Optional?) multiply instrcutions.
- Improve assembler to include support for planned pseudo instructions which will utilize existing instructions (e.g. IF, ADD16).
- More consistent testing patterns.
- Potentially move PUSH/POP instructions to be pseudo instructions, allowing the assembler to keep track of the stack pointer. This will also remove the stack pointer from the entire ISA.
