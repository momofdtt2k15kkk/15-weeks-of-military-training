"""Bộ test tuần 3 - Xử lý lỗi & Lập trình hướng đối tượng (OOP).

  - Bài viết hàm: kiem_tra_* nhận HÀM, tự gọi với nhiều đầu vào.
  - Bài viết class: kiem_tra_* nhận CLASS, tự tạo object và gọi phương thức theo từng kịch bản.
  - Bài đọc file (📡): kiem_tra_* nhận GIÁ TRỊ biến học viên đã gán, đáp án tính từ chính file trong data/.
"""

from __future__ import annotations

import csv
from pathlib import Path
from types import SimpleNamespace

try:
    from .runner import Case, kiem_tra, kiem_tra_gia_tri
except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
    from runner import Case, kiem_tra, kiem_tra_gia_tri

TIEU_DE_THO = "thoi_gian_s,toc_do_kmh,khoang_cach_m,ax"


def _tien_ich():
    try:
        from . import tien_ich_du_lieu
    except ImportError:  # khi chạy trực tiếp trong Colab, không qua package
        import tien_ich_du_lieu
    return tien_ich_du_lieu


def _mo_data(ten_file):
    return open(_tien_ich().duong_dan_data(ten_file), encoding="utf-8")


def _cham_class(ten_bai, TenLop, cac_kich_ban):
    """cac_kich_ban: list (mô tả, hàm nhận class và trả về giá trị quan sát được, mong đợi | ValueError)."""
    if not isinstance(TenLop, type):
        return kiem_tra(ten_bai, None, [])
    cases = []
    for mo_ta, kich_ban, mong_doi in cac_kich_ban:
        if mong_doi is ValueError:
            cases.append(Case(args=(kich_ban,), raises=ValueError, mo_ta=mo_ta))
        else:
            cases.append(Case(args=(kich_ban,), expected=mong_doi, mo_ta=mo_ta))
    return kiem_tra(ten_bai, lambda kich_ban: kich_ban(TenLop), cases)


# --------------------------------------------------------------------------
# Bài 1: Lỗi, ngoại lệ và ghi file
# --------------------------------------------------------------------------

def kiem_tra_1_1(ham) -> bool:
    """doc_so(chuoi) -> float, hoặc None nếu không đọc được. Bỏ khoảng trắng hai đầu, dấu phẩy thành dấu chấm."""
    return kiem_tra(
        "Bài 1.1 - Đọc một ô số",
        ham,
        [
            Case(args=("12.5",), expected=12.5, mo_ta='doc_so("12.5")'),
            Case(args=(" 7 ",), expected=7.0, mo_ta='doc_so(" 7 ") - có khoảng trắng hai đầu'),
            Case(args=("40,5",), expected=40.5, mo_ta='doc_so("40,5") - dấu phẩy thập phân'),
            Case(args=("-3.00",), expected=-3.0, mo_ta='doc_so("-3.00") - số âm vẫn đọc được'),
            Case(args=("N/A",), expected=None, mo_ta='doc_so("N/A")'),
            Case(args=("ERR",), expected=None, mo_ta='doc_so("ERR")'),
            Case(args=("",), expected=None, mo_ta='doc_so("") - ô trống'),
        ],
    )


def kiem_tra_1_2(ham) -> bool:
    """phan_loai_dong(dong) -> "OK" | "THIEU_COT" | "SAI_SO". Chỉ xét định dạng, không xét giá trị có hợp lý không."""
    return kiem_tra(
        "Bài 1.2 - Phân loại một dòng log",
        ham,
        [
            Case(args=("12.30,40,8.20,0.010\n",), expected="OK", mo_ta='phan_loai_dong("12.30,40,8.20,0.010\\n")'),
            Case(args=("12.50,40",), expected="THIEU_COT", mo_ta='phan_loai_dong("12.50,40") - dòng bị cắt'),
            Case(args=("2.80\n",), expected="THIEU_COT", mo_ta='phan_loai_dong("2.80\\n") - chỉ còn 1 cột'),
            Case(args=("12.60,N/A,8.20,0.010",), expected="SAI_SO", mo_ta='phan_loai_dong("12.60,N/A,8.20,0.010")'),
            Case(args=("12.70,40,,0.010",), expected="SAI_SO", mo_ta='phan_loai_dong("12.70,40,,0.010") - ô trống'),
            Case(args=(TIEU_DE_THO + "\n",), expected="SAI_SO", mo_ta="phan_loai_dong(dòng tiêu đề)"),
            Case(args=("16.10,2,-3.00,0.552",), expected="OK",
                 mo_ta='phan_loai_dong("16.10,2,-3.00,0.552") - số vô lý nhưng đúng định dạng'),
        ],
    )


def kiem_tra_1_3(ham) -> bool:
    """kiem_tra_mau(toc_do_kmh, khoang_cach_m) -> True, hoặc raise ValueError với thông báo đúng như đề."""

    def ham_cham(toc_do_kmh, khoang_cach_m):
        try:
            return ham(toc_do_kmh, khoang_cach_m)
        except ValueError as loi:
            return f"ValueError: {loi}"

    return kiem_tra(
        "Bài 1.3 - Kiểm tra giá trị hợp lý",
        ham_cham if callable(ham) else ham,
        [
            Case(args=(40, 8.2), expected=True, mo_ta="kiem_tra_mau(40, 8.2)"),
            Case(args=(0, 12.0), expected=True, mo_ta="kiem_tra_mau(0, 12.0) - đúng biên vẫn hợp lệ"),
            Case(args=(250, 0.1), expected=True, mo_ta="kiem_tra_mau(250, 0.1) - đúng biên vẫn hợp lệ"),
            Case(args=(40, -3.0), expected="ValueError: khoang_cach ngoai tam", mo_ta="kiem_tra_mau(40, -3.0)"),
            Case(args=(40, 15.5), expected="ValueError: khoang_cach ngoai tam", mo_ta="kiem_tra_mau(40, 15.5)"),
            Case(args=(900, 8.2), expected="ValueError: toc_do ngoai tam", mo_ta="kiem_tra_mau(900, 8.2)"),
            Case(args=(-5, 8.2), expected="ValueError: toc_do ngoai tam", mo_ta="kiem_tra_mau(-5, 8.2)"),
            Case(args=(900, -3.0), expected="ValueError: toc_do ngoai tam",
                 mo_ta="kiem_tra_mau(900, -3.0) - cả hai sai, báo tốc độ trước"),
        ],
    )


def _dap_an_1_4():
    hop_le = []
    dem = {"THIEU_COT": 0, "SAI_SO": 0, "NGOAI_TAM": 0}
    with _mo_data("nhat_ky_tho.csv") as f:
        next(f)
        for dong in f:
            cot = dong.strip().split(",")
            try:
                so = [float(cot[i]) for i in range(4)]
            except IndexError:
                dem["THIEU_COT"] += 1
                continue
            except ValueError:
                dem["SAI_SO"] += 1
                continue
            if 0 <= so[1] <= 250 and 0.1 <= so[2] <= 12.0:
                hop_le.append(so)
            else:
                dem["NGOAI_TAM"] += 1
    return hop_le, dem


def _doc_file_sach():
    """Đọc lại nhat_ky_sach.csv học viên ghi ở thư mục làm việc: (tiêu đề, list các dòng số)."""
    duong_dan = Path.cwd() / "nhat_ky_sach.csv"
    if not duong_dan.is_file():
        return "chưa có file nhat_ky_sach.csv ở thư mục làm việc"
    with open(duong_dan, encoding="utf-8", newline="") as f:
        cac_dong = [d for d in csv.reader(f) if d]
    if not cac_dong:
        return "file nhat_ky_sach.csv rỗng"
    try:
        so = [[round(float(o), 6) for o in d] for d in cac_dong[1:]]
    except ValueError as loi:
        return f"có ô không phải số: {loi}"
    return ",".join(cac_dong[0]), so


def kiem_tra_1_4(so_dong_hop_le, so_loi_theo_loai) -> bool:
    """so_dong_hop_le, so_loi_theo_loai -> đếm từ nhat_ky_tho.csv; file nhat_ky_sach.csv gồm tiêu đề và dòng hợp lệ."""
    hop_le, dem = _dap_an_1_4()
    mong_doi_file = (TIEU_DE_THO, [[round(x, 6) for x in d] for d in hop_le])
    return kiem_tra_gia_tri(
        "Bài 1.4 - Làm sạch log thô",
        [
            ("so_dong_hop_le (nhat_ky_tho.csv)", so_dong_hop_le, len(hop_le)),
            ("so_loi_theo_loai (nhat_ky_tho.csv)", so_loi_theo_loai, dem),
            ("file nhat_ky_sach.csv (tiêu đề + các dòng hợp lệ)", _doc_file_sach(), mong_doi_file),
        ],
    )


# --------------------------------------------------------------------------
# Bài 2: Từ dict đến class
# --------------------------------------------------------------------------

def _ba_thuoc_tinh(m):
    return (m.thoi_gian_s, m.toc_do_kmh, m.khoang_cach_m)


def kiem_tra_2_1(MauCamBien) -> bool:
    """class MauCamBien: __init__(self, thoi_gian_s, toc_do_kmh, khoang_cach_m) lưu ba thuộc tính cùng tên."""

    def hai_object(L):
        a, b = L(113.0, 29, 7.36), L(0.0, 0, 12.0)
        return _ba_thuoc_tinh(a), _ba_thuoc_tinh(b)

    return _cham_class("Bài 2.1 - Class MauCamBien", MauCamBien, [
        ("MauCamBien(113.0, 29, 7.36): ba thuộc tính",
         lambda L: _ba_thuoc_tinh(L(113.0, 29, 7.36)), (113.0, 29, 7.36)),
        ("MauCamBien(5.0, 12, None): khoảng cách None vẫn lưu được",
         lambda L: _ba_thuoc_tinh(L(5.0, 12, None)), (5.0, 12, None)),
        ("hai object giữ giá trị riêng", hai_object, ((113.0, 29, 7.36), (0.0, 0, 12.0))),
    ])


def _dap_an_2_2():
    return [(t, toc_do, khoang_cach) for t, khoang_cach, toc_do, pin in _tien_ich().doc_chuyen_xe()]


def kiem_tra_2_2(danh_sach_mau) -> bool:
    """danh_sach_mau -> list 181 object MauCamBien(t, toc_do, khoang_cach) theo thứ tự giây của doc_chuyen_xe()."""
    dap_an = _dap_an_2_2()

    def xem(i):
        if not isinstance(danh_sach_mau, list) or len(danh_sach_mau) <= i:
            return None
        m = danh_sach_mau[i]
        try:
            return (type(m).__name__,) + _ba_thuoc_tinh(m)
        except AttributeError as loi:
            return f"thiếu thuộc tính: {loi}"

    return kiem_tra_gia_tri(
        "Bài 2.2 - Danh sách mẫu của chuyến xe",
        [
            ("len(danh_sach_mau)", len(danh_sach_mau) if isinstance(danh_sach_mau, list) else danh_sach_mau,
             len(dap_an)),
            ("danh_sach_mau[0] (giây 0)", xem(0), ("MauCamBien",) + dap_an[0]),
            ("danh_sach_mau[113] (giây 113, vừa phanh gấp)", xem(113), ("MauCamBien",) + dap_an[113]),
            ("danh_sach_mau[180] (giây cuối)", xem(180), ("MauCamBien",) + dap_an[180]),
        ],
    )


# --------------------------------------------------------------------------
# Bài 3: Phương thức
# --------------------------------------------------------------------------

def kiem_tra_3_1(MauCamBien) -> bool:
    """MauCamBien thêm toc_do_ms() (làm tròn 2 chữ số) và co_vat_can_gan(nguong=5.0)."""
    return _cham_class("Bài 3.1 - Phương thức của MauCamBien", MauCamBien, [
        ("MauCamBien(113.0, 36, 4.2).toc_do_ms()", lambda L: L(113.0, 36, 4.2).toc_do_ms(), 10.0),
        ("MauCamBien(113.0, 29, 7.36).toc_do_ms() - làm tròn 2 chữ số",
         lambda L: L(113.0, 29, 7.36).toc_do_ms(), 8.06),
        ("MauCamBien(113.0, 36, 4.2).co_vat_can_gan()", lambda L: L(113.0, 36, 4.2).co_vat_can_gan(), True),
        ("MauCamBien(113.0, 29, 7.36).co_vat_can_gan()", lambda L: L(113.0, 29, 7.36).co_vat_can_gan(), False),
        ("MauCamBien(1.0, 0, 5.0).co_vat_can_gan() - đúng bằng ngưỡng",
         lambda L: L(1.0, 0, 5.0).co_vat_can_gan(), True),
        ("MauCamBien(113.0, 29, 7.36).co_vat_can_gan(8.0) - ngưỡng khác",
         lambda L: L(113.0, 29, 7.36).co_vat_can_gan(8.0), True),
        ("MauCamBien(5.0, 12, None).co_vat_can_gan() - không có khoảng cách",
         lambda L: L(5.0, 12, None).co_vat_can_gan(), False),
    ])


def _pin_xa_roi_sac(L):
    p = L(15.8)
    p.xa(1.0)
    sau_xa, can = round(p.muc_pct, 6), p.can_sac()
    p.sac(90)
    return sau_xa, can, round(p.muc_pct, 6)


def kiem_tra_3_2(Pin) -> bool:
    """class Pin: muc_pct, xa(luong) không xuống dưới 0, sac(luong) không quá 100, can_sac() khi muc_pct < 15."""

    def xa_qua(L):
        p = L(3)
        p.xa(10)
        return p.muc_pct

    return _cham_class("Bài 3.2 - Class Pin", Pin, [
        ("Pin(15.8): xa(1.0), can_sac(), rồi sac(90) -> (muc sau xa, can_sac, muc sau sac)",
         _pin_xa_roi_sac, (14.8, True, 100)),
        ("Pin(3).xa(10) -> muc_pct không âm", xa_qua, 0),
        ("Pin(50).can_sac()", lambda L: L(50).can_sac(), False),
        ("Pin(15).can_sac() - đúng 15 thì chưa cần sạc", lambda L: L(15).can_sac(), False),
        ("Pin(14.9).can_sac()", lambda L: L(14.9).can_sac(), True),
    ])


def kiem_tra_3_3(Xe) -> bool:
    """class Xe(bien_so, odo_km=0): cap_nhat_odo(gia_tri) không cho lùi, di_them(km) không nhận số âm."""

    def kich_ban(*buoc):
        def chay(L):
            xe = L("30A-12345", 120)
            ket_qua = None
            for ten, gia_tri in buoc:
                ket_qua = getattr(xe, ten)(gia_tri)
            return ket_qua, round(xe.odo_km, 6)
        return chay

    return _cham_class("Bài 3.3 - Class Xe", Xe, [
        ('Xe("30A-12345").odo_km - mặc định 0', lambda L: L("30A-12345").odo_km, 0),
        ("odo 120, cap_nhat_odo(50) -> (kết quả, odo)", kich_ban(("cap_nhat_odo", 50)), (False, 120)),
        ("odo 120, cap_nhat_odo(150)", kich_ban(("cap_nhat_odo", 150)), (True, 150)),
        ("odo 120, cap_nhat_odo(120) - bằng odo hiện tại vẫn nhận", kich_ban(("cap_nhat_odo", 120)), (True, 120)),
        ("odo 120, di_them(1.3)", kich_ban(("di_them", 1.3)), (True, 121.3)),
        ("odo 120, di_them(-2)", kich_ban(("di_them", -2)), (False, 120)),
        ("odo 120, di_them(10) rồi cap_nhat_odo(125)",
         kich_ban(("di_them", 10), ("cap_nhat_odo", 125)), (False, 130)),
    ])


# --------------------------------------------------------------------------
# Bài 4: Object đáng tin và dễ đọc
# --------------------------------------------------------------------------

def kiem_tra_4_1(Pin) -> bool:
    """Pin: __init__ raise ValueError khi muc_pct ngoài 0-100; __str__ trả "Pin {muc_pct}%"; vẫn giữ xa/sac/can_sac."""
    return _cham_class("Bài 4.1 - Pin kiểm tra dữ liệu và in được", Pin, [
        ("Pin(120) -> ValueError", lambda L: L(120), ValueError),
        ("Pin(-1) -> ValueError", lambda L: L(-1), ValueError),
        ("str(Pin(15.8))", lambda L: str(L(15.8)), "Pin 15.8%"),
        ("str(Pin(100)) - đúng biên vẫn tạo được", lambda L: str(L(100)), "Pin 100%"),
        ("str(Pin(0)) - đúng biên vẫn tạo được", lambda L: str(L(0)), "Pin 0%"),
        ("Pin(15.8): xa(1.0), can_sac(), sac(90) vẫn đúng như bài 3.2", _pin_xa_roi_sac, (14.8, True, 100)),
    ])


def kiem_tra_4_2(NhatKyLoi) -> bool:
    """class NhatKyLoi(ten_xe): ban_ghi riêng từng object, ghi(ma_loi, thoi_gian_s), so_lan(ma_loi)."""

    def hai_nhat_ky(L):
        a, b = L("xe A"), L("xe B")
        a.ghi("P0113", 3.4)
        a.ghi("P0113", 21.8)
        b.ghi("C0035", 113.2)
        return a, b

    return _cham_class("Bài 4.2 - Class NhatKyLoi", NhatKyLoi, [
        ("a ghi P0113 hai lần: a.so_lan('P0113')", lambda L: hai_nhat_ky(L)[0].so_lan("P0113"), 2),
        ("b chưa ghi P0113: b.so_lan('P0113') - không dính bản ghi của a",
         lambda L: hai_nhat_ky(L)[1].so_lan("P0113"), 0),
        ("b.so_lan('C0035')", lambda L: hai_nhat_ky(L)[1].so_lan("C0035"), 1),
        ("a.ban_ghi", lambda L: hai_nhat_ky(L)[0].ban_ghi, [("P0113", 3.4), ("P0113", 21.8)]),
        ("b.ban_ghi", lambda L: hai_nhat_ky(L)[1].ban_ghi, [("C0035", 113.2)]),
        ("nhật ký mới tạo: so_lan('P0562')", lambda L: L("xe C").so_lan("P0562"), 0),
    ])


# --------------------------------------------------------------------------
# Bài 5: Object chứa object
# --------------------------------------------------------------------------

def kiem_tra_5_1(ChuyenXe) -> bool:
    """class ChuyenXe(): danh_sach_mau rỗng, them(mau), so_mau(), toc_do_max() (None khi chưa có mẫu)."""

    def ba_mau(L):
        cx = L()
        for v in (0, 65, 42):
            cx.them(SimpleNamespace(thoi_gian_s=0.0, toc_do_kmh=v, khoang_cach_m=12.0))
        return cx.so_mau(), cx.toc_do_max()

    def hai_chuyen(L):
        a, b = L(), L()
        a.them(SimpleNamespace(thoi_gian_s=0.0, toc_do_kmh=5, khoang_cach_m=12.0))
        return b.so_mau()

    return _cham_class("Bài 5.1 - Class ChuyenXe", ChuyenXe, [
        ("ChuyenXe().so_mau() - chưa có mẫu", lambda L: L().so_mau(), 0),
        ("ChuyenXe().toc_do_max() - chưa có mẫu", lambda L: L().toc_do_max(), None),
        ("thêm 3 mẫu tốc độ 0, 65, 42 -> (so_mau, toc_do_max)", ba_mau, (3, 65)),
        ("hai chuyến xe: thêm mẫu vào chuyến a, chuyến b vẫn 0 mẫu", hai_chuyen, 0),
    ])


def _dap_an_5_2():
    giay_gan, nhanh = [], None
    for t, khoang_cach, toc_do, pin in _tien_ich().doc_chuyen_xe():
        if khoang_cach is not None and khoang_cach <= 5.0:
            giay_gan.append(t)
        if nhanh is None or toc_do > nhanh[1]:
            nhanh = (t, toc_do)
    return giay_gan, nhanh


def kiem_tra_5_2(chuyen_xe) -> bool:
    """chuyen_xe -> ChuyenXe chứa 181 mẫu; giay_vat_can_gan(), mau_nhanh_nhat() (mẫu đầu tiên có tốc độ lớn nhất)."""
    giay_gan, nhanh = _dap_an_5_2()

    def goi(ten):
        if chuyen_xe is None:
            return None
        try:
            return getattr(chuyen_xe, ten)()
        except Exception as loi:  # noqa: BLE001 - in lỗi cho học viên đọc
            return f"lỗi {type(loi).__name__}: {loi}"

    nhanh_nhat = goi("mau_nhanh_nhat")
    if nhanh_nhat is not None and not isinstance(nhanh_nhat, str):
        nhanh_nhat = (getattr(nhanh_nhat, "thoi_gian_s", None), getattr(nhanh_nhat, "toc_do_kmh", None))
    return kiem_tra_gia_tri(
        "Bài 5.2 - Phân tích chuyến xe bằng object",
        [
            ("chuyen_xe.so_mau()", goi("so_mau"), 181),
            ("chuyen_xe.giay_vat_can_gan()", goi("giay_vat_can_gan"), giay_gan),
            ("chuyen_xe.mau_nhanh_nhat() -> (thoi_gian_s, toc_do_kmh)", nhanh_nhat, nhanh),
        ],
    )


# --------------------------------------------------------------------------
# Dự án tuần 3 - Budget App (giữ nguyên kịch bản của khoá cũ)
# --------------------------------------------------------------------------

def _chay_kich_ban_hm(TenLop, so_kich_ban):
    if so_kich_ban == 1:
        hm = TenLop("An uong")
        hm.nap_tien(500000)
        return hm.so_du()
    if so_kich_ban == 2:
        hm = TenLop("An uong")
        hm.nap_tien(500000)
        hm.rut_tien(200000)
        return hm.so_du()
    if so_kich_ban == 3:
        hm = TenLop("An uong")
        hm.nap_tien(100000)
        thanh_cong = hm.rut_tien(200000)
        return (thanh_cong, hm.so_du())
    if so_kich_ban == 4:
        a = TenLop("Xang xe")
        b = TenLop("Sua chua")
        a.nap_tien(300000)
        a.chuyen_tien(b, 100000)
        return (a.so_du(), b.so_du())
    if so_kich_ban == 5:
        hm = TenLop("Giai tri")
        hm.nap_tien(50000)
        return str(hm)
    raise ValueError(f"kịch bản không hợp lệ: {so_kich_ban}")


def kiem_tra_du_an(TenLop) -> bool:
    """class HangMuc (Category).

    __init__(self, ten)
    nap_tien(self, so_tien, mo_ta="") -> None
    rut_tien(self, so_tien, mo_ta="") -> bool (False và KHÔNG trừ nếu không đủ tiền)
    chuyen_tien(self, hang_muc_khac, so_tien) -> bool
    so_du(self) -> tổng các giao dịch trong ledger
    __str__(self) -> "{ten}: {so_du} VND"
    """
    ham = (lambda so: _chay_kich_ban_hm(TenLop, so)) if isinstance(TenLop, type) else None
    return kiem_tra(
        "Dự án tuần 3 - Budget App (Category)",
        ham,
        [
            Case(args=(1,), expected=500000, mo_ta="nạp tiền"),
            Case(args=(2,), expected=300000, mo_ta="nạp rồi rút"),
            Case(args=(3,), expected=(False, 100000), mo_ta="rút vượt số dư -> thất bại"),
            Case(args=(4,), expected=(200000, 100000), mo_ta="chuyển tiền giữa 2 hạng mục"),
            Case(args=(5,), expected="Giai tri: 50000 VND", mo_ta="định dạng chuỗi qua __str__"),
        ],
    )
