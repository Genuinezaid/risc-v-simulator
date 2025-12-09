class Memory:
    def __init__(self, size=256):
        self.memory = [0] * size

    def access_memory(self, opcode, address, value=None):

        addr_word = address // 4

        if opcode in ['lw', 'lb', 'lh']:
            if 0 <= addr_word < len(self.memory):
                return self.memory[addr_word]

        elif opcode in ['sw', 'sb', 'sh']:
            if 0 <= addr_word < len(self.memory):
                self.memory[addr_word] = value
                return value

        return address

    def reset(self):
        self.memory = [0] * len(self.memory)