# AGENTS.md — UnitConverter TDD Harness

## 주제

**길이 변환을 테스트 가능한 모듈로 만든다.**
PRD(`README.md`)와 설계(`docs/SPEC.md`)로부터 추적 가능한 모듈을 TDD로 구현한다.

## RGIO (작업 정의)

| 항목 | 값 |
|------|----|
| **Role** | 개발자 |
| **Goal** | C2C (Concept → Code: PRD 개념을 추적 가능한 코드로) |
| **Input** | `unit:val` (예: `meter:2.5`) |
| **Output** | 전 단위 변환 결과 (입력 단위 제외) |

## ARRR 개발 루프 (RED → GREEN → REFACTOR)

모든 기능은 아래 4단계를 1사이클로 반복한다. **테스트 없이 프로덕션 코드를 먼저 쓰지 않는다.**

| 단계 | 의미 | TDD 위상 | 산출물 |
|------|------|----------|--------|
| **Ask** | 실패하는 테스트부터 작성 | 🔴 RED | `tests/test_convert.py` 스켈레톤 (실패) |
| **Respond** | 통과시킬 최소 구현 | 🟢 GREEN | `Registry` + `Converter` 최소 구현 |
| **Refine** | 구조 개선, 동작 불변 | 🛠 REFACTOR | `Parser` / `Formatter` 분리 + Golden Master |
| **Repeat** | 다음 요구를 새 RED로 | 🔴 → 반복 | 추가 요구를 1개씩 사이클 반복 |

### 확장 (Repeat 대상)

- 동적 단위 등록 (`1 cubit = 0.4572 meter`)
- 출력 3포맷 (`table` / `json` / `csv`)

## 루프 규칙

1. **RED 먼저**: 새 동작은 항상 실패하는 테스트로 시작한다. 테스트가 실패하는 것을 먼저 확인한다.
2. **최소 GREEN**: 테스트를 통과시키는 가장 단순한 코드만 작성한다. 미래 대비 일반화 금지.
3. **REFACTOR는 그린 상태에서만**: 테스트가 모두 통과할 때만 구조를 바꾼다. Golden Master로 출력 회귀를 고정한다.
4. **한 번에 한 요구**: 한 사이클은 PRD 추적표의 1개 ID(FR/NFR/EXT)만 다룬다.
5. **추적성**: 각 테스트는 대상 요구 ID를 명시한다 (예: `# FR-02`).

## Dual-Track RED 설계 (Ask 단계)

RED 테스트는 두 트랙으로 나눠 설계한다. 상세표는 `docs/SPEC.md` §7.1 참조.

| Track | 범위 | 대표 Test ID |
|-------|------|--------------|
| **A — UI / Boundary** | 입출력·검증 경계 | `U-IN-01`(빈 입력), `U-IN-02`(콜론 없음), `U-IN-03`(음수 거부), `U-OUT-01`(3줄 출력) |
| **B — Domain / Logic** | 순수 함수 | `D-CNV-01`(`to_meter`), `D-CNV-02`/`D-CNV-03`(`convert_all`), `D-REG-01`(`register`), `D-CFG-01`(`load json`→`ConfigError`) |

### RED 단계 금지 규칙

- RED 단계에서 **구현 코드 작성 금지** (테스트만 작성)
- `pytest.fail("RED: ...")` 허용
- `skip` / `xfail` **금지** (실패는 실패로 남긴다)
- **1 RED 묶음 = 1 커밋**

## 명령어

```bash
pytest -q                      # 전체
pytest tests/test_convert.py   # 현재 사이클
pytest -k "FR_02"              # 특정 요구
```

## 참조

- 요구사항: `README.md`
- 설계/추적표: `docs/SPEC.md` (§4 아키텍처, §4.1 패키지 구조, §7 PRD→TC 추적표)
- 루프 규칙 상세: `.cursor/rules/tdd-arrr-loop.mdc`
- 워크플로 스킬: `.cursor/skills/length-converter-tdd/SKILL.md`
