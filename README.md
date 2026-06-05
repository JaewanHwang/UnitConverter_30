
## Unit Converter (Python)
![unit-converter](./docs/unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 실행 (인자 기반 CLI)
python -m unit_converter "meter:2.5"

# 레거시 인터랙티브 실행 (내부적으로 동일 패키지 사용)
python UnitConverter.py

# 테스트
pytest -q

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   $ python -m unit_converter "meter:2.5"
   +-------+-------+--------+
   | unit  | input | result |
   +-------+-------+--------+
   | meter |   2.5 |    2.5 |
   | feet  |   2.5 | 8.2021 |
   | yard  |   2.5 | 2.7340 |
   +-------+-------+--------+
   ```
   (출력 정밀도 기본 4자리, `--precision`으로 조정. table은 전 단위를 그리드로 표시.)

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것. (OCP — `UnitRegistry` 비율 등록)

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 추가 기능 (CLI 옵션)
```bash
# 출력 포맷 선택 (table | json | csv)
python -m unit_converter "meter:2.5" --format json

# 설정 파일에서 비율 로드 (EXT-01)
python -m unit_converter "meter:2.5" --config examples/units.json

# 동적 단위 등록: 1 cubit = 0.4572 meter (EXT-02)
python -m unit_converter "cubit:1" --register "cubit=0.4572"
```

설계·추적표(PRD→TC)는 [`docs/SPEC.md`](./docs/SPEC.md) 참조.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
