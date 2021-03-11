from dot.DotInterpreter import DotInterpreter
from dataflow.DataFlow import DataFlow


# TODO DESCRIPTION AND COMMENTS
class Simulator:

    def __init__(self, dot_file_path: str):
        self._di = DotInterpreter(dot_file_path)
        self._df = DataFlow(self._di)

    def start(self, type_of_input_generation: int, tam_input_data: int,
              generated_files_path: str):
        self._df.create_dataflow(type_of_input_generation, tam_input_data,
                                 generated_files_path)
        ticks = 0
        while self._df.get_done() == 0:
            self._df.tick()
            ticks += 1
        print("Simulation done! The archives were created.")
        print("The simulation took " + str(ticks) + " ticks.")
