import sys
import time

from assemble import CLEAR_SCREEN, Assemble


class AssembleConsole(Assemble):
    def run(self) -> None:
        self.execute()

    def print_(self, msg: str) -> None:
        print(msg, end="", flush=True)

    def println(self, msg: str) -> None:
        print(msg)

    def read_line(self) -> str | None:
        try:
            return input()
        except EOFError:
            return None

    def clear(self) -> None:
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()

    def delay(self, ms: int) -> None:
        time.sleep(ms / 1000.0)
