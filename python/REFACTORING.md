# Python 리팩토링 계획

## 배경 (Context)

`python/assemble.py`는 절차지향 스타일의 단일 파일로, 다음 문제를 안고 있었다.

- 전역변수(`q0`~`q4`)로 상태를 관리
- 차량 타입/엔진/제동장치/조향장치가 모두 매직넘버(1, 2, 3 ...)와 if/elif 나열로 하드코딩
- `except:` bare except 사용 (안전하지 않은 문법)
- 호환성 규칙(`is_valid_check`)과 화면 출력(`print`)이 뒤섞여 있어 유닛테스트 불가능
- 차량 타입/부품이 추가될 때마다 여러 함수(`show_menu`, `select_*`, `is_valid_check`, `run_produced_car`, `test_produced_car`)를 전부 고쳐야 함 → 확장성 없음

레거시 문서에 명시된 개선 목표(유지보수성, 안전한 문법, 확장성, 유닛테스트)를 모두 반영해 단계적으로 리팩토링한다. 원본 저장소의 `java/v2` 참고 구현(전역변수 제거 + I/O 추상화로 테스트 가능하게 만든 패턴)을 기반으로 하되, 호환성 규칙까지 데이터 기반으로 분리해 확장성 문제까지 해결한다.

## 최종 구조

```
python/
  models.py            # CarType, EngineType, BrakeType, SteeringType enum + CarSpec
  rules.py              # CompatibilityRule, RULES, CompatibilityChecker
  assemble.py           # Assemble 추상 클래스 (메뉴/스텝 진행 로직, I/O는 추상 메서드)
  assemble_console.py   # AssembleConsole(Assemble) - 실제 콘솔 입출력
  assemble_testable.py  # AssembleTestable(Assemble) - 입력 배열 주입, 출력 문자열 캡처 (테스트용)
  main.py               # 진입점: AssembleConsole().run()
  tests/
    test_rules.py        # 호환성 규칙 단위테스트 (순수 로직)
    test_assemble.py      # 전체 플로우 시나리오 테스트 (AssembleTestable 사용)
```

기존 `python/assemble.py`(절차형 단일 파일)는 위 구조로 대체된다.

## 핵심 설계

### enum 기반 부품 정의 (`models.py`)

각 부품(`CarType`, `EngineType`, `BrakeType`, `SteeringType`)을 `(코드, 표시이름)` 튜플 값을 갖는 `Enum`으로 정의한다.

```python
class CarType(Enum):
    SEDAN = (1, "Sedan")
    SUV = (2, "SUV")
    TRUCK = (3, "Truck")

    def __new__(cls, code, label):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.label = label
        return obj
```

메뉴 출력, 선택 확인 메시지, RUN 결과 출력이 모두 `enum.label`을 순회/조회해서 생성되므로, **새 타입을 추가할 때는 enum에 멤버 한 줄만 추가**하면 메뉴/출력 로직은 수정할 필요가 없다.

`CarSpec`은 4개 선택값(`car_type`, `engine`, `brake`, `steering`)을 담는 `dataclass`.

### 데이터 기반 호환성 규칙 (`rules.py`)

기존 `is_valid_check`/`test_produced_car`에 중복돼 있던 5개 규칙(if-elif 나열)을 `CompatibilityRule(predicate, message)` 객체 리스트 `RULES`로 분리한다.

- Sedan + Continental 불가
- SUV + Toyota 엔진 불가
- Truck + WIA 엔진 불가
- Truck + Mando 제동장치 불가
- Bosch 제동장치 + non-Bosch 조향장치 불가

`CompatibilityChecker.check(spec) -> list[str]`가 위반 메시지 목록을 반환한다. **새 제약조건이 생기면 `RULES`에 항목을 추가**하기만 하면 되고, RUN/TEST 로직은 그대로 재사용된다 (조건 분기 수정 불필요).

### I/O 분리 (테스트 가능성)

원본 저장소 `java/v2/Assemble.java` 패턴과 동일하게, 메뉴/스텝 진행 로직을 `Assemble` 추상 클래스에 두고 `print_`, `println`, `read_line`, `clear`, `delay`를 추상 메서드로 분리한다.

- `AssembleConsole`: 실제 `print`/`input`/`time.sleep` 사용
- `AssembleTestable`: 입력 문자열 리스트를 순서대로 반환하고, 출력은 버퍼에 누적해 문자열로 반환 (pytest에서 시나리오 재현용)

상태(`step`, 각 스텝별 선택값)는 전역변수 대신 인스턴스 속성으로 보관하고, `bare except`는 `except ValueError`로 교체한다.

## 단계별 진행 (각 단계 = 커밋 1개)

- [x] **0. 계획 문서 작성** (본 문서) — 실제 구현 전 계획을 먼저 문서화하고 커밋
- [x] **1. 모델/규칙 계층 작성** — `models.py`, `rules.py` 추가. 아직 기존 `assemble.py`는 건드리지 않음. `tests/test_rules.py`로 5개 규칙 + PASS 케이스를 pytest로 검증 (순수 로직이라 UI 없이 먼저 테스트 가능)
- [x] **2. Assemble 클래스 리팩토링** — `assemble.py`를 절차형 함수 → `Assemble` 추상 클래스로 재작성. 전역변수 제거, enum/규칙 계층 사용, bare except 제거. `assemble_console.py`, `assemble_testable.py` 분리 작성
- [ ] **3. 진입점 정리** — `main.py` 추가, 기존 `assemble.py`의 `main()` 진입 로직 제거. 수동으로 콘솔 실행해 기존과 동일한 UX인지 스모크 테스트
- [ ] **4. 유닛테스트 작성** — `tests/test_assemble.py`에 `AssembleTestable`로 전체 시나리오 테스트: 정상 조합 PASS, 5개 위반 규칙 각각 FAIL, 고장난 엔진 RUN 실패, 잘못된 입력 범위 에러, 뒤로가기(0) 동작

## 검증 방법

- 각 단계마다 `pytest python/tests` 실행해 통과 확인
- 단계 3 이후 `python python/main.py`로 직접 실행해 기존과 동일하게 동작하는지 수동 확인 (Sedan → GM → Mando → Bosch → RUN/Test 등 몇 가지 조합)
- 최종적으로 기존 `assemble.py`의 모든 분기(5개 호환성 규칙 + 고장난 엔진)가 새 구조에서도 동일한 메시지로 재현되는지 확인

## 원본 대비 알려진 차이 (기능에 영향 없음)

- 제동장치/조향장치 **선택 확인** 메시지가 원본에서는 대문자(`MANDO`, `BOSCH` 등)였으나, RUN 결과 출력에 쓰이던 표기(`Mando`, `Bosch` 등)로 통일함. 원본 자체가 두 메시지 사이에 표기가 일관되지 않았던 부분을 정리한 것으로, 통과/실패 판정이나 로직에는 영향 없음.
- Test 결과 메시지는 원본 `assemble.py`와 동일하게 `"PASS"` / `"FAIL\n<사유>"` 형식을 그대로 유지함 (Java `v2` 버전의 `"자동차 부품 조합 테스트 결과 : PASS/FAIL"` 형식과는 다름 — 파이썬 원본 문구를 기준으로 함).
