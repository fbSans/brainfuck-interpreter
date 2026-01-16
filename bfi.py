from collections import deque
import sys


class BF_Interpreter:
    def __init__(self):
        self.ptr: int = 0
        self.mem = deque([0 for i in range(255)])

    def _points_zero(self) -> bool:
        return self.mem[self.ptr] == 0

    def _inc(self):
        self.mem[self.ptr] = (self.mem[self.ptr] + 1) % 256   #byte arithmetic


    def _dec(self):
        self.mem[self.ptr] = (self.mem[self.ptr] - 1) % 256   #byte arithmetic

    def _move_right(self):
        if self.ptr+1 == len(self.mem):
            self.mem.append(0)       #in case we are in the very left
        self.ptr += 1

    def _move_left(self):
        if self.ptr == 0:
            self.mem.appendleft(0)   #points to the leftmost element, but index now still points to zero in deque
        else:
            self.ptr -= 1            #move pointer to the left

    def _read(self):
        print(chr(self.mem[self.ptr]), end='')

    def _write(self, v: int):
        self.mem[self.ptr] = v

    def __str__(self):
        return f"{self.ptr} {self.mem}"

    def interpret_program(self, extended_instructions: list[tuple[str, int] | str]):
        ip = 0
        while ip < len(extended_instructions):
            inst = extended_instructions[ip]
            match(inst):
                case '.':
                    self._read()
                    ip += 1
                case ',':
                    self._write(int(input("write to cell: ")))
                    ip += 1
                case '+':
                    self._inc()
                    ip += 1
                case '-':
                    self._dec()
                    ip += 1
                case '>':
                    self._move_right()
                    ip += 1
                case '<':
                    self._move_left()
                    ip += 1
                case (']', jump_addr):
                    if not self._points_zero():
                        ip = jump_addr
                    else:
                        ip += 1
                case ('[', jump_addr):
                    if self._points_zero():
                        ip = jump_addr
                    else:
                        ip += 1
                case _:
                    print('Unreachable', inst)
                    exit(1)


def load_intructions_from_file(filepath: str) -> list[(str, int)]:
    #collect instructions
    with open(filepath, 'r') as f:
        temp_str: str = ""
        for line in f.readlines():
            temp_str += line
        insts = [c for c in  temp_str if c in '+-.,><[]']
    return insts


def extend_instructions(instructions: list[str]) -> list[tuple[str, int] | str]:
    '''Extend instructions to add jump addresses to [ and ]'''
    matching_stack: list[int] = []
    extended_instructions : list[tuple[str, int] | str] = []
    for ip in range(len(instructions)):
        if instructions[ip] == '[':
            matching_stack.append(ip)
            extended_instructions.append("") # push a placeholder for the jump instrunctions
        elif instructions[ip] == ']':
            if len(matching_stack) < 1:
                print(f"Error: The {ip} instruction ] is unbalaced")
                exit(1)
            index = matching_stack.pop()
            extended_instructions[index] = ("[", ip + 1)          # [ jump address points to the next instruction after ]
            extended_instructions.append(("]", index + 1))        # ] jump address points to the next instruction after [
        else:
            extended_instructions.append(instructions[ip])
    if len(matching_stack) > 0:
        print(f"Error:The {ip} instruction [ is unbalaced")
        exit(1)
    return extended_instructions


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python brainfuck.py <inputfile>")
        exit(1)

    input_path: str = sys.argv[1]
    bf_instructions = load_intructions_from_file(input_path)
    extended_instructions = extend_instructions(bf_instructions)
    iterpreter = BF_Interpreter()
    iterpreter.interpret_program(extended_instructions)

