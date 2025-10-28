import streamlit as st
import pandas as pd


st.set_page_config(page_title="전공별·학력별 임금 분석", layout="wide")


st.title("전공별·학력별 임금 및 근로 특성 분석")


# 사용자 CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")


if uploaded_file is not None:
df = pd.read_csv(uploaded_file)


# 총합 행 제거 (pivot 시 중복 방지)
df_no_total = df[df['전공대분류'] != '총합']


# 전공 선택
majors = df_no_total['전공대분류'].unique().tolist()
selected_major = st.selectbox("전공대분류 선택", majors)


# 선택된 전공 데이터 필터링
major_df = df_no_total[df_no_total['전공대분류'] == selected_major]


st.subheader(f"{selected_major} 분석")
st.dataframe(major_df)


# 월평균 임금 비교
st.subheader("학력별 월평균 임금 비교")
st.bar_chart(major_df.set_index('최종학력')['소득(월평균임금_만원)'])


# 근속연수 비교
st.subheader("학력별 평균 근속연수")
st.bar_chart(major_df.set_index('최종학력')['평균근속연수(년)'])


# 주당근로시간 비교
st.subheader("학력별 주당 평균 근로시간")
st.bar_chart(major_df.set_index('최종학력')['주당평균근로시간(시간)'])


# 전체 전공 비교 히트맵(표) 생성
pivot_df = df_no_total.pivot(index='전공대분류', columns='최종학력', values='소득(월평균임금_만원)')
st.subheader("전공별·학력별 월평균임금 표")
st.dataframe(pivot_df)


st.markdown("---")
st.markdown("본 대시보드는 전공과 학력별로 월평균임금, 근속연수, 주당근로시간을 시각적으로 비교할 수 있도록 제작되었습니다.")
else:
st.info("먼저 CSV 파일을 업로드해주세요.")
