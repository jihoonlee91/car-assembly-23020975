from assemble_testable import AssembleTestable


def test_정상_조합이면_PASS():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "1",  # GM
        "1",  # MANDO
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "PASS" in output


def test_Sedan에_Continental이면_FAIL():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "1",  # GM
        "2",  # CONTINENTAL
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "FAIL" in output
    assert "Sedan에는 Continental제동장치 사용 불가" in output


def test_SUV에_Toyota면_FAIL():
    app = AssembleTestable()

    inputs = [
        "2",  # SUV
        "2",  # TOYOTA
        "1",  # MANDO
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "FAIL" in output
    assert "SUV에는 TOYOTA엔진 사용 불가" in output


def test_Truck에_WIA면_FAIL():
    app = AssembleTestable()

    inputs = [
        "3",  # Truck
        "3",  # WIA
        "2",  # CONTINENTAL (Mando는 별도로 Truck에서 막혀 있으므로 다른 브레이크 사용)
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "FAIL" in output
    assert "Truck에는 WIA엔진 사용 불가" in output


def test_Truck에_Mando면_FAIL():
    app = AssembleTestable()

    inputs = [
        "3",  # Truck
        "1",  # GM
        "1",  # MANDO
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "FAIL" in output
    assert "Truck에는 Mando제동장치 사용 불가" in output


def test_Bosch제동장치에_Mobis조향장치면_FAIL():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "1",  # GM
        "3",  # BOSCH
        "2",  # MOBIS
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "FAIL" in output
    assert "Bosch제동장치에는 Bosch조향장치 이외 사용 불가" in output


def test_고장난_엔진이면_RUN_실패():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "4",  # 고장난 엔진
        "1",  # MANDO
        "1",  # BOSCH
        "1",  # RUN
    ]

    output = app.run(inputs)

    assert "엔진이 고장나있습니다." in output
    assert "자동차가 움직이지 않습니다." in output


def test_정상_조합이면_RUN_성공():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "1",  # GM
        "1",  # MANDO
        "1",  # BOSCH
        "1",  # RUN
    ]

    output = app.run(inputs)

    assert "자동차가 동작됩니다." in output


def test_범위를_벗어난_입력이면_에러_메시지():
    app = AssembleTestable()

    inputs = [
        "9",  # 잘못된 차량 타입
        "1",  # Sedan
        "1",  # GM
        "1",  # MANDO
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능" in output
    assert "PASS" in output


def test_각_스텝별_범위_에러_메시지_조사_정확성():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "1",  # GM
        "9",  # 잘못된 제동장치
        "1",  # MANDO
        "9",  # 잘못된 조향장치
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능" in output
    assert "ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능" in output
    assert "PASS" in output


def test_숫자가_아닌_입력이면_에러_메시지():
    app = AssembleTestable()

    inputs = [
        "abc",
        "1",  # Sedan
        "1",  # GM
        "1",  # MANDO
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "ERROR :: 숫자만 입력 가능" in output
    assert "PASS" in output


def test_뒤로가기로_이전_단계_재선택():
    app = AssembleTestable()

    inputs = [
        "1",  # Sedan
        "2",  # TOYOTA (실수로 선택)
        "0",  # 뒤로가기 -> 엔진 재선택
        "1",  # GM
        "1",  # MANDO
        "1",  # BOSCH
        "2",  # Test
    ]

    output = app.run(inputs)

    assert "PASS" in output


def test_exit_입력시_종료():
    app = AssembleTestable()

    output = app.run(["exit"])

    assert "바이바이" in output
