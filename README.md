# assemblyCar

차량 조립 프로젝트 (원본: [mincoding-ai/assemblyCar](https://github.com/mincoding-ai/assemblyCar))

## 이 저장소에 대해

이 저장소는 원본 저장소를 그대로 가져온 뒤, **`python/assemble.py`(파이썬 구현체)만** 리팩토링 실습용으로 사용합니다.
`java/`, `cpp/`, `v2/` 등 다른 언어/버전 구현체는 원본 상태 그대로 유지되며 손대지 않습니다.

**파이썬 리팩토링 작업은 완료되었습니다.** 전역변수/절차형 코드를 enum·dataclass 기반 모델과 `Assemble` 클래스(+ I/O 분리)로 재작성했고, pytest 유닛테스트(19개)까지 갖췄습니다. 실행/테스트 방법은 [`python/README.md`](python/README.md), 리팩토링 배경·설계·단계별 진행 내역은 [`python/REFACTORING.md`](python/REFACTORING.md) 문서를 참고하세요.
