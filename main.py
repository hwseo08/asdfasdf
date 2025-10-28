import streamlit as st
import pandas as pd
import altair as alt

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="MBTI by Country Dashboard",
    page_icon="🌍",
    layout="centered"
)

# --- 헤더 ---
st.title("🌍 MBTI 유형별 국가 분석 대시보드")
st.caption("각 MBTI 유형이 가장 높은 국가 TOP 10을 시각적으로 확인하세요.")

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# --- MBTI 유형 선택 ---
mbti_types = [c for c in df.columns if c != "Country"]
selected_mbti = st.selectbox("🔎 분석할 MBTI 유형을 선택하세요:", mbti_types)

# --- 데이터 처리 ---
top10 = (
    df[["Country", selected_mbti]]
    .sort_values(by=selected_mbti, ascending=False)
    .head(10)
)

# --- 시각화 (Altair 사용) ---
bar_chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        x=alt.X(f"{selected_mbti}:Q", title=f"{selected_mbti} 비율(%)"),
        y=alt.Y("Country:N", sort="-x", title="국가"),
        color=alt.Color(f"{selected_mbti}:Q", scale=alt.Scale(scheme="tealblues")),
        tooltip=["Country", selected_mbti]
    )
    .properties(width=600, height=400, title=f"{selected_mbti}가 높은 국가 TOP 10")
    .configure_axis(labelFontSize=12, titleFontSize=13)
    .configure_title(fontSize=18, anchor="start", color="#004C6D")
)

st.altair_chart(bar_chart, use_container_width=True)

# --- 데이터 테이블 ---
with st.expander("📋 데이터 보기"):
    st.dataframe(top10.style.format({selected_mbti: "{:.2f}"}))

# --- 푸터 ---
st.markdown(
    """
    ---
    **💡 Tip:**  
    다른 MBTI 유형을 선택하면 자동으로 그래프와 표가 업데이트됩니다.  
    데이터 출처: `countriesMBTI_16types.csv`
    """
)
