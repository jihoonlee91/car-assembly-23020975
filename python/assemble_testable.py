from assemble import Assemble


class AssembleTestable(Assemble):
    def __init__(self):
        super().__init__()
        self._inputs: list[str] = []
        self._input_index = 0
        self._out: list[str] = []

    def run(self, inputs) -> str:
        if isinstance(inputs, str):
            inputs = inputs.splitlines() if inputs else []

        self._inputs = list(inputs)
        self._input_index = 0
        self._out = []

        self.execute()

        return "".join(self._out)

    def print_(self, msg: str) -> None:
        self._out.append(msg)

    def println(self, msg: str) -> None:
        self._out.append(msg + "\n")

    def read_line(self) -> str | None:
        if self._input_index >= len(self._inputs):
            return None

        line = self._inputs[self._input_index]
        self._input_index += 1
        return line

    def clear(self) -> None:
        pass

    def delay(self, ms: int) -> None:
        pass
