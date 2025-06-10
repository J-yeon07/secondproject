import streamlit as st
import folium
from folium.plugins import MarkerCluster
import pandas as pd

# 페이지 설정
st.set_page_config(layout="wide", page_title="삿포로 관광 가이드")

st.title("🌸 삿포로 주요 관광지 가이드 🌸")
st.write("안녕하세요! 아름다운 삿포로 여행을 위한 친절하고 자세한 가이드에 오신 것을 환영합니다. 스트림릿과 폴리움으로 삿포로의 매력을 함께 탐험해볼까요?")

st.image("https://visit.sapporo.travel/ko/wp-content/uploads/2021/04/main_img.jpg", caption="삿포로의 아름다운 풍경 (출처: Visit Sapporo)", use_column_width=True)

st.header("🗺️ 삿포로 주요 관광지 지도")
st.write("아래 지도에서 삿포로의 주요 관광지들을 한눈에 확인해보세요! 각 마커를 클릭하면 간단한 정보를 볼 수 있습니다.")

# 삿포로 중심 좌표
sapporo_coords = [43.0642, 141.3469]

# 관광지 데이터 (Visit Sapporo 이미지 링크로 업데이트)
tourist_spots = [
    {"name": "오도리 공원", "lat": 43.0630, "lon": 141.3537,
     "description": "삿포로 시내 중심을 가로지르는 아름다운 공원입니다. 사계절 내내 다양한 행사와 축제가 열립니다. 삿포로 눈 축제, 라일락 축제 등.",
     "image_url": "https://www.sapporo.travel/cms/wp-content/uploads/2020/10/f_odoripark_01main-1200x600-1.jpg"},
    {"name": "삿포로 TV 타워", "lat": 43.0614, "lon": 141.3571,
     "description": "오도리 공원 동쪽 끝에 위치한 삿포로의 랜드마크입니다. 전망대에서 삿포로 시내를 한눈에 조망할 수 있습니다.",
     "image_url": "https://visit.sapporo.travel/ko/wp-content/uploads/sites/8/2022/09/spot_tvtower-2.jpg"},
    {"name": "삿포로 시계탑", "lat": 43.0634, "lon": 141.3524,
     "description": "삿포로의 상징적인 건축물로, 1878년에 지어진 유서 깊은 건물입니다. 붉은 지붕과 흰 벽이 인상적입니다.",
     "image_url": "https://www.sapporo.travel/cms/wp-content/uploads/2020/10/tokeidaiMV_slide1.jpg"},
    {"name": "삿포로 맥주 박물관", "lat": 43.0766, "lon": 141.3725,
     "description": "일본에서 가장 오래된 맥주 브랜드 중 하나인 삿포로 맥주의 역사와 양조 과정을 배울 수 있는 곳입니다. 시음도 가능합니다.",
     "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSln3-HKLIdCvKLkXf2T8X1sgnAg88lLQx-UQ&s"},
    {"name": "홋카이도 구 본청사 (아카렌가 청사)", "lat": 43.0620, "lon": 141.3510,
     "description": "붉은 벽돌로 지어진 아름다운 건물로, 홋카이도 개척 시대의 상징입니다. 내부에는 박물관과 자료실이 있습니다.",
     "image_url": "https://www.sapporo.travel/cms/wp-content/uploads/2020/10/c005-012.jpg"},
    {"name": "삿포로 팩토리", "lat": 43.0664, "lon": 141.3659,
     "description": "옛 삿포로 맥주 공장 부지에 조성된 복합 쇼핑몰입니다. 쇼핑, 레스토랑, 영화관 등 다양한 시설이 있습니다.",
     "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxE4zcrCrB2Nlo2Q74D5AGNwXF-_wBPDnPIg&s"},
    {"name": "모이와 산 (모이와야마)", "lat": 43.0298, "lon": 141.3283,
     "description": "삿포로 야경을 감상하기 좋은 명소입니다. 로프웨이를 타고 정상에 오르면 아름다운 삿포로의 파노라마 야경을 볼 수 있습니다.",
     "image_url": "https://www.sapporo.travel/cms/wp-content/uploads/2020/10/moiwa-yakei-1200x600-1.jpg"},
    {"name": "시로이 코이비토 파크", "lat": 43.0858, "lon": 141.2828,
     "description": "홋카이도의 유명한 과자 '시로이 코이비토'를 테마로 한 테마파크입니다. 과자 만들기 체험, 정원, 카페 등이 있습니다.",
     "image_url": "https://media.triple.guide/triple-cms/c_limit,f_auto,h_1024,w_1024/b723950c-e152-4bd9-8561-ae17a550dbc5.jpeg"},
    {"name": "스스키노", "lat": 43.0563, "lon": 141.3524,
     "description": "삿포로 최대의 번화가이자 유흥가입니다. 다양한 레스토랑, 바, 상점들이 밀집해 있으며 밤에는 화려한 네온사인으로 빛납니다.",
     "image_url": "https://www.visit-hokkaido.jp/lsc/upfile/spot/0001/0009/10009_1_l.jpg"}
]

# Folium 지도 생성
m = folium.Map(location=sapporo_coords, zoom_start=12, tiles="cartodbpositron")

# 마커 클러스터 추가 (마커가 많을 경우 유용)
marker_cluster = MarkerCluster().add_to(m)

# 관광지 마커 추가
for spot in tourist_spots:
    html = f"""
    <h4>{spot['name']}</h4>
    <img src="{spot['image_url']}" alt="{spot['name']}" style="width:150px;height:auto;"><br>
    <p>{spot['description']}</p>
    """
    iframe = folium.IFrame(html, width=200, height=250)
    popup = folium.Popup(iframe, max_width=260)
    folium.Marker(
        location=[spot['lat'], spot['lon']],
        popup=popup,
        tooltip=spot['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(marker_cluster)

# 지도를 HTML로 저장 후 Streamlit에 표시
st.components.v1.html(folium.Figure().add_child(m).render(), height=500)

# --- (이 줄이 76번 줄 근처일 가능성이 높습니다) ---
st.markdown("---") # 76번째 줄 또는 그 주변일 수 있습니다.

st.header("🌟 주요 관광지 상세 가이드")

# 각 관광지에 대한 상세 정보 섹션
for i, spot in enumerate(tourist_spots):
    st.subheader(f"{i+1}. {spot['name']}")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(spot['image_url'], caption=spot['name'], width=250)
    with col2:
        st.write(f"**📍 위치:** 위도 {spot['lat']}, 경도 {spot['lon']}")
        st.write(f"**📝 설명:** {spot['description']}")
        st.write("더 자세한 정보를 원하시면 해당 장소의 공식 웹사이트나 여행 가이드를 참고해주세요!")
    st.markdown("---")

# --- (새로 추가된 유튜브 브이로그 섹션 시작) ---
st.header("🎬 삿포로 여행 브이로그 (조회수 높은 순)")
st.write("삿포로 여행의 생생함을 느껴보고 싶다면, 인기 유튜브 브이로그를 통해 미리 경험해보세요! 썸네일을 클릭하면 영상으로 이동합니다.")

# 조회수 높은 삿포로 여행 브이로그 (예시)
# 실제 조회수 기준이 아닐 수 있으니, 필요시 최신 정보로 업데이트해주세요.
# 중요: 아래 YOUR_VIDEO_ID_X와 YOUR_YOUTUBE_URL_X, YOUR_THUMBNAIL_URL_X를 실제 값으로 반드시 교체해야 합니다.
# YouTube 썸네일 URL은 일반적으로 다음 패턴을 따릅니다:
# https://img.youtube.com/vi/[VIDEO_ID]/maxresdefault.jpg (고해상도, 없을 수 있음)
# https://img.youtube.com/vi/[VIDEO_ID]/sddefault.jpg (표준 해상도)
# https://img.youtube.com/vi/[VIDEO_ID]/hqdefault.jpg (고품질)
# https://img.youtube.com/vi/[VIDEO_ID]/mqdefault.jpg (중간 품질)
# https://img.youtube.com/vi/[VIDEO_ID]/default.jpg (기본)
# 대부분의 경우 mqdefault.jpg나 hqdefault.jpg가 안정적으로 작동합니다.
youtube_vlogs = [
    {
        "title": "삿포로 혼자 여행 vlog 🇯🇵 역시 겨울 여행은 삿포로지❄️ 오타루, 르타오 디저트, 오르골당, 스프카레, 헌터 단톤 쇼핑, 스스키노 가성비 숙소 | EP.1",
        "video_id": "YfcBGt_fbF8?si=ypFPcGM0kwWlwFM7", # 실제 유튜브 영상 ID로 교체 (예시)
        "thumbnail_url": "https://img.youtube.com/vi/YfcBGt_fbF8?si=ypFPcGM0kwWlwFM7/sdddefault.jpg", # 위 video_id 기반
        "youtube_url": "https://youtu.be/YfcBGt_fbF8?si=ypFPcGM0kwWlwFM7" # 위 video_id 기반
    },
    {
        "title": "홋카이도여행 여길 안 가봤다고?(가장 인기 있는 코스 3박 4일 일정, 삿포로, 오타루, 비에이편)",
        "video_id": "ml1rIL1Xkyc?si=Rs4LMcuUHbXKEVcG", 
        "thumbnail_url": "https://img.youtube.com/vi/ml1rIL1Xkyc?si=Rs4LMcuUHbXKEVcG/sddefault.jpg", # 위 video_id 기반
        "youtube_url": "https://youtu.be/ml1rIL1Xkyc?si=Rs4LMcuUHbXKEVcG" # 위 video_id 기반
    },
    {
        "title": ☀올여름 무조건 가야하는 삿포로 3박4일 여행코스 완벽정리💯(+경비,꿀팁까지⁉️)",
        "video_id": "2fG60iqVrDA?si=tKw_WRgO3bIV94wR", # 실제 유튜브 영상 ID로 교체 (예시)
        "thumbnail_url": "https://img.youtube.com/vi/2fG60iqVrDA?si=tKw_WRgO3bIV94wR/sddefault.jpg", # 위 video_id 기반
        "youtube_url": "https://youtu.be/2fG60iqVrDA?si=tKw_WRgO3bIV94wR" # 위 video_id 기반
    }
]

# 유튜브 브이로그 표시
for vlog in youtube_vlogs:
    st.subheader(vlog['title'])
    st.markdown(f"""
    <a href="{vlog['youtube_url']}" target="_blank">
        <img src="{vlog['thumbnail_url']}" alt="{vlog['title']}" style="width:300px; border-radius: 8px;">
    </a>
    """, unsafe_allow_html=True)
    st.write(f"[영상 보러가기]({vlog['youtube_url']})")
    st.markdown("---")

# --- (유튜브 브이로그 섹션 끝) ---

st.header("🍜 삿포로에서 꼭 맛봐야 할 음식")
st.write("삿포로는 맛있는 음식으로도 유명하죠! 삿포로에 오시면 꼭 드셔보세요.")
st.markdown("""
* **삿포로 미소 라멘:** 삿포로를 대표하는 음식 중 하나입니다. 진한 된장 육수에 쫄깃한 면발이 일품입니다.
* **징기스칸:** 양고기를 구워 먹는 홋카이도 향토 음식입니다. 특제 소스에 찍어 먹으면 잡내 없이 고소합니다.
* **스프 카레:** 다양한 토핑이 들어간 스프 형태의 카레입니다. 따뜻한 국물과 신선한 재료의 조화가 좋습니다.
* **해산물 요리:** 신선한 해산물이 풍부한 홋카이도인 만큼, 신선한 초밥, 회덮밥 등 다양한 해산물 요리를 즐길 수 있습니다.
* **삿포로 맥주:** 삿포로에서 생산되는 유명한 맥주입니다. 맥주 박물관에서 시음도 가능합니다.
""")

st.header("🛍️ 삿포로 쇼핑 추천")
st.write("여행의 즐거움 중 하나는 쇼핑이죠! 삿포로에서 기념품이나 쇼핑을 즐겨보세요.")
st.markdown("""
* **다누키코지 상점가:** 삿포로에서 가장 오래된 상점가 중 하나로, 다양한 상점과 식당들이 밀집해 있습니다.
* **삿포로 역 주변:** JR 삿포로 역을 중심으로 백화점, 쇼핑몰 등이 많이 있습니다.
* **오도리 공원 지하상가 (오로라 타운, 폴 타운):** 날씨에 상관없이 쾌적하게 쇼핑을 즐길 수 있는 지하상가입니다.
* **시로이 코이비토 파크:** 시로이 코이비토 과자 및 다양한 기념품을 구매할 수 있습니다.
""")

st.header("🗓️ 삿포로 여행 팁")
st.markdown("""
* **교통:** 삿포로 시내는 지하철과 버스, 노면 전차로 편리하게 이동할 수 있습니다. JR 삿포로 역을 중심으로 주요 관광지로의 접근성이 좋습니다.
* **날씨:** 삿포로는 겨울에 눈이 많이 오고 매우 춥습니다. 여름은 비교적 시원하지만 일교차가 있을 수 있습니다. 방문 시기에 맞춰 옷차림을 준비하세요.
* **삿포로 눈 축제:** 매년 2월 초에 열리는 삿포로 눈 축제는 세계적으로 유명하니, 이 시기에 방문하시면 특별한 경험을 할 수 있습니다. (숙소 예약 필수!)
* **홋카이도 프리패스:** 홋카이도 전체를 여행할 계획이라면 JR 홋카이도에서 제공하는 프리패스를 고려해보세요.
""")

st.markdown("---")
st.write("이 가이드가 삿포로 여행에 도움이 되셨기를 바랍니다! 즐겁고 행복한 삿포로 여행 되세요! 🌸")
