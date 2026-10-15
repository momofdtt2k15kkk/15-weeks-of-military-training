# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/momofdtt2k15kkk/15-weeks-of-military-training/blob/main/week2/week_2.ipynb)
#
# # Tuần 2 — Cấu trúc dữ liệu, hàm và chuỗi
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Dùng `list`: lấy phần tử theo chỉ số, cắt lát, thêm phần tử, lọc bằng vòng lặp và
#    list comprehension.
# 2. Dùng `tuple`, `enumerate` và `zip` để duyệt dữ liệu kèm chỉ số hoặc theo từng cặp.
# 3. Dùng tham số mặc định, và phân biệt biến cục bộ với biến toàn cục.
# 4. Cắt, tìm và dịch ký tự trên chuỗi.
# 5. Dùng `dict` và `set` để đếm, gom nhóm, gộp cấu hình và so sánh tập hợp.
# 6. Gom dữ liệu của cả chuyến xe vào list và dict rồi thống kê.
#
# **Quy tắc:** không sửa nội dung các ô kiểm tra. Chỉ viết code vào chỗ có `# TODO`
# hoặc chỗ được đánh dấu là chỗ viết của bạn.

# %%
# Ô thiết lập - chạy đầu tiên, mỗi lần mở notebook.
import os
import sys
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/momofdtt2k15kkk/15-weeks-of-military-training/main"

# File của tuần này. Chỉ tải file chưa có trên máy.
FILE_TESTS = ("runner.py", "test_week2.py", "tien_ich_du_lieu.py")
FILE_DATA = ("khoang_cach_truoc.csv", "gps.nmea", "obd.csv", "ma_loi.csv")

# Mở notebook từ thư mục week2/ trên máy: lùi ra thư mục gốc, nơi có sẵn tests/.
if not os.path.isdir("tests") and os.path.isdir(os.path.join("..", "tests")):
    os.chdir("..")

for thu_muc, danh_sach in (("tests", FILE_TESTS), ("data", FILE_DATA)):
    os.makedirs(thu_muc, exist_ok=True)
    for ten_file in danh_sach:
        duong_dan = os.path.join(thu_muc, ten_file)
        if not os.path.isfile(duong_dan):
            urllib.request.urlretrieve(f"{REPO_RAW}/{thu_muc}/{ten_file}", duong_dan)
open(os.path.join("tests", "__init__.py"), "a").close()

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from tests.test_week2 import (
    kiem_tra_1_1,
    kiem_tra_1_2,
    kiem_tra_1_3,
    kiem_tra_1_4,
    kiem_tra_2_1,
    kiem_tra_2_2,
    kiem_tra_2_3,
    kiem_tra_3_1,
    kiem_tra_3_2,
    kiem_tra_3_3,
    kiem_tra_4_1,
    kiem_tra_4_2,
    kiem_tra_5_1,
    kiem_tra_5_2,
    kiem_tra_5_3,
    kiem_tra_5_4,
    kiem_tra_5_5,
    kiem_tra_du_an,
    kiem_tra_lab,
)

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Cách làm bài và chấm bài
#
# Mỗi bài tập gồm hai ô đi liền nhau: ô bạn viết code, và ô kiểm tra ngay dưới nó. Ô
# kiểm tra đọc các biến hoặc hàm mà ô trên tạo ra, nên **tên phải khớp từng chữ**.
#
# 1. Sửa xong ô code phải chạy lại chính ô đó rồi mới chạy ô kiểm tra. Bỏ qua bước này
#    thì ô kiểm tra vẫn đọc giá trị cũ.
# 2. Chưa làm gì mà chạy ô kiểm tra thì nó báo FAIL kèm dòng "thực tế: None". Đó là
#    trạng thái bình thường lúc mới mở notebook.
# 3. Dòng "mong đợi" trong báo lỗi cho biết đáp án đúng phải trông ra sao. So nó với
#    dòng "thực tế" để biết lệch ở đâu.
#
# Chạy lại cả notebook từ đầu bằng `Runtime > Restart and run all` nếu thấy kết quả
# lộn xộn không giải thích được.

# %% [markdown]
# ---
# ## Bài 1 — List
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `[a, b, c]` | list: dãy các giá trị có thứ tự, đặt trong ngoặc vuông, ngăn cách bằng dấu phẩy | `khoang_cach = [5.2, 3.1, 0.8]` |
# | `[]` | list rỗng | `canh_bao = []` |
# | `ds[i]` | phần tử ở chỉ số `i`, chỉ số đếm từ `0` | `[5.2, 3.1, 0.8][0]` → `5.2` |
# | `ds[-1]` | chỉ số âm đếm từ cuối lên, `-1` là phần tử cuối | `[5.2, 3.1, 0.8][-1]` → `0.8` |
# | `ds[a:b]` | cắt lát: lấy từ chỉ số `a` đến chỉ số `b - 1`, trả về list mới, `ds` giữ nguyên | `[10, 20, 30, 40][1:3]` → `[20, 30]` |
# | `ds[:b]`, `ds[a:]` | bỏ trống `a` là lấy từ đầu, bỏ trống `b` là lấy tới cuối | `[10, 20, 30, 40][-2:]` → `[30, 40]` |
# | `ds[::-1]` | bước `-1` duyệt ngược, cho list đảo ngược | `[1, 2, 3][::-1]` → `[3, 2, 1]` |
# | `ds[:]` | cắt lát từ đầu tới cuối, cho một bản sao của `ds` | `ds2 = ds[:]` |
# | `len(ds)` | số phần tử của `ds` | `len([5, 6, 7])` → `3` |
# | `ds.append(x)` | thêm `x` vào cuối `ds`, sửa thẳng lên `ds` | `canh_bao.append(0.8)` |
# | `x in ds` | `True` nếu `x` có trong `ds` | `3 in [1, 2, 3]` → `True` |
# | `sum(ds)`, `max(ds)`, `min(ds)` | tổng, giá trị lớn nhất, giá trị nhỏ nhất của `ds` | `max([4, 9, 2])` → `9` |
# | `sorted(ds)` | list mới gồm các phần tử của `ds` xếp tăng dần, `ds` giữ nguyên | `sorted([3, 1, 2])` → `[1, 2, 3]` |
# | `for x in ds:` | duyệt từng phần tử của `ds`, mỗi vòng `x` nhận một phần tử | `for kc in khoang_cach:` |
# | `[bt for x in ds if dk]` | list comprehension: tạo list mới từ các `x` thoả điều kiện `dk`, mỗi phần tử của list mới là biểu thức `bt`. Bỏ phần `if dk` thì lấy mọi `x` | `[x for x in [5, 1, 8] if x > 3]` → `[5, 8]` |
#
# #### ⚠️ Lỗi hay gặp
#
# - Chỉ số vượt ngoài list báo `IndexError`: list 3 phần tử có chỉ số `0`, `1`, `2`, và
#   `ds[3]` báo lỗi. Phần tử cuối luôn có chỉ số `len(ds) - 1`.
# - Cắt lát vượt ngoài list không báo lỗi: `[1, 2, 3][1:10]` cho `[2, 3]`.
# - `b = a` không sao chép list: `a` và `b` cùng trỏ vào một list, thêm phần tử qua tên
#   này thì tên kia cũng đổi. Muốn bản sao thì viết `b = a[:]`.
# - `ds = ds.append(x)` làm `ds` thành `None`, vì `append` sửa tại chỗ và trả về
#   `None`. Viết `ds.append(x)` một mình trên một dòng.
# - Thêm hoặc xoá phần tử của chính list đang duyệt bằng `for` làm chỉ số bị lệch. Muốn
#   lọc thì tạo list mới.
# - `max([])` báo `ValueError`, còn `sum([])` cho `0`.

# %%
# 💻 Ví dụ: chỉ số
khoang_cach_lidar = [5.2, 3.1, 0.8, 4.5, 1.2, 0.3]   # list 6 phần tử, chỉ số từ 0 đến 5
print(khoang_cach_lidar[0], khoang_cach_lidar[-1])     # 5.2 0.3

# %% [markdown]
# Chỉ số `0` là phần tử đầu, chỉ số `-1` là phần tử cuối.

# %%
# 💻 Ví dụ: cắt lát
print(khoang_cach_lidar[1:4])      # [3.1, 0.8, 4.5] - chỉ số 1, 2, 3
print(khoang_cach_lidar[-3:])      # [4.5, 1.2, 0.3] - ba phần tử cuối
print(khoang_cach_lidar[::-1])     # list đảo ngược

# %% [markdown]
# `[1:4]` dừng trước chỉ số `4` nên có `4 - 1 = 3` phần tử. `[-3:]` bỏ trống vế phải nên
# chạy tới cuối list.

# %%
# 💻 Ví dụ: for kết hợp append
canh_bao = []
for kc in khoang_cach_lidar:
    if kc < 1.0:
        canh_bao.append(kc)    # append: thêm kc vào cuối list canh_bao
print(canh_bao)                # [0.8, 0.3]

# %% [markdown]
# `canh_bao` được đặt về list rỗng trước vòng lặp, rồi mỗi giá trị nhỏ hơn `1.0` được
# thêm vào.

# %%
# 💻 Ví dụ: list comprehension
canh_bao_gon = [kc for kc in khoang_cach_lidar if kc < 1.0]
print(canh_bao_gon == canh_bao)    # True

# %% [markdown]
# Một dòng cho cùng kết quả với cả vòng `for` ở ô trên.

# %%
# 💻 Ví dụ: hai tên cùng một list
a = [1, 2]
b = a              # b và a cùng trỏ vào một list
b.append(3)
print(a)           # [1, 2, 3]

# %% [markdown]
# Thêm phần tử qua `b` thì `a` cũng đổi, vì chỉ có một list.

# %%
# 💻 Ví dụ: bản sao
c = a[:]           # c là list mới có cùng phần tử
c.append(4)
print(a, c)        # [1, 2, 3] [1, 2, 3, 4]

# %% [markdown]
# `a[:]` cắt lát từ đầu đến cuối nên cho ra list mới, thêm vào `c` không đụng tới `a`.

# %%
# 💻 Ví dụ: thống kê tốc độ của nhiều xe
toc_do_doi_xe = [42, 55, 38, 61]
print(max(toc_do_doi_xe), sum(toc_do_doi_xe) / len(toc_do_doi_xe))   # 61 49.0

# %% [markdown]
# `max` tìm giá trị lớn nhất, `sum` cộng cả list, `len` đếm phần tử, nên tốc độ trung
# bình là `sum / len`.

# %%
# 💻 Ví dụ: tự làm max bằng vòng for
lon_nhat = toc_do_doi_xe[0]
for v in toc_do_doi_xe:
    if v > lon_nhat:
        lon_nhat = v
print(lon_nhat == max(toc_do_doi_xe))    # True

# %% [markdown]
# Vòng `for` giữ lại giá trị lớn nhất đã gặp, cho cùng kết quả với `max`.

# %%
# 💻 Ví dụ: gom một cột của obd.csv vào list
import csv

rpm_list = []
with open("data/obd.csv") as f:
    for hang in csv.DictReader(f):
        rpm_list.append(int(hang["rpm"]))    # hang["rpm"] là chuỗi, ép int rồi mới thêm
print(len(rpm_list), rpm_list[:3])           # 181 [820, 821, 794]

# %% [markdown]
# Mỗi dòng dữ liệu của file thành một phần tử, nên `len(rpm_list)` bằng số dòng dữ liệu.

# %% [markdown]
# ### 🎯 Bài tập 1.1 — Lọc vật cản gần
#
# Viết hàm `loc_vat_can_gan(khoang_cach, nguong)` trả về một list gồm các giá trị
# trong `khoang_cach` nhỏ hơn `nguong`, giữ nguyên thứ tự xuất hiện.
#
# Ví dụ: `loc_vat_can_gan([5.2, 3.1, 0.8, 4.5, 1.2, 0.3], 1.0)` cho `[0.8, 0.3]`.
# `loc_vat_can_gan([2.0, 1.0, 0.5], 1.0)` cho `[0.5]`, vì `1.0` đúng bằng ngưỡng nên
# không lấy.

# %%
def loc_vat_can_gan(khoang_cach, nguong):
    # TODO: trả về list các phần tử nhỏ hơn nguong
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_1_1(loc_vat_can_gan)

# %% [markdown]
# ### 🎯 Bài tập 1.2 — Trung bình n mẫu cuối
#
# Cảm biến ghi liên tục, nhưng chỉ `n` lần đọc mới nhất phản ánh trạng thái hiện tại.
# Viết hàm `tb_n_mau_cuoi(ds, n)` trả về trung bình cộng của `n` phần tử cuối của
# `ds`. Nếu `ds` có ít hơn `n` phần tử thì lấy trung bình của tất cả. Nếu `ds` rỗng
# thì trả về `None`.
#
# Ví dụ: `tb_n_mau_cuoi([10, 20, 30, 40], 2)` cho `35.0`. `tb_n_mau_cuoi([10, 20], 5)`
# cho `15.0`. `tb_n_mau_cuoi([], 3)` cho `None`.

# %%
def tb_n_mau_cuoi(ds, n):
    # TODO: cắt lấy n phần tử cuối, tính trung bình, xử lý list rỗng
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_1_2(tb_n_mau_cuoi)

# %% [markdown]
# ### 📡 Bài tập 1.3 — Gom tốc độ vào list
#
# Đọc `data/obd.csv` (OBD-II, 1 mẫu mỗi giây, 181 dòng dữ liệu) bằng
# `csv.DictReader`. Gán `toc_do_list` là list các giá trị cột `toc_do_kmh` (kiểu
# `int`) của mọi dòng, theo thứ tự trong file. Gán `toc_do_cao` là list các tốc độ lớn
# hơn `60` km/h, cũng theo thứ tự đó.
#
# Ví dụ: ba dòng có `toc_do_kmh` lần lượt là `0`, `42`, `65` cho
# `toc_do_list = [0, 42, 65]` và `toc_do_cao = [65]`.

# %%
toc_do_list = None  # TODO
toc_do_cao = None   # TODO

# Viết code đọc file của bạn vào ngay dưới dòng này. Khung cú pháp:
# toc_do_list = []
# toc_do_cao = []
# with open("data/obd.csv") as f:
#     for hang in csv.DictReader(f):
#         ...


# %%
kiem_tra_1_3(toc_do_list, toc_do_cao)

# %% [markdown]
# ### 🎯 Bài tập 1.4 — Trung bình trượt
#
# Tốc độ OBD có độ phân giải 1 km/h nên đường tốc độ lởm chởm. Để thấy xu hướng, thay
# mỗi mẫu bằng trung bình của `k` mẫu liên tiếp bắt đầu từ mẫu đó. Với list `x` có
# $n$ phần tử, list kết quả `y` có $n - k + 1$ phần tử:
#
# $$y_i = \frac{1}{k} \sum_{j=i}^{i+k-1} x_j, \qquad i = 0, 1, \dots, n - k$$
#
# Viết hàm `trung_binh_truot(ds, k)` trả về list `y` gồm các số `float`. Nếu `k` lớn
# hơn độ dài của `ds` thì trả về list rỗng.
#
# Ví dụ: `trung_binh_truot([2, 4, 6, 8], 2)` cho `[3.0, 5.0, 7.0]`, ứng với
# $\frac{2+4}{2}$, $\frac{4+6}{2}$, $\frac{6+8}{2}$. `trung_binh_truot([1, 2, 3, 4, 5], 3)`
# cho `[2.0, 3.0, 4.0]`.

# %%
def trung_binh_truot(ds, k):
    # TODO: với mỗi i từ 0 đến n - k, tính trung bình k phần tử bắt đầu từ chỉ số i, thêm vào list kết quả
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_1_4(trung_binh_truot)

# %% [markdown]
# ---
# ## Bài 2 — Tuple, enumerate và zip
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `(a, b)` | tuple: dãy các giá trị có thứ tự đặt trong ngoặc tròn, có thể tách vào nhiều biến cùng lúc | `vi_tri = (21.0, 105.8)`, rồi `vi_do, kinh_do = vi_tri` |
# | `t[i]`, `t[a:b]` | chỉ số và cắt lát dùng như list, nhưng tuple không sửa được phần tử | `(21.0, 105.8)[1]` → `105.8` |
# | `a, b = b, a` | đổi chỗ hai biến, không cần biến tạm | `a, b = 1, 2` rồi `a, b = b, a` → `a` là `2`, `b` là `1` |
# | `return a, b` | hàm trả về hai giá trị cùng lúc (là một tuple), nơi gọi tách bằng `x, y = ham()` | `nho, lon = nho_lon(ds)` |
# | `for i, x in enumerate(ds):` | duyệt `ds` kèm chỉ số: mỗi vòng `i` là chỉ số (bắt đầu từ `0`), `x` là phần tử | `enumerate([5, 9])` cho `(0, 5)`, `(1, 9)` |
# | `zip(a, b)` | ghép hai list theo từng cặp cùng chỉ số, dừng khi list ngắn hơn hết | `for x, y in zip([1, 2], ["a", "b"]):` |
# | `zip(ds, ds[1:])` | cặp phần tử liền kề của `ds`: `(ds[0], ds[1])`, `(ds[1], ds[2])`, ... | `list(zip([1, 4, 9], [4, 9]))` → `[(1, 4), (4, 9)]` |
#
# #### ⚠️ Lỗi hay gặp
#
# - Gán vào phần tử của tuple báo `TypeError`: `vi_tri[0] = 20`. Muốn đổi thì tạo tuple
#   mới.
# - Tuple một phần tử phải có dấu phẩy: `(5,)`. Viết `(5)` chỉ là số `5` trong ngoặc.
# - Tách tuple vào số biến khác số phần tử báo `ValueError`: `a, b = (1, 2, 3)`.
# - `zip(a, b)` và `enumerate(ds)` không in ra nội dung. Bọc `list(...)` để xem:
#   `print(list(zip(a, b)))`.
# - `zip` dừng ở list ngắn hơn, phần dư của list dài bị bỏ.

# %%
# 💻 Ví dụ: tuple và gán nhiều biến
vi_tri = (21.0045, 105.8430)       # tuple: vĩ độ, kinh độ
vi_do, kinh_do = vi_tri            # tách tuple vào hai biến
print(vi_do, kinh_do, vi_tri[1])   # 21.0045 105.843 105.843

# %% [markdown]
# Dòng `a, b = 17, 5` cũng làm đúng việc này: vế phải là tuple `(17, 5)`, được tách vào
# hai biến `a` và `b`.

# %%
# 💻 Ví dụ: tuple không sửa được
# vi_tri[0] = 20   # Bỏ dấu # để thấy lỗi TypeError

# %% [markdown]
# Muốn thay một phần tử thì tạo tuple mới.

# %%
# 💻 Ví dụ: đổi chỗ hai biến
gia_tri_a, gia_tri_b = 40, 65
gia_tri_a, gia_tri_b = gia_tri_b, gia_tri_a
print(gia_tri_a, gia_tri_b)    # 65 40

# %% [markdown]
# Vế phải được tính xong cả hai giá trị rồi mới gán, nên không cần biến tạm.

# %%
# 💻 Ví dụ: hàm trả về hai giá trị
def nho_lon(ds):
    return min(ds), max(ds)    # trả về một tuple (nhỏ nhất, lớn nhất)


nho, lon = nho_lon([42, 55, 38, 61])
print(nho, lon)                # 38 61

# %% [markdown]
# Nơi gọi tách tuple trả về vào hai biến `nho` và `lon`.

# %%
# 💻 Ví dụ: enumerate
toc_do_xe = [10, 30, 55, 20]
for giay, toc_do in enumerate(toc_do_xe):    # enumerate: kèm chỉ số, bắt đầu từ 0
    if toc_do > 50:
        print(giay, toc_do)                  # 2 55

# %% [markdown]
# `giay` là chỉ số của phần tử, cũng là giây thứ mấy nếu mỗi phần tử là một giây.

# %%
# 💻 Ví dụ: zip hai list
ten_cam_bien = ["lidar", "camera", "radar"]
gia_tri_doc = [12.5, 0.98, 45.0]
for ten, gia_tri in zip(ten_cam_bien, gia_tri_doc):    # zip: ghép theo cặp cùng chỉ số
    print(ten, gia_tri)

# %% [markdown]
# Mỗi vòng nhận một cặp, tách thành hai biến `ten` và `gia_tri`.

# %%
# 💻 Ví dụ: cặp liền kề
pin_theo_giay = [15.8, 15.7, 15.5]
print(list(zip(pin_theo_giay, pin_theo_giay[1:])))    # [(15.8, 15.7), (15.7, 15.5)]

# %% [markdown]
# `pin_theo_giay[1:]` lệch một vị trí so với `pin_theo_giay`, nên `zip` ghép mỗi phần tử
# với phần tử ngay sau nó. List dài `n` cho `n - 1` cặp.

# %% [markdown]
# ### 🎯 Bài tập 2.1 — Giây vượt ngưỡng
#
# Viết hàm `giay_vuot_nguong(ds, nguong)` trả về list các chỉ số `i` mà `ds[i]` lớn hơn
# `nguong`, theo thứ tự tăng dần. Dùng `enumerate`.
#
# Ví dụ: `giay_vuot_nguong([0, 42, 65, 70, 50], 60)` cho `[2, 3]`.
# `giay_vuot_nguong([10, 20, 30], 30)` cho `[]`, vì `30` đúng bằng ngưỡng nên không lấy.

# %%
def giay_vuot_nguong(ds, nguong):
    # TODO: duyệt bằng enumerate, thêm chỉ số vào list kết quả, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_2_1(giay_vuot_nguong)

# %% [markdown]
# ### 🎯 Bài tập 2.2 — Chênh lệch liên tiếp
#
# Hiệu của hai giây liên tiếp cho biết xe đang tăng tốc hay giảm tốc. Viết hàm
# `chenh_lech_lien_tiep(ds)` trả về list các hiệu `ds[i + 1] - ds[i]`, theo thứ tự. Dùng
# `zip`. List ít hơn 2 phần tử thì trả về list rỗng.
#
# Ví dụ: tốc độ bốn giây 112 đến 115 của chuyến xe là `[30, 29, 7, 0]`, đúng lúc phanh
# gấp. `chenh_lech_lien_tiep([30, 29, 7, 0])` cho `[-1, -22, -7]`.
# `chenh_lech_lien_tiep([1, 4, 9, 16])` cho `[3, 5, 7]`.

# %%
def chenh_lech_lien_tiep(ds):
    # TODO: duyệt các cặp liền kề, thêm hiệu vào list kết quả, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_2_2(chenh_lech_lien_tiep)

# %% [markdown]
# ### 📡 Bài tập 2.3 — Quỹ đạo GPS
#
# Đọc `data/gps.nmea` bằng `open` và `for`, bỏ qua câu không phải `$GNGGA`. Mỗi câu
# `$GNGGA` ứng với 1 giây của chuyến, bắt đầu từ giây `0`. Cột 2 là vĩ độ, cột 3 là
# hướng vĩ độ, cột 4 là kinh độ, cột 5 là hướng kinh độ (đếm từ 0 sau khi cắt theo dấu
# phẩy). Giây 94, 95, 96 xe chạy dưới tán cây, mất fix và các ô này để trống, bỏ qua các
# giây đó.
#
# Gán `quy_dao` là list các tuple `(giay, vi_do, kinh_do)` của các giây có toạ độ, theo
# thứ tự. Hàm `nmea_sang_do(chuoi, huong)` đổi toạ độ NMEA sang độ thập phân, đã viết
# sẵn trong ô dưới.
#
# Ví dụ: ba câu `$GNGGA` có vĩ độ `2103.00000` N, ô trống, `2103.60000` N, kinh độ
# `10603.00000` E, ô trống, `10603.60000` E cho
# `quy_dao = [(0, 21.05, 106.05), (2, 21.06, 106.06)]`.

# %%
from tests.tien_ich_du_lieu import nmea_sang_do

quy_dao = None  # TODO

# Viết code đọc file của bạn vào ngay dưới dòng này. Khung cú pháp:
# quy_dao = []
# giay = -1
# with open("data/gps.nmea") as f:
#     for dong in f:
#         ...


# %%
kiem_tra_2_3(quy_dao)

# %% [markdown]
# ---
# ## Bài 3 — Tham số mặc định và phạm vi biến
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `def ten(a, b=gia_tri):` | `b` có giá trị mặc định: gọi mà không truyền `b` thì `b` nhận `gia_tri`. Tham số có mặc định phải đứng sau mọi tham số không có mặc định | `def giam(v, p=0):` |
# | `ten(a, b=5)` | gọi bằng tên tham số (keyword argument), không cần đúng thứ tự khai báo | `giam(v=80, p=25)` |
# | `ds=None` | cách khai báo tham số mặc định cho list: mặc định là `None`, list mới được tạo bên trong hàm | `def them(x, ds=None):` |
# | `x is None` | `True` nếu `x` là `None` | `if ds is None:` |
# | biến cục bộ | biến được gán bên trong hàm, chỉ tồn tại lúc hàm chạy, riêng với biến cùng tên ở ngoài hàm | `muc_pin = muc_pin - 20` trong thân hàm |
# | biến toàn cục | biến được gán ở ngoài mọi hàm, hàm đọc được nhưng chưa gán lại được | `so_lan_loi = 0` ở ngoài hàm |
# | `global ten_bien` | khai báo trong hàm để gán lại biến toàn cục `ten_bien` | `global so_lan_loi` |
# | `max(a, b)`, `min(a, b)` | số lớn hơn, số nhỏ hơn trong hai số | `max(3, 7)` → `7` |
#
# #### ⚠️ Lỗi hay gặp
#
# - Giá trị mặc định được tạo **một lần**, lúc Python đọc dòng `def`, không tạo lại
#   mỗi lần gọi. Mặc định là list (`ds=[]`) thì mọi lần gọi không truyền `ds` dùng chung
#   đúng một list đó.
# - `def f(a=1, b):` báo `SyntaxError` ngay khi định nghĩa hàm, chưa cần gọi.
# - Gán lại một tham số bên trong hàm (`ds = ds + [99]`) không đổi biến bên ngoài.
#   `ds.append(99)` thì sửa thẳng lên list bên ngoài, vì hai tên cùng trỏ vào một list.
# - Gán biến toàn cục bên trong hàm mà thiếu `global` thì Python báo
#   `UnboundLocalError`.
# - Hạn chế `global`. Đưa giá trị vào hàm bằng tham số và đưa kết quả ra bằng `return`.

# %%
# 💻 Ví dụ: tham số mặc định
def tinh_goc_danh_lai(do_lech_lan, goc_co_ban=0):
    return goc_co_ban + do_lech_lan * 1.5


print(tinh_goc_danh_lai(10))               # 15.0 - dùng goc_co_ban mặc định là 0
print(tinh_goc_danh_lai(10, 5))            # 20.0 - truyền goc_co_ban = 5
print(tinh_goc_danh_lai(do_lech_lan=-5))   # -7.5 - gọi bằng tên tham số

# %% [markdown]
# Giá trị truyền vào thay cho mặc định, không cộng dồn với nó.

# %%
# 💻 Ví dụ: thứ tự tham số
# def vi_du_sai_thu_tu(a=1, b):   # Bỏ dấu # để thấy lỗi SyntaxError

# %% [markdown]
# Tham số có mặc định phải đứng sau tham số không có mặc định.

# %%
# 💻 Ví dụ: mặc định là list
def them_loi(ma, ds=[]):      # list rỗng này chỉ được tạo một lần
    ds.append(ma)
    return ds


print(them_loi("P0113"))   # ['P0113']
print(them_loi("C0035"))   # ['P0113', 'C0035'] - hai lần gọi dùng chung một list

# %% [markdown]
# Hai lần gọi độc lập nhưng lần hai thấy lại phần tử của lần một.

# %%
# 💻 Ví dụ: mặc định None
def them_dung(ma, ds=None):
    if ds is None:         # None: chưa truyền list, tạo list mới trong hàm
        ds = []
    ds.append(ma)
    return ds


print(them_dung("P0113"))   # ['P0113']
print(them_dung("C0035"))   # ['C0035']

# %% [markdown]
# Mỗi lần gọi không truyền `ds` tạo một list mới, nên hai lần gọi không ảnh hưởng nhau.

# %%
# 💻 Ví dụ: gán lại và sửa tại chỗ
def gan_lai(ds):
    ds = ds + [99]      # tạo list mới, list bên ngoài giữ nguyên
    return ds


def sua_tai_cho(ds):
    ds.append(99)       # sửa thẳng lên list bên ngoài
    return ds


goc_1, goc_2 = [1, 2], [1, 2]
gan_lai(goc_1)
sua_tai_cho(goc_2)
print(goc_1, goc_2)     # [1, 2] [1, 2, 99]

# %% [markdown]
# `gan_lai` không đổi `goc_1`, còn `sua_tai_cho` đổi `goc_2` vì `ds` bên trong hàm và
# `goc_2` bên ngoài cùng trỏ vào một list.

# %%
# 💻 Ví dụ: biến cục bộ
def tru_pin(muc_pin, luong_tieu_thu):
    muc_pin = muc_pin - luong_tieu_thu    # muc_pin này là biến cục bộ, riêng với muc_pin bên ngoài
    return muc_pin


muc_pin = 100
ket_qua = tru_pin(muc_pin, 20)
print(muc_pin, ket_qua)    # 100 80

# %% [markdown]
# Theo dõi `muc_pin`:
#
# | Mốc | `muc_pin` ngoài hàm | Đang diễn ra |
# |---|---|---|
# | 1 | `100` | trước khi gọi `tru_pin(muc_pin, 20)` |
# | 2 | `100` | bên trong hàm, tham số `muc_pin` cục bộ là `100`, tính ra `80` rồi `return 80` |
# | 3 | `100` | sau khi gọi xong, `80` nằm trong `ket_qua`, muốn dùng thì gán lại `muc_pin = tru_pin(muc_pin, 20)` |

# %%
# 💻 Ví dụ: global
so_lan_loi = 0


def ghi_nhan_loi():
    global so_lan_loi     # khai báo để gán lại biến toàn cục
    so_lan_loi += 1


ghi_nhan_loi()
ghi_nhan_loi()
print(so_lan_loi)         # 2

# %% [markdown]
# Bỏ dòng `global so_lan_loi` thì `so_lan_loi += 1` báo `UnboundLocalError`.

# %% [markdown]
# ### 🎯 Bài tập 3.1 — Giảm tốc độ
#
# Viết hàm `giam_toc_do(toc_do_goc, phan_tram=0)` trả về tốc độ sau khi giảm
# `phan_tram` %, làm tròn 2 chữ số sau dấu phẩy. Không truyền `phan_tram` thì mặc
# định là không giảm.
#
# Trong đó $v$ là `toc_do_goc`, $p$ là `phan_tram` và $v'$ là tốc độ sau khi giảm:
#
# $$v' = v \times \left(1 - \frac{p}{100}\right)$$
#
# Ví dụ: `giam_toc_do(80, 25)` cho `60.0`. `giam_toc_do(120)` cho `120.0`.
# `giam_toc_do(45, 33)` cho `30.15`.

# %%
def giam_toc_do(toc_do_goc, phan_tram=0):
    # TODO: tính theo công thức trên, làm tròn 2 chữ số, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_3_1(giam_toc_do)

# %% [markdown]
# ### 🎯 Bài tập 3.2 — Mức pin sau tiêu hao
#
# Viết hàm `tru_hao_pin(muc_pin, luong_tieu_hao, san=0)` trả về mức pin sau khi trừ
# lượng tiêu hao, nhưng không thấp hơn `san`. Không truyền `san` thì sàn là `0`.
#
# Trong đó $m$ là `muc_pin`, $e$ là `luong_tieu_hao`, $s$ là `san` và $r$ là mức pin sau tiêu hao:
#
# $$r = \max\left(m - e,\ s\right)$$
#
# Ví dụ: `tru_hao_pin(100, 30)` cho `70`. `tru_hao_pin(20, 30)` cho `0`, vì tiêu hao
# vượt mức pin hiện có. `tru_hao_pin(50, 30, 15)` cho `20`. `tru_hao_pin(30, 30, 15)`
# cho `15`.

# %%
def tru_hao_pin(muc_pin, luong_tieu_hao, san=0):
    # TODO: tính theo công thức trên, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_3_2(tru_hao_pin)

# %% [markdown]
# ### 🎯 Bài tập 3.3 — Nhật ký cảnh báo
#
# Viết hàm `ghi_canh_bao(thong_bao, nhat_ky=None)` thêm `thong_bao` vào cuối `nhat_ky`
# rồi trả về `nhat_ky`. Không truyền `nhat_ky` thì bắt đầu từ một list rỗng mới, và
# hai lần gọi không truyền `nhat_ky` không ảnh hưởng nhau.
#
# Ví dụ: `ghi_canh_bao("phanh gap")` cho `["phanh gap"]`. Gọi tiếp
# `ghi_canh_bao("mat gps")` cho `["mat gps"]`, không dính `"phanh gap"` của lần trước.
# `ghi_canh_bao("pin yeu", ["phanh gap"])` cho `["phanh gap", "pin yeu"]`.

# %%
def ghi_canh_bao(thong_bao, nhat_ky=None):
    # TODO: tạo list mới nếu chưa có nhat_ky, thêm thong_bao, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_3_3(ghi_canh_bao)

# %% [markdown]
# ---
# ## Bài 4 — Chuỗi ký tự
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `s[i]`, `s[a:b]`, `s[-1]` | chỉ số và cắt lát trên chuỗi dùng giống hệt list, mỗi ký tự là một phần tử | `"GNGGA"[0:2]` → `"GN"` |
# | `len(s)` | số ký tự của `s` | `len("GNGGA")` → `5` |
# | `s.index(x)` | chỉ số của lần xuất hiện đầu tiên của `x` trong `s` | `"GN,GGA".index(",")` → `2` |
# | `s.split(",")` | cắt `s` theo dấu phẩy, trả về list các đoạn | `"a,b,c".split(",")` → `["a", "b", "c"]` |
# | `for c in s:` | duyệt từng ký tự của `s` | `for c in "xe":` |
# | `ord(c)` | mã số (mã ASCII) của ký tự `c` | `ord("a")` → `97` |
# | `chr(n)` | ký tự có mã số `n`, làm ngược lại `ord` | `chr(98)` → `"b"` |
# | `c.isalpha()`, `c.isupper()` | `True` nếu `c` là chữ cái, `True` nếu `c` là chữ hoa | `"A".isalpha()` → `True`, `"a".isupper()` → `False` |
#
# #### ⚠️ Lỗi hay gặp
#
# - Chuỗi không sửa được từng ký tự: `s[0] = "x"` báo `TypeError`. Muốn đổi thì tạo
#   chuỗi mới từ các lát cắt.
# - `s.index(x)` báo `ValueError` khi `x` không có trong `s`.
# - Chữ cái có dấu tiếng Việt (`à`, `ê`...) cũng cho `isalpha()` là `True`, nhưng mã của
#   chúng nằm ngoài khoảng `a`-`z`. Bài tập chỉ xét chữ cái không dấu.
# - `chr` và `ord` làm việc với một ký tự. `ord("ab")` báo `TypeError`.

# %%
# 💻 Ví dụ: cắt lát chuỗi
cau = "$GNGGA,165920.00,2100.27369,N,10550.57970,E,2,11,1.0,12.4,M,-22.1,M,1.0,0000*4A"
print(cau[1:6], cau[-2:])    # GNGGA 4A

# %% [markdown]
# `cau[1:6]` bỏ ký tự `$` ở chỉ số `0` và dừng trước chỉ số `6`. `cau[-2:]` lấy hai ký tự
# cuối.

# %%
# 💻 Ví dụ: index và split
print(cau.index(","), cau.split(",")[6])    # 6 2

# %% [markdown]
# Dấu phẩy đầu tiên nằm ở chỉ số `6`. `split(",")` cho một list các đoạn, nên `[6]` lấy
# đoạn thứ 6, là mã fix.

# %%
# 💻 Ví dụ: ord, chr và isalpha
print(ord("a"), ord("A"))              # 97 65
print(chr(98), chr(66))                # b B
print("A".isalpha(), "5".isalpha())    # True False

# %% [markdown]
# Chữ thường và chữ hoa có mã khác nhau. `isalpha()` phân biệt chữ cái với chữ số.

# %% [markdown]
# ### 📡 Bài tập 4.1 — Loại câu NMEA
#
# Mỗi câu NMEA của `data/gps.nmea` bắt đầu bằng `$`, tiếp theo là tên câu (ví dụ
# `GNGGA`) và kết thúc ở dấu phẩy đầu tiên.
#
# Viết hàm `loai_cau(cau)` trả về tên câu, không có dấu `$`.
#
# Ví dụ: `loai_cau("$GNRMC,165940.00,A,2100.35986,N,10550.57994,E,21.60,0.0,081026,,,F*45")`
# cho `"GNRMC"`. `loai_cau("$GPGSV,3,1,12*74")` cho `"GPGSV"`.

# %%
def loai_cau(cau):
    # TODO: cắt lấy phần từ sau dấu $ đến trước dấu phẩy đầu tiên, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_4_1(loai_cau)

# %% [markdown]
# ### 🎯 Bài tập 4.2 — Mã hoá Caesar
#
# Xe nhận lệnh điều khiển qua sóng vô tuyến, cần mã hoá để tránh bị nghe lén. Mã hoá
# Caesar dịch mỗi chữ cái đi một số vị trí cố định trong bảng chữ cái, vòng lại từ đầu
# nếu vượt quá `z`. Trước khi viết hàm đầy đủ, dịch thử một ký tự bằng công thức số học,
# không cần `if`. Tham số `goc` cho biết dịch từ `"a"` (chữ thường) hay `"A"` (chữ hoa):

# %%
def dich_ky_tu(c, dich_chuyen, goc="a"):
    return chr((ord(c) - ord(goc) + dich_chuyen) % 26 + ord(goc))


print(dich_ky_tu("a", 3))          # 'd' - gốc mặc định là "a"
print(dich_ky_tu("y", 3))          # 'b' - vòng qua từ z về a
print(dich_ky_tu("Y", 3, "A"))     # 'B' - truyền goc="A" để dịch chữ hoa

# %% [markdown]
# `ord(c) - ord(goc)` đưa `c` về vị trí `0` đến `25` trong bảng chữ cái, không phụ thuộc
# mã ASCII gốc. Cộng `dich_chuyen` rồi `% 26` để vòng lại nếu vượt quá `25`, cộng lại
# `ord(goc)` để quay về đúng mã ký tự.
#
# Vết chạy với `c = "y"`, `dich_chuyen = 3`, `goc = "a"`:
#
# | Biểu thức | Kết quả |
# |---|---|
# | `ord("y")` | `121` |
# | `121 - ord("a")` | `121 - 97 = 24` |
# | `24 + 3` | `27` |
# | `27 % 26` | `1` |
# | `1 + ord("a")` | `1 + 97 = 98` |
# | `chr(98)` | `"b"` |
#
# `27 % 26` cho `1` thay vì `27`: đây là bước vòng lại từ `z` (vị trí `25`) về `a` (vị
# trí `0`).

# %%
def dich_chuoi_thuong(van_ban, dich_chuyen):
    ket_qua = ""
    for c in van_ban:
        ket_qua += dich_ky_tu(c, dich_chuyen)
    return ket_qua


print(dich_chuoi_thuong("hello", 3))   # 'khoor'
print(dich_chuoi_thuong("xyz", 3))     # 'abc'

# %% [markdown]
# Vòng `for` ghép từng ký tự đã dịch vào `ket_qua`, với chuỗi chỉ toàn chữ thường.
#
# Viết hàm `ma_hoa_caesar(van_ban, dich_chuyen)` làm đúng việc `dich_chuoi_thuong` vừa
# làm, cộng thêm hai việc:
#
# 1. Ký tự không phải chữ cái (số, dấu câu, khoảng trắng) giữ nguyên, không dịch. Dùng
#    `c.isalpha()` để kiểm tra trước khi dịch.
# 2. Chữ hoa gọi `dich_ky_tu(c, dich_chuyen, goc="A")`, chữ thường gọi
#    `dich_ky_tu(c, dich_chuyen)`. Dùng `c.isupper()` để biết ký tự đang xét là hoa hay
#    thường.
#
# Ví dụ: `ma_hoa_caesar("Hello, World!", 3)` cho `"Khoor, Zruog!"`.
# `ma_hoa_caesar("Python 3.11", 5)` cho `"Udymts 3.11"`, số và dấu chấm giữ nguyên.

# %%
def ma_hoa_caesar(van_ban, dich_chuyen):
    # TODO: dịch từng chữ cái, giữ nguyên ký tự không phải chữ cái, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_4_2(ma_hoa_caesar)

# %% [markdown]
# ---
# ## Bài 5 — Dict và set
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `{k1: v1, k2: v2}` | dict: các cặp khoá `:` giá trị đặt trong ngoặc nhọn, khoá không trùng nhau. `{}` là dict rỗng | `{"toc_do": 30, "camera": "1080p"}` |
# | `d[k]` | giá trị của khoá `k`, báo `KeyError` nếu `k` chưa có | `{"toc_do": 30}["toc_do"]` → `30` |
# | `d[k] = v` | gán giá trị cho khoá `k`: khoá chưa có thì thêm mới, có rồi thì ghi đè | `cau_hinh["toc_do"] = 40` |
# | `d.get(k, mac_dinh)` | giá trị của khoá `k`, nếu `k` chưa có thì trả về `mac_dinh` thay vì báo lỗi | `{}.get("camera", "chua dat")` → `"chua dat"` |
# | `k in d` | `True` nếu `k` là một khoá của `d` | `"toc_do" in {"toc_do": 30}` → `True` |
# | `d.items()` | các cặp `(khoá, giá trị)` của `d`, dùng trong `for` | `for k, v in d.items():` |
# | `dict(d)` | bản sao của `d` | `d2 = dict(d)` |
# | `d[k].append(x)` | khi giá trị của khoá `k` là một list: thêm `x` vào list đó. Khoá chưa có thì phải gán `d[k] = []` trước | `nhom["P0113"].append(3.4)` |
# | `d.update(d2)` | chép mọi cặp của `d2` vào `d`, khoá trùng thì lấy giá trị của `d2`, sửa thẳng lên `d` | `d.update({"toc_do": 40})` |
# | `{a, b, c}` | set: tập hợp các giá trị không trùng nhau, không có thứ tự | `{"lidar", "gps"}` |
# | `set()` | set rỗng | `da_thay = set()` |
# | `s.add(x)` | thêm `x` vào `s`, `x` đã có thì không đổi gì | `da_thay.add("P0113")` |
# | `x in s` | `True` nếu `x` có trong `s`, tra cứu nhanh | `"gps" in {"lidar", "gps"}` → `True` |
# | `a` &#124; `b` | hợp (ký hiệu là gạch đứng): các phần tử nằm ở `a` hoặc `b` | `{1, 2}` &#124; `{2, 3}` → `{1, 2, 3}` |
# | `a & b` | giao: các phần tử nằm ở cả `a` và `b` | `{1, 2} & {2, 3}` → `{2}` |
# | `a - b` | hiệu: các phần tử nằm ở `a` mà không nằm ở `b` | `{1, 2} - {2, 3}` → `{1}` |
# | `a <= b` | `True` nếu mọi phần tử của `a` đều nằm trong `b` (`a` là tập con của `b`) | `{1, 2} <= {1, 2, 3}` → `True` |
#
# #### ⚠️ Lỗi hay gặp
#
# - `d[k]` với khoá chưa có báo `KeyError`. Dùng `d.get(k, mac_dinh)`, hoặc kiểm tra
#   `k in d` trước.
# - `{}` là dict rỗng. Set rỗng phải viết `set()`.
# - Set không có thứ tự nên không có `s[0]`, và thứ tự in ra có thể khác nhau giữa các
#   lần chạy. Cần thứ tự cố định thì dùng `sorted(s)`.
# - Phần tử của set và khoá của dict phải là kiểu bất biến: số, chuỗi, tuple được,
#   `list` không được. `{[1, 2]}` báo `TypeError`.
# - `d.update(d2)` sửa thẳng lên `d`. Muốn giữ `d` nguyên thì tạo bản sao trước bằng
#   `dict(d)` rồi `update` trên bản sao.

# %%
# 💻 Ví dụ: dict
cau_hinh_xe = {"toc_do": 30, "camera": "1080p"}
print(cau_hinh_xe["toc_do"], cau_hinh_xe.get("mau_son", "chua dat"))    # 30 chua dat

# %% [markdown]
# `cau_hinh_xe["toc_do"]` lấy giá trị của khoá `toc_do`. Khoá `mau_son` chưa có nên
# `.get` trả về giá trị mặc định `"chua dat"`.

# %%
# 💻 Ví dụ: khoá chưa có
# print(cau_hinh_xe["mau_son"])   # Bỏ dấu # để thấy lỗi KeyError

# %% [markdown]
# Truy cập khoá chưa có bằng `[]` thì Python báo lỗi.

# %%
# 💻 Ví dụ: tự làm get bằng if
if "mau_son" in cau_hinh_xe:
    ket_qua_tay = cau_hinh_xe["mau_son"]
else:
    ket_qua_tay = "chua dat"
print(ket_qua_tay == cau_hinh_xe.get("mau_son", "chua dat"))   # True

# %% [markdown]
# Khối `if` và `.get` cho cùng kết quả, `.get` viết gọn hơn.

# %%
# 💻 Ví dụ: update sửa thẳng lên dict gốc
cau_hinh_xe.update({"toc_do": 25, "mau_son": "do"})
print(cau_hinh_xe)    # {'toc_do': 25, 'camera': '1080p', 'mau_son': 'do'}

# %% [markdown]
# `toc_do` bị ghi đè thành `25`, `mau_son` được thêm mới, và `cau_hinh_xe` thay đổi
# ngay.

# %%
# 💻 Ví dụ: đếm bằng dict
dem = {}
for lenh in ["GIAM_TOC", "BINH_THUONG", "GIAM_TOC"]:
    dem[lenh] = dem.get(lenh, 0) + 1     # chưa có khoá thì get trả 0, rồi cộng 1
print(dem)    # {'GIAM_TOC': 2, 'BINH_THUONG': 1}

# %% [markdown]
# Lệnh nào chưa gặp thì `.get` cho `0`, cộng `1` ra lần đếm đầu tiên.

# %%
# 💻 Ví dụ: duyệt dict bằng items
for lenh, so_lan in dem.items():    # items: từng cặp (khoá, giá trị)
    print(lenh, so_lan)

# %% [markdown]
# Mỗi vòng `for` nhận một cặp, tách thành hai biến `lenh` và `so_lan`.

# %%
# 💻 Ví dụ: set loại trùng
da_thay = set()
for ma in ["P0113", "C0035", "P0113"]:
    da_thay.add(ma)
print(len(da_thay), "P0113" in da_thay)    # 2 True

# %% [markdown]
# `P0113` được thêm hai lần nhưng set chỉ giữ một.

# %%
# 💻 Ví dụ: phép toán trên set
xe_a, xe_b = {"P0113", "P0562"}, {"P0562", "C0035"}
print(sorted(xe_a | xe_b))    # ['C0035', 'P0113', 'P0562']
print(xe_a & xe_b, xe_a - xe_b, {"P0113"} <= xe_a)    # {'P0562'} {'P0113'} True

# %% [markdown]
# `|` gộp mã lỗi của hai xe, `&` lấy mã cả hai cùng có, `-` lấy mã chỉ xe A có. `<=`
# hỏi tập bên trái có nằm trọn trong tập bên phải không.

# %%
# 💻 Ví dụ: dict chứa list
nhom = {}
for lenh, giay in [("GIAM_TOC", 3), ("BINH_THUONG", 4), ("GIAM_TOC", 9)]:
    if lenh not in nhom:
        nhom[lenh] = []        # lệnh mới: tạo list rỗng cho khoá đó
    nhom[lenh].append(giay)
print(nhom)    # {'GIAM_TOC': [3, 9], 'BINH_THUONG': [4]}

# %% [markdown]
# Mỗi khoá giữ một list các giây có lệnh đó. Khoá chưa gặp thì tạo list rỗng trước khi `append`.

# %% [markdown]
# ### 🎯 Bài tập 5.1 — Hợp nhất cấu hình
#
# Xe có cấu hình mặc định, người dùng có thể tuỳ chỉnh vài khoá. Viết hàm
# `hop_nhat_cau_hinh(mac_dinh, tuy_chinh)` trả về một dict mới chứa mọi khoá của
# `mac_dinh`, trong đó khoá nào có trong `tuy_chinh` thì lấy giá trị của `tuy_chinh`.
# Khoá chỉ có trong `tuy_chinh` cũng được thêm vào. Không được sửa `mac_dinh` và
# `tuy_chinh`.
#
# Ví dụ: `mac_dinh = {"toc_do": 30, "camera": "1080p"}`, `tuy_chinh = {"toc_do": 40}`
# cho `{"toc_do": 40, "camera": "1080p"}`, và `mac_dinh` vẫn là
# `{"toc_do": 30, "camera": "1080p"}` sau khi gọi.

# %%
def hop_nhat_cau_hinh(mac_dinh, tuy_chinh):
    # TODO: tạo bản sao của mac_dinh, ghi đè bằng tuy_chinh, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_5_1(hop_nhat_cau_hinh)

# %% [markdown]
# ### 🎯 Bài tập 5.2 — Cảm biến còn thiếu
#
# Viết hàm `cam_bien_con_thieu(dang_bat, yeu_cau)` trả về một `set` gồm các cảm biến có
# trong `yeu_cau` mà chưa có trong `dang_bat`.
#
# Ví dụ: `dang_bat = {"lidar", "camera"}`, `yeu_cau = {"lidar", "gps"}` cho `{"gps"}`.
# `dang_bat = {"lidar", "gps", "radar"}`, `yeu_cau = {"lidar"}` cho `set()`, vì
# cảm biến bật dư không tính là thiếu.

# %%
def cam_bien_con_thieu(dang_bat, yeu_cau):
    # TODO: trả về set các cảm biến yêu cầu mà chưa bật
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_5_2(cam_bien_con_thieu)

# %% [markdown]
# ### 📡 Bài tập 5.3 — Đếm giây theo mã fix
#
# Đọc `data/gps.nmea`, bỏ qua câu không phải `$GNGGA`. Mã fix nằm ở cột 6 của câu
# `$GNGGA` (đếm từ 0 sau khi cắt theo dấu phẩy), mỗi câu `$GNGGA` ứng với 1 giây.
#
# Gán `so_giay_theo_fix` là dict có khoá là mã fix (kiểu `int`) và giá trị là số giây
# có mã fix đó.
#
# Ví dụ: ba câu `$GNGGA` có mã fix `4`, `5`, `4` cho `so_giay_theo_fix = {4: 2, 5: 1}`.

# %%
so_giay_theo_fix = None  # TODO

# Viết code đọc file của bạn vào ngay dưới dòng này. Khung cú pháp:
# so_giay_theo_fix = {}
# with open("data/gps.nmea") as f:
#     for dong in f:
#         ...


# %%
kiem_tra_5_3(so_giay_theo_fix)

# %% [markdown]
# ### 📡 Bài tập 5.4 — Thống kê mã lỗi chẩn đoán
#
# `data/ma_loi.csv` là nhật ký mã lỗi chẩn đoán (DTC) mà ECU báo qua OBD-II, 15 dòng dữ
# liệu. Một mã có thể được báo nhiều lần. Đọc file bằng `csv.DictReader`, cột mã lỗi là
# `ma_loi`.
#
# Gán `so_lan_theo_ma` là dict có khoá là mã lỗi và giá trị là số lần mã đó được báo.
# Gán `ma_loi_theo_thu_tu` là list các mã lỗi, mỗi mã một lần, xếp theo thứ tự lần
# đầu xuất hiện. Dùng một `set` để nhớ những mã đã gặp.
#
# Ví dụ: năm dòng có mã `P0113`, `C0035`, `P0113`, `U0121`, `C0035` cho
# `so_lan_theo_ma = {"P0113": 2, "C0035": 2, "U0121": 1}` và
# `ma_loi_theo_thu_tu = ["P0113", "C0035", "U0121"]`.

# %%
so_lan_theo_ma = None        # TODO
ma_loi_theo_thu_tu = None    # TODO

# Viết code đọc file của bạn vào ngay dưới dòng này:


# %%
kiem_tra_5_4(so_lan_theo_ma, ma_loi_theo_thu_tu)

# %% [markdown]
# ### 📡 Bài tập 5.5 — Gom thời điểm theo mã lỗi
#
# Cũng với `data/ma_loi.csv`, đọc bằng `csv.DictReader`, cột thời điểm là `thoi_gian_s`
# (ép sang `float`). Gán `thoi_diem_theo_ma` là dict có khoá là mã lỗi và giá trị là
# list các thời điểm mã đó được báo, theo thứ tự trong file.
#
# Ví dụ: ba dòng `3.40,P0113`, `113.20,C0035`, `21.80,P0113` cho
# `thoi_diem_theo_ma = {"P0113": [3.4, 21.8], "C0035": [113.2]}`.

# %%
thoi_diem_theo_ma = None  # TODO

# Viết code đọc file của bạn vào ngay dưới dòng này. Khung cú pháp:
# thoi_diem_theo_ma = {}
# with open("data/ma_loi.csv") as f:
#     for hang in csv.DictReader(f):
#         ...


# %%
kiem_tra_5_5(thoi_diem_theo_ma)

# %% [markdown]
# ---
# ## Dự án tuần 2 — Kiểm tra trước khi xuất phát và phân tích chuyến xe
#
# Phần 1 viết hàm kiểm tra xe trước khi chạy, ghép hai hàm `hop_nhat_cau_hinh` và
# `cam_bien_con_thieu`. Phần 2 gom dữ liệu của chuyến xe dài 180 giây vào list rồi thống
# kê.
#
# #### Phần 1 — Bộ kiểm tra trước khi xuất phát
#
# Viết hàm `kiem_tra_truoc_khi_di(mac_dinh, tuy_chinh, dang_bat, yeu_cau)` trả về một
# `dict` có ba khoá:
#
# | Khoá | Giá trị |
# |---|---|
# | `"cau_hinh"` | kết quả `hop_nhat_cau_hinh(mac_dinh, tuy_chinh)` |
# | `"cam_bien_thieu"` | kết quả `cam_bien_con_thieu(dang_bat, yeu_cau)` |
# | `"san_sang"` | `True` nếu không thiếu cảm biến nào, ngược lại `False` |
#
# Ví dụ: `mac_dinh = {"toc_do": 30, "camera": "1080p"}`, `tuy_chinh = {"toc_do": 40}`,
# `dang_bat = {"lidar", "camera"}`, `yeu_cau = {"lidar", "gps"}` cho
#
# ```python
# {"cau_hinh": {"toc_do": 40, "camera": "1080p"}, "cam_bien_thieu": {"gps"}, "san_sang": False}
# ```
#
# Bộ chấm gọi hàm ba lần, gồm một lần đủ cảm biến và một lần chưa bật cảm biến nào.

# %%
def kiem_tra_truoc_khi_di(mac_dinh, tuy_chinh, dang_bat, yeu_cau):
    # TODO: gọi hop_nhat_cau_hinh và cam_bien_con_thieu, gộp ba giá trị vào một dict, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_du_an(kiem_tra_truoc_khi_di)

# %% [markdown]
# #### Phần 2 — Phân tích cả chuyến xe
#
# `doc_chuyen_xe()` được viết sẵn. Nó đọc `khoang_cach_truoc.csv` và `obd.csv`, ghép về
# mỗi giây một bộ bốn giá trị:
#
# | Giá trị | Nghĩa |
# |---|---|
# | `t` | thời điểm, giây |
# | `khoang_cach` | khoảng cách phía trước (m), là trung vị các mẫu LiDAR hợp lệ trong giây đó, `None` nếu giây đó không có mẫu hợp lệ |
# | `toc_do` | tốc độ (km/h) |
# | `pin` | mức pin (%) |
#
# Cú pháp lấy bốn giá trị cùng lúc, mỗi vòng gán lần lượt vào bốn tên:
#
# ```python
# for t, khoang_cach, toc_do, pin in doc_chuyen_xe():
#     ...
# ```
#
# Gán bốn biến:
#
# - `toc_do_theo_giay`: list tốc độ `toc_do` của mọi giây, theo thứ tự.
# - `giay_vat_can_gan`: list các `t` mà giây đó có `khoang_cach` và `khoang_cach <= 5.0`.
#   Giây có `khoang_cach` là `None` thì bỏ qua.
# - `toc_do_muot`: trung bình trượt 5 giây của `toc_do_theo_giay`, tính bằng hàm
#   `trung_binh_truot` đã viết.
# - `quang_duong_gps_m`: tổng quãng đường theo GPS (mét), bằng tổng khoảng cách giữa
#   các cặp điểm liền kề của `quy_dao`. `khoang_cach_hai_diem_m(diem_a, diem_b)` viết sẵn,
#   nhận hai tuple `(giay, vi_do, kinh_do)` và trả về khoảng cách giữa hai điểm (mét).
#
# Ví dụ: ba giây `(0, 12.0, 0, 15.8)`, `(1, None, 3, 15.8)`, `(2, 4.2, 8, 15.8)` cho
# `toc_do_theo_giay = [0, 3, 8]` và `giay_vat_can_gan = [2]`. Giây 1 bị bỏ qua khỏi
# `giay_vat_can_gan` vì `khoang_cach` là `None`.
# `quy_dao = [(0, 21.0, 105.8), (1, 21.0001, 105.8), (2, 21.0003, 105.8)]` có hai cặp
# liền kề, cách nhau khoảng 11.1 m và 22.3 m, cho `quang_duong_gps_m` khoảng `33.4`.

# %%
from tests.tien_ich_du_lieu import doc_chuyen_xe, khoang_cach_hai_diem_m, ve_phan_tich_chuyen_xe

toc_do_theo_giay = []    # TODO: thêm tốc độ của từng giây vào list này
giay_vat_can_gan = []    # TODO: thêm các giây có vật cản trong 5 m vào list này
toc_do_muot = None       # TODO
quang_duong_gps_m = None # TODO

# Viết vòng lặp của bạn vào ngay dưới dòng này. Khung cú pháp:
# for t, khoang_cach, toc_do, pin in doc_chuyen_xe():
#     ...


# %%
kiem_tra_lab(toc_do_theo_giay, toc_do_muot, giay_vat_can_gan, quang_duong_gps_m)

# %% [markdown]
# Vẽ tốc độ đã làm mượt cùng các giây có vật cản gần, và số giây theo mã fix GPS
# (`so_giay_theo_fix`).

# %%
ve_phan_tich_chuyen_xe(toc_do_theo_giay, toc_do_muot, giay_vat_can_gan, so_giay_theo_fix)

# %% [markdown]
# ---
# ## Tổng kết tuần 2
#
# Chạy ô dưới để kiểm tra toàn bộ bài trong tuần.

# %%
ket_qua = [
    kiem_tra_1_1(loc_vat_can_gan),
    kiem_tra_1_2(tb_n_mau_cuoi),
    kiem_tra_1_3(toc_do_list, toc_do_cao),
    kiem_tra_1_4(trung_binh_truot),
    kiem_tra_2_1(giay_vuot_nguong),
    kiem_tra_2_2(chenh_lech_lien_tiep),
    kiem_tra_2_3(quy_dao),
    kiem_tra_3_1(giam_toc_do),
    kiem_tra_3_2(tru_hao_pin),
    kiem_tra_3_3(ghi_canh_bao),
    kiem_tra_4_1(loai_cau),
    kiem_tra_4_2(ma_hoa_caesar),
    kiem_tra_5_1(hop_nhat_cau_hinh),
    kiem_tra_5_2(cam_bien_con_thieu),
    kiem_tra_5_3(so_giay_theo_fix),
    kiem_tra_5_4(so_lan_theo_ma, ma_loi_theo_thu_tu),
    kiem_tra_5_5(thoi_diem_theo_ma),
    kiem_tra_du_an(kiem_tra_truoc_khi_di),
    kiem_tra_lab(toc_do_theo_giay, toc_do_muot, giay_vat_can_gan, quang_duong_gps_m),
]

print(f"\nTONG KET TUAN 2: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Lưu bài và nộp bài
#
# Bản mở từ link là bản của repo, không lưu được bài làm. Vào
# `File > Save a copy in Drive` ngay từ đầu rồi làm trên bản trong Drive. Đóng tab khi
# chưa lưu thì bài làm trong phiên này mất.
#
# Để nộp bài:
#
# 1. Tạo repo của bạn từ template tại
#    https://github.com/momofdtt2k15kkk/15-weeks-of-military-training/generate
#    (chỉ làm một lần, nên chọn Private).
# 2. Ở bản trong Drive, vào `File > Save a copy in GitHub` (dòng này chỉ có trên bản
#    trong Drive), chọn repo của bạn, đường dẫn `week2/week_2.ipynb`, ghi commit
#    message dạng `week2: hoan thanh bai tap`.
# 3. Mở tab Actions của repo: dấu xanh là mọi bài đạt, dấu đỏ là còn bài sai.
