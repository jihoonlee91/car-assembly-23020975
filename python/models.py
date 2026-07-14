from dataclasses import dataclass
from enum import Enum


class _LabeledEnum(Enum):
    def __new__(cls, code, label):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.label = label
        return obj

    @classmethod
    def from_code(cls, code):
        return cls(code)


class CarType(_LabeledEnum):
    SEDAN = (1, "Sedan")
    SUV = (2, "SUV")
    TRUCK = (3, "Truck")


class EngineType(_LabeledEnum):
    GM = (1, "GM")
    TOYOTA = (2, "TOYOTA")
    WIA = (3, "WIA")
    BROKEN = (4, "고장난 엔진")


class BrakeType(_LabeledEnum):
    MANDO = (1, "Mando")
    CONTINENTAL = (2, "Continental")
    BOSCH = (3, "Bosch")


class SteeringType(_LabeledEnum):
    BOSCH = (1, "Bosch")
    MOBIS = (2, "Mobis")


@dataclass(frozen=True)
class CarSpec:
    car_type: CarType
    engine: EngineType
    brake: BrakeType
    steering: SteeringType
