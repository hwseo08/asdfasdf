import streamlit as st
import pandas as pd
import altair as alt

# --- 페이지 설정 ---
st.set_page_config(
    page_title="MBTI by Country Dashboard",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 MBTI 유형별 국가 분석 대시보드")
st.caption("CSV 파일을 업로드하고, MBTI 유형별 상위 10개 국가를 시각적으로 확인하세요.")

# --- 파일 업로드 섹션 ---
uploaded_file = st.file_uploader("📂 MBTI 데이터 파일을 업로드하세요 (.csv 형식)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # --- 기본 구조 확인 ---
        if "Country" not in df.columns:
            st.error("❌ 업로드된 CSV에 'Country' 컬럼이 없습니다. 국가 이름이 있는 열 제목을 'Country'로 수정해주세요.")
            st.stop()

        # --- MBTI 컬럼 탐색 ---
        mbti_types = [c for c in df.columns if c != "Country"]
        if len(mbti_types) == 0:
            st.error("❌ MBTI 유형 데이터가 존재하지 않습니다. INFJ, ISFJ 등의 컬럼이 포함되어야 합니다.")
            st.stop()

        # --- MBTI 유형 선택 ---
        selected_mbti = st.selectbox("🔎 분석할 MBTI 유형을 선택하세요:", mbti_types)

        # --- TOP 10 국가 계산 ---
        top10 = (
            df[["Country", selected_mbti]]
            .sort_values(by=selected_mbti, ascending=False)
            .head(10)
        )

        # --- 시각화 (Altair) ---
        chart = (
            alt.Chart(top10)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X(f"{selected_mbti}:Q", title=f"{selected_mbti} 비율(%)"),
                y=alt.Y("Country:N", sort="-x", title="국가"),
                color=alt.Color(f"{selected_mbti}:Q", scale=alt.Scale(scheme="tealblues")),
                tooltip=["Country", selected_mbti]
            )
            .properties(
                width=600,
                height=400,
                title=f"{selected_mbti}가 높은 국가 TOP 10"
            )
            .configure_axis(labelFontSize=12, titleFontSize=13)
            .configure_title(fontSize=18, anchor="start", color="#004C6D")
        )

        st.altair_chart(chart, use_container_width=True)

        # --- 데이터 표 ---
        with st.expander("📋 데이터 보기"):
            st.dataframe(top10.style.format({selected_mbti: "{:.2f}"}))

        st.success("✅ 분석이 완료되었습니다. 다른 MBTI 유형을 선택해보세요!")

    except Exception as e:
        st.error(f"⚠️ 파일을 불러오는 중 오류가 발생했습니다: {e}")

else:
    st.info("👆 먼저 CSV 파일을 업로드해주세요. 예: `countriesMBTI_16types.csv`")

# --- 푸터 ---
st.markdown("---")
st.markdown("💡 Tip: CSV에는 반드시 `Country` 열과 MBTI 유형 열들(`INFJ`, `ENFP`, 등)이 포함되어야 합니다.")
