from cpu import CPU
from memory import Memory
from alu import ALU
from hazard_detector import HazardDetector
from opcode import Opcode
from parser import Parser


class RISCVSimulator:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.alu = ALU()
        self.hazard_detector = HazardDetector()
        self.opcode = Opcode()
        self.parser = Parser(self.opcode)

        self.instructions = []
        self.components = {}

    def load_program(self, code):
        self.instructions = self.parser.load_program(code)
        self.components = {
            'instructions': self.instructions,
            'memory': self.memory,
            'alu': self.alu,
            'hazard_detector': self.hazard_detector
        }
        return len(self.instructions)

    def step(self):
        return self.cpu.step(self.components)

    def reset(self):
        self.cpu.reset()
        self.memory.reset()
        self.hazard_detector.hazards_detected = 0
        self.instructions = []

    @property
    def registers(self):
        return self.cpu.registers

    @property
    def memory_values(self):
        return self.memory.memory

    @property
    def pipeline(self):
        return self.cpu.pipeline

    @property
    def cycle(self):
        return self.cpu.cycle

    @property
    def instructions_executed(self):
        return self.cpu.instructions_executed

    @property
    def hazards_detected(self):
        return self.hazard_detector.hazards_detected

    @property
    def execution_log(self):
        return self.cpu.execution_log

    def get_cpi(self):
        return self.cpu.get_cpi()