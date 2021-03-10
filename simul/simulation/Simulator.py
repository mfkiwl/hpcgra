from dot.DotInterpreter import DotInterpreter
from dataflow.DataFlow import DataFlow


class Simulator:
    di = ""
    df = ""

    def __init__(self, dot_file_path: str):
        self.di = DotInterpreter(dot_file_path)
        self.df = DataFlow(self.di)

    def start(self, type_of_input_generation: int, tam_input_data: int,
              output_files_path: str):
        self.df.create_dataflow(type_of_input_generation, tam_input_data,
                                output_files_path)
        while self.df.get_done() == 0:
            self.df.do_clock()
        print("Simulation done! Archives created.")
