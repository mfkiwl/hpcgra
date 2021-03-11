# TODO DESCRIPTION AND COMMENTS


class VerilogSimulator:

    def __init__(self, files, cgra_gen: str, bin_gen: str):
        self._files = files
        self._cgra_gen = cgra_gen
        self._bin_gen = bin_gen

    def start(self):
        self.create_cgra()
        self.simul_cgra()

    def create_cgra(self):
        from self._cgra_gen_path. import Cgra

    def simul_cgra(self):
        pass
