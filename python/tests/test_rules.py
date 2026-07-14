from models import BrakeType, CarSpec, CarType, EngineType, SteeringType
from rules import CompatibilityChecker


def make_spec(car_type=CarType.SEDAN, engine=EngineType.GM, brake=BrakeType.MANDO, steering=SteeringType.BOSCH):
    return CarSpec(car_type=car_type, engine=engine, brake=brake, steering=steering)


def test_valid_combination_has_no_violations():
    checker = CompatibilityChecker()

    violations = checker.check(make_spec())

    assert violations == []


def test_sedan_with_continental_brake_is_invalid():
    checker = CompatibilityChecker()

    violations = checker.check(make_spec(car_type=CarType.SEDAN, brake=BrakeType.CONTINENTAL))

    assert "Sedan에는 Continental제동장치 사용 불가" in violations


def test_suv_with_toyota_engine_is_invalid():
    checker = CompatibilityChecker()

    violations = checker.check(make_spec(car_type=CarType.SUV, engine=EngineType.TOYOTA))

    assert "SUV에는 TOYOTA엔진 사용 불가" in violations


def test_truck_with_wia_engine_is_invalid():
    checker = CompatibilityChecker()

    violations = checker.check(make_spec(car_type=CarType.TRUCK, engine=EngineType.WIA))

    assert "Truck에는 WIA엔진 사용 불가" in violations


def test_truck_with_mando_brake_is_invalid():
    checker = CompatibilityChecker()

    violations = checker.check(make_spec(car_type=CarType.TRUCK, brake=BrakeType.MANDO))

    assert "Truck에는 Mando제동장치 사용 불가" in violations


def test_bosch_brake_requires_bosch_steering():
    checker = CompatibilityChecker()

    violations = checker.check(make_spec(brake=BrakeType.BOSCH, steering=SteeringType.MOBIS))

    assert "Bosch제동장치에는 Bosch조향장치 이외 사용 불가" in violations
