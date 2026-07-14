from dataclasses import dataclass
from typing import Callable

from models import BrakeType, CarSpec, CarType, EngineType, SteeringType


@dataclass(frozen=True)
class CompatibilityRule:
    predicate: Callable[[CarSpec], bool]
    message: str


RULES = [
    CompatibilityRule(
        lambda spec: spec.car_type is CarType.SEDAN and spec.brake is BrakeType.CONTINENTAL,
        "Sedan에는 Continental제동장치 사용 불가",
    ),
    CompatibilityRule(
        lambda spec: spec.car_type is CarType.SUV and spec.engine is EngineType.TOYOTA,
        "SUV에는 TOYOTA엔진 사용 불가",
    ),
    CompatibilityRule(
        lambda spec: spec.car_type is CarType.TRUCK and spec.engine is EngineType.WIA,
        "Truck에는 WIA엔진 사용 불가",
    ),
    CompatibilityRule(
        lambda spec: spec.car_type is CarType.TRUCK and spec.brake is BrakeType.MANDO,
        "Truck에는 Mando제동장치 사용 불가",
    ),
    CompatibilityRule(
        lambda spec: spec.brake is BrakeType.BOSCH and spec.steering is not SteeringType.BOSCH,
        "Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
    ),
]


class CompatibilityChecker:
    def __init__(self, rules=RULES):
        self._rules = rules

    def check(self, spec: CarSpec) -> list[str]:
        return [rule.message for rule in self._rules if rule.predicate(spec)]
