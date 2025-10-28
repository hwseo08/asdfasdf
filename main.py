import streamlit as st
import pandas as pd
import altair as alt

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="MBTI World Map Dashboard",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 MBTI 유형별 세계 지도 시각화 대시보드")
st.caption("업로드한 데이터를 기반으로 MBTI 유형 분포를 세계 지도 위에 시각적으로 확인해보세요.")

# --- MBTI 특징 요약 데이터 ---
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
uploaded_file = st.file_uploader("📂 MBTI 데이터 파일을 업로드하세요 (.csv 형식)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # --- Country 열 확인 ---
        if "Country" not in df.columns:
            st.error("❌ 업로드된 CSV에 'Country' 컬럼이 없습니다.")
            st.stop()

        # --- MBTI 유형 리스트 ---
        mbti_types = [c for c in df.columns if c != "Country"]
        if len(mbti_types) == 0:
            st.error("❌ MBTI 데이터가 없습니다. INFJ, ENFP 등 컬럼이 포함되어야 합니다.")
            st.stop()

        # --- MBTI 선택 ---
        selected_mbti = st.selectbox("🔎 시각화할 MBTI 유형을 선택하세요:", mbti_types)

        # --- 지도 데이터 준비 ---
        df_map = df[["Country", selected_mbti]].copy()
        df_map[selected_mbti] = pd.to_numeric(df_map[selected_mbti], errors="coerce")

        # --- Altair 세계지도 (내장 topojson 사용) ---
        countries = alt.topo_feature("https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/world-110m.json", "countries")

        map_chart = (
            alt.Chart(countries)
            .mark_geoshape(stroke="lightgray")
            .encode(
                color=alt.Color(
                    f"{selected_mbti}:Q",
                    scale=alt.Scale(scheme="tealblues"),
                    title=f"{selected_mbti} 비율(%)"
                ),
                tooltip=["Country:N", f"{selected_mbti}:Q"]
            )
            .transform_lookup(
                lookup="properties.name",
                from_=alt.LookupData(df_map, "Country", [selected_mbti])
            )
            .project("equalEarth")
            .properties(
                width=750,
                height=450,
                title=f"🌐 전세계 {selected_mbti} 분포 지도"
            )
        )

        st.altair_chart(map_chart, use_container_width=True)

        # --- MBTI 설명 표시 ---
        with st.expander(f"🧠 {selected_mbti} 유형 특징 보기"):
            st.markdown(f"**{selected_mbti}** — {mbti_descriptions.get(selected_mbti, '유형 설명이 없습니다.')}")
            st.dataframe(df_map.sort_values(by=selected_mbti, ascending=False).head(10).style.format({selected_mbti: "{:.2f}"}))

        st.success("✅ 지도와 MBTI 분석이 완료되었습니다!")

    except Exception as e:
        st.error(f"⚠️ 파일을 불러오는 중 오류가 발생했습니다: {e}")

else:
    st.info("👆 먼저 CSV 파일을 업로드해주세요. 예시: `countriesMBTI_16types.csv`")

# --- 푸터 ---
st.markdown("---")
st.markdown("💡 Tip: 'Country' 열에는 국가 이름이, 각 MBTI 열에는 해당 유형의 비율(%)이 포함되어야 합니다.")
