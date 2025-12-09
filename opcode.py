class Opcode:
    def __init__(self):
        self.opcodes = {
            'add': 0x33, 'sub': 0x33, 'and': 0x33, 'or': 0x33, 'xor': 0x33,
            'sll': 0x33, 'srl': 0x33, 'sra': 0x33, 'slt': 0x33, 'sltu': 0x33,
            'addi': 0x13, 'andi': 0x13, 'ori': 0x13, 'xori': 0x13,
            'slti': 0x13, 'sltiu': 0x13, 'slli': 0x13, 'srli': 0x13, 'srai': 0x13,
            'lw': 0x03, 'lb': 0x03, 'lh': 0x03, 'lbu': 0x03, 'lhu': 0x03,
            'sw': 0x23, 'sb': 0x23, 'sh': 0x23,
            'beq': 0x63, 'bne': 0x63, 'blt': 0x63, 'bge': 0x63, 'bltu': 0x63, 'bgeu': 0x63,
            'jal': 0x6F, 'jalr': 0x67,
            'lui': 0x37, 'auipc': 0x17
        }

    def get_instruction_type(self, op):
        if op in ['add', 'sub', 'and', 'or', 'xor', 'sll', 'srl', 'sra', 'slt', 'sltu']:
            return 'R'
        if op in ['addi', 'andi', 'ori', 'xori', 'slti', 'sltiu', 'slli', 'srli', 'srai', 'jalr'] or op.startswith('l'):
            return 'I'
        if op in ['sw', 'sb', 'sh']:
            return 'S'
        if op.startswith('b'):
            return 'B'
        if op == 'jal':
            return 'J'
        if op in ['lui', 'auipc']:
            return 'U'
        return 'R'

    def get_opcode(self, op):
        return self.opcodes.get(op, 0)