# ReEntropy DB Builder

Zotero에서 내보낸 CSV를 업로드하면, 논문 초록과 키워드를 자동 분석해 우선순위 정렬된 Excel 파일을 생성합니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 우선순위 기준

| 등급 | 조건 |
|------|------|
| ⭐⭐⭐ | 인장물성 + 공정변수 + 77K |
| ⭐⭐ | 인장물성 + 공정변수 |
| ⭐ | 인장물성 또는 공정변수 |
| 📄 | 해당 없음 |

## 키워드 수정

`config.py`에서 `TENSILE_KEYWORDS`, `PROCESS_KEYWORDS`, `CRYO_KEYWORDS` 목록을 수정하세요.
