class VM:
    # dict of number of params for each opcode. a paramater is something that can have a mode (destination addrs aren't params)
    PARAMLEN = {1: 2,  # (opcode: number of paramaters)
                2: 2,
                3: 1,
                4: 1,
                5: 2,
                6: 2,
                7: 2,
                8: 2,
                99: 0}
    # dict of total ints taken up by each instruction, including the opcode
    INSTRUCTIONLEN = {1: 4,  # (opcode: number of ints for instruction)
                      2: 4,
                      3: 2,
                      4: 2,
                      5: 3,
                      6: 3,
                      7: 4,
                      8: 4,
                      99: 1}

    def __init__(self, debug=False):
        """ intcode interpreter. if debug, dumps memory after every instruction """
        self.ip = 0  # instruction pointer
        self.mem = []  # memory, array of ints
        self.debug = debug  # noisy debug

    class Halt(Exception):
        """ big red stop button """
        pass

    @staticmethod
    def sanitise_memory(mem):
        """ clean dirty input """
        if type(mem) == str:  # expected (from adventofcode.com)
            mem = [int(n) for n in mem.split(',')]
        elif type(mem) == list:  # already good
            pass
        else:  # unkown input form
            print("ERROR: bad input type: '{0}'".format(type(mem)))
        return mem

    def dump_memory(self):
        """ take a peek """
        return "{0} | {1}".format(self.ip, self.mem)

    def compute(self, mem, return_addr=0):
        """ take in a set of instructions and do em, returns item in return addr """
        self.load_memory(mem)
        if self.mem:
            try:
                while True:
                    self.do_next_instruction()
                    if self.debug:
                        print(self.dump_memory())
            except self.Halt:
                return self.get_immediate(return_addr)

    def load_memory(self, mem):
        """ start fresh with new memory """
        self.ip = 0
        self.mem = self.sanitise_memory(mem)

    def get_immediate(self, addr):
        """ immediate mode: return value at mem addr """
        return self.mem[addr]

    def get_position(self, addr):
        """ position mode: return nested value at address, just a double get_immediate() """
        return self.mem[self.mem[addr]]

    def set(self, addr, value):
        self.mem[addr] = value

    def parse_mac(self, mac):
        """ parse first int of an instruction, the MAC (modes and opcode), eg 1002 -> modes 01, opcode 2 """
        mac = str(mac)  # cast int to string so it can be sliced
        op = int(mac[len(mac)-2:len(mac)])  # last two digits, recast to int
        modes = mac[:len(mac)-2][::-1].ljust(self.PARAMLEN.get(op), '0')  # everything before last two digits, reversed, padded with as many missing modes needed to match opcode's parameters
        return op, modes

    def get_paramaters(self, modes):
        """ returns as many paramaters as needed in their correct mode """
        params = []
        for ip_offset, m in enumerate(modes, 1):  # start offset at 1 cause offset of 0 won't change the ip
            if m == '0':  # position mode param
                params.append(self.get_position(self.ip + ip_offset))
            elif m == '1':  # immediate mode param
                params.append(self.get_immediate(self.ip + ip_offset))
            else:
                print("ERROR: invalid mode in '{0}'".format(modes))
                raise self.Halt
        if len(params) == 1:  # give single param not in a list
            return params[0]
        return params

    def do_next_instruction(self):
        """ does whatever is at the ip right now """
        op, modes = self.parse_mac(self.mem[self.ip])

        if op == 99:  # halt
            raise self.Halt

        elif op == 1:  # add
            p1, p2 = self.get_paramaters(modes)
            dest = self.get_immediate(self.ip + 3)  # third param (destination) is always immediate mode
            value = p1 + p2
            self.set(dest, value)
            self.ip += self.INSTRUCTIONLEN[op]

        elif op == 2:  # multiply
            p1, p2 = self.get_paramaters(modes)
            dest = self.get_immediate(self.ip + 3)  # third param (destination) is always immediate mode
            value = p1 * p2
            self.set(dest, value)
            self.ip += self.INSTRUCTIONLEN[op]

        elif op == 3:  # read
            # p1 = self.get_paramaters(modes)
            value = int(input("> "))
            dest = self.get_immediate(self.ip + 1)  # opcode 3's single paramater is always in immediate mode: input goes to memory address in param 1
            self.set(dest, value)
            self.ip += self.INSTRUCTIONLEN[op]

        elif op == 4:  # write
            value = self.get_paramaters(modes)  # only param is also the output
            print("VM says: '{0}'".format(value))
            self.ip += self.INSTRUCTIONLEN[op]

        elif op == 5:  # jump if true
            p1, p2 = self.get_paramaters(modes)
            if p1 != 0:
                self.ip = p2
            else:
                self.ip += self.INSTRUCTIONLEN[op]

        elif op == 6:  # jump if false
            p1, p2 = self.get_paramaters(modes)
            if p1 == 0:
                self.ip = p2
            else:
                self.ip += self.INSTRUCTIONLEN[op]

        elif op == 7:  # less than
            p1, p2 = self.get_paramaters(modes)
            value = 1 if p1 < p2 else 0
            dest = self.get_immediate(self.ip + 3)
            self.set(dest, value)
            self.ip += self.INSTRUCTIONLEN[op]

        elif op == 8:  # equal to
            p1, p2 = self.get_paramaters(modes)
            value = 1 if p1 == p2 else 0
            dest = self.get_immediate(self.ip + 3)
            self.set(dest, value)
            self.ip += self.INSTRUCTIONLEN[op]

        else:  # unknown
            print("ERROR: unknown opcode '{0}'".format(op))
            raise self.Halt

