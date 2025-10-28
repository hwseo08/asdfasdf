import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="전공별·학력별 임금 분석", layout="wide")

st.title("전공별·학력별 임금 및 근로 특성 분석")

# 사용자 CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 전공 선택
    majors = df['전공대분류'].unique().tolist()
    selected_major = st.selectbox("전공대분류 선택", majors)

    # 선택된 전공 데이터 필터링
    major_df = df[df['전공대분류'] == selected_major]

    st.subheader(f"{selected_major} 분석")
    st.dataframe(major_df)

    # 월평균 임금 비교 그래프
    st.subheader("학력별 월평균 임금 비교")
    fig = px.bar(major_df, x='최종학력', y='소득(월평균임금_만원)', color='최종학력', text='소득(월평균임금_만원)')
    fig.update_layout(yaxis_title='월평균임금 (만원)', xaxis_title='최종학력')
    st.plotly_chart(fig, use_container_width=True)

    # 근속연수 비교 그래프
    st.subheader("학력별 평균 근속연수")
    fig2 = px.bar(major_df, x='최종학력', y='평균근속연수(년)', color='최종학력', text='평균근속연수(년)')
    fig2.update_layout(yaxis_title='평균근속연수 (년)', xaxis_title='최종학력')
    st.plotly_chart(fig2, use_container_width=True)

    # 주당근로시간 비교 그래프
    st.subheader("학력별 주당 평균 근로시간")
    fig3 = px.bar(major_df, x='최종학력', y='주당평균근로시간(시간)', color='최종학력', text='주당평균근로시간(시간)')
    fig3.update_layout(yaxis_title='주당평균근로시간 (시간)', xaxis_title='최종학력')
    st.plotly_chart(fig3, use_container_width=True)

    # 전체 전공 비교 히트맵
    st.subheader("전공별·학력별 월평균임금 히트맵")
    pivot_df = df.pivot('전공대분류', '최종학력', '소득(월평균임금_만원)')
    fig4 = px.imshow(pivot_df, text_auto='.1f', color_continuous_scale='RdBu_r')
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("본 대시보드는 전공과 학력별로 월평균임금, 근속연수, 주당근로시간을 시각적으로 비교할 수 있도록 제작되었습니다.")
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
