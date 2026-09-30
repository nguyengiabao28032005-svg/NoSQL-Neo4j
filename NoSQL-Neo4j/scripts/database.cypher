// ==========================================
// 1. KHỞI TẠO CÁC NODE HÌNH TỨ GIÁC (SHAPES)
// ==========================================

CREATE (tg:Shape {
    ten: 'Tứ giác tổng quát',
    tinh_chat: 'Tổng 4 góc bằng 360 độ. Có 4 đỉnh và 4 cạnh khép kín bất kỳ.',
    nhan_biet: 'Đa giác lồi/lõm có 4 cạnh không cắt nhau.',
    chu_vi: 'P = a + b + c + d',
    dien_tich: 'Tùy theo bài toán (có thể chia thành các tam giác nhỏ)'
});

CREATE (ht:Shape {
    ten: 'Hình thang',
    tinh_chat: 'Có ít nhất một cặp cạnh đối song song gọi là hai cạnh đáy.',
    nhan_biet: 'Tứ giác có 1 cặp cạnh đối song song.',
    chu_vi: 'P = a + b + c + d',
    dien_tich: 'S = ((a + b) * h) / 2'
});

CREATE (hd:Shape {
    ten: 'Hình diều',
    tinh_chat: 'Có 2 cặp cạnh kề bằng nhau. Hai đường chéo vuông góc với nhau.',
    nhan_biet: 'Tứ giác có 2 cặp cạnh kề bằng nhau.',
    chu_vi: 'P = 2 * (a + b)',
    dien_tich: 'S = (1/2) * d1 * d2'
});

CREATE (htc:Shape {
    ten: 'Hình thang cân',
    tinh_chat: 'Hình thang có 2 góc kề một đáy bằng nhau. Hai đường chéo bằng nhau.',
    nhan_biet: 'Hình thang có 2 góc kề một đáy bằng nhau, hoặc hình thang có 2 đường chéo bằng nhau.',
    chu_vi: 'P = a + b + c + d',
    dien_tich: 'S = ((a + b) * h) / 2'
});

CREATE (hbh:Shape {
    ten: 'Hình bình hành',
    tinh_chat: 'Các cặp cạnh đối song song và bằng nhau. Các góc đối bằng nhau. 2 đường chéo cắt nhau tại trung điểm.',
    nhan_biet: 'Tứ giác có các cặp cạnh đối song song, hoặc hình thang có 2 cặp cạnh đối bằng nhau.',
    chu_vi: 'P = 2 * (a + b)',
    dien_tich: 'S = a * h'
});

CREATE (hcn:Shape {
    ten: 'Hình chữ nhật',
    tinh_chat: 'Có 4 góc vuông. Các cạnh đối song song và bằng nhau. 2 đường chéo bằng nhau.',
    nhan_biet: 'Hình bình hành có 1 góc vuông, hoặc tứ giác có 3 góc vuông.',
    chu_vi: 'P = 2 * (dài + rộng)',
    dien_tich: 'S = dài * rộng'
});

CREATE (htoi:Shape {
    ten: 'Hình thoi',
    tinh_chat: 'Có 4 cạnh bằng nhau. Các góc đối bằng nhau. 2 đường chéo vuông góc và là đường phân giác của các góc.',
    nhan_biet: 'Hình bình hành có 2 cạnh kề bằng nhau, hoặc tứ giác có 4 cạnh bằng nhau.',
    chu_vi: 'P = 4 * a',
    dien_tich: 'S = (1/2) * d1 * d2'
});

CREATE (hv:Shape {
    ten: 'Hình vuông',
    tinh_chat: 'Vừa là hình chữ nhật vừa là hình thoi. Có 4 góc vuông và 4 cạnh bằng nhau.',
    nhan_biet: 'Hình chữ nhật có 2 cạnh kề bằng nhau, hoặc hình thoi có 1 góc vuông.',
    chu_vi: 'P = 4 * a',
    dien_tich: 'S = a * a'
});


// ==========================================
// 2. KHỞI TẠO CÁC MỐI QUAN HỆ CHUYỂN HÓA (TRO_THANH)
// ==========================================

MATCH (a:Shape {ten: 'Tứ giác tổng quát'}), (b:Shape {ten: 'Hình thang'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 1 cặp cạnh đối song song'}]->(b);

MATCH (a:Shape {ten: 'Tứ giác tổng quát'}), (b:Shape {ten: 'Hình diều'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 2 cặp cạnh kề bằng nhau'}]->(b);

MATCH (a:Shape {ten: 'Hình thang'}), (b:Shape {ten: 'Hình thang cân'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 2 góc kề một đáy bằng nhau hoặc 2 đường chéo bằng nhau'}]->(b);

MATCH (a:Shape {ten: 'Hình thang'}), (b:Shape {ten: 'Hình bình hành'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm cặp cạnh đối còn lại song song hoặc 2 cặp cạnh đối bằng nhau'}]->(b);

MATCH (a:Shape {ten: 'Hình bình hành'}), (b:Shape {ten: 'Hình chữ nhật'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 1 góc vuông hoặc 2 đường chéo bằng nhau'}]->(b);

MATCH (a:Shape {ten: 'Hình bình hành'}), (b:Shape {ten: 'Hình thoi'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 2 cạnh kề bằng nhau hoặc 2 đường chéo vuông góc'}]->(b);

MATCH (a:Shape {ten: 'Hình chữ nhật'}), (b:Shape {ten: 'Hình vuông'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 2 cạnh kề bằng nhau hoặc 2 đường chéo vuông góc'}]->(b);

MATCH (a:Shape {ten: 'Hình thoi'}), (b:Shape {ten: 'Hình vuông'})
CREATE (a)-[:TRO_THANH {dieu_kien: 'Thêm 1 góc vuông hoặc 2 đường chéo bằng nhau'}]->(b);