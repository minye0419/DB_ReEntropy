# ReEntropy DB Builder

Zotero에서 내보낸 CSV를 업로드하면, 논문 초록과 키워드를 자동 분석해 우선순위 정렬된 Excel 파일을 생성합니다.

## 요구 사항

- **Python 3.8 이상** (3.9+ 권장)
- Windows / macOS / Linux 모두 지원

## 설치 및 실행

```bash
# 1. 패키지 설치 (최초 1회)
pip install -r requirements.txt

# 2. 앱 실행
streamlit run app.py
```

> 가상환경 사용을 권장합니다.
> ```bash
> python -m venv .venv
> # Windows
> .venv\Scripts\activate
> # macOS / Linux
> source .venv/bin/activate
> pip install -r requirements.txt
> streamlit run app.py
> ```

## Zotero CSV 내보내기 방법

1. Zotero에서 분석할 컬렉션 선택
2. 파일 → 내보내기 → **CSV** 형식 선택
3. 내보낸 `.csv` 파일을 앱에 업로드

## 우선순위 기준

| 등급 | 조건 |
|------|------|
| ⭐⭐⭐ | 인장물성 + 공정변수 + 77K |
| ⭐⭐ | 인장물성 + 공정변수 |
| ⭐ | 인장물성 또는 공정변수 |
| 📄 | 해당 없음 |

## 키워드 수정

`config.py`에서 `TENSILE_KEYWORDS`, `PROCESS_KEYWORDS`, `CRYO_KEYWORDS` 목록을 수정하세요.
