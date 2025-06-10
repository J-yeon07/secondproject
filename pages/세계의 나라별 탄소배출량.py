import streamlit as st
import folium
import pandas as pd
# geopandas 설치가 가능하다면 이것을 사용해도 좋습니다.
# import geopandas as gpd
import json

# 1. 앱 제목 설정
st.set_page_config(layout="wide") # 지도가 넓게 보이도록 설정
st.title("🌎 세계 나라별 탄소배출량 지도 (Folium)")
st.write("Folium을 이용하여 국가별 탄소배출량을 시각화합니다.")

# --- 데이터 준비 ---
# 실제 탄소배출량 데이터를 사용하려면 이 부분을 수정해야 합니다.
# 여기서는 예시를 위해 더미 데이터를 생성합니다.
# 실제 데이터는 CSV 파일이나 다른 데이터 소스에서 로드할 수 있습니다.

# 예시: 더미 탄소배출량 데이터 생성
# 국가 코드 (ISO A3 코드)와 탄소배출량 (단위: 백만 톤)
emission_data = {
    'country_code': ['USA', 'CHN', 'IND', 'RUS', 'JPN', 'DEU', 'GBR', 'CAN', 'KOR', 'BRA', 'AUS'],
    'emission_mt': [5000, 10000, 2500, 1700, 1000, 700, 400, 550, 600, 450, 400]
}
df_emission = pd.DataFrame(emission_data)

st.subheader("📊 탄소배출량 데이터 미리보기")
st.dataframe(df_emission)
st.write("_(탄소배출량 데이터는 예시이며, 실제 데이터로 대체할 수 있습니다.)_")


# 2. Folium 지도 생성 함수 (캐싱 적용)
@st.cache_data
def create_carbon_map(emission_df):
    # 세계 지도 GeoJSON 파일 로드
    # Folium 예시 데이터셋에서 직접 가져오거나 로컬 파일 사용
    try:
        # Folium example data에 포함된 world-countries.json 사용
        # 인터넷 연결 필요
        country_geo = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/countries_json/world-countries.json"
        
        # 또는 로컬 파일 사용 (다운로드 후 주석 해제)
        # with open('world-countries.json', 'r', encoding='utf-8') as f:
        #     country_geo = json.load(f)

    except Exception as e:
        st.error(f"GeoJSON 데이터를 불러오는 데 실패했습니다: {e}")
        st.info("인터넷 연결을 확인하거나, 'world-countries.json' 파일을 로컬에 다운로드하여 사용해 보세요.")
        return None

    # Folium 맵 초기화 (세계 중심, 확대 레벨)
    m = folium.Map(location=[0, 0], zoom_start=2, tiles="OpenStreetMap")

    # Choropleth 맵 생성
    folium.Choropleth(
        geo_data=country_geo, # 국가 경계 GeoJSON 데이터
        name='탄소배출량',
        data=emission_df, # 탄소배출량 데이터프레임
        columns=['country_code', 'emission_mt'], # 데이터프레임에서 사용할 컬럼
        key_on='feature.id', # GeoJSON 데이터와 데이터프레임을 연결할 키 (GeoJSON의 id 속성)
        fill_color='YlGnBu', # 색상 스케일 (Yellow-Green-Blue)
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='연간 탄소배출량 (백만 톤)',
        highlight=True # 마우스 오버 시 하이라이트 효과
    ).add_to(m)

    # 툴팁 추가 (각 국가에 마우스를 올렸을 때 정보 표시)
    style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity':0.1, 'weight':0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity':0.50, 'weight':0.1}
    
    NIL = folium.features.GeoJson(
        country_geo,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'id'], # GeoJSON의 속성
            aliases=['나라', '코드'], # 툴팁에 표시될 이름
            localize=True
        )
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)

    return m

# 3. 지도 생성 및 Streamlit에 표시
st.subheader("🗺️ 세계 탄소배출량 지도")

# Folium 지도를 생성합니다.
carbon_map = create_carbon_map(df_emission)

if carbon_map:
    # Streamlit에 Folium 지도를 표시
    # height 파라미터로 지도의 높이를 조절할 수 있습니다.
    folium_static_map = st.components.v1.html(carbon_map._repr_html_(), height=500)
else:
    st.warning("지도를 생성할 수 없습니다. GeoJSON 데이터 로드에 문제가 있을 수 있습니다.")

st.info("지도의 색상이 진할수록 탄소배출량이 많음을 나타냅니다.")
