class VM:
    def __init__(self):
        self.ip = 0  # instruction pointer
        self.mem = []  # memory, int array

    class Halt(Exception):
        """ halt operating """
        pass

    @staticmethod
    def sanitise_memory(mem):
        return [int(n) for n in mem.split(',')]

    def compute(self, mem):
        self.load_memory(mem)
        if self.mem:
            try:
                while True:
                    self.do_next_instruction()
            except self.Halt:
                return self.getval(0)  # return answer

    def load_memory(self, mem):
        self.ip = 0  # reset ip
        self.mem = self.sanitise_memory(mem) if type(mem) == str else mem  # sanitise string input

    def getval(self, addr):
        return self.mem[addr]

    def setval(self, addr, value):
        self.mem[addr] = value

    def do_next_instruction(self):
        op = self.mem[self.ip]

        if op == 99:  # halt
            raise self.Halt

        elif op == 1:  # add
            n1 = self.getval(self.getval(self.ip + 1))
            n2 = self.getval(self.getval(self.ip + 2))
            dest = self.getval(self.ip + 3)
            value = n1 + n2
            self.setval(dest, value)
            self.ip += 4  # continue

        elif op == 2:  # multiply
            n1 = self.getval(self.getval(self.ip + 1))
            n2 = self.getval(self.getval(self.ip + 2))
            dest = self.getval(self.ip + 3)
            value = n1 * n2
            self.setval(dest, value)
            self.ip += 4

        else:  # unknown
            print("VM ERROR: unknown opcode '{0}'".format(op))
            raise self.Halt
