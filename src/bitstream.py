from cgra import Cgra
from cgra_assembler import CgraAssembler
from utils import to_hex


class Bitstream:
    def __init__(self, cgra_json, assembly):
        self.align_bits = 512
        self.mask_input = 0
        self.mask_output = 0
        self.cgra = Cgra(cgra_json)
        self.assembler = CgraAssembler(self.cgra, assembly)
        src = self.assembler.compile().split('\n')

        sorted(self.cgra.input_ids)
        for i in range(len(self.cgra.input_ids)):
            if self.cgra.input_ids[i] in self.assembler.used_inputs:
                self.mask_input |= 1 << i

        sorted(self.cgra.output_ids)
        for i in range(len(self.cgra.output_ids)):
            if self.cgra.output_ids[i] in self.assembler.used_outputs:
                self.mask_output |= 1 << i

        size = to_hex(len(src), 32)
        mask_input = to_hex(self.mask_input, 64)
        mask_output = to_hex(self.mask_output, 64)

        self.initial_conf = to_hex(int(mask_output + mask_input + size, 16), 512)

        ignore_conf = [to_hex(0, 16) for _ in range(self.align_bits // 16)]
        ignore_loop_conf = [to_hex(0, 16) for _ in range(self.align_bits // 16)]
        for line, i, v in self.assembler.ostream_ignore:
            idx = self.cgra.output_ids.index(i)
            ignore_conf[idx] = to_hex(v, 16)
        for line, i, v in self.assembler.ostream_ignore_loop:
            idx = self.cgra.output_ids.index(i)
            ignore_loop_conf[idx] = to_hex(v, 16)

        self.initial_conf += '\n'
        self.initial_conf += "".join(reversed(ignore_conf))
        self.initial_conf += '\n'
        self.initial_conf += "".join(reversed(ignore_loop_conf))
        conf_size = self.align_bits // self.cgra.conf_bus_width
        src = [to_hex(int(c, 2), self.cgra.conf_bus_width) for c in src]
        count = 0
        conf = []
        for c in src:
            conf.append(c)
            count += 1
            if count == conf_size:
                self.initial_conf += '\n' + to_hex(int("".join(reversed(conf)), 16), 512)
                conf.clear()
                count = 0

        self.initial_conf += '\n' + to_hex(int("".join(reversed(conf)), 16), 512)

    def get(self):
        return self.initial_conf

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.initial_conf)
            f.close()
