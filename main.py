import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 불러오기
file_path = 'education_income.csv'  # 같은 폴더에 파일 저장 필요
df = pd.read_csv(file_path)

st.set_page_config(page_title="전공별·학력별 임금 분석", layout="wide")

st.title("전공별·학력별 임금 및 근로 특성 분석")

# 전공 선택
majors = df['전공대분류'].unique().tolist()
selected_major = st.selectbox("전공대분류 선택", majors)

# 선택된 전공 데이터 필터링
major_df = df[df['전공대분류'] == selected_major]

st.subheader(f"{selected_major} 분석")
st.dataframe(major_df)

# 월평균 임금 비교 그래프
st.subheader("학력별 월평균 임금 비교")
fig, ax = plt.subplots()
sns.barplot(data=major_df, x='최종학력', y='소득(월평균임금_만원)', palette='coolwarm', ax=ax)
ax.set_ylabel('월평균임금 (만원)')
ax.set_xlabel('최종학력')
st.pyplot(fig)

# 근속연수 비교 그래프
st.subheader("학력별 평균 근속연수")
fig2, ax2 = plt.subplots()
sns.barplot(data=major_df, x='최종학력', y='평균근속연수(년)', palette='viridis', ax=ax2)
ax2.set_ylabel('평균근속연수 (년)')
ax2.set_xlabel('최종학력')
st.pyplot(fig2)

# 주당근로시간 비교 그래프
st.subheader("학력별 주당 평균 근로시간")
fig3, ax3 = plt.subplots()
sns.barplot(data=major_df, x='최종학력', y='주당평균근로시간(시간)', palette='magma', ax=ax3)
ax3.set_ylabel('주당평균근로시간 (시간)')
ax3.set_xlabel('최종학력')
st.pyplot(fig3)

# 전체 전공 비교 히트맵
st.subheader("전공별·학력별 월평균임금 히트맵")
pivot_df = df.pivot('전공대분류', '최종학력', '소득(월평균임금_만원)')
fig4, ax4 = plt.subplots(figsize=(8,6))
sns.heatmap(pivot_df, annot=True, fmt='.1f', cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

st.markdown("---")
st.markdown("본 대시보드는 전공과 학력별로 월평균임금, 근속연수, 주당근로시간을 시각적으로 비교할 수 있도록 제작되었습니다.")
