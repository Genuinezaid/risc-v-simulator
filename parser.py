import re


class Parser:
    def __init__(self, opcode_unit):
        self.opcode = opcode_unit

    def parse_register(self, reg):
        if not reg:
            return 0
        reg = reg.lower().replace('x', '')
        try:
            return int(reg)
        except:
            return 0

    def parse_instruction(self, line):
        line = line.strip().lower()
        if not line or line.startswith('#'):
            return None

        parts = re.split(r'[\s,()]+', line)
        parts = [p for p in parts if p]

        if not parts:
            return None

        op = parts[0]

        if op not in self.opcode.opcodes:
            return None

        instruction = {
            'op': op,
            'raw': line,
            'type': self.opcode.get_instruction_type(op),
            'rd': 0,
            'rs1': 0,
            'rs2': 0,
            'imm': 0
        }

        try:
            if instruction['type'] == 'R':
                instruction['rd'] = self.parse_register(parts[1])
                instruction['rs1'] = self.parse_register(parts[2])
                instruction['rs2'] = self.parse_register(parts[3])
            elif instruction['type'] == 'I':
                instruction['rd'] = self.parse_register(parts[1])
                if op.startswith('l'):
                    instruction['imm'] = int(parts[2]) if len(parts) > 2 else 0
                    instruction['rs1'] = self.parse_register(parts[3]) if len(parts) > 3 else 0
                else:
                    instruction['rs1'] = self.parse_register(parts[2]) if len(parts) > 2 else 0
                    instruction['imm'] = int(parts[3]) if len(parts) > 3 else 0
            elif instruction['type'] == 'S':
                instruction['rs2'] = self.parse_register(parts[1])
                instruction['imm'] = int(parts[2]) if len(parts) > 2 else 0
                instruction['rs1'] = self.parse_register(parts[3]) if len(parts) > 3 else 0
            elif instruction['type'] == 'B':
                instruction['rs1'] = self.parse_register(parts[1])
                instruction['rs2'] = self.parse_register(parts[2]) if len(parts) > 2 else 0
                instruction['imm'] = int(parts[3]) if len(parts) > 3 else 0
            elif instruction['type'] == 'J':
                instruction['rd'] = self.parse_register(parts[1])
                instruction['imm'] = int(parts[2]) if len(parts) > 2 else 0
            elif instruction['type'] == 'U':
                instruction['rd'] = self.parse_register(parts[1])
                instruction['imm'] = int(parts[2]) if len(parts) > 2 else 0
        except (ValueError, IndexError):
            pass

        return instruction

    def load_program(self, code):
        lines = code.split('\n')
        instructions = []

        for line in lines:
            inst = self.parse_instruction(line)
            if inst:
                instructions.append(inst)

        return instructions