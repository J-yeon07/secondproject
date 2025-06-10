import streamlit as st
import pandas as pd
import plotly.express as px
import os # 파일 경로 확인 및 임시 CSV 파일 저장에 사용 (선택 사항)

st.set_page_config(layout="wide") # 페이지 전체 너비 사용

st.title('세계 주요국의 연도별 탄소배출량 추이')

# --- 엑셀 파일 업로드 섹션 ---
st.header("1. 엑셀 파일 업로드")
uploaded_file = st.file_uploader("탄소배출량 데이터 엑셀 파일을 업로드해주세요.", type=['xlsx', 'xls'])

df = pd.DataFrame() # 기본적으로 빈 데이터프레임 초기화

if uploaded_file is not None:
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(uploaded_file)

        # 필요한 컬럼이 있는지 확인
        required_columns = ['연도', '나라', '탄소배출량']
        if not all(col in df.columns for col in required_columns):
            st.error(f"업로드된 파일에 '{', '.join(required_columns)}' 컬럼이 모두 포함되어야 합니다.")
            df = pd.DataFrame() # 컬럼이 없으면 데이터프레임을 비웁니다.
        else:
            st.success("파일이 성공적으로 업로드되었습니다!")
            st.dataframe(df.head()) # 데이터 미리보기
            st.info("그래프를 생성하려면 아래 옵션들을 조정해주세요.")

    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
        st.warning("파일 형식이 올바른 엑셀(.xlsx 또는 .xls)인지 확인해주세요.")
else:
    st.info("아직 파일이 업로드되지 않았습니다. 엑셀 파일을 업로드해주세요.")
    # 파일이 없을 때 기본적으로 보여줄 예시 데이터를 추가할 수도 있습니다.
    # 하지만 여기서는 파일 업로드를 필수로 가정합니다.

# --- 그래프 생성 섹션 ---
st.header("2. 그래프 생성 옵션")

if not df.empty:
    # 연도 범위 슬라이더
    min_year, max_year = int(df['연도'].min()), int(df['연도'].max())
    year_range = st.slider(
        '연도 범위를 선택하세요:',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year) # 기본값: 전체 연도
    )

    # 나라 다중 선택
    all_countries = sorted(df['나라'].unique())
    # 기본 선택 나라 설정: 데이터셋의 첫 5개 나라 또는 전체가 5개 미만이면 모두 선택
    default_countries_selection = all_countries[:min(5, len(all_countries))]

    selected_countries = st.multiselect(
        '데이터를 보고 싶은 나라를 선택하세요:',
        options=all_countries,
        default=default_countries_selection # 기본적으로 상위 5개 나라 선택
    )

    # 선택된 조건에 따라 데이터 필터링
    filtered_df = df[
        (df['연도'] >= year_range[0]) &
        (df['연도'] <= year_range[1]) &
        (df['나라'].isin(selected_countries))
    ]

    if not filtered_df.empty:
        # Plotly Express를 이용한 선 그래프 생성
        fig = px.line(
            filtered_df,
            x='연도',
            y='탄소배출량',
            color='나라',
            title=f'선택된 나라들의 연도별 탄소배출량 ({year_range[0]} - {year_range[1]})',
            labels={'탄소배출량': '탄소배출량', '연도': '연도'},
            hover_data={'탄소배출량': ':.2f'}
        )

        # 레이아웃 개선
        fig.update_layout(
            xaxis_title="연도",
            yaxis_title="탄소배출량",
            legend_title="나라",
            hovermode="x unified"
        )
        fig.update_xaxes(tickformat=".0f")

        # 스트림릿에 그래프 표시
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택하신 조건에 해당하는 데이터가 없습니다. 다른 나라나 연도를 선택해보세요.")

    st.markdown("---")
    st.subheader("원본 데이터 미리보기")
    st.dataframe(df)
else:
    st.info("그래프를 생성하려면 먼저 엑셀 파일을 업로드해주세요.")import streamlit as st
import pandas as pd
import plotly.express as px
import os # 파일 경로 확인을 위해 추가

st.set_page_config(layout="wide") # 페이지 전체 너비 사용

st.title('세계 주요국의 연도별 탄소배출량 추이')

# 데이터 파일 경로 설정
DATA_FILE = 'carbon_emissions.csv'

# 데이터 로드 함수 (캐싱을 사용하여 앱 성능 최적화)
@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"오류: 데이터 파일 '{file_path}'를 찾을 수 없습니다. "
                 "스크립트와 같은 디렉토리에 파일을 놓거나 경로를 확인해주세요.")
        # 예시 데이터를 반환하여 앱이 바로 죽지 않도록 합니다.
        st.info("임시 예시 데이터를 로드합니다. 실제 데이터를 넣어주세요!")
        example_data = {
            '연도': [1990, 1990, 1990, 2000, 2000, 2000, 2010, 2010, 2010, 2020, 2020, 2020],
            '나라': ['한국', '미국', '중국', '한국', '미국', '중국', '한국', '미국', '중국', '한국', '미국', '중국'],
            '탄소배출량': [250, 4800, 2000, 400, 5000, 4500, 600, 5200, 8000, 650, 5300, 10000]
        }
        return pd.DataFrame(example_data)
    try:
        df = pd.read_csv(file_path)
        # 데이터프레임 컬럼명 확인 및 정제 (필요시)
        # 예: df.columns = ['연도', '나라', '탄소배출량']
        if not all(col in df.columns for col in ['연도', '나라', '탄소배출량']):
            st.error("CSV 파일에 '연도', '나라', '탄소배출량' 컬럼이 모두 포함되어야 합니다.")
            return pd.DataFrame() # 빈 데이터프레임 반환
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()

df = load_data(DATA_FILE)

if not df.empty:
    # 연도 범위 슬라이더
    min_year, max_year = int(df['연도'].min()), int(df['연도'].max())
    year_range = st.slider(
        '연도 범위를 선택하세요:',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # 나라 다중 선택
    all_countries = sorted(df['나라'].unique())
    selected_countries = st.multiselect(
        '데이터를 보고 싶은 나라를 선택하세요:',
        options=all_countries,
        default=all_countries[0:5] # 기본적으로 상위 5개 나라 선택 (또는 임의의 초기값)
    )

    # 선택된 조건에 따라 데이터 필터링
    filtered_df = df[
        (df['연도'] >= year_range[0]) &
        (df['연도'] <= year_range[1]) &
        (df['나라'].isin(selected_countries))
    ]

    if not filtered_df.empty:
        # Plotly Express를 이용한 선 그래프 생성
        # x축: 연도, y축: 탄소배출량, color: 나라 (나라별로 다른 색상)
        fig = px.line(
            filtered_df,
            x='연도',
            y='탄소배출량',
            color='나라',
            title=f'선택된 나라들의 연도별 탄소배출량 ({year_range[0]} - {year_range[1]})',
            labels={'탄소배출량': '탄소배출량', '연도': '연도'},
            hover_data={'탄소배출량': ':.2f'} # 툴팁에 소수점 2자리까지 표시
        )

        # 레이아웃 개선
        fig.update_layout(
            xaxis_title="연도",
            yaxis_title="탄소배출량",
            legend_title="나라",
            hovermode="x unified" # 마우스 오버 시 모든 선의 정보를 한 번에 표시
        )
        fig.update_xaxes(tickformat=".0f") # 연도 레이블을 정수로 표시

        # 스트림릿에 그래프 표시
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택하신 조건에 해당하는 데이터가 없습니다. 다른 나라나 연도를 선택해보세요.")

    st.markdown("---")
    st.subheader("데이터 미리보기")
    st.dataframe(df) # 원본 데이터 전체를 보여줍니다.
else:
    st.info("데이터 로드에 실패했거나 데이터가 비어 있습니다. CSV 파일을 확인해주세요.")
