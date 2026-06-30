import sys
import streamlit as st
from parse_csv import load_and_analyze
from export_excel import build_excel

st.set_page_config(page_title="ReEntropy DB Builder", page_icon="⭐", layout="wide")

if sys.version_info < (3, 8):
    st.error(f"Python 3.8 이상이 필요합니다. 현재 버전: {sys.version.split()[0]}")
    st.stop()

st.markdown("""
<style>
div.stButton > button[kind="primary"],
div.stDownloadButton > button[kind="primary"] {
    background-color: #2F6DB5;
    border-color: #2F6DB5;
    color: white;
}
div.stButton > button[kind="primary"]:hover,
div.stDownloadButton > button[kind="primary"]:hover {
    background-color: #1F5A9F;
    border-color: #1F5A9F;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("ReEntropy DB Builder")
st.caption("Zotero CSV → 우선순위 정렬 Excel 변환 도구")

st.divider()

uploaded_file = st.file_uploader("Zotero에서 내보낸 CSV 파일을 업로드하세요", type="csv")

# 다른 파일로 교체 시 이전 결과 초기화
if uploaded_file is not None:
    if st.session_state.get("last_file_name") != uploaded_file.name:
        for key in ("result_df", "stats", "excel_bytes"):
            st.session_state.pop(key, None)
        st.session_state["last_file_name"] = uploaded_file.name

if uploaded_file is not None:
    if st.button("분석 실행", type="primary", use_container_width=True):
        with st.spinner("키워드 분석 중..."):
            progress = st.progress(0, text="CSV 로딩 중...")
            try:
                result_df, stats = load_and_analyze(uploaded_file)
            except ValueError as e:
                st.error(str(e))
                st.stop()
            progress.progress(60, text="Excel 생성 중...")
            excel_bytes = build_excel(result_df)
            progress.progress(100, text="완료!")
            progress.empty()

        st.session_state["result_df"] = result_df
        st.session_state["stats"] = stats
        st.session_state["excel_bytes"] = excel_bytes

    if "result_df" in st.session_state:
        stats = st.session_state["stats"]
        result_df = st.session_state["result_df"]
        excel_bytes = st.session_state["excel_bytes"]

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
