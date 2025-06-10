import streamlit as st
import folium
import pandas as pd
import json

# 1. 앱 제목 설정
st.set_page_config(layout="wide") # 지도가 넓게 보이도록 설정
st.title("🌎 세계 나라별 탄소배출량 지도")
st.write("엑셀 파일에 직접 입력한 데이터를 바탕으로 국가별 탄소배출량을 시각화합니다.")

# --- 데이터 준비 ---
st.sidebar.header("데이터 업로드")
# CSV와 Excel 파일 모두 업로드 가능하도록 설정
uploaded_file = st.sidebar.file_uploader("탄소배출량 CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx", "xls"])

df_emission = pd.DataFrame() # 기본 빈 데이터프레임 설정

if uploaded_file is not None:
    try:
        # 파일 확장자에 따라 읽는 방식 변경
        if uploaded_file.name.endswith('.csv'):
            df_emission = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df_emission = pd.read_excel(uploaded_file)
        else:
            st.error("지원되지 않는 파일 형식입니다. CSV 또는 Excel 파일을 업로드해주세요.")
            df_emission = pd.DataFrame() # 데이터프레임 초기화

        # 파일이 성공적으로 읽혔다면, 필수 컬럼 존재 여부 확인 및 데이터 처리
        if not df_emission.empty:
            # 당신의 엑셀 파일의 열 이름에 맞게 'country_code'와 'emission_mt'를 수정할 수 있습니다.
            required_cols = ['country_code', 'emission_mt'] 
            
            if not all(col in df_emission.columns for col in required_cols):
                st.error(f"업로드된 파일에 '{required_cols[0]}' 또는 '{required_cols[1]}' 열이 없습니다. 열 이름을 확인해주세요.")
                st.info("예시: 첫 번째 시트의 첫 번째 행에 'country_code', 'emission_mt'라고 입력")
                df_emission = pd.DataFrame() # 데이터프레임 초기화
            else:
                # 'emission_mt' 열이 숫자로 변환 가능한지 확인하고 변환
                df_emission['emission_mt'] = pd.to_numeric(df_emission['emission_mt'], errors='coerce')
                # 숫자로 변환 실패한 행 또는 'country_code'가 없는 행 제거
                df_emission.dropna(subset=['emission_mt', 'country_code'], inplace=True) 

                if df_emission.empty:
                    st.error("업로드된 파일에 유효한 탄소배출량 데이터가 없습니다. 열 내용과 형식을 확인해주세요.")
                else:
                    st.sidebar.success("파일이 성공적으로 업로드되었습니다!")
                    st.subheader("📊 업로드된 탄소배출량 데이터 미리보기")
                    st.dataframe(df_emission.head())
                    st.write(f"총 {len(df_emission)}개 국가의 데이터가 로드되었습니다.")

    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
        st.info("엑셀 파일 형식이 올바른지, 또는 필요한 'openpyxl' 라이브러리가 설치되었는지 확인해주세요.")

else:
    # 파일이 업로드되지 않은 경우 안내 메시지 또는 예시 데이터 사용
    st.info("좌측 사이드바에서 탄소배출량 CSV 또는 Excel 파일을 업로드해주세요. 'country_code'와 'emission_mt' 열이 포함되어야 합니다.")
    
    # 예시 데이터 (파일 업로드 없을 때 기본으로 보여줄 데이터)
    st.subheader("📊 예시 탄소배출량 데이터 (파일 업로드 전)")
    example_emission_data = {
        'country_code': ['USA', 'CHN', 'IND', 'RUS', 'JPN'],
        'emission_mt': [5000, 10000, 2500, 1700, 1000]
    }
    df_emission = pd.DataFrame(example_emission_data)
    st.dataframe(df_emission)
    st.write("_(이 데이터는 예시입니다. 좌측 사이드바에서 당신의 파일을 업로드하세요.)_")


# 2. Folium 지도 생성 함수 (캐싱 적용)
# 이 함수는 이전 코드와 동일하게 유지됩니다.
# 중요한 것은 'df_emission'이 'country_code'와 'emission_mt' 열을 가진 DataFrame이어야 한다는 것입니다.
@st.cache_data
def create_carbon_map(emission_df):
    # 세계 지도 GeoJSON 파일 로드 (로컬 파일 사용)
    try:
        geojson_path = "world-countries.json" 
        with open(geojson_path, 'r', encoding='utf-8') as f:
            country_geo = json.load(f)
            
    except FileNotFoundError:
        st.error(f"GeoJSON 파일 '{geojson_path}'을(를) 찾을 수 없습니다. 파일을 프로젝트 디렉토리에 저장했는지 확인해주세요.")
        return None
    except json.JSONDecodeError:
        st.error(f"GeoJSON 파일 '{geojson_path}'의 내용이 올바른 JSON 형식이 아닙니다. 파일 내용을 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"GeoJSON 데이터를 불러오는 데 실패했습니다: {e}")
        st.info("GeoJSON 파일이 손상되었거나, 다른 문제가 발생했을 수 있습니다.")
        return None

    # Folium 맵 초기화
    m = folium.Map(location=[0, 0], zoom_start=2, tiles="OpenStreetMap")

    # Choropleth 맵 생성
    folium.Choropleth(
        geo_data=country_geo,
        name='탄소배출량',
        data=emission_df,
        columns=['country_code', 'emission_mt'], # 이 열 이름들이 당신의 엑셀 열 이름과 일치해야 합니다.
        key_on='feature.id', # GeoJSON의 id 속성 (ISO A3 코드)
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='연간 탄소배출량 (백만 톤)',
        highlight=True
    ).add_to(m)

    # 툴팁 추가
    style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity':0.1, 'weight':0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity':0.50, 'weight':0.1}
    
    NIL = folium.features.GeoJson(
        country_geo,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'id'], # GeoJSON의 속성 (나라 이름, 코드)
            aliases=['나라', '코드'],
            localize=True
        )
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)

    return m

# 3. 지도 생성 및 Streamlit에 표시
st.subheader("🗺️ 세계 탄소배출량 지도")

# df_emission이 비어 있지 않고 필수 컬럼이 존재할 때만 지도를 생성
if not df_emission.empty and 'country_code' in df_emission.columns and 'emission_mt' in df_emission.columns:
    carbon_map = create_carbon_map(df_emission)

    if carbon_map:
        folium_static_map = st.components.v1.html(carbon_map._repr_html_(), height=500)
    else:
        st.warning("지도를 생성할 수 없습니다. 데이터 또는 GeoJSON 로드에 문제가 있을 수 있습니다.")
else:
    st.info("유효한 탄소배출량 데이터가 없으므로 지도를 표시할 수 없습니다. 파일을 업로드하거나 예시 데이터를 확인해주세요.")

st.info("지도의 색상이 진할수록 탄소배출량이 많음을 나타냅니다.")
