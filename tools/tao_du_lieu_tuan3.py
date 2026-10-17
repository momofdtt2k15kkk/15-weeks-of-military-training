"""Sinh data/nhat_ky_tho.csv, log thô của chuyến xe dùng cho tuần 3 (xử lý lỗi khi đọc file).

Chạy từ thư mục gốc repo:
    python tools/tao_du_lieu_tuan3.py

Giá trị lấy từ 4 file của tuần 1 (obd.csv, khoang_cach_truoc.csv, imu.csv), gộp về 10 mẫu mỗi giây, nên khớp
mọi sự kiện của chuyến xe. Sau đó làm hỏng có chủ đích khoảng 5% số dòng, seed cố định, chạy lại cho ra đúng
từng byte. Không đọc hay ghi file nào khác trong data/.
"""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
DATA = GOC / "data"
SEED = 2026
TIEU_DE = "thoi_gian_s,toc_do_kmh,khoang_cach_m,ax"

SO_O_HONG = 30        # một ô ghi N/A, ERR hoặc để trống
SO_DONG_CUT = 15      # dòng bị cắt ngang
SO_NGOAI_TAM = 20     # đọc được số nhưng giá trị vô lý
VI_TRI_TIEU_DE_LAP = (612, 1407)   # log khởi động lại, tiêu đề lặp giữa file


def doc_toc_do() -> dict[int, int]:
    with open(DATA / "obd.csv", encoding="utf-8") as f:
        return {round(float(h["thoi_gian_s"])): int(h["toc_do_kmh"]) for h in csv.DictReader(f)}


def doc_khoang_cach() -> dict[int, float]:
    """Khoá là số phần trăm giây (t * 100). Mẫu lỗi của LiDAR thay bằng mẫu hợp lệ gần nhất phía trước."""
    ket_qua, truoc = {}, 12.0
    with open(DATA / "khoang_cach_truoc.csv", encoding="utf-8") as f:
        for h in csv.DictReader(f):
            o = h["khoang_cach_cm"]
            if o != "" and float(o) != 0.0:
                truoc = float(o) / 100
            ket_qua[round(float(h["thoi_gian_s"]) * 100)] = truoc
    return ket_qua


def doc_ax() -> dict[int, float]:
    with open(DATA / "imu.csv", encoding="utf-8") as f:
        return {round(float(h["thoi_gian_s"]) * 100): float(h["ax"]) for h in csv.DictReader(f)}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    toc_do, khoang_cach, ax = doc_toc_do(), doc_khoang_cach(), doc_ax()

    dong = []
    for i in range(1801):                       # 0.0 đến 180.0 giây, bước 0.1
        k = i * 10                              # phần trăm giây
        dong.append(f"{k / 100:.2f},{toc_do[k // 100]},{khoang_cach[k]:.2f},{ax[k]:.3f}")

    rs = random.Random(SEED)
    vi_tri = rs.sample(range(5, len(dong)), SO_O_HONG + SO_DONG_CUT + SO_NGOAI_TAM)
    o_hong = vi_tri[:SO_O_HONG]
    dong_cut = vi_tri[SO_O_HONG:SO_O_HONG + SO_DONG_CUT]
    ngoai_tam = vi_tri[SO_O_HONG + SO_DONG_CUT:]

    for i in o_hong:
        cot = dong[i].split(",")
        cot[rs.choice((1, 2, 3))] = rs.choice(("N/A", "ERR", ""))
        dong[i] = ",".join(cot)
    for i in dong_cut:
        dong[i] = ",".join(dong[i].split(",")[:rs.choice((1, 2, 3))])
    for i in ngoai_tam:
        cot = dong[i].split(",")
        if rs.random() < 0.5:
            cot[2] = rs.choice(("-3.00", "0.00", "15.50"))       # ngoài tầm LiDAR 0.1 - 12 m
        else:
            cot[1] = rs.choice(("900", "-5"))                   # ngoài tầm tốc độ 0 - 250 km/h
        dong[i] = ",".join(cot)

    for i in sorted(VI_TRI_TIEU_DE_LAP, reverse=True):
        dong.insert(i, TIEU_DE)

    duong_dan = DATA / "nhat_ky_tho.csv"
    with open(duong_dan, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join([TIEU_DE] + dong) + "\n")
    print(f"Đã ghi {duong_dan}: {len(dong)} dòng dữ liệu, {SO_O_HONG} ô hỏng, {SO_DONG_CUT} dòng cụt, "
          f"{SO_NGOAI_TAM} dòng ngoài tầm, {len(VI_TRI_TIEU_DE_LAP)} tiêu đề lặp")


if __name__ == "__main__":
    main()
