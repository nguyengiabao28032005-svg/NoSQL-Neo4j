import streamlit as st
from neo4j import GraphDatabase
import streamlit.components.v1 as components
from pyvis.network import Network
import tempfile
import os

# Cấu hình kết nối trực tiếp Neo4j
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")  

@st.cache_resource
def get_neo4j_driver():
    """Hàm cache driver kết nối giúp tối ưu hiệu năng"""
    return GraphDatabase.driver(URI, auth=AUTH)

def run_query(query, parameters=None):
    """Hàm thực thi câu lệnh Cypher trực tiếp qua driver đã cache"""
    try:
        driver = get_neo4j_driver()
        with driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]
    except Exception as e:
        return []

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Hệ thống Tri thức Hình học 2D", page_icon="📐", layout="wide")

st.title("📐 Hệ thống Tri thức Hình học Tứ giác 2D (Neo4j)")
st.write("Tra cứu tính chất, dấu hiệu nhận biết, công thức toán học và biểu diễn đồ thị mạng lưới tri thức.")

# Cache danh sách tên các hình để load cực nhanh
@st.cache_data
def get_shape_names():
    res = run_query("MATCH (s:Shape) RETURN s.ten AS ten ORDER BY s.ten")
    return [item["ten"] for item in res] if res else []

shape_names = get_shape_names()

# Cache dữ liệu đồ thị bản đồ
@st.cache_data
def get_graph_data():
    nodes_res = run_query("MATCH (s:Shape) RETURN s.ten AS ten")
    edges_res = run_query("MATCH (s:Shape)-[r:TRO_THANH]->(t:Shape) RETURN s.ten AS source, t.ten AS target, r.dieu_kien AS label")
    return nodes_res, edges_res

# Cache dữ liệu toàn bộ thẻ flashcard
@st.cache_data
def get_all_flashcards():
    return run_query("MATCH (s:Shape) RETURN s.ten AS ten, s.nhan_biet AS nhan_biet, s.tinh_chat AS tinh_chat, s.chu_vi AS chu_vi, s.dien_tich AS dien_tich")

if shape_names:
    st.sidebar.success("🟢 Kết nối Neo4j thành công!")
    st.sidebar.header("🔍 Điều hướng hệ thống")
    
    menu_mode = st.sidebar.radio(
        "Chọn chức năng:", 
        [
            "Tra cứu chi tiết hình", 
            "Tìm đường đi chuyển hóa ngắn nhất",
            "Bản đồ Đồ thị Tương tác", 
            "🃏 Flashcard Ôn tập Nhanh (Mới)"
        ]
    )
    
    # ================= CHẾ ĐỘ 0: FLASHCARD ÔN TẬP NHANH =================
    if menu_mode == "🃏 Flashcard Ôn tập Nhanh (Mới)":
        st.header("🃏 Thẻ Flashcard Ôn tập Nhanh Hình học 2D")
        st.write("Phương pháp ghi nhớ chủ động (*Active Recall*): Đọc dấu hiệu nhận biết, tự suy nghĩ xem đây là hình gì, sau đó bấm lật thẻ để kiểm tra đáp án và công thức.")
        
        cards = get_all_flashcards()
        
        if cards:
            if "card_index" not in st.session_state:
                st.session_state.card_index = 0
            if "show_back" not in st.session_state:
                st.session_state.show_back = False
                
            current_card = cards[st.session_state.card_index]
            
            st.markdown(f"**Thẻ số {st.session_state.card_index + 1} / {len(cards)}**")
            
            with st.container():
                st.markdown(
                    """
                    <style>
                    .flashcard {
                        background-color: #1e1e2f;
                        border: 2px solid #4f46e5;
                        border-radius: 15px;
                        padding: 30px;
                        text-align: center;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                        margin-bottom: 20px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                
                if not st.session_state.show_back:
                    st.markdown(
                        f"""
                        <div class="flashcard">
                            <h3>🔍 Dấu hiệu nhận biết / Đặc điểm:</h3>
                            <h2 style="color: #38bdf8; margin-top: 20px;">"{current_card['nhan_biet']}"</h2>
                            <p style="color: #94a3b8; margin-top: 30px;"><i>(Hãy suy nghĩ xem đây là hình gì, sau đó bấm nút bên dưới để lật thẻ!)</i></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="flashcard" style="border-color: #10b981;">
                            <h3 style="color: #10b981;">✨ Đáp án chính xác:</h3>
                            <h1 style="color: #facc15; margin: 15px 0;">{current_card['ten']}</h1>
                            <p style="text-align: left; color: #e2e8f0;"><b>📝 Tính chất:</b> {current_card['tinh_chat']}</p>
                            <p style="text-align: left; color: #e2e8f0;"><b>📐 Chu vi:</b> <code>{current_card['chu_vi']}</code> | <b>Diện tích:</b> <code>{current_card['dien_tich']}</code></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button("⬅️ Thẻ trước", use_container_width=True):
                    st.session_state.card_index = (st.session_state.card_index - 1) % len(cards)
                    st.session_state.show_back = False
                    st.rerun()
            with col_b2:
                flip_label = "🔄 Lật mặt sau (Xem đáp án)" if not st.session_state.show_back else "🔄 Lật mặt trước (Đố tiếp)"
                if st.button(flip_label, type="primary", use_container_width=True):
                    st.session_state.show_back = not st.session_state.show_back
                    st.rerun()
            with col_b3:
                if st.button("Thẻ tiếp theo ➡️", use_container_width=True):
                    st.session_state.card_index = (st.session_state.card_index + 1) % len(cards)
                    st.session_state.show_back = False
                    st.rerun()

    # ================= CHẾ ĐỘ 1: BẢN ĐỒ ĐỒ THỊ TƯƠNG TÁC =================
    elif menu_mode == "Bản đồ Đồ thị Tương tác":
        st.header("Sơ đồ Mạng lưới Tri thức Hình học 2D")
        st.write("Mô hình hóa cơ sở dữ liệu đồ thị Neo4j dưới dạng mạng lưới trực quan. Bạn có thể dùng chuột kéo thả xem chi tiết các node.")
        
        nodes_res, edges_res = get_graph_data()
        
        if nodes_res:
            net = Network(height="520px", width="100%", bgcolor="#0e1117", font_color="white", directed=True)
            
            # Sử dụng barnes_hut chuẩn an toàn không lỗi tham số
            net.barnes_hut(gravity=-2000, central_gravity=0.3, spring_length=150)
            
            for item in nodes_res:
                node_name = item["ten"]
                if node_name == "Tứ giác tổng quát":
                    color = "#ff4b4b"
                elif node_name == "Hình vuông":
                    color = "#00cc96"
                else:
                    color = "#ffa15a"
                    
                net.add_node(node_name, label=node_name, title=f"Hình: {node_name}", color=color, size=28)
            
            for edge in edges_res:
                net.add_edge(edge["source"], edge["target"], title=f"Điều kiện: {edge['label']}", label="", arrows="to", color="#888888")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                net.save_graph(tmp.name)
                tmp_path = tmp.name
                
            with open(tmp_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            components.html(html_content, height=550)
            os.unlink(tmp_path)
            
            st.info("💡 **Mẹo:** Biểu đồ hiển thị ổn định, bạn có thể chuyển tab qua lại thoải mái!")

    # ================= CHẾ ĐỘ 2: TRA CỨU CHI TIẾT =================
    elif menu_mode == "Tra cứu chi tiết hình":
        selected_shape = st.sidebar.radio("Chọn hình:", shape_names)
        
        if selected_shape:
            query_detail = """
            MATCH (s:Shape {ten: $ten})
            RETURN s.ten AS ten, s.tinh_chat AS tinh_chat, s.nhan_biet AS nhan_biet, s.chu_vi AS chu_vi, s.dien_tich AS dien_tich
            """
            details = run_query(query_detail, {"ten": selected_shape})
            
            if details:
                d = details[0]
                st.header(f"📌 {d['ten']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📝 Tính chất cơ bản")
                    st.success(d['tinh_chat'])
                    
                    st.subheader("🔎 Dấu hiệu nhận biết")
                    st.info(d['nhan_biet'])
                    
                with col2:
                    st.subheader("📐 Công thức toán học")
                    st.markdown(f"**Chu vi ($P$):** `{d['chu_vi']}`")
                    st.markdown(f"**Diện tích ($S$):** `{d['dien_tich']}`")
            
            st.markdown("---")
            st.subheader("🔄 Quan hệ và Điều kiện chuyển hóa trực tiếp")
            
            query_trans = """
            MATCH (s:Shape {ten: $ten})-[r:TRO_THANH]->(target:Shape)
            RETURN target.ten AS target_name, r.dieu_kien AS dieu_kien
            """
            trans = run_query(query_trans, {"ten": selected_shape})
            
            if trans:
                for t in trans:
                    st.warning(f"👉 Chuyển thành **{t['target_name']}** khi thỏa mãn điều kiện: *{t['dieu_kien']}*")
            else:
                st.info("ℹ️ Hình này ở mức độ chuyên sâu hoặc không có quan hệ chuyển hóa tiếp theo.")
                
    # ================= CHẾ ĐỘ 3: ĐƯỜNG ĐI NGẮN NHẤT =================
    elif menu_mode == "Tìm đường đi chuyển hóa ngắn nhất":
        st.header("⚡ Thuật toán Đường đi ngắn nhất (Shortest Path)")
        st.write("Tính năng này sử dụng thuật toán đồ thị Neo4j để tìm ra lộ trình và các bước chuyển hóa tối ưu từ một hình nguồn đến một hình đích.")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            start_shape = st.selectbox("Chọn hình xuất phát:", shape_names, index=0)
        with col_s2:
            end_shape = st.selectbox("Chọn hình đích:", shape_names, index=len(shape_names)-1 if len(shape_names) > 1 else 0)
            
        if st.button("🚀 Tìm chuỗi chuyển hóa tối ưu", type="primary"):
            if start_shape == end_shape:
                st.info("ℹ️ Hình xuất phát và hình đích trùng nhau!")
            else:
                path_query = """
                MATCH p = shortestPath((start:Shape {ten: $start_ten})-[:TRO_THANH*]->(end:Shape {ten:$end_ten}))
                RETURN [node IN nodes(p) | node.ten] AS path_nodes
                """
                path_res = run_query(path_query, {"start_ten": start_shape, "end_ten": end_shape})
                
                if path_res and path_res[0]["path_nodes"]:
                    nodes_in_path = path_res[0]["path_nodes"]
                    st.success(f"🎉 Tìm thấy chuỗi chuyển hóa gồm {len(nodes_in_path) - 1} bước!")
                    
                    step_str = " → ".join([f"**{node}**" for node in nodes_in_path])
                    st.markdown(f"### 📍 Lộ trình: {step_str}")
                    
                    st.markdown("#### 📋 Chi tiết các bước chuyển hóa:")
                    for i in range(len(nodes_in_path) - 1):
                        curr = nodes_in_path[i]
                        nxt = nodes_in_path[i+1]
                        
                        cond_query = """
                        MATCH (s:Shape {ten: $curr})-[r:TRO_THANH]->(t:Shape {ten:$nxt})
                        RETURN r.dieu_kien AS dk
                        """
                        cond_res = run_query(cond_query, {"curr": curr, "nxt": nxt})
                        dk_text = cond_res[0]["dk"] if cond_res and cond_res[0]["dk"] else "Thỏa mãn điều kiện hình học"
                        
                        st.info(f"**Bước {i+1}:** Từ **{curr}** $\\rightarrow$ **{nxt}** \n\n *Điều kiện:* {dk_text}")
                else:
                    st.warning("⚠️ Không tìm thấy đường đi chuyển hóa trực tiếp giữa hai hình này theo chiều đã chọn.")
else:
    st.error("⚠️ Không thể kết nối với Neo4j hoặc chưa có dữ liệu.")