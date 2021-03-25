from src.simul.simul_dot.dataflow.dataflow import DataFlow
from src.simul.simul_dot.dot.dot_interpreter import DotInterpreter


# TODO DESCRIPTION AND COMMENTS
class DotSimulator:

    def __init__(self, files):
        self._di = DotInterpreter(files)
        self._df = DataFlow(self._di)
        self._ticks = 0

    def start(self, type_of_input_generation: int, tam_input_data: int, paths):
        self._df.create_dataflow(type_of_input_generation, tam_input_data,
                                 paths)
        while self._df.get_done() == 0:
            self._df.tick()
            self._ticks += 1
        print("Dot simulation done! The input and output archives were "
              "created.")
        print("The simulation took " + str(self._ticks) + " ticks.")
