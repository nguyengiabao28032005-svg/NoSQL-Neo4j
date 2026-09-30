BÁO CÁO TỔNG QUAN DỰ ÁN
ĐỀ TÀI: XÂY DỰNG HỆ THỐNG TRI THỨC HÌNH HỌC TỨ GIÁC 2D SỬ DỤNG NEO4J
1. TỔNG QUAN VỀ DỰ ÁN
Tên đề tài: XÂY DỰNG HỆ THỐNG TRI THỨC HÌNH HỌC TỨ GIÁC 2D SỬ DỤNG NEO4J.
	Biểu diễn tri thức dạng đồ thị: Mô hình hóa hệ thống hình học tứ giác 2D (từ tứ giác tổng quát đến các hình đặc biệt như hình vuông, hình chữ nhật, hình thoi, hình thang cân,...) thành các thực thể (Node) và mối quan hệ chuyển hóa (TRO_THANH) trong cơ sở dữ liệu đồ thị.
	Xây dựng ứng dụng tra cứu trực quan: Cung cấp giao diện web thân thiện giúp người dùng dễ dàng tra cứu thông tin hình học, tính chất, dấu hiệu nhận biết, công thức toán học (chu vi, diện tích) và điều kiện chuyển hóa.
	Khai thác thuật toán đồ thị: Tích hợp thuật toán tìm đường đi ngắn nhất (shortestPath) nhằm tự động hoạch định lộ trình và chuỗi các bước chuyển hóa tối ưu giữa các hình học trong hệ thống.
2. Kiến trúc hệ thống và Công nghệ sử dụng
	Tầng dữ liệu (Data):
	Sử dụng hệ quản trị cơ sở dữ liệu đồ thị Neo4j (chạy trên môi trường cục bộ neo4j://localhost:7687).
	Lưu trữ các thuộc tính chi tiết cho mỗi hình: tính chất cơ bản, dấu hiệu nhận biết, chu vi, diện tích và thuộc tính điều kiện (dieu_kien) trên mối quan hệ.
 
	Tầng ứng dụng (Source App):
	Xây dựng bằng ngôn ngữ Python thông qua framework Streamlit.
	Sử dụng driver neo4j để thực thi trực tiếp các câu lệnh truy vấn Cypher và hiển thị kết quả theo thời gian thực.
3. Các tính năng chính của hệ thống
 Tra cứu chi tiết hình học:
	Chọn chức năng Tra cứu chi tiết hình trên menu điều hướng bên trái.
	Lựa chọn hình tứ giác cần xem, hệ thống sẽ truy vấn trực tiếp từ Neo4j và hiển thị:
	Tính chất cơ bản.
	Dấu hiệu nhận biết.
	Công thức toán học (Chu vi P, Diện tích S).
	Quan hệ chuyển hóa trực tiếp kèm điều kiện.
 
Thuật toán đường đi ngắn nhất (Shortest Path):
	Chọn chức năng Tìm đường đi chuyển hóa ngắn nhất (Cải tiến 1) trên menu trái.
	Lựa chọn Hình xuất phát và Hình đích (Ví dụ: Từ Tứ giác tổng quát đến Hình vuông).
 
	Bấm nút Tìm chuỗi chuyển hóa tối ưu, hệ thống sẽ tự động quét đồ thị Neo4j và trả về lộ trình các bước chuyển hóa chi tiết kèm theo điều kiện hình học ở từng chặng.
 
4. DANH MỤC CÁC HÌNH TỨ GIÁC VÀ QUY LUẬT CHUYỂN HÓA
Bảng Hệ Thống Hóa Các Hình Tứ Giác 2D
Tên gọi	Tính chất cơ bản	Dấu hiệu nhận biết	Chu vi (P)	Diện tích (S)
1. Tứ giác tổng quát	- Tổng 4 góc bằng 360^∘.


- Có 4 đỉnh và 4 cạnh khép kín.	- Đa giác có 4 cạnh bất kỳ không cắt nhau.	P=a+b+c+d


(Tổng độ dài 4 cạnh)	Tùy theo dạng bài toán (thường chia thành các tam giác nhỏ).
2. Hình thang	- Có ít nhất một cặp cạnh đối song song (gọi là hai cạnh đáy).	- Tứ giác có 2 cạnh đối song song.	P=a+b+c+d


(với a,b là cạnh đáy; c,d là 2 cạnh bên)	S=((a+b)×h)/2


(h là chiều cao)
3. Hình thang cân	- Là hình thang có 2 góc kề một đáy bằng nhau.


- Hai đường chéo bằng nhau.	- Hình thang có 2 góc kề một đáy bằng nhau.


- Hình thang có 2 đường chéo bằng nhau.	P=a+b+c+d	S=((a+b)×h)/2
4. Hình bình hành	- Các cặp cạnh đối song song và bằng nhau.


- Các góc đối bằng nhau.


- 2 đường chéo cắt nhau tại trung điểm mỗi đường.	- Tứ giác có các cạnh đối song song.


- Tứ giác có các cạnh đối bằng nhau.


- Tứ giác có 2 đường chéo cắt nhau tại trung điểm.	P=2×(a+b)


(với a,b là 2 cạnh kề)	S=a×h


(a là cạnh đáy, h là chiều cao tương ứng)
5. Hình chữ nhật	- Có 4 góc vuông (90^∘).


- Các cạnh đối song song và bằng nhau.


- 2 đường chéo bằng nhau và cắt nhau tại trung điểm.	- Hình bình hành có 1 góc vuông.


- Tứ giác có 3 góc vuông.	P=2×(dài+rộng)


(ký hiệu: 2(a+b))	S=dài×rộng


(ký hiệu: a×b)
6. Hình thoi	- Có 4 cạnh bằng nhau.


- Các góc đối bằng nhau.


- 2 đường chéo vuông góc với nhau và là đường phân giác của các góc.	- Hình bình hành có 2 cạnh kề bằng nhau.


- Hình bình hành có 2 đường chéo vuông góc.


- Tứ giác có 4 cạnh bằng nhau.	P=4×a


(a là độ dài cạnh)	S=1/2×d_1×d_2


(d_1,d_2 là 2 đường chéo)
7. Hình vuông	- Vừa là hình chữ nhật, vừa là hình thoi.


- Có 4 góc vuông và 4 cạnh bằng nhau.


- 2 đường chéo bằng nhau, vuông góc và cắt nhau tại trung điểm.	- Hình chữ nhật có 2 cạnh kề bằng nhau.


- Hình chữ nhật có 2 đường chéo vuông góc.


- Hình thoi có 1 góc vuông.	P=4×a	S=a^2


(a là độ dài cạnh)
Quan hệ giữa các hình 
1. Từ Tứ giác tổng quát → Hình thang / Hình diều
	Tứ giác + 1 cặp cạnh đối song song → Hình thang.
	Tứ giác + 2 cặp cạnh kề bằng nhau (2 cặp kề một đỉnh) → Hình diều.
2. Từ Hình thang → Hình thang cân / Hình bình hành
	Hình thang + 2 góc kề một đáy bằng nhau → Hình thang cân.
	Hình thang + 2 đường chéo bằng nhau → Hình thang cân.
	Hình thang + Cả 2 cặp cạnh đối song song → Hình bình hành. (Vì hình thang vốn đã có sẵn 1 cặp song song, nếu cặp còn lại cũng song song thì thành hình bình hành).
	Hình thang + 2 cặp cạnh đối bằng nhau → Hình bình hành. (Như bạn vừa nhắc đến: hình thang có các cạnh đối bằng nhau từng đôi một sẽ tự động song song và trở thành hình bình hành).
	Hình thang + 2 đường chéo cắt nhau tại trung điểm mỗi đường → Hình bình hành.
3. Từ Hình bình hành → Hình chữ nhật / Hình thoi
	Hình bình hành + 1 góc vuông → Hình chữ nhật. (Khi có 1 góc vuông, các góc còn lại cũng sẽ vuông).
	Hình bình hành + 2 đường chéo bằng nhau → Hình chữ nhật.
	Hình bình hành + 2 cạnh kề bằng nhau → Hình thoi. (Vì vốn là hình bình hành nên các cạnh đối đã bằng nhau, nếu thêm 2 cạnh kề bằng nhau thì cả 4 cạnh đều bằng nhau).
	Hình bình hành + 2 đường chéo vuông góc với nhau → Hình thoi.
	Hình bình hành + 1 đường chéo là đường phân giác của một góc → Hình thoi.
4. Từ Hình chữ nhật hoặc Hình thoi → Hình vuông
	Hình chữ nhật + 2 cạnh kề bằng nhau → Hình vuông. (Chữ nhật có các cạnh kề bằng nhau nghĩa là cả 4 cạnh bằng nhau).
	Hình chữ nhật + 2 đường chéo vuông góc với nhau → Hình vuông.
	Hình chữ nhật + 1 đường chéo là đường phân giác của một góc → Hình vuông.
	Hình thoi + 1 góc vuông → Hình vuông. (Thoi có 1 góc vuông thì các góc còn lại cũng vuông, biến thành hình chữ nhật kết hợp với hình thoi sẵn có thành hình vuông).
	Hình thoi + 2 đường chéo bằng nhau → Hình vuông.

