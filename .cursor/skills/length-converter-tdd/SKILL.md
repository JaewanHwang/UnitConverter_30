---
name: length-converter-tdd
description: Develop the UnitConverter length-conversion CLI with the ARRR (RED→GREEN→REFACTOR) TDD loop. Use when implementing or extending UnitConverter modules (parser, validator, registry, converter, formatters), writing tests in tests/, or when the user mentions TDD, ARRR, RED/GREEN/REFACTOR, Golden Master, or PRD/FR/NFR traceability for this project.
---

# Length Converter TDD (ARRR)

## 주제

길이 변환을 테스트 가능한 모듈로 만든다. PRD(`README.md`) / 설계(`SPEC.md`)에서 추적 가능한 코드로 구현(C2C).

## RGIO

- **Role**: 개발자
- **Goal**: C2C (개념 → 코드)
- **Input**: `unit:val` (예: `meter:2.5`)
- **Output**: 전 단위 변환 (입력 단위 제외)

## ARRR 루프 (한 사이클 = 요구 1개)

Copy this checklist per cycle:

```
ARRR Cycle — 대상 요구 ID: ____
- [ ] Ask    (🔴 RED): 실패 테스트 작성 → 실패 확인
- [ ] Respond(🟢 GREEN): 최소 구현 → 통과 확인
- [ ] Refine (🛠 REFACTOR): 구조 분리 + Golden Master → 여전히 통과
- [ ] Repeat: 다음 요구로
```

### Ask — 🔴 RED
`tests/test_convert.py`에 실패하는 테스트부터 작성한다. 대상 요구 ID를 주석으로 단다. 실행해 **실패를 먼저 확인**한다.

RED 테스트는 두 트랙으로 나눠 설계한다 (상세표: `SPEC.md` §7.1):

- **Track A — UI / Boundary**: `U-IN-01`(빈 입력), `U-IN-02`(콜론 없음), `U-IN-03`(음수 거부), `U-OUT-01`(3줄 출력 스켈레톤)
- **Track B — Domain / Logic**: `D-CNV-01`(`to_meter`), `D-CNV-02`/`D-CNV-03`(`convert_all`), `D-REG-01`(`register`), `D-CFG-01`(`load json`→`ConfigError`)

**RED 단계 금지 규칙**:
- RED 단계에서 구현 코드 작성 금지 (테스트만 작성)
- `pytest.fail("RED: ...")` 허용
- `skip` / `xfail` 금지 (실패는 실패로 남긴다)
- 1 RED 묶음 = 1 커밋

```bash
pytest tests/test_convert.py -q   # RED 확인
```

### Respond — 🟢 GREEN
`registry.py` + `converter.py`에 테스트를 통과시키는 **최소** 코드만 쓴다. 미래 대비 일반화 금지.

```bash
pytest -q   # GREEN 확인
```

### Refine — 🛠 REFACTOR
GREEN 상태에서만 구조 개선: `parser.py` / `formatters/`를 분리한다. 출력 회귀는 **Golden Master**로 고정한다.

```python
# tests/test_golden.py — 출력 스냅샷 고정
def test_table_golden():  # EXT-03
    out = render("meter:2.5", fmt="table")
    assert out == "2.5 meter = 8.2021 feet\n2.5 meter = 2.7340 yard"
```

### Repeat
추가 요구를 1개씩 새 RED로 반복. 확장 대상:
- **동적 단위 등록**: `registry.register("cubit", 1/0.4572)` → 변환기 코드 무수정 (OCP)
- **출력 3포맷**: `table` / `json` / `csv` → `formatters/`에 클래스 추가 (OCP)

## 추적성 매핑 (테스트 ↔ 요구)

| 요구 | 단계 진입점 | 테스트 |
|------|-------------|--------|
| FR-01 파싱 | Refine(Parser) | `test_parser.py` |
| FR-02 전 단위 출력 | Ask/Respond | `test_convert.py` |
| FR-03/04/05 검증 | Repeat | `test_validator.py` |
| NFR-01 OCP | Repeat(등록) | `test_registry.py` |
| EXT-01/02/03 | 확장 | `test_config.py`, `test_formatters.py` |

자세한 설계·추적표는 `SPEC.md`, 루프 규칙은 `.cursor/rules/tdd-arrr-loop.mdc` 참조.

## 금지 사항

- 테스트보다 프로덕션 코드 먼저 작성 금지
- RED가 아닌(이미 통과하는) 테스트로 사이클 시작 금지
- REFACTOR 중 동작/출력 변경 금지 (Golden Master로 가드)
- 단위 추가 시 `converter.py` 분기 수정 금지 (반드시 `registry`)
