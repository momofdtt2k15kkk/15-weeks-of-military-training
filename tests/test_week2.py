"""Bộ test tuần 2 - Cấu trúc dữ liệu, hàm và chuỗi.

Tuần 2 đã dạy `def`, nên hầu hết hàm kiem_tra_* nhận HÀM và tự chọn đầu vào để gọi.
Bài tập đọc file (📡) nhận GIÁ TRỊ biến học viên đã gán, đáp án tính từ chính file trong data/.
"""

from __future__ import annotations

import copy

try:
    from .runner import Case, kiem_tra, kiem_tra_gia_tri
except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
    from runner import Case, kiem_tra, kiem_tra_gia_tri


def _mo_data(ten_file):
    try:
        from .tien_ich_du_lieu import duong_dan_data
    except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
        from tien_ich_du_lieu import duong_dan_data
    return open(duong_dan_data(ten_file), encoding="utf-8")


def _lam_tron_list(ds, so_chu_so=9):
    """Làm tròn list số để so sánh không vướng sai số cuối của số thực. Giá trị khác list giữ nguyên."""
    if isinstance(ds, list) and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in ds):
        return [round(x, so_chu_so) for x in ds]
    return ds


# --------------------------------------------------------------------------
# Bài 1: List
# --------------------------------------------------------------------------

def kiem_tra_1_1(ham) -> bool:
    """loc_vat_can_gan(khoang_cach, nguong) -> list các khoảng cách < nguong, giữ thứ tự."""
    return kiem_tra(
        "Bài 1.1 - Lọc vật cản gần",
        ham,
        [
            Case(args=([5.2, 3.1, 0.8, 4.5, 1.2, 0.3], 1.0), expected=[0.8, 0.3],
                 mo_ta="loc_vat_can_gan([5.2, 3.1, 0.8, 4.5, 1.2, 0.3], 1.0)"),
            Case(args=([2.0, 1.0, 0.5], 1.0), expected=[0.5],
                 mo_ta="loc_vat_can_gan([2.0, 1.0, 0.5], 1.0) - đúng bằng ngưỡng thì không lấy"),
            Case(args=([1.5, 2.5, 0.9], 1.5), expected=[0.9],
                 mo_ta="loc_vat_can_gan([1.5, 2.5, 0.9], 1.5) - ngưỡng khác"),
            Case(args=([], 1.0), expected=[], mo_ta="loc_vat_can_gan([], 1.0) - list rỗng"),
        ],
    )


def kiem_tra_1_2(ham) -> bool:
    """tb_n_mau_cuoi(ds, n) -> trung bình n phần tử cuối, ít hơn n thì lấy hết, list rỗng là None."""
    return kiem_tra(
        "Bài 1.2 - Trung bình n mẫu cuối",
        ham,
        [
            Case(args=([10, 20, 30, 40], 2), expected=35.0, mo_ta="tb_n_mau_cuoi([10, 20, 30, 40], 2)"),
            Case(args=([4, 8, 6, 2, 10], 3), expected=6.0, mo_ta="tb_n_mau_cuoi([4, 8, 6, 2, 10], 3)"),
            Case(args=([10, 20], 5), expected=15.0,
                 mo_ta="tb_n_mau_cuoi([10, 20], 5) - ít phần tử hơn n thì lấy hết"),
            Case(args=([7], 1), expected=7.0, mo_ta="tb_n_mau_cuoi([7], 1)"),
            Case(args=([], 3), expected=None, mo_ta="tb_n_mau_cuoi([], 3) - list rỗng"),
        ],
    )


def _dap_an_1_3():
    import csv
    with _mo_data("obd.csv") as f:
        toc_do = [int(hang["toc_do_kmh"]) for hang in csv.DictReader(f)]
    return toc_do, [v for v in toc_do if v > 60]


def kiem_tra_1_3(toc_do_list, toc_do_cao) -> bool:
    """toc_do_list -> cột toc_do_kmh của obd.csv. toc_do_cao -> các tốc độ > 60, giữ thứ tự."""
    toc_do, cao = _dap_an_1_3()
    return kiem_tra_gia_tri(
        "Bài 1.3 - Gom tốc độ vào list",
        [
            ("toc_do_list (cột toc_do_kmh của obd.csv)", toc_do_list, toc_do),
            ("toc_do_cao (các tốc độ lớn hơn 60)", toc_do_cao, cao),
        ],
    )


def kiem_tra_1_4(ham) -> bool:
    """trung_binh_truot(ds, k) -> list trung bình của mọi cửa sổ k phần tử liên tiếp."""

    def ham_cham(ds, k):
        ket_qua = ham(ds, k)
        return _lam_tron_list(ket_qua)

    return kiem_tra(
        "Bài 1.4 - Trung bình trượt",
        ham_cham if callable(ham) else ham,
        [
            Case(args=([2, 4, 6, 8], 2), expected=[3.0, 5.0, 7.0],
                 mo_ta="trung_binh_truot([2, 4, 6, 8], 2)"),
            Case(args=([1, 2, 3, 4, 5], 3), expected=[2.0, 3.0, 4.0],
                 mo_ta="trung_binh_truot([1, 2, 3, 4, 5], 3)"),
            Case(args=([5, 7], 1), expected=[5.0, 7.0], mo_ta="trung_binh_truot([5, 7], 1) - k = 1"),
            Case(args=([0, 0, 60, 30], 4), expected=[22.5],
                 mo_ta="trung_binh_truot([0, 0, 60, 30], 4) - k bằng độ dài list"),
            Case(args=([3, 4], 5), expected=[], mo_ta="trung_binh_truot([3, 4], 5) - k lớn hơn độ dài list"),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Tuple, enumerate, zip
# --------------------------------------------------------------------------

def kiem_tra_2_1(ham) -> bool:
    """giay_vuot_nguong(ds, nguong) -> list chỉ số i có ds[i] > nguong."""
    return kiem_tra(
        "Bài 2.1 - Giây vượt ngưỡng",
        ham,
        [
            Case(args=([0, 42, 65, 70, 50], 60), expected=[2, 3], mo_ta="giay_vuot_nguong([0, 42, 65, 70, 50], 60)"),
            Case(args=([10, 20, 30], 30), expected=[], mo_ta="giay_vuot_nguong([10, 20, 30], 30) - đúng bằng ngưỡng thì không lấy"),
            Case(args=([5, 9, 7, 12], 6), expected=[1, 2, 3], mo_ta="giay_vuot_nguong([5, 9, 7, 12], 6)"),
            Case(args=([], 1), expected=[], mo_ta="giay_vuot_nguong([], 1) - list rỗng"),
        ],
    )


def kiem_tra_2_2(ham) -> bool:
    """chenh_lech_lien_tiep(ds) -> list hiệu hai phần tử liền kề (sau trừ trước)."""
    return kiem_tra(
        "Bài 2.2 - Chênh lệch liên tiếp",
        ham,
        [
            Case(args=([30, 29, 7, 0],), expected=[-1, -22, -7], mo_ta="chenh_lech_lien_tiep([30, 29, 7, 0])"),
            Case(args=([1, 4, 9, 16],), expected=[3, 5, 7], mo_ta="chenh_lech_lien_tiep([1, 4, 9, 16])"),
            Case(args=([5],), expected=[], mo_ta="chenh_lech_lien_tiep([5]) - chỉ một phần tử"),
            Case(args=([],), expected=[], mo_ta="chenh_lech_lien_tiep([]) - list rỗng"),
        ],
    )


def _dap_an_2_3():
    try:
        from .tien_ich_du_lieu import nmea_sang_do
    except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
        from tien_ich_du_lieu import nmea_sang_do
    quy_dao, giay = [], -1
    with _mo_data("gps.nmea") as f:
        for dong in f:
            if not dong.startswith("$GNGGA"):
                continue
            giay += 1
            cot = dong.split(",")
            if cot[2] == "":
                continue
            quy_dao.append((giay, nmea_sang_do(cot[2], cot[3]), nmea_sang_do(cot[4], cot[5])))
    return quy_dao


def kiem_tra_2_3(quy_dao) -> bool:
    """quy_dao -> list tuple (giây, vĩ độ, kinh độ) của các giây có fix trong gps.nmea."""
    return kiem_tra_gia_tri(
        "Bài 2.3 - Quỹ đạo GPS",
        [("quy_dao (gps.nmea, các giây có fix)", quy_dao, _dap_an_2_3())],
    )


# --------------------------------------------------------------------------
# Bài 3: Tham số mặc định và phạm vi biến
# --------------------------------------------------------------------------

def kiem_tra_3_1(ham) -> bool:
    """giam_toc_do(toc_do_goc, phan_tram=0) -> float, làm tròn 2 chữ số."""
    return kiem_tra(
        "Bài 3.1 - Giảm tốc độ",
        ham,
        [
            Case(args=(120,), expected=120.0, mo_ta="giam_toc_do(120) - không truyền phần trăm, dùng mặc định"),
            Case(args=(120, 10), expected=108.0, mo_ta="giam_toc_do(120, 10)"),
            Case(args=(80, 25), expected=60.0, mo_ta="giam_toc_do(80, 25)"),
            Case(args=(45, 33), expected=30.15, mo_ta="giam_toc_do(45, 33) - làm tròn 2 chữ số"),
            Case(args=(60, 100), expected=0.0, mo_ta="giam_toc_do(60, 100) - giảm hết, xe dừng"),
            Case(kwargs={"toc_do_goc": 90, "phan_tram": 10}, expected=81.0,
                 mo_ta="giam_toc_do(toc_do_goc=90, phan_tram=10) - gọi bằng tên tham số"),
        ],
    )


def kiem_tra_3_2(ham) -> bool:
    """tru_hao_pin(muc_pin, luong_tieu_hao, san=0) -> mức pin sau tiêu hao, không thấp hơn san."""
    return kiem_tra(
        "Bài 3.2 - Mức pin sau tiêu hao",
        ham,
        [
            Case(args=(100, 30), expected=70, mo_ta="tru_hao_pin(100, 30)"),
            Case(args=(20, 30), expected=0, mo_ta="tru_hao_pin(20, 30) - tiêu hao vượt mức pin, về 0"),
            Case(args=(50, 0), expected=50, mo_ta="tru_hao_pin(50, 0) - không tiêu hao"),
            Case(args=(50, 30, 15), expected=20, mo_ta="tru_hao_pin(50, 30, 15) - còn trên sàn 15"),
            Case(args=(30, 30, 15), expected=15, mo_ta="tru_hao_pin(30, 30, 15) - chạm sàn 15"),
            Case(kwargs={"muc_pin": 40, "luong_tieu_hao": 5, "san": 10}, expected=35,
                 mo_ta="tru_hao_pin(muc_pin=40, luong_tieu_hao=5, san=10) - gọi bằng tên tham số"),
        ],
    )


def kiem_tra_3_3(ham) -> bool:
    """ghi_canh_bao(thong_bao, nhat_ky=None) -> list nhật ký, mỗi lần gọi không truyền nhat_ky là list mới.

    Các Case chạy lần lượt trên cùng một hàm, nên mặc định `nhat_ky=[]` dùng chung sẽ làm
    Case thứ hai trả về hai phần tử.
    """
    return kiem_tra(
        "Bài 3.3 - Nhật ký cảnh báo",
        ham,
        [
            Case(args=("phanh gap",), expected=["phanh gap"], mo_ta='ghi_canh_bao("phanh gap")'),
            Case(args=("mat gps",), expected=["mat gps"],
                 mo_ta='ghi_canh_bao("mat gps") - gọi lần hai, không dính cảnh báo của lần một'),
            Case(args=("pin yeu", ["phanh gap"]), expected=["phanh gap", "pin yeu"],
                 mo_ta='ghi_canh_bao("pin yeu", ["phanh gap"]) - thêm vào nhật ký có sẵn'),
            Case(args=("mat gps",), expected=["mat gps"],
                 mo_ta='ghi_canh_bao("mat gps") - gọi lần nữa vẫn bắt đầu từ list rỗng'),
        ],
    )


# --------------------------------------------------------------------------
# Bài 4: Chuỗi ký tự
# --------------------------------------------------------------------------

CAU_RMC = "$GNRMC,165940.00,A,2100.35986,N,10550.57994,E,21.60,0.0,081026,,,F*45"
CAU_GGA = "$GNGGA,165900.00,2100.27089,N,10550.57792,E,1,07,1.4,11.8,M,-22.1,M,,*67"


def kiem_tra_4_1(ham) -> bool:
    """loai_cau(cau) -> tên câu NMEA, phần giữa "$" và dấu phẩy đầu tiên."""
    return kiem_tra(
        "Bài 4.1 - Loại câu NMEA",
        ham,
        [
            Case(args=(CAU_GGA,), expected="GNGGA", mo_ta='loai_cau("$GNGGA,165900.00,2100.27089,...")'),
            Case(args=(CAU_RMC,), expected="GNRMC", mo_ta='loai_cau("$GNRMC,165940.00,A,2100.35986,...")'),
            Case(args=("$GPGSV,3,1,12*74",), expected="GPGSV", mo_ta='loai_cau("$GPGSV,3,1,12*74")'),
        ],
    )


def kiem_tra_4_2(ham) -> bool:
    """ma_hoa_caesar(van_ban, dich_chuyen) -> str.

    Chỉ dịch chữ cái a-z/A-Z, giữ nguyên số/dấu câu/khoảng trắng, có vòng qua chữ z/Z.
    """
    return kiem_tra(
        "Bài 4.2 - Mã hoá Caesar",
        ham,
        [
            Case(args=("Hello, World!", 3), expected="Khoor, Zruog!", mo_ta='ma_hoa_caesar("Hello, World!", 3)'),
            Case(args=("abc XYZ", 2), expected="cde ZAB", mo_ta='ma_hoa_caesar("abc XYZ", 2)'),
            Case(args=("Python 3.11", 5), expected="Udymts 3.11",
                 mo_ta='ma_hoa_caesar("Python 3.11", 5) - số và dấu chấm giữ nguyên'),
            Case(args=("xyz", 3), expected="abc", mo_ta='ma_hoa_caesar("xyz", 3) - vòng qua từ z về a'),
        ],
    )


# --------------------------------------------------------------------------
# Bài 5: Dict và set
# --------------------------------------------------------------------------

def kiem_tra_5_1(ham) -> bool:
    """hop_nhat_cau_hinh(mac_dinh, tuy_chinh) -> dict mới, không sửa mac_dinh."""

    def ham_cham(mac_dinh, tuy_chinh):
        goc_mac_dinh, goc_tuy_chinh = copy.deepcopy(mac_dinh), copy.deepcopy(tuy_chinh)
        ket_qua = ham(mac_dinh, tuy_chinh)
        if mac_dinh != goc_mac_dinh or tuy_chinh != goc_tuy_chinh:
            return "hàm đã sửa dict truyền vào, cần trả về dict mới"
        return ket_qua

    return kiem_tra(
        "Bài 5.1 - Hợp nhất cấu hình",
        ham_cham if callable(ham) else ham,
        [
            Case(args=({"toc_do": 30, "camera": "1080p"}, {"toc_do": 40}),
                 expected={"toc_do": 40, "camera": "1080p"},
                 mo_ta='hop_nhat_cau_hinh({"toc_do": 30, "camera": "1080p"}, {"toc_do": 40})'),
            Case(args=({"toc_do": 30, "pin_toi_thieu": 20}, {"toc_do": 50, "camera": "720p"}),
                 expected={"toc_do": 50, "pin_toi_thieu": 20, "camera": "720p"},
                 mo_ta="hop_nhat_cau_hinh(...) - tuy_chinh vừa ghi đè vừa thêm khoá mới"),
            Case(args=({"toc_do": 30}, {}), expected={"toc_do": 30},
                 mo_ta="hop_nhat_cau_hinh({\"toc_do\": 30}, {}) - không tuỳ chỉnh gì"),
            Case(args=({}, {"camera": "720p"}), expected={"camera": "720p"},
                 mo_ta="hop_nhat_cau_hinh({}, {\"camera\": \"720p\"}) - mặc định rỗng"),
        ],
    )


def kiem_tra_5_2(ham) -> bool:
    """cam_bien_con_thieu(dang_bat, yeu_cau) -> set các cảm biến yêu cầu mà chưa bật."""
    return kiem_tra(
        "Bài 5.2 - Cảm biến còn thiếu",
        ham,
        [
            Case(args=({"lidar", "camera"}, {"lidar", "gps"}), expected={"gps"},
                 mo_ta='cam_bien_con_thieu({"lidar", "camera"}, {"lidar", "gps"})'),
            Case(args=({"lidar", "gps", "radar"}, {"lidar"}), expected=set(),
                 mo_ta='cam_bien_con_thieu({"lidar", "gps", "radar"}, {"lidar"}) - bật dư, không thiếu gì'),
            Case(args=(set(), {"gps", "lidar"}), expected={"gps", "lidar"},
                 mo_ta='cam_bien_con_thieu(set(), {"gps", "lidar"}) - chưa bật cảm biến nào'),
        ],
    )


def _dap_an_5_3():
    dem = {}
    with _mo_data("gps.nmea") as f:
        for dong in f:
            if dong.startswith("$GNGGA"):
                ma = int(dong.split(",")[6])
                dem[ma] = dem.get(ma, 0) + 1
    return dem


def kiem_tra_5_3(so_giay_theo_fix) -> bool:
    """so_giay_theo_fix -> dict {mã fix (int): số câu $GNGGA} của gps.nmea."""
    return kiem_tra_gia_tri(
        "Bài 5.3 - Đếm giây theo mã fix",
        [("so_giay_theo_fix (gps.nmea)", so_giay_theo_fix, _dap_an_5_3())],
    )


def _dap_an_5_4():
    import csv
    dem, theo_thu_tu = {}, []
    with _mo_data("ma_loi.csv") as f:
        for hang in csv.DictReader(f):
            ma = hang["ma_loi"]
            if ma not in dem:
                theo_thu_tu.append(ma)
            dem[ma] = dem.get(ma, 0) + 1
    return dem, theo_thu_tu


def kiem_tra_5_4(so_lan_theo_ma, ma_loi_theo_thu_tu) -> bool:
    """so_lan_theo_ma -> dict {mã lỗi: số lần}. ma_loi_theo_thu_tu -> list mã, mỗi mã một lần, theo lần đầu."""
    dem, theo_thu_tu = _dap_an_5_4()
    return kiem_tra_gia_tri(
        "Bài 5.4 - Thống kê mã lỗi chẩn đoán",
        [
            ("so_lan_theo_ma (ma_loi.csv)", so_lan_theo_ma, dem),
            ("ma_loi_theo_thu_tu (ma_loi.csv, mỗi mã một lần)", ma_loi_theo_thu_tu, theo_thu_tu),
        ],
    )


def _dap_an_5_5():
    import csv
    nhom = {}
    with _mo_data("ma_loi.csv") as f:
        for hang in csv.DictReader(f):
            nhom.setdefault(hang["ma_loi"], []).append(float(hang["thoi_gian_s"]))
    return nhom


def kiem_tra_5_5(thoi_diem_theo_ma) -> bool:
    """thoi_diem_theo_ma -> dict {mã lỗi: list thời điểm (float) báo mã đó, theo thứ tự trong file}."""
    return kiem_tra_gia_tri(
        "Bài 5.5 - Gom thời điểm theo mã lỗi",
        [("thoi_diem_theo_ma (ma_loi.csv)", thoi_diem_theo_ma, _dap_an_5_5())],
    )


# ==========================================================================
# Dự án: kiểm tra trước khi xuất phát, rồi phân tích cả chuyến xe.
# ==========================================================================

def kiem_tra_du_an(ham) -> bool:
    """kiem_tra_truoc_khi_di(mac_dinh, tuy_chinh, dang_bat, yeu_cau)
    -> dict {"cau_hinh": ..., "cam_bien_thieu": ..., "san_sang": ...}
    """
    return kiem_tra(
        "Dự án phần 1 - Bộ kiểm tra trước khi xuất phát",
        ham,
        [
            Case(
                args=({"toc_do": 30, "camera": "1080p"}, {"toc_do": 40}, {"lidar", "camera"}, {"lidar", "gps"}),
                expected={"cau_hinh": {"toc_do": 40, "camera": "1080p"}, "cam_bien_thieu": {"gps"},
                          "san_sang": False},
                mo_ta="thiếu gps nên chưa sẵn sàng",
            ),
            Case(
                args=({"toc_do": 30}, {}, {"lidar", "gps", "radar"}, {"lidar", "gps"}),
                expected={"cau_hinh": {"toc_do": 30}, "cam_bien_thieu": set(), "san_sang": True},
                mo_ta="đủ cảm biến, không tuỳ chỉnh gì",
            ),
            Case(
                args=({"toc_do": 30, "pin_toi_thieu": 20}, {"pin_toi_thieu": 35}, set(), {"lidar"}),
                expected={"cau_hinh": {"toc_do": 30, "pin_toi_thieu": 35}, "cam_bien_thieu": {"lidar"},
                          "san_sang": False},
                mo_ta="ghi đè pin_toi_thieu, chưa bật cảm biến nào",
            ),
        ],
    )


def _dap_an_lab():
    try:
        from .tien_ich_du_lieu import doc_chuyen_xe, khoang_cach_hai_diem_m
    except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
        from tien_ich_du_lieu import doc_chuyen_xe, khoang_cach_hai_diem_m
    toc_do_theo_giay, giay_vat_can_gan = [], []
    for t, khoang_cach, toc_do, pin in doc_chuyen_xe():
        toc_do_theo_giay.append(toc_do)
        if khoang_cach is not None and khoang_cach <= 5.0:
            giay_vat_can_gan.append(t)
    toc_do_muot = [sum(toc_do_theo_giay[i:i + 5]) / 5 for i in range(len(toc_do_theo_giay) - 4)]
    quy_dao = _dap_an_2_3()
    quang_duong_gps_m = sum(khoang_cach_hai_diem_m(a, b) for a, b in zip(quy_dao, quy_dao[1:]))
    return toc_do_theo_giay, toc_do_muot, giay_vat_can_gan, quang_duong_gps_m


def kiem_tra_lab(toc_do_theo_giay, toc_do_muot, giay_vat_can_gan, quang_duong_gps_m) -> bool:
    """Gom dữ liệu cả chuyến xe: tốc độ từng giây, trung bình trượt 5 giây, các giây có vật cản <= 5 m,
    quãng đường GPS."""
    toc_do, muot, gan, quang_duong = _dap_an_lab()
    return kiem_tra_gia_tri(
        "Dự án phần 2 - Phân tích cả chuyến xe",
        [
            ("toc_do_theo_giay (tốc độ của từng giây)", toc_do_theo_giay, toc_do),
            ("toc_do_muot (trung bình trượt 5 giây)", _lam_tron_list(toc_do_muot), _lam_tron_list(muot)),
            ("giay_vat_can_gan (các giây khoảng cách <= 5.0 m)", giay_vat_can_gan, gan),
            ("quang_duong_gps_m (cộng khoảng cách các cặp điểm liền kề của quy_dao)", quang_duong_gps_m, quang_duong),
        ],
        sai_so=1e-4,
    )
