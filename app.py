import streamlit as st
from parse_csv import load_and_analyze
from export_excel import build_excel

st.set_page_config(page_title="ReEntropy DB Builder", page_icon="⭐", layout="wide")

st.title("ReEntropy DB Builder")
st.caption("Zotero CSV → 우선순위 정렬 Excel 변환 도구")

st.divider()

uploaded_file = st.file_uploader("Zotero에서 내보낸 CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    if st.button("분석 실행", type="primary", use_container_width=True):
        with st.spinner("키워드 분석 중..."):
            progress = st.progress(0, text="CSV 로딩 중...")
            result_df, stats = load_and_analyze(uploaded_file)
            progress.progress(60, text="Excel 생성 중...")
            excel_bytes = build_excel(result_df)
            progress.progress(100, text="완료!")
            progress.empty()

        st.success(f"분석 완료 — 총 {stats['total']}편")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("⭐⭐⭐ 최우선", stats["⭐⭐⭐"])
        col2.metric("⭐⭐ 높음", stats["⭐⭐"])
        col3.metric("⭐ 보통", stats["⭐"])
        col4.metric("📄 낮음", stats["📄"])

        st.divider()

        st.subheader("결과 미리보기 (상위 50건)")
        st.dataframe(result_df.head(50), use_container_width=True, hide_index=True)

        st.divider()

        st.download_button(
            label="Excel 다운로드",
            data=excel_bytes,
            file_name="논문_우선순위.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
        )
