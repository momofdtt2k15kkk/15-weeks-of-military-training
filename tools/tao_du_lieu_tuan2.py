"""Sinh data/ma_loi.csv, nhật ký mã lỗi chẩn đoán (DTC) của chuyến xe trong tuần 2.

Chạy từ thư mục gốc repo:
    python tools/tao_du_lieu_tuan2.py

Dữ liệu mô phỏng, khớp thời điểm với bốn file của chuyến xe do tools/tao_du_lieu.py sinh:
mã lỗi xuất hiện đúng lúc có sự kiện tương ứng (phanh gấp lúc 113 giây, pin tụt dưới 15% lúc 165 giây).
Không dùng số ngẫu nhiên, chạy lại cho ra đúng từng byte.
"""

from __future__ import annotations

import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent

# (giây, mã lỗi). Xếp theo thời gian, cùng một mã có thể lặp lại.
SU_KIEN = [
    (3.40, "P0113"),    # cảm biến nhiệt độ khí nạp, tín hiệu cao, nhiễu lẻ tẻ lúc xe mới nổ máy
    (21.80, "P0113"),
    (47.10, "P0113"),
    (83.60, "P0113"),
    (113.20, "C0035"),  # cảm biến tốc độ bánh trước trái, nhiễu khi phanh gấp lúc 113.1 giây
    (113.40, "U0121"),  # mất kết nối với module ABS
    (113.90, "C0035"),
    (114.20, "U0121"),
    (114.60, "C0035"),
    (165.30, "P0562"),  # điện áp hệ thống thấp, pin dưới 15% từ giây 165
    (167.80, "P0562"),
    (170.30, "P0562"),
    (172.80, "P0562"),
    (175.30, "P0562"),
    (177.80, "P0562"),
]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    dong = ["thoi_gian_s,ma_loi"] + [f"{t:.2f},{ma}" for t, ma in SU_KIEN]
    duong_dan = GOC / "data" / "ma_loi.csv"
    duong_dan.parent.mkdir(exist_ok=True)
    with open(duong_dan, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(dong) + "\n")
    print(f"Đã ghi {duong_dan} ({len(SU_KIEN)} dòng dữ liệu)")


if __name__ == "__main__":
    main()
