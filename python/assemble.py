from abc import ABC, abstractmethod
from enum import IntEnum

from models import BrakeType, CarSpec, CarType, EngineType, SteeringType
from rules import CompatibilityChecker

CLEAR_SCREEN = "\033[H\033[2J"

CAR_TYPE_BANNER = (
    "        ______________\n"
    "       /|            |\n"
    "  ____/_|_____________|____\n"
    " |                      O  |\n"
    " '-(@)----------------(@)--'"
)

SEPARATOR = "==============================="


class Step(IntEnum):
    CAR_TYPE = 0
    ENGINE = 1
    BRAKE = 2
    STEERING = 3
    RUN_TEST = 4


STEP_PART_ENUM = {
    Step.CAR_TYPE: CarType,
    Step.ENGINE: EngineType,
    Step.BRAKE: BrakeType,
    Step.STEERING: SteeringType,
}

STEP_HEADER = {
    Step.CAR_TYPE: "어떤 차량 타입을 선택할까요?",
    Step.ENGINE: "어떤 엔진을 탑재할까요?",
    Step.BRAKE: "어떤 제동장치를 선택할까요?",
    Step.STEERING: "어떤 조향장치를 선택할까요?",
}

STEP_ERROR_PREFIX = {
    Step.CAR_TYPE: "차량 타입은",
    Step.ENGINE: "엔진은",
    Step.BRAKE: "제동장치는",
    Step.STEERING: "조향장치는",
}

STEP_MIN_ANSWER = {
    Step.CAR_TYPE: 1,
    Step.ENGINE: 0,
    Step.BRAKE: 0,
    Step.STEERING: 0,
    Step.RUN_TEST: 0,
}

SELECTION_MESSAGE = {
    Step.CAR_TYPE: "차량 타입으로 {label}을 선택하셨습니다.",
    Step.ENGINE: "{label} 엔진을 선택하셨습니다.",
    Step.BRAKE: "{label} 제동장치를 선택하셨습니다.",
    Step.STEERING: "{label} 조향장치를 선택하셨습니다.",
}


class Assemble(ABC):
    def __init__(self):
        self._checker = CompatibilityChecker()
        self._step = Step.CAR_TYPE
        self._selections = {}

    def execute(self):
        self._step = Step.CAR_TYPE
        self._selections = {}

        while True:
            self.clear()
            self._show_menu()
            self.print_("INPUT > ")
            buf = self.read_line()

            if buf is None:
                break

            buf = buf.strip()

            if buf == "exit":
                self.println("바이바이")
                break

            try:
                answer = int(buf)
            except ValueError:
                self.println("ERROR :: 숫자만 입력 가능")
                self.delay(800)
                continue

            if not self._is_valid_range(answer):
                self.delay(800)
                continue

            if answer == 0:
                if self._step == Step.RUN_TEST:
                    self._step = Step.CAR_TYPE
                elif self._step > Step.CAR_TYPE:
                    self._step = Step(self._step - 1)
                continue

            self._handle_answer(answer)

    def _show_menu(self):
        if self._step == Step.RUN_TEST:
            self.println("멋진 차량이 완성되었습니다.")
            self.println("0. 처음 화면으로 돌아가기")
            self.println("1. RUN")
            self.println("2. Test")
            self.println(SEPARATOR)
            return

        if self._step == Step.CAR_TYPE:
            self.println(CAR_TYPE_BANNER)
            self.println(SEPARATOR)

        self.println(STEP_HEADER[self._step])

        if self._step != Step.CAR_TYPE:
            self.println("0. 뒤로가기")

        part_enum = STEP_PART_ENUM[self._step]
        for part in part_enum:
            self.println(f"{part.code}. {part.label}")

        self.println(SEPARATOR)

    def _is_valid_range(self, answer):
        if self._step == Step.RUN_TEST:
            if 0 <= answer <= 2:
                return True
            self.println("ERROR :: Run 또는 Test 중 하나를 선택 필요")
            return False

        part_enum = STEP_PART_ENUM[self._step]
        min_answer = STEP_MIN_ANSWER[self._step]
        max_answer = len(part_enum)

        if min_answer <= answer <= max_answer:
            return True

        self.println(f"ERROR :: {STEP_ERROR_PREFIX[self._step]} 1 ~ {max_answer} 범위만 선택 가능")
        return False

    def _handle_answer(self, answer):
        if self._step == Step.RUN_TEST:
            if answer == 1:
                self._run()
                self.delay(2000)
            elif answer == 2:
                self.println("Test...")
                self.delay(1500)
                self._test()
                self.delay(2000)
            return

        part_enum = STEP_PART_ENUM[self._step]
        part = part_enum.from_code(answer)
        self._selections[self._step] = part

        self.println(SELECTION_MESSAGE[self._step].format(label=part.label))
        self.delay(800)
        self._step = Step(self._step + 1)

    def _current_spec(self) -> CarSpec:
        return CarSpec(
            car_type=self._selections[Step.CAR_TYPE],
            engine=self._selections[Step.ENGINE],
            brake=self._selections[Step.BRAKE],
            steering=self._selections[Step.STEERING],
        )

    def _run(self):
        spec = self._current_spec()

        if self._checker.check(spec):
            self.println("자동차가 동작되지 않습니다")
            return

        if spec.engine is EngineType.BROKEN:
            self.println("엔진이 고장나있습니다.")
            self.println("자동차가 움직이지 않습니다.")
            return

        self.println(f"Car Type : {spec.car_type.label}")
        self.println(f"Engine   : {spec.engine.label}")
        self.println(f"Brake    : {spec.brake.label}")
        self.println(f"Steering : {spec.steering.label}")
        self.println("자동차가 동작됩니다.")

    def _test(self):
        violations = self._checker.check(self._current_spec())

        if violations:
            self.println(f"FAIL\n{violations[0]}")
        else:
            self.println("PASS")

    @abstractmethod
    def print_(self, msg: str) -> None: ...

    @abstractmethod
    def println(self, msg: str) -> None: ...

    @abstractmethod
    def read_line(self) -> str | None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def delay(self, ms: int) -> None: ...
