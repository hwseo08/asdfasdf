import streamlit as st
import pandas as pd
import altair as alt
import json
from urllib.request import urlopen

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="MBTI World Map", page_icon="🌍", layout="wide")

st.title("🌍 MBTI 유형별 세계 지도 시각화")
st.caption("업로드한 MBTI 데이터를 기반으로 국가별 비율을 시각적으로 확인할 수 있습니다.")

# --- MBTI 설명 ---
mbti_descriptions = {
    "INFJ": "통찰력 있고 이상주의적이며, 타인의 감정을 깊이 이해합니다.",
    "INFP": "감성적이고 창의적이며, 개인의 가치와 신념을 중시합니다.",
    "INTJ": "전략적이고 계획적이며, 장기적인 목표를 중시합니다.",
    "INTP": "논리적이고 호기심이 많으며, 아이디어 탐구를 즐깁니다.",
    "ISFJ": "성실하고 헌신적이며, 주변 사람을 잘 돌봅니다.",
    "ISFP": "온화하고 자유로운 영혼으로, 예술적 감각이 뛰어납니다.",
    "ISTJ": "체계적이고 책임감이 강하며, 전통과 규칙을 존중합니다.",
    "ISTP": "실용적이고 분석적이며, 손으로 무언가를 만드는 것을 좋아합니다.",
    "ENFJ": "사교적이고 배려심이 많으며, 타인을 이끄는 리더형입니다.",
    "ENFP": "열정적이고 상상력이 풍부하며, 새로운 경험을 즐깁니다.",
    "ENTJ": "결단력 있고 목표지향적이며, 리더십이 뛰어납니다.",
    "ENTP": "창의적이고 논쟁을 즐기며, 새로운 아이디어를 추구합니다.",
    "ESFJ": "친절하고 공동체 중심적이며, 조화를 중요하게 생각합니다.",
    "ESFP": "활기차고 사교적이며, 현재를 즐기는 낙천적인 성향입니다.",
    "ESTJ": "조직적이고 실용적이며, 규칙과 효율성을 중시합니다.",
    "ESTP": "대담하고 행동 중심적이며, 현실적인 문제 해결을 즐깁니다."
}

# --- 파일 업로드 ---
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (예: countriesMBTI_16types.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Country" not in df.columns:
        st.error("❌ CSV 파일에 'Country' 열이 없습니다.")
        st.stop()

    mbti_types = [col for col in df.columns if col != "Country"]
    if not mbti_types:
        st.error("❌ MBTI 유형 데이터가 없습니다 (예: INFJ, ENFP 등).")
        st.stop()

    selected_mbti = st.selectbox("🔍 시각화할 MBTI 유형을 선택하세요:", mbti_types)
    df[selected_mbti] = pd.to_numeric(df[selected_mbti], errors="coerce")
    df["Country"] = df["Country"].str.strip()

    # --- 세계지도 GeoJSON을 직접 로드 ---
    # CDN 접근 대신 local cache를 통해 altair가 접근 가능하도록 함
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    with urlopen(geojson_url) as response:
        countries = json.load(response)

    # --- 지도 생성 ---
    chart = (
        alt.Chart(alt.Data(values=countries["features"]))
        .mark_geoshape(stroke="gray", strokeWidth=0.4)
        .transform_lookup(
            lookup="properties.name",
            from_=alt.LookupData(df, "Country", [selected_mbti])
        )
        .encode(
            color=alt.Color(f"{selected_mbti}:Q",
                            scale=alt.Scale(scheme="blues"),
                            title=f"{selected_mbti} 비율(%)"),
            tooltip=["properties.name:N", f"{selected_mbti}:Q"]
        )
        .project("equalEarth")
        .properties(width=850, height=480, title=f"🌐 {selected_mbti} 분포 지도")
    )

    st.altair_chart(chart, use_container_width=True)

    # --- MBTI 설명 + 상위 국가 테이블 ---
    with st.expander(f"🧠 {selected_mbti} 특징 보기 및 상위 국가"):
        st.markdown(f"**{selected_mbti}** — {mbti_descriptions.get(selected_mbti, '유형 설명이 없습니다.')}")
        top10 = df.nlargest(10, selected_mbti)[["Country", selected_mbti]]
        st.dataframe(top10.style.format({selected_mbti: "{:.2f}"}))

else:
    st.info("👆 먼저 CSV 파일을 업로드해주세요. 예시: `countriesMBTI_16types.csv`")

st.markdown("---")
st.caption("💡 국가 이름은 영어로 입력되어 있어야 하며, MBTI별 비율(%) 열이 포함되어야 합니다.")
