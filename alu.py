class ALU:
    @staticmethod
    def execute(opcode, inst_type, op1, op2, imm, pc):

        result = 0

        if opcode in ['add', 'addi']:
            result = op1 + (imm if inst_type == 'I' else op2)
        elif opcode == 'sub':
            result = op1 - op2
        elif opcode in ['and', 'andi']:
            result = op1 & (imm if inst_type == 'I' else op2)
        elif opcode in ['or', 'ori']:
            result = op1 | (imm if inst_type == 'I' else op2)
        elif opcode in ['xor', 'xori']:
            result = op1 ^ (imm if inst_type == 'I' else op2)
        elif opcode in ['sll', 'slli']:
            result = op1 << (imm if inst_type == 'I' else (op2 & 0x1F))
        elif opcode in ['srl', 'srli']:
            result = (op1 & 0xFFFFFFFF) >> (imm if inst_type == 'I' else (op2 & 0x1F))
        elif opcode in ['sra', 'srai']:
            result = op1 >> (imm if inst_type == 'I' else (op2 & 0x1F))
        elif opcode in ['slt', 'slti']:
            result = 1 if op1 < (imm if inst_type == 'I' else op2) else 0
        elif opcode in ['lw', 'lb', 'lh', 'sw', 'sb', 'sh']:
            result = op1 + imm
        elif opcode == 'beq':
            result = 1 if op1 == op2 else 0
        elif opcode == 'bne':
            result = 1 if op1 != op2 else 0
        elif opcode == 'blt':
            result = 1 if op1 < op2 else 0
        elif opcode == 'bge':
            result = 1 if op1 >= op2 else 0
        elif opcode in ['jal', 'jalr']:
            result = pc + 4
        elif opcode == 'lui':
            result = imm << 12
        elif opcode == 'auipc':
            result = pc + (imm << 12)

        # Handle 32-bit signed arithmetic
        result = result & 0xFFFFFFFF
        if result & 0x80000000:
            result = result - 0x100000000

        return result