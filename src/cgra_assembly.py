from cgra_configuration import CgraConfiguration
import re


class CgraAssembly:
    def __init__(self, cgra, asm_file, outputfile):
        self.cgra = cgra
        self.cc = CgraConfiguration(cgra)
        self.asm_file = asm_file
        self.outputfile = outputfile
        self.alu_inst = {}
        self.routes_inst = {}
        self.const = []
        self.last_error = ''

    def parse(self):
        f = open(self.asm_file)
        lines = f.read().split('\n')
        f.close()
        i = 1
        self.last_error = ''
        for line in lines:
            if line and line[0] != '#':
                line = re.sub(' +', ' ', line)
                tokens = line.split(' ')
                if tokens[0] == 'route':
                    r, v = self.decode_route_inst(tokens)
                    if r:
                        self.routes_inst[i] = v
                    else:
                        self.last_error = 'line %d: %s' % (i, v)
                        return
                else:
                    r, v = self.decode_alu_inst(i, tokens)
                    if r:
                        self.alu_inst[i] = v
                    else:
                        self.last_error = 'line %d: %s' % (i, v)
                        return
            i += 1

    def decode_alu_inst(self, line, inst):
        try:
            op = inst[0]
            pe = int(inst[1][1:])
            alu_src = []
            delays = []
            tok = inst[2:]
            for j in range(len(tok)):
                i = tok[j]
                if '#' in i:
                    delays.append((j, int(i[1:])))
                else:
                    if 'alu' in i or 'istream' in i or 'acc' in i:
                        alu_src.append(i[1:])
                    elif '$' in i:
                        alu_src.append(int(i[1:]))
                    else:
                        alu_src.append('const')
                        self.const.append((line, pe, int(i)))

            for i in range(len(delays)):
                idx, v = delays[i]
                delays[i] = (alu_src.index(alu_src[idx]), v)

        except Exception as e:
            return False, str(e)

        return True, [pe, op, alu_src, delays]

    def decode_route_inst(self, inst):
        try:
            pe = int(inst[1][1:])
            if 'alu' in inst[2][1:]:
                src = 'alu'
            else:
                src = int(inst[2][1:])
            if 'ostream' in inst[3][1:]:
                dst = 'ostream'
            else:
                dst = int(inst[3][1:])
        except Exception as e:
            return False, str(e)

        return True, [pe, {src: dst}]

    def compile(self):
        self.parse()
        bitstream = ''
        if self.last_error == '':
            for line, conf in self.alu_inst.items():
                r, v = self.cc.create_alu_conf(conf[0], conf[1], conf[2], conf[3])
                if r:
                    for c in v:
                        bitstream += c + '\n'
                else:
                    self.last_error = 'line %d: %s' % (line, v)
                    break

                if 'acc' in conf[2]:
                    r, v = self.cc.create_reset_conf(conf[0])
                    if r:
                        for c in v:
                            bitstream += c + '\n'
                    else:
                        self.last_error = 'line %d: %s' % (line, v)
                        break

        if self.last_error == '':
            for line, id, const in self.const:
                r, v = self.cc.create_const_conf(id, const)
                if r:
                    for c in v:
                        bitstream += c + '\n'
                else:
                    self.last_error = 'line %d: %s' % (line, v)
                    break

        if self.last_error == '':
            routing = {}
            for line, c in self.routes_inst.items():
                if c[0] in routing.keys():
                    routing[c[0]].update(c[1])
                else:
                    routing[c[0]] = c[1]

            for line, c in self.routes_inst.items():
                r, v = self.cc.create_router_conf(c[0], routing[c[0]])
                if r:
                    for c in v:
                        bitstream += c + '\n'
                else:
                    self.last_error = 'line %d: %s' % (line, v)
                    break

        if self.last_error:
            print('Compile error on %s' % self.last_error)
            return False

        f = open(self.outputfile, 'w')
        f.write(bitstream[:-1])
        f.close()

        print('Build succeeded, output file save in %s' % self.outputfile)

        return True
