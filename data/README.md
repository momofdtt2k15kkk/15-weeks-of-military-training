# Dữ liệu cảm biến của một chuyến xe

Bốn file trong thư mục này ghi lại cùng một chuyến xe dài 180 giây, cùng mốc thời gian. Cột `thoi_gian_s` là số giây tính từ lúc bắt đầu chuyến (0.00 đến 180.00).

**Đây là dữ liệu mô phỏng.** Số liệu được sinh bằng `tools/tao_du_lieu.py` theo thông số của cảm biến thật (tần số, đơn vị, mức nhiễu, lỗi hay gặp), không phải ghi từ một chiếc xe thật. Chạy lại script cho ra đúng các file này, từng byte.

Mọi cột đều suy ra từ cùng một quỹ đạo: tốc độ, quãng đường, toạ độ GPS, khoảng cách tới vật cản, gia tốc và mức pin khớp nhau giữa các file.

## Sự kiện của chuyến xe

| t (giây) | Diễn biến | Dấu hiệu trong dữ liệu |
|---|---|---|
| 0–15 | Xe đứng yên, chờ GPS | `toc_do_kmh` = 0, `rpm` ≈ 800, mã fix GPS 1 (đến 6 s) rồi 2 |
| 15–35 | Tăng tốc lên 40 km/h | `ax` dương (≈ +0.55 m/s²) |
| 35–60 | Chạy đều 40 km/h, rẽ trái lần 1 (42–52 s) | `gz` lệch dương, `ay` dương; mã fix 5 (từ 35 s) rồi 4 (từ 48 s) |
| 60–80 | Tăng tốc lên 65 km/h | `toc_do_kmh` > 60 ở giây 77 đến 81 |
| 80–100 | Giảm về 30 km/h, rẽ phải lần 2 (91–99 s) | `gz` lệch âm; GPS mất fix (mã 0) ở giây 94, 95, 96 do tán cây |
| 100–112.8 | Chạy 30 km/h | khoảng cách phía trước = tầm tối đa `1200.0` cm |
| 112.8 | Vật cản chen vào cách xe 9.0 m | `khoang_cach_cm` tụt từ 1200.0 xuống ≈ 900 |
| 113.1 | Phanh gấp | `ax` ≈ −7 m/s², tốc độ về 0, xe dừng cách vật 1.5 m |
| 114.5–135 | Đứng yên trước vật cản | `khoang_cach_cm` ≈ 152 (≤ 200) |
| 135–180 | Vật cản đi, xe chạy lại và giữ 27 km/h từ giây 148 | khoảng cách tăng trở lại tầm tối đa; `muc_pin_pct` xuống dưới 15 ở giây 165 |

Pin bắt đầu ở 15.8% và giảm đều theo quãng đường. Tốc độ tụt pin đã được nén cho vừa chuyến 3 phút, không phản ánh mức hao pin thật của xe.

Chuyến xe bắt đầu lúc `16:59:00 UTC`, tức `23:59:00` giờ Việt Nam (UTC+7), nên giờ Việt Nam qua nửa đêm ở giây 60. Điểm xuất phát gần `21.0045° N, 105.8430° E`, lộ trình đi lên hướng Bắc, rẽ trái sang hướng Tây, rồi rẽ phải lại hướng Bắc, tổng cộng khoảng 1.3 km.

## `khoang_cach_truoc.csv` — LiDAR 1D đo phía trước

Kiểu TFmini Plus, tầm đo 0.1–12 m, tần số 20 Hz, 3601 dòng dữ liệu.

| Cột | Đơn vị | Kiểu | Ý nghĩa |
|---|---|---|---|
| `thoi_gian_s` | giây | số thực, 2 chữ số thập phân | thời điểm đo |
| `khoang_cach_cm` | cm | số thực, 1 chữ số thập phân | khoảng cách tới vật gần nhất phía trước |

- Nhiễu: σ ≈ 2 cm.
- Không có vật cản trong tầm đo: đọc tầm tối đa `1200.0`.
- Lỗi cố ý, cần bỏ qua khi tính toán:
  - Khoảng 1% mẫu (36 dòng) có `khoang_cach_cm` = `0.0`: mất tín hiệu.
  - 8 dòng để trống ô khoảng cách, ví dụ `9.75,`.

## `gps.nmea` — module GNSS RTK

Tần số 1 Hz. Mỗi giây có 2 câu NMEA: `$GNRMC` rồi `$GNGGA`, tổng 362 câu. Checksum `*hh` tính đúng chuẩn NMEA (XOR các ký tự giữa `$` và `*`).

Các cột dùng trong khoá học, đếm từ 0 sau khi cắt theo dấu phẩy:

| Câu | Cột | Ý nghĩa | Ví dụ |
|---|---|---|---|
| `$GNGGA` | 1 | giờ UTC, dạng `hhmmss.ss` | `165900.00` |
| `$GNGGA` | 2 | vĩ độ, dạng `ddmm.mmmmm` | `2100.27089` |
| `$GNGGA` | 3 | hướng vĩ độ (`N`/`S`) | `N` |
| `$GNGGA` | 4 | kinh độ, dạng `dddmm.mmmmm` | `10550.57792` |
| `$GNGGA` | 5 | hướng kinh độ (`E`/`W`) | `E` |
| `$GNGGA` | 6 | mã fix | `1` |
| `$GNGGA` | 7 | số vệ tinh | `07` |
| `$GNGGA` | 8 | HDOP (độ loãng chính xác ngang) | `1.4` |
| `$GNGGA` | 9 | độ cao so với mực nước biển (m) | `11.8` |
| `$GNRMC` | 7 | tốc độ mặt đất (knot) | `18.56` |
| `$GNRMC` | 8 | hướng chạy (độ, từ hướng Bắc theo chiều kim đồng hồ), trống khi xe đứng yên | `278.2` |

Mã fix và sai số vị trí:

| Mã fix | Tên | Sai số vị trí cỡ | Thời gian trong chuyến |
|---|---|---|---|
| 0 | không có fix | — | giây 94, 95, 96 |
| 1 | GPS thường | vài mét | giây 0–5 |
| 2 | DGPS | dưới 1 m | giây 6–34 |
| 5 | RTK float | vài chục cm | giây 35–47 và 97–105 |
| 4 | RTK fixed | vài cm | giây 48–93 và 106–180 |

Khi mã fix là 0, các ô vĩ độ, kinh độ, hướng, số vệ tinh ở cả hai câu để trống, câu `$GNRMC` có trạng thái `V` thay vì `A`.

## `obd.csv` — đọc qua OBD-II

Tần số 1 Hz, 181 dòng dữ liệu.

| Cột | Đơn vị | Kiểu | Ý nghĩa |
|---|---|---|---|
| `thoi_gian_s` | giây | số thực, 2 chữ số thập phân | thời điểm đọc |
| `toc_do_kmh` | km/h | **số nguyên** | tốc độ xe (PID 0x0D, độ phân giải 1 km/h) |
| `rpm` | vòng/phút | số nguyên | tốc độ quay động cơ, ≈ 800 khi xe đứng yên |
| `muc_pin_pct` | % | số thực, 1 chữ số thập phân | mức pin còn lại |

## `imu.csv` — IMU 6 trục

Tần số 50 Hz, 9001 dòng dữ liệu. Xe chạy về phía trước theo trục x.

| Cột | Đơn vị | Kiểu | Ý nghĩa |
|---|---|---|---|
| `thoi_gian_s` | giây | số thực, 2 chữ số thập phân | thời điểm đo |
| `ax` | m/s² | số thực, 3 chữ số thập phân | gia tốc dọc xe, dương khi tăng tốc, âm khi phanh |
| `ay` | m/s² | số thực, 3 chữ số thập phân | gia tốc ngang, dương khi rẽ trái |
| `az` | m/s² | số thực, 3 chữ số thập phân | gia tốc thẳng đứng, ≈ 9.81 khi xe nằm yên |
| `gx` | độ/giây | số thực, 2 chữ số thập phân | vận tốc góc quanh trục x (nghiêng ngang) |
| `gy` | độ/giây | số thực, 2 chữ số thập phân | vận tốc góc quanh trục y (chúi đầu) |
| `gz` | độ/giây | số thực, 2 chữ số thập phân | vận tốc góc quanh trục thẳng đứng, dương khi rẽ trái |

Nhiễu: σ ≈ 0.05 m/s² với gia tốc, σ ≈ 0.1 độ/giây với vận tốc góc.

## `ma_loi.csv` — nhật ký mã lỗi chẩn đoán (DTC)

Ghi lại mỗi lần ECU báo một mã lỗi chẩn đoán qua OBD-II, 15 dòng dữ liệu. Một mã có thể được báo nhiều lần.

| Cột | Đơn vị | Kiểu | Ý nghĩa |
|---|---|---|---|
| `thoi_gian_s` | giây | số thực, 2 chữ số thập phân | thời điểm ECU báo mã lỗi |
| `ma_loi` | | chuỗi | mã lỗi chẩn đoán |

Bốn mã trong chuyến xe, đều khớp với sự kiện ở bảng đầu trang:

| Mã | Ý nghĩa | Số lần | Thời điểm (giây) |
|---|---|---|---|
| `P0113` | tín hiệu cảm biến nhiệt độ khí nạp quá cao | 4 | 3.40, 21.80, 47.10, 83.60 |
| `C0035` | mạch cảm biến tốc độ bánh xe trước trái lỗi | 3 | 113.20, 113.90, 114.60 |
| `U0121` | mất liên lạc với module ABS | 2 | 113.40, 114.20 |
| `P0562` | điện áp hệ thống thấp | 6 | 165.30 đến 177.80, cách nhau 2.5 giây |

`C0035` và `U0121` xuất hiện ngay sau lần phanh gấp lúc 113.1 giây. `P0562` bắt đầu lúc 165.30 giây, ngay sau khi `muc_pin_pct` xuống dưới 15. Sinh bằng `tools/tao_du_lieu_tuan2.py`, riêng với bốn file còn lại.

## `nhat_ky_tho.csv` — log thô gộp, có dòng hỏng

Log gộp tốc độ, khoảng cách phía trước và gia tốc dọc của cả chuyến, 10 mẫu mỗi giây (giây 0.00 đến 180.00). Giá trị lấy từ `obd.csv`, `khoang_cach_truoc.csv` và `imu.csv`, nên khớp mọi sự kiện ở bảng đầu trang. Dùng để tập đọc file có lỗi mà chương trình không dừng.

| Cột | Đơn vị | Kiểu | Ý nghĩa |
|---|---|---|---|
| `thoi_gian_s` | giây | số thực, 2 chữ số thập phân | thời điểm ghi |
| `toc_do_kmh` | km/h | số nguyên | tốc độ, lấy từ `obd.csv` của giây đó |
| `khoang_cach_m` | m | số thực, 2 chữ số thập phân | khoảng cách phía trước, lấy từ `khoang_cach_truoc.csv`, mẫu LiDAR lỗi thay bằng mẫu hợp lệ gần nhất phía trước |
| `ax` | m/s² | số thực, 3 chữ số thập phân | gia tốc dọc, lấy từ `imu.csv` |

Các dòng hỏng có chủ đích:

| Kiểu hỏng | Số dòng | Ví dụ |
|---|---|---|
| một ô ghi `N/A`, `ERR` hoặc để trống | 30 | `1.00,0,12.00,ERR` |
| dòng bị cắt ngang (mất điện), còn 1 đến 3 cột | 15 | `2.80` |
| đọc được số nhưng vô lý: khoảng cách `-3.00`, `0.00`, `15.50` m hoặc tốc độ `900`, `-5` km/h | 20 | `16.10,2,-3.00,0.552` |
| dòng tiêu đề lặp giữa file (log khởi động lại) | 2 | `thoi_gian_s,toc_do_kmh,khoang_cach_m,ax` |

Còn lại 1736 dòng hợp lệ. Sinh bằng `tools/tao_du_lieu_tuan3.py`, seed cố định, riêng với các file khác.

## Tổng dung lượng

Khoảng 490 KB cho cả sáu file.
