import streamlit as st
import pandas as pd
import plotly.express as px

st.title('나라별 탄소배출량 추이')

# 1. 데이터 로드 또는 생성 (실제 데이터로 대체하세요)
# 예시 데이터
data = {
    '연도': [2000, 2000, 2001, 2001, 2002, 2002, 2003, 2003, 2004, 2004],
    '나라': ['한국', '미국', '한국', '미국', '한국', '미국', '한국', '미국', '한국', '미국'],
    '탄소배출량': [500, 5000, 520, 5100, 550, 5300, 580, 5450, 600, 5600]
}
df = pd.DataFrame(data)

# 2. 사용자 입력 (예: 나라 선택)
selected_countries = st.multiselect(
    '나라를 선택하세요:',
    options=df['나라'].unique(),
    default=df['나라'].unique() # 기본적으로 모든 나라 선택
)

if selected_countries:
    filtered_df = df[df['나라'].isin(selected_countries)]

    # 3. Plotly를 이용한 선 그래프 생성
    fig = px.line(
        filtered_df,
        x='연도',
        y='탄소배출량',
        color='나라', # 나라별로 다른 색상
        title='연도별 탄소배출량 (선택된 나라)',
        labels={'탄소배출량': '탄소배출량 (단위)', '연도': '연도'} # 라벨 설정
    )

    # 4. 스트림릿에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("나라를 선택해주세요.")

st.write("---")
st.write("원본 데이터:")
st.dataframe(df)
