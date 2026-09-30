import streamlit as st
from neo4j import GraphDatabase

# Cấu hình kết nối trực tiếp Neo4j
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")  

def run_query(query, parameters=None):
    """Hàm thực thi câu lệnh Cypher trực tiếp từ Neo4j"""
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
    except Exception as e:
        return []

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Hệ thống Tri thức Hình học 2D", page_icon="📐", layout="wide")

st.title("📐 Hệ thống Tri thức Hình học Tứ giác 2D (Neo4j)")
st.write("Tra cứu tính chất, dấu hiệu nhận biết, công thức toán học và các điều kiện chuyển hóa từ cơ sở dữ liệu Neo4j.")

# Lấy danh sách tên các hình từ Neo4j
try:
    shapes_data = run_query("MATCH (s:Shape) RETURN s.ten AS ten ORDER BY s.ten")
    shape_names = [item["ten"] for item in shapes_data] if shapes_data else []
except Exception:
    shape_names = []

if shape_names:
    st.sidebar.success("🟢 Kết nối Neo4j thành công!")
    st.sidebar.header("🔍 Điều hướng hệ thống")
    
    menu_mode = st.sidebar.radio("Chọn chức năng:", ["Tra cứu chi tiết hình", "Tìm đường đi chuyển hóa ngắn nhất"])
    
    if menu_mode == "Tra cứu chi tiết hình":
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
                        
                        # Đã sửa lỗi hiển thị ký tự mũi tên trực quan tuyệt đối
                        st.info(f"**Bước {i+1}:** Từ **{curr}** $\\rightarrow$ **{nxt}** \n\n *Điều kiện:* {dk_text}")
                else:
                    st.warning("⚠️ Không tìm thấy đường đi chuyển hóa trực tiếp giữa hai hình này theo chiều đã chọn.")
else:
    st.error("⚠️️ Không thể kết nối với Neo4j hoặc chưa có dữ liệu.")