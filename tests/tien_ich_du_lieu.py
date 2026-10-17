"""Hàm đọc, đồng bộ và vẽ dữ liệu chuyến xe, viết sẵn cho học viên dùng.

  - doc_chuyen_xe(): đọc các file trong data/, đồng bộ về 1 Hz.
  - ve_chuyen_xe(ham_quyet_dinh): vẽ kết quả của một hàm quyết định lên chuyến xe.
  - nmea_sang_do, khoang_cach_hai_diem_m: đổi toạ độ NMEA, đo khoảng cách hai điểm GPS.
  - ve_phan_tich_chuyen_xe(...): vẽ tốc độ đã làm mượt, các giây có vật cản gần và số giây theo mã fix GPS.
  - ve_so_du_hang_muc(cac_hang_muc): vẽ số dư của các hạng mục ngân sách (dự án tuần 3).
"""

from __future__ import annotations

import csv
import math
import statistics
from pathlib import Path

TAM_TOI_DA_M = 12.0
MAU_THEO_LENH = {
    "DUNG_KHAN_CAP": "red",
    "VE_TRAM_SAC": "orange",
    "GIAM_TOC": "gold",
    "BINH_THUONG": "green",
}


def duong_dan_data(ten_file: str) -> Path:
    """Tìm file trong data/, chạy được ở Colab (thư mục làm việc) và trên GitHub Actions."""
    goc_tests = Path(__file__).resolve().parent.parent
    for thu_muc in (Path.cwd() / "data", Path.cwd().parent / "data", goc_tests / "data"):
        duong_dan = thu_muc / ten_file
        if duong_dan.is_file():
            return duong_dan
    raise FileNotFoundError(f"Không tìm thấy data/{ten_file}. Chạy lại ô thiết lập ở đầu notebook.")


def _khoang_cach_theo_giay() -> dict[int, list[float]]:
    """Gom các mẫu LiDAR hợp lệ (mét) theo từng giây, bỏ dòng ô trống và dòng 0.0."""
    cac_mau: dict[int, list[float]] = {}
    with open(duong_dan_data("khoang_cach_truoc.csv"), encoding="utf-8") as f:
        next(f)
        for dong in f:
            thoi_gian, _, o_khoang_cach = dong.strip().partition(",")
            if o_khoang_cach == "" or float(o_khoang_cach) == 0.0:
                continue
            cac_mau.setdefault(int(float(thoi_gian)), []).append(float(o_khoang_cach) / 100)
    return cac_mau


def doc_chuyen_xe():
    """Mỗi lần lặp trả về (t, khoang_cach_m, toc_do_kmh, muc_pin_pct) của một giây.

    khoang_cach_m là trung vị các mẫu LiDAR hợp lệ trong giây đó, None nếu không có mẫu nào.
    """
    cac_mau = _khoang_cach_theo_giay()
    with open(duong_dan_data("obd.csv"), encoding="utf-8") as f:
        for hang in csv.DictReader(f):
            t = int(float(hang["thoi_gian_s"]))
            mau_giay = cac_mau.get(t)
            khoang_cach = statistics.median(mau_giay) if mau_giay else None
            yield t, khoang_cach, int(hang["toc_do_kmh"]), float(hang["muc_pin_pct"])


def _nmea_sang_do(chuoi: str) -> float:
    x = float(chuoi)
    return x // 100 + (x % 100) / 60


def _quy_dao_gps() -> dict[int, tuple[float, float]]:
    """Giây thứ k -> (đông, bắc) tính bằng mét so với điểm xuất phát. Bỏ giây mất fix."""
    diem: dict[int, tuple[float, float]] = {}
    goc = None
    giay = -1
    with open(duong_dan_data("gps.nmea"), encoding="utf-8") as f:
        for dong in f:
            if not dong.startswith("$GNGGA"):
                continue
            giay += 1
            cot = dong.split(",")
            if cot[2] == "" or cot[4] == "":
                continue
            vi_do, kinh_do = _nmea_sang_do(cot[2]), _nmea_sang_do(cot[4])
            if goc is None:
                goc = (vi_do, kinh_do)
            bac = (vi_do - goc[0]) * 111320.0
            dong_m = (kinh_do - goc[1]) * 111320.0 * math.cos(math.radians(goc[0]))
            diem[giay] = (dong_m, bac)
    return diem


def ve_chuyen_xe(ham_quyet_dinh) -> None:
    """Vẽ hai hình cạnh nhau, màu theo lệnh mà ham_quyet_dinh(khoang_cach, toc_do, muc_pin) trả về.

    Trái: tốc độ và khoảng cách theo thời gian. Phải: quỹ đạo GPS.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    ban_ghi = list(doc_chuyen_xe())
    lenh = [None if kc is None else ham_quyet_dinh(kc, v, pin) for _, kc, v, pin in ban_ghi]
    if all(l is None for l in lenh):
        print("Xong hàm quyết định rồi chạy lại ô này để xem hình.")
        return

    fig, (hinh_trai, hinh_phai) = plt.subplots(1, 2, figsize=(14, 5))

    for (t, _, _, _), l in zip(ban_ghi, lenh):
        hinh_trai.axvspan(t, t + 1, color=MAU_THEO_LENH.get(l, "lightgray"), alpha=0.3, linewidth=0)
    thoi_gian = [b[0] for b in ban_ghi]
    hinh_trai.plot(thoi_gian, [b[2] for b in ban_ghi], color="tab:blue")
    hinh_trai.set_xlabel("Thời gian (s)")
    hinh_trai.set_ylabel("Tốc độ (km/h)", color="tab:blue")
    truc_kc = hinh_trai.twinx()
    truc_kc.plot(thoi_gian, [float("nan") if b[1] is None else b[1] for b in ban_ghi],
                 color="black", linewidth=1)
    truc_kc.set_ylabel("Khoảng cách phía trước (m)")
    truc_kc.set_ylim(0, TAM_TOI_DA_M + 1)
    hinh_trai.set_title("Tốc độ và khoảng cách, nền tô màu theo lệnh")

    quy_dao = _quy_dao_gps()
    for (t, _, _, _), l in zip(ban_ghi, lenh):
        if t in quy_dao:
            uu_tien = list(MAU_THEO_LENH).index(l) if l in MAU_THEO_LENH else len(MAU_THEO_LENH)
            hinh_phai.scatter(*quy_dao[t], color=MAU_THEO_LENH.get(l, "lightgray"), s=25,
                              zorder=len(MAU_THEO_LENH) - uu_tien)    # lệnh nghiêm trọng vẽ lên trên
    hinh_phai.set_xlabel("Hướng Đông (m)")
    hinh_phai.set_ylabel("Hướng Bắc (m)")
    hinh_phai.set_aspect("equal")
    hinh_phai.set_title("Quỹ đạo GPS theo lệnh")
    hinh_phai.legend(handles=[Patch(color=m, label=ten) for ten, m in MAU_THEO_LENH.items()],
                     loc="lower left", fontsize=8)

    fig.tight_layout()
    plt.show()


TEN_MA_FIX = {0: "Không fix", 1: "GPS", 2: "DGPS", 4: "RTK fixed", 5: "RTK float"}


def nmea_sang_do(chuoi: str, huong: str) -> float | None:
    """Đổi toạ độ NMEA dạng ddmm.mmmmm hoặc dddmm.mmmmm sang độ thập phân, hướng S và W là số âm."""
    if chuoi == "":
        return None
    do = _nmea_sang_do(chuoi)
    return -do if huong in ("S", "W") else do


def khoang_cach_hai_diem_m(diem_a, diem_b) -> float:
    """Khoảng cách (mét) giữa hai điểm (t, vi_do, kinh_do), xấp xỉ mặt phẳng, đủ chính xác trong vài km."""
    _, vi_do_a, kinh_do_a = diem_a
    _, vi_do_b, kinh_do_b = diem_b
    bac = (vi_do_b - vi_do_a) * 111320.0
    dong = (kinh_do_b - kinh_do_a) * 111320.0 * math.cos(math.radians(vi_do_a))
    return math.hypot(dong, bac)


def ve_phan_tich_chuyen_xe(toc_do_theo_giay, toc_do_muot, giay_vat_can_gan, so_giay_theo_fix) -> None:
    """Vẽ hai hình cạnh nhau từ các list và dict học viên vừa tính.

    Trái: tốc độ từng giây (mờ), tốc độ đã làm mượt (đậm), nền đỏ ở các giây có vật cản gần.
    Phải: số giây của từng mã fix GPS.
    toc_do_muot ngắn hơn toc_do_theo_giay k - 1 phần tử, mỗi giá trị đặt ở giây cuối của cửa sổ.
    """
    import matplotlib.pyplot as plt

    if (not toc_do_theo_giay or toc_do_muot is None or giay_vat_can_gan is None
            or so_giay_theo_fix is None):
        print("Làm xong các biến của bài rồi chạy lại ô này để xem hình.")
        return

    fig, (hinh_trai, hinh_phai) = plt.subplots(1, 2, figsize=(14, 5))

    so_mau_cua_so = len(toc_do_theo_giay) - len(toc_do_muot) + 1
    hinh_trai.plot(range(len(toc_do_theo_giay)), toc_do_theo_giay, color="tab:blue", alpha=0.35,
                   label="Tốc độ từng giây")
    hinh_trai.plot(range(so_mau_cua_so - 1, len(toc_do_theo_giay)), toc_do_muot, color="tab:blue",
                   linewidth=2, label=f"Trung bình {so_mau_cua_so} giây gần nhất")
    for t in giay_vat_can_gan:
        hinh_trai.axvspan(t, t + 1, color="red", alpha=0.25, linewidth=0)
    hinh_trai.set_xlabel("Thời gian (s)")
    hinh_trai.set_ylabel("Tốc độ (km/h)")
    hinh_trai.set_title("Tốc độ và các giây có vật cản trong 5 m (nền đỏ)")
    hinh_trai.legend(loc="upper left", fontsize=8)

    ma_fix = sorted(so_giay_theo_fix)
    hinh_phai.bar([TEN_MA_FIX.get(m, str(m)) for m in ma_fix], [so_giay_theo_fix[m] for m in ma_fix],
                  color="tab:green")
    hinh_phai.set_ylabel("Số giây")
    hinh_phai.set_title("Số giây theo mã fix GPS")

    fig.tight_layout()
    plt.show()


def ve_so_du_hang_muc(cac_hang_muc) -> None:
    """Vẽ cột số dư của từng hạng mục. Mỗi phần tử cần có thuộc tính `ten` và phương thức `so_du()`."""
    import matplotlib.pyplot as plt

    try:
        ten = [hm.ten for hm in cac_hang_muc]
        so_du = [hm.so_du() for hm in cac_hang_muc]
    except Exception:  # noqa: BLE001 - class của học viên chưa xong thì chỉ nhắc
        so_du = [None]
    if any(not isinstance(s, (int, float)) for s in so_du):
        print("Làm xong class HangMuc rồi chạy lại ô này để xem hình.")
        return

    fig, truc = plt.subplots(figsize=(7, 4))
    cot = truc.bar(ten, so_du, color="tab:blue")
    truc.bar_label(cot, labels=[f"{s:,.0f}" for s in so_du])
    truc.set_ylabel("Số dư (VND)")
    truc.set_title("Số dư các hạng mục ngân sách")
    fig.tight_layout()
    plt.show()
