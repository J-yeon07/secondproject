import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. 앱 제목 설정
st.title("글로벌 시가총액 Top 10 기업 주가 변화 (최근 3년)")
st.write("yfinance를 사용하여 주요 기업들의 지난 3년간 주가 변화를 시각화합니다.")

# 2. 글로벌 시총 상위 기업 티커 (변동될 수 있으므로 최신 정보로 업데이트 필요)
tickers = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOG",  # Alphabet (Google)
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
        all_adj_close_data = pd.DataFrame()
        failed_tickers = []

        for ticker in ticker_list:
            try:
                # 각 티커별로 개별적으로 다운로드 시도
                # 이렇게 하면 한 티커의 실패가 전체 다운로드를 망가뜨리지 않습니다.
                stock = yf.Ticker(ticker)
                # period='3y'를 사용하면 정확히 3년 데이터를 가져올 수 있고,
                # start/end 날짜를 사용해도 됩니다.
                # data = stock.history(start=start, end=end)
                data = stock.history(period="3y") # 최근 3년 데이터 요청

                if not data.empty and 'Adj Close' in data.columns:
                    # 'Adj Close' 컬럼만 선택하여 DataFrame에 추가
                    adj_close = data[['Adj Close']].rename(columns={'Adj Close': ticker})
                    # 인덱스(날짜)를 기준으로 병합
                    if all_adj_close_data.empty:
                        all_adj_close_data = adj_close
                    else:
                        all_adj_close_data = all_adj_close_data.join(adj_close, how='outer')
                else:
                    st.warning(f"티커 '{ticker}'에 대한 'Adj Close' 데이터를 찾을 수 없거나 데이터가 비어 있습니다. 기간: {start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')}")
                    failed_tickers.append(ticker)
            except Exception as e:
                st.error(f"티커 '{ticker}' 데이터 다운로드 중 오류 발생: {e}")
                failed_tickers.append(ticker)
        
        if failed_tickers:
            st.error(f"다음 티커들은 데이터를 가져오지 못했습니다: {', '.join(failed_tickers)}")
            st.info("티커 심볼이 정확한지, 그리고 해당 기업이 지정된 기간 동안 주식 시장에 있었는지 확인해주세요.")

        return all_adj_close_data.sort_index() # 날짜를 기준으로 정렬

    st.info(f"데이터를 다운로드 중입니다... (시작일: {start_date.strftime('%Y-%m-%d')}, 종료일: {end_date.strftime('%Y-%m-%d')})")
    stock_data = get_stock_data(selected_tickers, start_date, end_date)

    if stock_data.empty:
        st.error("선택한 모든 기업에 대해 유효한 주가 데이터를 불러올 수 없습니다. 티커나 날짜 범위를 다시 확인해주세요.")
    else:
        # 결측치 제거
        # join 방식이 outer이므로, 데이터가 없는 날짜에 NaN이 있을 수 있습니다.
        # 차트 생성을 위해 NaN을 제거하는 것이 좋습니다.
        stock_data_cleaned = stock_data.dropna()

        if stock_data_cleaned.empty:
            st.warning("결측치를 제거한 후 표시할 데이터가 없습니다. 모든 기업의 데이터가 특정 날짜에 완전히 일치하는지 확인해주세요.")
            st.write("--- 원본 데이터 (결측치 포함) ---")
            st.write(stock_data.head()) # 결측치 포함된 원본 데이터 일부 출력
            st.write(stock_data.isnull().sum()) # 각 컬럼별 결측치 개수 출력
        else:
            # 첫날 주가로 나누어 상대적인 변화율 계산 (인덱스를 1로 정규화)
            # 0으로 나누는 오류 방지를 위해, 첫날 주가가 0이 아닌 컬럼만 처리
            normalized_stock_data = pd.DataFrame()
            for col in stock_data_cleaned.columns:
                if stock_data_cleaned[col].iloc[0] != 0:
                    normalized_stock_data[col] = stock_data_cleaned[col] / stock_data_cleaned[col].iloc[0]
                else:
                    st.warning(f"티커 '{col}'의 첫날 주가가 0이므로 정규화할 수 없습니다.")
                    normalized_stock_data[col] = stock_data_cleaned[col] # 정규화하지 않고 원본 값 사용

            if normalized_stock_data.empty:
                 st.error("정규화된 주가 데이터를 생성할 수 없습니다.")
            else:
                st.subheader("정규화된 주가 변화 (첫날 기준)")
                st.write("모든 기업의 주가를 첫날 주가에 대한 상대적인 변화율로 정규화하여 비교합니다.")
                st.line_chart(normalized_stock_data)

            st.subheader("원본 데이터 (일별 종가)")
            st.write(stock_data_cleaned.tail()) # 최근 데이터 5개 행 표시
