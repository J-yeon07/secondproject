import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network # 인터랙티브 그래프를 위해 pyvis 사용 권장

st.set_page_config(layout="wide")

st.title("중학교 학생 관계 시각화 맵")

# --- 1. 학생 이름 선택 (자신의 번호) ---
st.header("1. 당신은 몇 번 학생입니까?")
student_id = st.selectbox("자신의 학생 번호를 선택하세요:", options=range(1, 30))
st.write(f"당신은 {student_id}번 학생입니다.")

# --- 2. 설문 질문 ---
st.header("2. 친구 관계 설문")

# 질문 1: 수련회 방 (3명 선택)
st.subheader("질문 1. 수련회에서 4명이 함께 방을 사용해야 한다면 누구와 함께 방을 사용하고 싶니? (3명 선택)")
room_friends_options = [f"학생 {i}" for i in range(1, 30) if i != student_id]
room_friends = st.multiselect("3명의 친구를 선택하세요:", options=room_friends_options, max_selections=3)
room_friends_ids = [int(s.split(' ')[1]) for s in room_friends]

# 질문 2: 교실 짝 (1명 선택)
st.subheader("질문 2. 교실에서 짝이 되고 싶은 학생이 누구니? (1명 선택)")
pair_friend_options = [f"학생 {i}" for i in range(1, 30) if i != student_id]
pair_friend = st.selectbox("1명의 친구를 선택하세요:", options=pair_friend_options)
pair_friend_id = int(pair_friend.split(' ')[1]) if pair_friend else None

# 질문 3: 대화 상대 (모두 선택)
st.subheader("질문 3. 최근 3일간 누구와 대화를 나누었니? (모두 선택)")
talk_friends_options = [f"학생 {i}" for i in range(1, 30) if i != student_id]
talk_friends = st.multiselect("대화 나눈 친구를 모두 선택하세요:", options=talk_friends_options)
talk_friends_ids = [int(s.split(' ')[1]) for s in talk_friends]

# --- 3. 데이터 저장 및 처리 (예시: 실제로는 DB 또는 파일에 저장) ---
# 여기서는 간단히 세션 상태에 저장하여 시각화에 사용
if 'responses' not in st.session_state:
    st.session_state.responses = []

if st.button("응답 제출"):
    st.session_state.responses.append({
        'student_id': student_id,
        'room_friends': room_friends_ids,
        'pair_friend': pair_friend_id,
        'talk_friends': talk_friends_ids
    })
    st.success(f"{student_id}번 학생의 응답이 제출되었습니다!")

# --- 4. 관계 맵 시각화 ---
st.header("3. 학생 관계 시각화 맵")

if st.session_state.responses:
    G = nx.Graph()

    # 모든 학생 노드 추가 (29명)
    for i in range(1, 30):
        G.add_node(i)

    # 엣지 추가 및 가중치/속성 부여
    for response in st.session_state.responses:
        current_student = response['student_id']

        # 질문 1: 친밀한 관계
        for friend in response['room_friends']:
            G.add_edge(current_student, friend, type='친밀', weight=2, color='skyblue', width=2) # width는 pyvis에서 사용

        # 질문 2: 가장 친밀한 관계
        if response['pair_friend']:
            G.add_edge(current_student, response['pair_friend'], type='가장_친밀', weight=3, color='red', width=4)

        # 질문 3: 약간 친밀한 관계
        for friend in response['talk_friends']:
            # 중복 엣지 방지 (이미 더 강한 관계가 있다면 추가하지 않음)
            if not G.has_edge(current_student, friend) or G[current_student][friend].get('type') not in ['가장_친밀', '친밀']:
                G.add_edge(current_student, friend, type='약간_친밀', weight=1, color='lightgray', width=1)


    # Pyvis를 이용한 인터랙티브 그래프
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True)
    net.toggle_physics(True) # 노드 간의 물리적 힘 적용

    for node in G.nodes():
        net.add_node(node, label=str(node), title=f"학생 {node}")

    for edge in G.edges(data=True):
        source, target, data = edge
        net.add_edge(source, target, title=data['type'], color=data['color'], width=data['width'])

    # HTML 파일로 저장하고 Streamlit에 임베드
    net.save_graph("student_relationships.html")
    with open("student_relationships.html", 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=800, scrolling=True)

    st.write("---")
    st.write("**관계 맵 설명:**")
    st.write("- **빨간색 굵은 선:** 가장 친밀한 관계 (짝이 되고 싶은 학생)")
    st.write("- **하늘색 보통 선:** 친밀한 관계 (수련회 방 친구)")
    st.write("- **회색 얇은 선:** 약간 친밀한 관계 (대화 나눈 친구)")

else:
    st.info("학생들이 설문 응답을 제출하면 관계 맵이 여기에 표시됩니다.")

st.markdown("---")
st.markdown("### 개발 노트:")
st.markdown("- **데이터 저장:** 실제 운영 환경에서는 `st.session_state` 대신 데이터베이스 (예: SQLite, PostgreSQL) 또는 CSV/JSON 파일에 응답을 저장하고 불러오는 로직이 필요합니다.")
st.markdown("- **그래프 레이아웃:** `pyvis`는 자체적인 레이아웃 엔진을 가지고 있어 노드들이 서로 잘 보이도록 자동으로 배치됩니다. `networkx`를 `matplotlib`과 함께 사용할 경우 `nx.spring_layout`, `nx.circular_layout` 등을 사용하여 노드 위치를 조정할 수 있습니다.")
st.markdown("- **사용자 경험:** 여러 학생이 동시에 접근하여 응답을 제출할 수 있도록 하려면 데이터 저장 방식을 더욱 견고하게 구현해야 합니다.")
st.markdown("- **학생별 맵 보기:** 특정 학생이 선택한 관계만 보고 싶다면, 필터링 기능을 추가하여 해당 학생이 선택한 엣지만 강조하거나 보여줄 수 있습니다.")
