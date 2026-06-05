# UnitConverter 재구현 스펙

> 목표: 길이 단위 변환 CLI인 UnitConverter를 **PRD와 테스트로부터 추적 가능하게** 재구현한다.
> 본 문서는 PRD(요구) → 설계(모듈) → 테스트(TC)로 이어지는 단일 추적 기준이다.

---

## 1. 범위 (Scope)

| 구분 | 내용 |
|------|------|
| 대상 | 길이 단위(meter / feet / yard, 확장 가능) 변환 CLI |
| 입력 | `단위:값` 형식 문자열 (예: `meter:2.5`) |
| 출력 | 입력 단위를 제외한 전 단위 변환 결과 (table / json / csv) |
| 비범위 | GUI, 온도·무게 등 비길이 단위, 다국어 메시지 |

---

## 2. 용어 (Glossary)

| 용어 | 정의 |
|------|------|
| **Base unit** | 모든 변환의 기준 단위. 본 시스템은 `meter`를 기준으로 한다. |
| **Ratio** | `1 base = N unit` 형태의 변환 비율. `meter → unit` 방향으로 정의. |
| **Registry** | 단위와 비율을 보관/조회/등록하는 저장소. |

---

## 3. 비즈니스 규칙 (Conversion Rules)

- 기준 단위: `meter`
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- 모든 변환은 **입력값 → meter → 목표 단위** 2단계로 수행한다. (단위 N개여도 비율은 N개만 유지 → DRY/OCP)
- 출력 정밀도: 기본 **소수점 4자리**(`--precision`으로 조정 가능, 기본 4).
- 변환 라인에는 **입력 단위 자기 자신을 제외**한다.
- 맨 앞에 **입력 에코(헤더) 라인**을 1줄 추가한다 → 총 출력 3줄 이상 (U-OUT-01).

---

## 4. 아키텍처 (SRP / OCP)

```
입력 문자열
   │
   ▼
┌──────────────┐   "meter:2.5" → ParsedInput(unit="meter", value=2.5)
│  InputParser │   FR-01, FR-05
└──────┬───────┘
       │ ParsedInput
       ▼
┌──────────────┐   음수·형식·범위 검증
│  Validator   │   FR-04, FR-05
└──────┬───────┘
       │
       ▼
┌──────────────┐   단위 ↔ 비율 조회/등록 (설정파일·동적등록)
│  UnitRegistry│   FR-03, EXT-01, EXT-02, NFR-01(OCP)
└──────┬───────┘
       │ ratios
       ▼
┌──────────────┐   value → meter → 전 단위 (자기 단위 제외)
│  Converter   │   FR-02
└──────┬───────┘
       │ ConversionResult[]
       ▼
┌──────────────┐   table / json / csv 직렬화
│  OutputFormatter (전략) │   EXT-03
└──────┬───────┘
       │
       ▼
┌──────────────┐   I/O 경계 (인자/표준입출력)
│  CLI (main)  │
└──────────────┘
```

### 모듈 책임 (각 1책임 = SRP)

| 모듈 | 단일 책임 | 비고 |
|------|-----------|------|
| `InputParser` | `단위:값` 문자열 → 구조화 객체 | I/O 없음(순수 함수) |
| `Validator` | 형식/음수/미등록 단위 검증, 명확한 오류 발생 | 도메인 예외 발생 |
| `UnitRegistry` | 단위·비율 보관, 조회, 동적 등록, 설정 로드 | OCP 핵심. 단위 추가 시 코드 무수정 |
| `Converter` | 비율 기반 변환 계산 | 비율 출처 무관(주입받음) |
| `OutputFormatter` | 결과 직렬화(table/json/csv) | 전략 패턴, 포맷 추가 시 클래스만 추가 |
| `CLI / main` | 인자 파싱 + 모듈 조립(orchestration) | 유일한 I/O 경계 |

### 핵심 인터페이스(개념)

```python
@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float

@dataclass(frozen=True)
class ConversionResult:
    source_unit: str
    source_value: float
    target_unit: str
    target_value: float

class OutputFormatter(Protocol):
    def format(self, results: list[ConversionResult]) -> str: ...
```

### 도메인 예외(명확한 오류 — FR-03/04/05)

| 예외 | 발생 조건 | 종료코드 |
|------|-----------|----------|
| `InvalidFormatError` | `:` 누락, 값이 숫자 아님 | 2 |
| `NegativeValueError` | 값 < 0 | 2 |
| `UnknownUnitError` | 미등록 단위 | 2 |

---

## 4.1 패키지 구조 (OCP / SRP)

```
UnitConverter_30/
├── unit_converter/                 # 소스 패키지
│   ├── __init__.py                 # 공개 API 노출 (Converter, UnitRegistry 등)
│   ├── __main__.py                 # python -m unit_converter 진입점
│   ├── cli.py                      # 인자 파싱 + 모듈 조립 (I/O 경계)
│   ├── models.py                   # ParsedInput, ConversionResult (frozen dataclass)
│   ├── exceptions.py               # InvalidFormatError / NegativeValueError / UnknownUnitError
│   ├── parser.py                   # InputParser : "unit:value" → ParsedInput
│   ├── validator.py                # Validator : 형식·음수·미등록 검증
│   ├── registry.py                 # UnitRegistry : 비율 보관/조회/동적등록
│   ├── converter.py                # Converter : value → meter → 전 단위
│   ├── config.py                   # ConfigLoader : units.json/yaml 로드
│   └── formatters/                 # 출력 전략 (포맷 추가 = 파일 추가)
│       ├── __init__.py             # FORMATTERS 레지스트리 + get_formatter()
│       ├── base.py                 # OutputFormatter Protocol/ABC
│       ├── table.py                # TableFormatter
│       ├── json_fmt.py             # JsonFormatter
│       └── csv_fmt.py              # CsvFormatter
├── tests/                          # PRD 추적 테스트
│   ├── test_parser.py              # FR-01, FR-05
│   ├── test_validator.py           # FR-04, FR-05
│   ├── test_registry.py            # FR-03, NFR-01, EXT-02
│   ├── test_converter.py           # FR-02, NFR-01
│   ├── test_config.py              # EXT-01
│   ├── test_formatters.py          # EXT-03
│   └── test_cli.py                 # end-to-end (조립 검증)
├── units.json                      # 기본 변환 비율 (외부화, EXT-01)
├── requirements.txt
├── README.md                       # 인자 기반 CLI로 갱신
└── SPEC.md
```

### 모듈 → FR/NFR 매핑

| 모듈 | 단일 책임 (SRP) | 충족 요구 |
|------|----------------|-----------|
| `parser.py` | 문자열 → 구조화 객체 (순수 함수) | **FR-01**, FR-05 |
| `validator.py` | 형식/음수/미등록 검증, 도메인 예외 | **FR-04**, FR-05, FR-03 |
| `registry.py` | 단위·비율 보관/조회/동적등록 | **FR-03**, **NFR-01(OCP)**, EXT-02 |
| `config.py` | 비율 외부 설정 로드 | EXT-01 |
| `converter.py` | 비율 기반 변환 계산 (비율 주입) | **FR-02**, NFR-01 |
| `formatters/` | 결과 직렬화 (전략 패턴) | **EXT-03** |
| `cli.py` / `__main__.py` | 인자 파싱 + 조립 (유일한 I/O) | 통합 |
| `models.py` / `exceptions.py` | 데이터·예외 계약 | 횡단(NFR-02) |

### OCP 보장 지점 (확장 시 기존 코드 무수정)

1. **새 단위 추가** → `registry.register(...)` 호출 또는 `units.json` 한 줄. `converter.py` 분기 수정 없음.

```python
registry.register("inch", 39.3701)   # 기존 코드 변경 0
```

2. **새 출력 포맷 추가** → `formatters/`에 클래스 1개 추가 + 레지스트리 등록. `cli.py`·`converter.py` 무수정.

```python
# formatters/__init__.py
FORMATTERS = {"table": TableFormatter, "json": JsonFormatter, "csv": CsvFormatter}
def get_formatter(name): return FORMATTERS[name]()
```

### SRP 보장 지점 (변경 사유 1:1 격리)

| 변경 사유 | 수정 대상 |
|-----------|-----------|
| 파싱 규칙 변경 | `parser.py` |
| 검증 정책 변경 | `validator.py` |
| 비율 출처 변경(하드코딩→설정→DB) | `registry.py` / `config.py` |
| 출력 모양 변경 | `formatters/` |

### 의존성 방향

```
cli → parser → validator → registry → converter → formatters
                              ↑
                          config (로드 시 주입)
```

- 핵심 도메인(`converter`, `registry`)은 I/O(`cli`, 설정 파일)에 의존하지 않음 → 의존성 역전, 단위 테스트 용이(NFR-03).
- `models` / `exceptions`는 모든 계층이 공유하는 안정적 계약(leaf 의존성).

---

## 5. CLI 명세

```bash
# 기본 (인자)
python -m unit_converter "meter:2.5"

# 출력 포맷 선택
python -m unit_converter "meter:2.5" --format json
python -m unit_converter "meter:2.5" --format csv

# 설정 파일 로드 (비율 외부화)
python -m unit_converter "meter:2.5" --config units.json

# 동적 단위 등록 후 변환
python -m unit_converter "cubit:1" --register "cubit=0.4572"
```

### 예상 출력 (table, 기본)

```
$ python -m unit_converter "meter:2.5"
2.5 meter:
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

### 설정 파일 형식 (`units.json`, EXT-01)

```json
{
  "base": "meter",
  "ratios": {
    "feet": 3.28084,
    "yard": 1.09361
  }
}
```
- `ratios[unit]` = `1 meter = N unit`.
- 파일 부재/파싱 실패 시 내장 기본 비율로 폴백 후 경고.

---

## 6. 품질 요구사항 (NFR)

| ID | 요구 | 충족 방식 |
|----|------|-----------|
| NFR-01 | OCP | 단위 추가 = `UnitRegistry`에 비율 등록(코드/설정), 변환기 분기 수정 없음 |
| NFR-02 | SRP | Parser / Validator / Registry / Converter / Formatter 분리 |
| NFR-03 | 테스트 용이성 | I/O를 CLI 경계로 격리, 핵심 로직은 순수 함수 |
| NFR-04 | 정확성 | meter 경유 단일 비율, 소수 4자리 반올림 일관 적용 |

---

## 7. PRD → 테스트 추적표 (Traceability)

각 요구는 최소 1개 TC와 1:1 이상 매핑된다. (Given–When–Then)

| ID | 요구 | TC ID | Given | When | Then | P |
|----|------|-------|-------|------|------|---|
| FR-01 | `meter:2.5` 파싱 | `test_parse_valid` | `"meter:2.5"` | parse | `unit="meter", value=2.5` | P0 |
| FR-02 | 전 단위 출력 | `test_convert_meter_all` | `meter 2.5` | convert | `feet≈8.2021, yard≈2.7340` (자기 단위 제외) | P0 |
| FR-03 | 미등록 단위 | `test_unknown_unit` | `"cubit:1"` (미등록) | parse+validate | `UnknownUnitError` | P0 |
| FR-04 | 음수 거부 | `test_negative_value` | `"meter:-1"` | validate | `NegativeValueError` | P0 |
| FR-05 | 잘못된 형식 | `test_invalid_format` | `"meter"`, `"meter:abc"`, `"meter/abc"` | parse | `InvalidFormatError` | P0 |
| NFR-01 | OCP | `test_register_no_core_change` | `inch=39.3701` 등록 | convert | 변환기 코드 변경 없이 inch 변환 | P0 |
| NFR-02 | SRP | `test_modules_independent` | 각 모듈 단독 | unit test | Parser/Validator/Registry/Converter/Formatter 독립 검증 | P0 |
| EXT-01 | 설정 파일 | `test_load_config_json` | `units.json` | load | Registry에 비율 반영 | P1 |
| EXT-02 | 동적 등록 | `test_dynamic_register` | `1 cubit = 0.4572 meter` 등록 | convert | cubit 즉시 변환 가능 | P1 |
| EXT-03 | 출력 포맷 | `test_format_json`, `test_format_csv`, `test_format_table` | 변환 결과 | format | 포맷별 직렬화 검증 | P1 |

---

## 7.1 Dual-Track RED 설계표

RED(🔴) 단계에서 작성할 실패 테스트를 두 트랙으로 나눠 설계한다.
**Track A**는 UI/경계(입출력·검증), **Track B**는 도메인/로직(순수 함수)을 다룬다.

### Track A — UI / Boundary

| Test ID | Given | Then (Expected RED) |
|---------|-------|---------------------|
| `U-IN-01` | `""` (빈 입력) | 형식 오류 메시지 |
| `U-IN-02` | `meter` (콜론 없음) | 형식 오류 |
| `U-IN-03` | `meter:-1` | 음수 거부 |
| `U-OUT-01` | `meter:2.5` | 3줄 이상 출력 (스켈레톤) |

### Track B — Domain / Logic

| Test ID | 함수 | Given / Then |
|---------|------|--------------|
| `D-CNV-01` | `to_meter` | `1 feet → 0.3048 m` (±ε) |
| `D-CNV-02` | `convert_all` | `2.5 m → 8.20210 ft` (5자리) |
| `D-CNV-03` | `convert_all` | `feet→yard`, meter 경유 일치 |
| `D-REG-01` | `register` | `cubit 0.4572` → 변환 기능 |
| `D-CFG-01` | `load json` | 깨진 파일 → `ConfigError` |

### Track C — Output / Formatter (EXT-03)

| Test ID | 대상 | Given / Then |
|---------|------|--------------|
| `F-TBL-01` | `TableFormatter` | 변환 결과 → `"src = val unit"` 라인 문자열 |
| `F-JSN-01` | `JsonFormatter` | 변환 결과 → 파싱 가능한 JSON 배열 |
| `F-CSV-01` | `CsvFormatter` | 변환 결과 → 헤더 + 행 CSV |
| `F-REG-01` | `get_formatter` | `"xml"`(미지원) → 명확한 오류 |

### RED 단계 금지 규칙

- RED 단계에서 **구현 코드 작성 금지** (테스트만 작성)
- `pytest.fail("RED: ...")` 허용
- `skip` / `xfail` **금지** (실패는 실패로 남긴다)
- **1 RED 묶음 = 1 커밋**

---

## 8. 마일스톤

1. **M1 (P0 기본)**: Parser·Validator·Registry·Converter·Formatter(table) + FR/NFR TC
2. **M2 (P1 확장)**: 설정 로드(EXT-01) · 동적 등록(EXT-02) · json/csv 포맷(EXT-03) + TC
3. **M3 (정리)**: 패키지화(`unit_converter/`), README 갱신(인자 기반 CLI·정밀도 명세 통일)

---

## 9. 레거시 대비 변경 요약

| 레거시 스멜 | 본 스펙의 해소 |
|-------------|----------------|
| God function `main()` | 모듈 5분리 (SRP) |
| `if/elif` 단위 분기 | Registry 비율 조회 (OCP) |
| 매직 넘버 중복 | 비율을 Registry/설정에 단일 보관 (DRY) |
| 역변환 오차 | meter 경유 단일 비율 + 일관 반올림 |
| `input()` 결합 | I/O를 CLI 경계로 격리 |
| 음수 미검증 | `Validator` + `NegativeValueError` |
| 자기 단위 출력 | 출력 시 입력 단위 제외 |
| 포맷 고정 | `OutputFormatter` 전략 |
| 테스트 0개 | FR/NFR/EXT 전 항목 TC 매핑 |
