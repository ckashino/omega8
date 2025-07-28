import sys
import re
from typing import Optional

instr_type_opcode = {
        "ldi": 0x00,
        "ld": 0x10,
        "st": 0x11,
        "mov": 0x20,
        "add": 0x30,
        "addc": 0x31,
        "sub": 0x32,
        "subb": 0x33,
        "and": 0x34,
        "or": 0x35,
        "xor": 0x36,
        "addi": 0x40,
        "jmp": 0x50,
        "jz": 0x51,
        "jnz": 0x52,
        "jn": 0x53,
        "jnn": 0x54,
        "call": 0x60,
        "ret": 0x70,
        "push": 0x80,
        "pop": 0x81,
        "nop": 0xFF
        }

def assm_instr(opcode: int, r1: Optional[int],
               r2: Optional[int], r3: Optional[int],
               imm8: Optional[int], imm16: Optional[int]) -> str:
    instr_list = list("0" * 30)

    if imm16 is not None:
        if imm16 < 0:
            instr_list[14:] = "{0:016b}".format(imm16 & ((1 << 16) - 1))
        else:
            instr_list[14:] = "{0:016b}".format(imm16)
    elif imm8 is not None:
        if imm8 < 0:
            instr_list[22:] = "{0:08b}".format(imm8 & ((1 << 8) - 1))
        else:
            instr_list[22:] = "{0:08b}".format(imm8)

    if r1 is not None:
        instr_list[8:11] = "{0:03b}".format(r1)

    if r2 is not None:
        instr_list[11:14] = "{0:03b}".format(r2)

    if r3 is not None:
        instr_list[14:17] = "{0:03b}".format(r3)

    instr_list[0:8] = "{0:08b}".format(opcode)

    return "".join(instr_list)
   
def extract_imm8(imm: str) -> int:
    try:
        imm_num = int(imm, 0)
    except ValueError:
        print("Invalid Imm: " + imm)
        exit(7)

    if imm_num > 0xFF:
        print("imm8 too large: " + imm)
        exit(8)

    return imm_num

def extract_imm16(imm: str) -> int:
    try:
        imm_num = int(imm, 0)
    except ValueError:
        print("Invalid Imm: " + imm)
        exit(7)

    if imm_num > 0xFFFF:
        print("imm16 too large: " + imm)
        exit(8)

    return imm_num

def extract_reg(reg: str) -> int:
    if (reg[0] != 'r'):
        print("Invalid register: " + reg)
        exit(4)

    reg_num_str = reg[1:]
    reg_num = None

    try:
        reg_num = int(reg_num_str)
    except ValueError:
        print("Non-Integer register: " + reg)
        exit(5)
    
    if reg_num > 7 or reg_num < 0:
        print("Invalid register: " + reg)
        exit(6)

    return reg_num

def get_assm(machine_code: str) -> str:
    standardized = machine_code.strip()
    pc = re.search(r"0[xX][a-f0-9A-F]:\s?", standardized)
    if pc is None:
        print("Start all lines with instruction number")
        exit(2)

    standardized = standardized[pc.span()[1]:]
    comments = re.search(r"(#.*)", standardized)
    if comments is not None:
        standardized = standardized[:comments.span()[0]].strip()

    
    instr_parts = list(filter(None, re.split(r' |,', standardized)))
    instr_type = instr_parts[0]

    imm8 = None
    imm16 = None
    r1, r2, r3 = None, None, None
    
    match instr_type:
        case "ldi":
            r3 = extract_reg(instr_parts[1])
            imm8 = extract_imm8(instr_parts[2])
        case "ld":
            r3 = extract_reg(instr_parts[1])
            imm16 = extract_imm16(instr_parts[2])
        case "st":
            imm16 = extract_imm16(instr_parts[1])
            r1 = extract_reg(instr_parts[2])
        case "mov":
            r3 = extract_reg(instr_parts[1])
            r1 = extract_reg(instr_parts[2])
        case "add" | "addc" | "sub" | "subb" | "add" | "or" | "xor":
            r3 = extract_reg(instr_parts[1])
            r1 = extract_reg(instr_parts[2])
            r2 = extract_reg(instr_parts[3])
        case "addi":
            r3 = extract_reg(instr_parts[1])
            r1 = extract_reg(instr_parts[2])
            imm8 = extract_imm8(instr_parts[3])
        case "jmp" | "jz" | "jnz" | "jn" | "jnn" | "call":
            imm16 = extract_imm16(instr_parts[1])
        case "ret":
            pass
        case "push" | "pop":
            r1 = extract_reg(instr_parts[1])
        case "nop":
            pass
        case _:
            print("Invalid instruction " + instr_type)
            exit(3)

    return assm_instr(instr_type_opcode[instr_type], r1, r2, r3, imm8, imm16)

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Not enough arguments")
        exit(1)
    
    verilog_format = False

    if (len(sys.argv) > 2):
        if sys.argv[2] == "verilog":
            verilog_format = True

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if verilog_format:
                print(f"16'd{i}: instr = 30'b" + get_assm(line) + ";")
            else:
                print(get_assm(line))
