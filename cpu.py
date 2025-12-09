class CPU:
    def __init__(self):
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0
        self.instructions_executed = 0

        self.pipeline = {
            'IF': {'instruction': None, 'pc': 0},
            'ID': {'instruction': None, 'pc': 0, 'opcode': None, 'rs1': 0, 'rs2': 0, 'rd': 0,
                   'imm': 0, 'rs1Val': 0, 'rs2Val': 0},
            'EX': {'instruction': None, 'pc': 0, 'rd': 0, 'aluResult': 0, 'rs2Val': 0},
            'MEM': {'instruction': None, 'pc': 0, 'rd': 0, 'data': 0},
            'WB': {'instruction': None, 'pc': 0, 'rd': 0, 'data': 0}
        }

        self.execution_log = []
        self.is_running = False

    def parse_register(self, reg):
        if not reg:
            return 0
        reg = reg.lower().replace('x', '')
        try:
            return int(reg)
        except:
            return 0

    def flush_pipeline(self):
        self.pipeline['IF'] = {'instruction': None, 'pc': 0}
        self.pipeline['ID'] = {'instruction': None}

    def fetch(self, instructions):
        if self.pc >= len(instructions) * 4:
            self.pipeline['IF']['instruction'] = None
            return

        inst_index = self.pc // 4
        if inst_index < len(instructions):
            self.pipeline['IF']['instruction'] = instructions[inst_index]
            self.pipeline['IF']['pc'] = self.pc

    def decode(self, instructions, hazard_detector):
        if not self.pipeline['IF']['instruction']:
            self.pipeline['ID'] = {'instruction': None}
            return

        inst = self.pipeline['IF']['instruction']
        self.pipeline['ID'] = {
            'instruction': inst,
            'pc': self.pipeline['IF']['pc'],
            'opcode': inst['op'],
            'rs1': inst.get('rs1', 0),
            'rs2': inst.get('rs2', 0),
            'rd': inst.get('rd', 0),
            'imm': inst.get('imm', 0),
            'rs1Val': self.registers[inst.get('rs1', 0)],
            'rs2Val': self.registers[inst.get('rs2', 0)]
        }

        # Check for hazards
        if hazard_detector:
            hazard = hazard_detector.detect_hazards(self.pipeline)
            if hazard:
                self.log_message(f"Hazard detected: {hazard}", 'hazard')
                hazard_detector.hazards_detected += 1

    def execute(self, alu, hazard_detector):
        if not self.pipeline['ID'].get('instruction'):
            self.pipeline['EX'] = {'instruction': None}
            return

        inst = self.pipeline['ID']

        # Get operand values with forwarding if needed
        op1, op2 = hazard_detector.get_operands_with_forwarding(
            inst, self.pipeline['EX'], self.pipeline['MEM'], self.registers
        )

        # Execute ALU operation
        result = alu.execute(
            inst['opcode'],
            inst['instruction']['type'],
            op1,
            op2,
            inst['imm'],
            inst['pc']
        )

        self.pipeline['EX'] = {
            'instruction': inst['instruction'],
            'pc': inst['pc'],
            'rd': inst['rd'],
            'aluResult': result,
            'rs2Val': op2
        }

    def memory_access(self, memory_unit):
        if not self.pipeline['EX'].get('instruction'):
            self.pipeline['MEM'] = {'instruction': None}
            return

        inst = self.pipeline['EX']
        data = inst['aluResult']
        op = inst['instruction']['op']

        # Perform memory operation if needed
        if op in ['lw', 'lb', 'lh'] or op in ['sw', 'sb', 'sh']:
            data = memory_unit.access_memory(
                op, inst['aluResult'], inst['rs2Val']
            )

        self.pipeline['MEM'] = {
            'instruction': inst['instruction'],
            'pc': inst['pc'],
            'rd': inst['rd'],
            'data': data
        }

    def write_back(self, instructions, hazard_detector):
        if not self.pipeline['MEM'].get('instruction'):
            self.pipeline['WB'] = {'instruction': None}
            return

        inst = self.pipeline['MEM']
        op = inst['instruction']['op']

        # Write back to register if needed
        if inst['rd'] != 0 and not op.startswith('s') and not op.startswith('b'):
            self.registers[inst['rd']] = inst['data']

        # Handle branches and jumps
        if op.startswith('b') and inst['data'] == 1:
            branch_target = inst['pc'] + inst['instruction']['imm']
            self.pc = branch_target
            self.log_message(f"Branch taken to PC: {branch_target}", 'forward')
            self.flush_pipeline()
        elif op == 'jal':
            self.pc = inst['pc'] + inst['instruction']['imm']
            self.log_message(f"Jump to PC: {self.pc}", 'forward')
            self.flush_pipeline()
        elif op == 'jalr':
            self.pc = (self.registers[inst['instruction']['rs1']] +
                       inst['instruction']['imm']) & ~1
            self.log_message(f"Jump register to PC: {self.pc}", 'forward')
            self.flush_pipeline()
        elif not op.startswith('b'):
            self.pc += 4
        else:
            self.pc += 4

        self.pipeline['WB'] = inst
        self.instructions_executed += 1
        self.registers[0] = 0  # x0 is always 0

    def step(self, components):
        """Execute one pipeline step"""
        if (self.pc >= len(components['instructions']) * 4 and
                not any(self.pipeline[stage].get('instruction')
                        for stage in ['IF', 'ID', 'EX', 'MEM', 'WB'])):
            self.log_message('Program execution completed')
            return False

        # Pipeline stages in reverse order (WB to IF)
        self.write_back(components['instructions'], components['hazard_detector'])
        self.memory_access(components['memory'])
        self.execute(components['alu'], components['hazard_detector'])
        self.decode(components['instructions'], components['hazard_detector'])
        self.fetch(components['instructions'])

        self.cycle += 1
        self.log_message(f"Cycle {self.cycle} completed", 'cycle')
        return True

    def reset(self):
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0
        self.instructions_executed = 0
        self.execution_log = []

        self.pipeline = {
            'IF': {'instruction': None, 'pc': 0},
            'ID': {'instruction': None},
            'EX': {'instruction': None},
            'MEM': {'instruction': None},
            'WB': {'instruction': None}
        }

        self.log_message('CPU reset')

    def log_message(self, message, msg_type='info'):
        self.execution_log.append({
            'cycle': self.cycle,
            'message': message,
            'type': msg_type
        })

    def get_cpi(self):
        if self.instructions_executed > 0:
            return self.cycle / self.instructions_executed
        return 0.0