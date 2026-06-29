# ReEntropy DB Builder

## 목적
각자 담당 3개년도씩 논문을 찾아도 1000여개가 넘는 경우가 있기 때문에  
팀원 7명이 각자 담당 논문 파트를 효율적으로 처리하기 위해 사용.  
논문을 하나씩 직접 읽는 대신, **초록과 키워드 기반으로 우선순위를 자동 정렬**하여  
기한 내 최대한 많은 논문을 DB에 입력하도록 돕는 보조 도구.

---

## 배경 및 데이터 흐름

### 논문 수집 방법
1. Web of Science(WoS)에서 Fe 기반 합금 관련 논문 검색
2. **Full Record + Cited References** 형식으로 RIS 추출
   - Full record에는 Abstract, Author Keywords, Keywords Plus, Document Type 등 포함
3. Zotero에 RIS 임포트 → 컬렉션 정리
4. Zotero에서 **CSV 형식으로 내보내기** → 이 CSV가 본 툴의 입력값

### 조성 조건
- WoS 검색 단계에서 이미 1차 필터링 완료
- Fe 기반 + Mn/Cr/Ni 관련 키워드로 검색했기 때문에
- 본 툴에서는 **조성 필터링 불필요**
- 인장물성 + 공정변수 + 77K 여부만 체크하면 됨

---

## 입출력

### 입력
- Zotero에서 내보낸 **CSV 파일 1개**
- CSV에 포함된 주요 컬럼:
  - `Title` : 논문 제목
  - `Author` : 저자
  - `Publication Year` : 출판 연도
  - `DOI` : DOI 링크
  - `Abstract` : 초록 ← **키워드 체크 대상 1**
  - `Author Keywords` : 저자 키워드 ← **키워드 체크 대상 2**
  - `Keywords Plus` : WoS 자동생성 키워드 ← **키워드 체크 대상 3**
  - `Document Type` : 문서 타입 (Article / Review 등)

### 출력
- **우선순위 정렬된 Excel 파일**
- 팀원이 다운로드 후 순서대로 논문 열어서 DB 입력

---

## 우선순위 로직

### 체크 항목 3가지
각 항목은 Abstract + Author Keywords + Keywords Plus 전부 합쳐서 키워드 검색

| 항목 | 설명 |
|------|------|
| 인장물성 | UTS/YS/TE 관련 키워드 포함 여부 |
| 공정변수 | 열처리/압연/가공 관련 키워드 포함 여부 |
| 77K | 극저온 관련 키워드 포함 여부 (보너스) |

### 등급 기준

| 등급 | 조건 |
|------|------|
| ⭐⭐⭐ 최우선 | 인장물성 + 공정변수 + 77K 전부 언급 |
| ⭐⭐ 높음 | 인장물성 + 공정변수 언급 |
| ⭐ 보통 | 인장물성 or 공정변수 하나만 언급 |
| 📄 낮음 | 관련 언급 거의 없음 |

> **탈락 판정 없음.**  
> 초록/키워드에 없어도 본문에 데이터가 있을 수 있으므로 탈락 판정은 하지 않음.  
> 우선순위만 조정하고, 팀원이 시간 내에 최대한 많이 확인하는 방식으로 운영.

---

## 키워드 목록 (config.py에서 관리)

### 인장물성 키워드
```python
TENSILE_KEYWORDS = [
    "UTS", "YS", "TE",
    "tensile strength", "yield strength", "elongation",
    "ultimate tensile", "fracture", "tensile properties",
    "mechanical properties", "tensile behavior"
]
```

### 공정변수 키워드
```python
PROCESS_KEYWORDS = [
    "annealing", "homogenization", "solution treatment",
    "cold rolling", "hot rolling", "forging",
    "heat treatment", "rolling", "deformation",
    "aging", "quenching", "sintering"
]
```

### 77K 보너스 키워드
```python
CRYO_KEYWORDS = [
    "77K", "77 K", "cryogenic", "liquid nitrogen",
    "low temperature", "cryogenic temperature"
]
```

---

## 출력 Excel 컬럼 구조

| 컬럼명 | 설명 |
|--------|------|
| Title | 논문 제목 (길면 잘라서 표시) |
| Author / Year | 저자 et al., 연도 형식 |
| DOI | 클릭 시 논문 바로 열리는 하이퍼링크 |
| Document Type | Article / Review 등 |
| 인장물성 | ✅ or ❌ |
| 공정변수 | ✅ or ❌ |
| 77K | ⭐ or ❌ |
| 우선순위 | ⭐⭐⭐ / ⭐⭐ / ⭐ / 📄 |

### 출력 예시

| Title | Author/Year | DOI | Document Type | 인장물성 | 공정변수 | 77K | 우선순위 |
|-------|------------|-----|--------------|---------|---------|-----|---------|
| Fe-Mn-Based... | Smith et al., 2021 | 링크 | Article | ✅ | ✅ | ⭐ | ⭐⭐⭐ |
| Effect of Cr... | Kim et al., 2020 | 링크 | Article | ✅ | ✅ | ❌ | ⭐⭐ |
| Microstructure... | Lee et al., 2022 | 링크 | Article | ✅ | ❌ | ❌ | ⭐ |
| Al-Ti Alloy... | Park et al., 2021 | 링크 | Review | ❌ | ❌ | ❌ | 📄 |

---

## 웹앱 화면 구성 (Streamlit)

```
[ CSV 파일 업로드 ]
        ↓
[ 분석 실행 버튼 ]
        ↓
진행률 표시 ████░░ 60%
        ↓
결과 테이블 미리보기 (우선순위 높은 순 정렬)
        ↓
[ Excel 다운로드 버튼 ]
```

---

## 폴더 구조

> ReEntropy 프로젝트와 별도 분리된 독립 Git 레포로 관리

```
db_builder/               ← 별도 Git 레포
├── .venv/                # 가상환경 (git 제외)
├── app.py                # Streamlit 메인 (UI + 흐름 제어)
├── parse_csv.py          # Zotero CSV 파싱 + 키워드 체크 + 우선순위 계산
├── export_excel.py       # 우선순위 정렬 + Excel 출력
├── config.py             # 키워드 목록 관리 (수정 시 여기만 건드림)
├── requirements.txt      # 패키지 목록 (Streamlit Cloud 배포용)
├── .gitignore            # .venv/ 제외
└── README.md
```

### 각 파일 역할 요약

| 파일 | 역할 |
|------|------|
| `app.py` | Streamlit UI, CSV 업로드, 실행 버튼, 결과 미리보기, Excel 다운로드 |
| `parse_csv.py` | CSV 로드, Abstract + Keywords 합쳐서 키워드 체크, 우선순위 계산 |
| `export_excel.py` | 우선순위 정렬, Excel 파일 생성, DOI 하이퍼링크 삽입 |
| `config.py` | 인장물성 / 공정변수 / 77K 키워드 목록 |
| `requirements.txt` | streamlit, pandas, openpyxl |

---

## 배포 흐름

### 개발자
```
로컬 (VSCode + .venv)에서 개발 및 테스트
        ↓
GitHub push (.venv는 .gitignore로 제외)
        ↓
Streamlit Cloud에서 GitHub 레포 연결
requirements.txt 보고 자동 패키지 설치
        ↓
URL 생성 (https://xxx.streamlit.app)
        ↓
팀원 7명한테 URL 공유
```

### 팀원 7명 (사용자)
```
1. WoS에서 담당 연도 검색 → Full Record RIS 추출
2. Zotero 임포트 → CSV 내보내기
3. 웹앱 URL 브라우저 접속 (설치 필요없음)
4. CSV 파일 업로드
5. 분석 실행
6. 결과 Excel 다운로드
7. ⭐⭐⭐부터 순서대로 논문 열어서 DB 입력
```

---

## 후순위 추가 기능 (여유 생기면)
- PDF 업로드 → 본문 텍스트 파싱
- 키워드 포함 문장 하이라이트 표시
- 초록에 없는 논문 본문 재확인
- Document Type 필터 (Review 자동 하단 정렬)
