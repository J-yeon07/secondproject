import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="글로벌 시총 Top 10 기업 주가 변화", layout="wide")

st.title("📈 글로벌 시총 Top 10 기업의 최근 3년 주가 변화")
st.markdown("데이터 제공: Yahoo Finance | 시각화: Streamlit + yfinance")

# 시총 Top 10 기업 (2025년 기준 추정)
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Nvidia': 'NVDA',
    'Berkshire Hathaway': 'BRK-B',
    'Meta (Facebook)': 'META',
    'TSMC': 'TSM',
    'Eli Lilly': 'LLY'
}

# 날짜 범위 설정
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365 * 3)

# 사용자 선택
selected_companies = st.multiselect(
    "📌 시각화할 기업 선택:",
    options=list(top10_tickers.keys()),
    default=list(top10_tickers.keys())
)

if selected_companies:
    st.write(f"📆 데이터 범위: {start_date} ~ {end_date}")
    data = pd.DataFrame()

    # 각 기업 주가 수집
    for name in selected_companies:
        ticker = top10_tickers[name]
        df = yf.download(ticker, start=start_date, end=end_date)
        df = df[['Close']].rename(columns={'Close': name})
        if data.empty:
            data = df
        else:
            data = data.join(df, how='outer')

    # 시각화
    st.line_chart(data)

    # 개별 그래프 표시
    st.subheader("📊 개별 기업 주가 그래프")
    for name in selected_companies:
        st.line_chart(data[[name]].dropna())
else:
    st.warning("기업을 하나 이상 선택해주세요.")

