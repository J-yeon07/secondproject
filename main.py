import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="삿포로 관광 가이드", layout="wide")
st.title("🗾 삿포로 관광 가이드")
st.markdown("일본 홋카이도의 중심지, **삿포로**의 주요 관광지를 소개합니다. 지도에서 위치도 함께 확인해보세요!")

# 관광지 데이터 정의
sapporo_spots = [
    {
        "name": "삿포로 TV 타워",
        "location": [43.0619, 141.3543],
        "description": "삿포로 오도리 공원 동쪽 끝에 위치한 전망 타워로, 삿포로 시내를 한눈에 내려다볼 수 있어요."
    },
    {
        "name": "오도리 공원",
        "location": [43.0606, 141.3448],
        "description": "도심을 가로지르는 녹지 공간으로, 계절마다 다양한 축제와 이벤트가 열립니다."
    },
    {
        "name": "홋카이도 대학",
        "location": [43.0718, 141.3400],
        "description": "풍부한 자연과 전통을 자랑하는 일본의 명문 국립대학. 은행나무 길이 유명합니다."
    },
    {
        "name": "삿포로 맥주 박물관",
        "location": [43.0723, 141.3724],
        "description": "일본 최초의 맥주 브랜드인 삿포로 맥주의 역사와 제조 과정을 알 수 있는 곳이에요."
    },
    {
        "name": "스스키노 거리",
        "location": [43.0540, 141.3535],
        "description": "삿포로의 번화가로, 맛집과 바, 쇼핑 장소가 가득해요!"
    },
    {
        "name": "홋카이도 신궁",
        "location": [43.0568, 141.3080],
        "description": "홋카이도의 개척신을 모시는 전통 신사로, 벚꽃 명소로도 유명합니다."
    }
