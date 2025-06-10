import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. 앱 제목 설정
st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년)")
st.write("yfinance를 사용하여 주요 기업들의 지난 3년간 주가 변화를 시각화합니다.")

# 2. 글로벌 시총 상위 기업 티커 (변동될 수 있으므로 최신 정보로 업데이트 필요)
# 2024년 6월 기준 대략적인 글로벌 시총 상위 기업들입니다.
# 실제 시총 순위는 실시간으로 변동되므로, 이 리스트는 참고용입니다.
# 티커를 정확히 확인하는 것이 중요합니다.
tickers = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOG",  # Alphabet (Google) - GOOGL도 있지만 GOOG를 대표로 사용
    "AMZN",  # Amazon
    "NVDA",  # NVIDIA
    "META",  # Meta Platforms
    "TSLA",  # Tesla
    "BRK-A", # Berkshire Hathaway (Class A)
    "LLY",   # Eli Lilly and Company
    "JPM",   # JPMorgan Chase & Co.
    "V",     # Visa Inc.
    "JNJ"    # Johnson & Johnson
]

# 3. 날짜 범위 설정 (최근 3년)
end_date = datetime.now()
start_date = end_date - timedelta(days=3 * 365) # 대략 3년 전

st.sidebar.header("설정")
selected_tickers = st.sidebar.multiselect(
    "보고 싶은 기업 선택",
    options=tickers,
    default=tickers # 기본적으로 모든 기업 선택
)

if not selected_tickers:
    st.warning("차트를 표시하려면 최소 하나 이상의 기업을 선택해주세요.")
else:
    # 4. 데이터 다운로드 및 처리
    @st.cache_data
    def get_stock_data(ticker_list, start, end):
        data = yf.download(ticker_list, start=start, end=end)['Adj Close']
        return data

    st.info(f"데이터를 다운로드 중입니다... (시작일: {start_date.strftime('%Y-%m-%d')}, 종료일: {end_date.strftime('%Y-%m-%d')})")
    stock_data = get_stock_data(selected_tickers, start_date, end_date)

    if stock_data.empty:
        st.error("선택한 기간 동안의 주가 데이터를 불러올 수 없습니다. 티커나 날짜 범위를 확인해주세요.")
    else:
        # 데이터가 단일 시리즈로 다운로드될 경우 DataFrame으로 변환
        if isinstance(stock_data, pd.Series):
            stock_data = stock_data.to_frame()

        # 결측치 제거
        stock_data_cleaned = stock_data.dropna()

        if stock_data_cleaned.empty:
            st.error("결측치를 제거한 후 표시할 데이터가 없습니다. 데이터 소스를 확인해주세요.")
        else:
            # 첫날 주가로 나누어 상대적인 변화율 계산 (인덱스를 1로 정규화)
            # 0으로 나누는 오류 방지를 위해, 첫날 주가가 0인 경우를 처리하거나 필터링해야 합니다.
            # 이 예시에서는 단순화를 위해 0이 아닐 것이라고 가정합니다.
            normalized_stock_data = stock_data_cleaned / stock_data_cleaned.iloc[0]

            st.subheader("정규화된 주가 변화 (첫날 기준)")
            st.write("모든 기업의 주가를 첫날 주가에 대한 상대적인 변화율로 정규화하여 비교합니다.")
            st.line_chart(normalized_stock_data)

            st.subheader("원본 데이터 (일별 종가)")
            st.write(stock_data_cleaned.tail()) # 최근 데이터 5개 행 표시
