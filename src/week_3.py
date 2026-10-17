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
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/momofdtt2k15kkk/15-weeks-of-military-training/blob/main/week3/week_3.ipynb)
#
# # Tuần 3 — Xử lý lỗi & Lập trình hướng đối tượng (OOP)
#
# **Mục tiêu sau tuần này, bạn phải làm được:**
#
# 1. Đọc traceback để biết lỗi gì, ở dòng nào, trong hàm nào.
# 2. Bọc đoạn code có thể lỗi bằng `try/except`, chủ động `raise` khi dữ liệu sai, ghi kết quả ra file.
# 3. Định nghĩa `class` với `__init__`, `self`, thuộc tính và phương thức.
# 4. Viết class tự kiểm tra dữ liệu, in ra dễ đọc, và chứa các object khác.
# 5. Viết một ứng dụng nhỏ có trạng thái (Budget App) hoàn toàn bằng OOP.
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
FILE_TESTS = ("runner.py", "test_week3.py", "tien_ich_du_lieu.py")
FILE_DATA = ("khoang_cach_truoc.csv", "obd.csv", "nhat_ky_tho.csv")

# Mở notebook từ thư mục week3/ trên máy: lùi ra thư mục gốc, nơi có sẵn tests/.
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

from tests.test_week3 import (
    kiem_tra_1_1,
    kiem_tra_1_2,
    kiem_tra_1_3,
    kiem_tra_1_4,
    kiem_tra_2_1,
    kiem_tra_2_2,
    kiem_tra_3_1,
    kiem_tra_3_2,
    kiem_tra_3_3,
    kiem_tra_4_1,
    kiem_tra_4_2,
    kiem_tra_5_1,
    kiem_tra_5_2,
    kiem_tra_du_an,
)

print("Moi truong san sang. Phien ban Python:", sys.version.split()[0])

# %% [markdown]
# ---
# ## Cách làm bài và chấm bài
#
# Mỗi bài tập gồm hai ô đi liền nhau: ô bạn viết code, và ô kiểm tra ngay dưới nó. Ô
# kiểm tra đọc các biến, hàm hoặc class mà ô trên tạo ra, nên **tên phải khớp từng chữ**.
#
# Mỗi đề bài có năm mục, đọc theo thứ tự:
#
# | Mục | Cho biết |
# |---|---|
# | **Đầu vào** | dữ liệu lấy từ đâu, và bạn có phải tự khai báo dữ liệu không |
# | **Bạn viết** | hàm, class hay đoạn code gán biến, tên là gì |
# | **Đầu ra** | hàm trả về gì, hoặc biến nào phải có giá trị gì |
# | **Ví dụ** | đầu vào cụ thể và kết quả đúng |
# | **Bộ chấm** | ô kiểm tra sẽ gọi hàm hay tạo object như thế nào |
#
# Trong ô code, dòng `# ---------- Dữ liệu cho sẵn, không sửa ----------` đánh dấu phần
# đề bài đã viết sẵn. Bạn viết ở dưới dòng `# ---------- Chỗ bạn viết ----------`.
#
# 1. Sửa xong ô code phải chạy lại chính ô đó rồi mới chạy ô kiểm tra.
# 2. Chưa làm gì mà chạy ô kiểm tra thì nó báo FAIL. Đó là trạng thái bình thường lúc mới mở
#    notebook.
# 3. Dòng "mong đợi" trong báo lỗi cho biết đáp án đúng phải trông ra sao. So nó với dòng
#    "thực tế" để biết lệch ở đâu.
#
# Chạy lại cả notebook từ đầu bằng `Runtime > Restart and run all` nếu thấy kết quả lộn xộn
# không giải thích được.

# %% [markdown]
# ---
# ## Bài 1 — Lỗi, ngoại lệ và ghi file
#
# File log thô của xe luôn có dòng hỏng: cảm biến ghi `N/A`, mất điện làm dòng bị cắt
# ngang, log khởi động lại chèn dòng tiêu đề vào giữa. Bài này giúp chương trình đọc hết
# file mà không dừng giữa chừng, rồi ghi phần dữ liệu tốt ra file mới.
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | traceback | thông báo Python in ra khi chương trình dừng vì lỗi. Đọc từ dòng cuối lên: dòng cuối là loại lỗi và lý do, các cặp dòng phía trên là đường đi qua các hàm | `ValueError: could not convert string to float: 'N/A'` |
# | `try:` rồi `except LoaiLoi:` | chạy khối `try`; nếu một dòng trong đó gây lỗi `LoaiLoi` thì nhảy ngay xuống khối `except`, chương trình không dừng | `try:` / `    x = float(o)` / `except ValueError:` / `    x = None` |
# | `except (LoaiA, LoaiB):` | một khối `except` bắt nhiều loại lỗi, các loại đặt trong ngoặc tròn | `except (ValueError, IndexError):` |
# | nhiều khối `except` liền nhau | mỗi loại lỗi một cách xử lý, xét từ trên xuống, gặp khối khớp đầu tiên thì dừng | `except IndexError:` rồi `except ValueError:` |
# | `except LoaiLoi as loi:` | gán lỗi vừa bắt vào biến `loi`, `str(loi)` là câu thông báo của lỗi | `print(str(loi))` |
# | `else:` | đặt sau các `except`, chỉ chạy khi khối `try` không có lỗi nào | `else:` / `    print(x * 2)` |
# | `finally:` | đặt cuối cùng, luôn chạy, có lỗi hay không, kể cả khi `try` đã `return` | `finally:` / `    print("xong")` |
# | `raise ValueError("thong bao")` | chủ động báo lỗi ngay tại dòng đó, khi dữ liệu sai theo luật của bạn | `raise ValueError("toc_do ngoai tam")` |
# | `s.replace(a, b)` | chuỗi mới, mọi đoạn `a` trong `s` được thay bằng `b` | `"40,5".replace(",", ".")` → `"40.5"` |
# | `s.upper()` | chuỗi mới, viết hoa toàn bộ | `"n/a".upper()` → `"N/A"` |
# | `open(duong_dan, "w")` | mở file để ghi: chưa có thì tạo mới, có rồi thì xoá sạch nội dung cũ | `with open("bao_cao.txt", "w") as f:` |
# | `f.write(s)` | ghi chuỗi `s` vào file, không tự xuống dòng | `f.write("dong 1\n")` |
# | `csv.writer(f)` và `w.writerow(ds)` | ghi list `ds` thành một dòng CSV, tự thêm dấu phẩy và xuống dòng | `w.writerow([0.0, 0, 12.0])` |
# | `newline=""` | tham số của `open` khi ghi CSV, tránh dòng trống xen giữa trên Windows | `open("a.csv", "w", newline="")` |
# | `FileNotFoundError` | lỗi khi mở để đọc một file không có | `open("data/khong_co.csv")` |
#
# Các loại lỗi hay gặp, mỗi loại kèm một dòng gây ra nó:
#
# | Lỗi | Khi nào | Dòng gây lỗi |
# |---|---|---|
# | `ValueError` | đúng kiểu nhưng giá trị không dùng được | `float("N/A")` |
# | `TypeError` | sai kiểu, hoặc gọi hàm sai số tham số | `"40" + 5` |
# | `ZeroDivisionError` | chia cho 0 | `10 / 0` |
# | `NameError` | dùng tên chưa được gán | `print(toc_do_chua_co)` |
# | `IndexError` | chỉ số vượt ngoài list | `"12.50,40".split(",")[3]` |
# | `KeyError` | khoá không có trong dict | `{"a": 1}["b"]` |
# | `AttributeError` | object không có thuộc tính hoặc phương thức đó | `"abc".lenght` |
# | `FileNotFoundError` | mở để đọc file không có | `open("khong_co.csv")` |
#
# #### ⚠️ Lỗi hay gặp
#
# - `except:` không ghi loại lỗi thì bắt luôn cả lỗi do chính bạn gõ sai tên biến. Luôn ghi
#   rõ loại lỗi: `except ValueError:`.
# - Đặt `except Exception:` (bắt mọi loại lỗi) lên trước các `except` cụ thể thì các khối
#   sau không bao giờ chạy tới.
# - Nhét cả chục dòng vào `try` làm khó biết dòng nào lỗi. Chỉ để trong `try` dòng có thể
#   lỗi, phần chạy tiếp khi thành công đặt vào `else`.
# - `open(..., "w")` xoá sạch file cũ. Muốn ghi nối vào cuối file thì mở bằng `"a"`.
# - Quên `"\n"` khi `f.write(...)` thì mọi dòng dính vào nhau.

# %%
# 💻 Ví dụ: một lỗi khi chạy
# print(float("N/A"))   # Bỏ dấu # để thấy lỗi ValueError

# %% [markdown]
# `float` không đọc được `"N/A"`, Python dừng chương trình và in traceback.

# %%
# 💻 Ví dụ: đọc traceback qua hai hàm
import traceback


def doi_so(o):
    return float(o)


def doc_toc_do(dong):
    cot = dong.split(",")
    return doi_so(cot[1])


try:
    doc_toc_do("12.60,N/A,8.20,0.010")
except ValueError:
    traceback.print_exc()      # in traceback ra mà notebook không dừng, try/except học ngay dưới

# %% [markdown]
# Đọc traceback vừa in, từ dưới lên:
#
# | Dòng | Cho biết |
# |---|---|
# | cuối cùng: `ValueError: could not convert string to float: 'N/A'` | loại lỗi và lý do |
# | ngay trên: `return float(o)` trong `doi_so` | dòng thật sự gây lỗi |
# | trên nữa: `return doi_so(cot[1])` trong `doc_toc_do` | hàm nào đã gọi `doi_so`, với ô nào |
#
# Lỗi nổ ở `doi_so` nhưng nguyên nhân là ô `N/A` mà `doc_toc_do` truyền vào.

# %%
# 💻 Ví dụ: try / except
o = "N/A"
try:
    toc_do = float(o)
except ValueError:
    toc_do = None
print(toc_do)    # None

# %% [markdown]
# `float(o)` gây `ValueError`, Python nhảy xuống khối `except`, gán `None`, rồi chạy tiếp.

# %%
# 💻 Ví dụ: lỗi xảy ra trước khi kịp gán
o = "ERR"
try:
    toc_do_2 = float(o)
except ValueError:
    print("o khong phai so:", o)
# print(toc_do_2 * 2)   # Bỏ dấu # để thấy lỗi NameError

# %% [markdown]
# `float(o)` lỗi nên dòng gán `toc_do_2 = ...` chưa chạy xong, tên `toc_do_2` chưa tồn tại.
# Phần chỉ chạy khi thành công phải đặt vào `else`.

# %%
# 💻 Ví dụ: else
for o in ["40", "N/A"]:
    try:
        so = float(o)
    except ValueError:
        print(o, "-> bo qua")
    else:
        print(o, "->", so * 2)    # chỉ chạy khi float(o) thành công

# %% [markdown]
# Với `"40"` khối `else` chạy, với `"N/A"` khối `except` chạy.

# %%
# 💻 Ví dụ: nhiều except
for dong in ["12.50,40", "12.60,N/A,8.20,0.010"]:
    cot = dong.split(",")
    try:
        toc_do = float(cot[1])
        khoang_cach = float(cot[2])
    except IndexError:
        print("thieu cot:", dong)
    except ValueError:
        print("sai so:", dong)

# %% [markdown]
# Dòng đầu chỉ có 2 cột nên `cot[2]` gây `IndexError`. Dòng hai có ô `N/A` nên `float`
# gây `ValueError`. Mỗi lỗi rơi vào đúng khối của nó.

# %%
# 💻 Ví dụ: as loi
try:
    float("ERR")
except ValueError as loi:          # as loi: giữ lại lỗi vừa bắt
    print("thong bao:", str(loi))

# %% [markdown]
# `str(loi)` là câu Python giải thích lỗi, dùng được để in hoặc ghi vào nhật ký.

# %%
# 💻 Ví dụ: đếm dòng hỏng trong cả file
dem_hong = 0
with open("data/nhat_ky_tho.csv") as f:
    next(f)                                   # bỏ dòng tiêu đề
    for dong in f:
        try:
            ax = float(dong.strip().split(",")[3])
        except (ValueError, IndexError):      # một khối bắt hai loại lỗi
            dem_hong += 1
print(dem_hong)    # 32

# %% [markdown]
# Ô này chỉ xét cột `ax` (cột 3), nên đếm được các dòng bị cắt, dòng tiêu đề lặp và dòng hỏng
# ô `ax`. Ô hỏng ở cột khác thì ô này không thấy.

# %%
# 💻 Ví dụ: finally
def doc_mot_o(o):
    try:
        return float(o)
    except ValueError:
        return None
    finally:
        print("da xu ly o:", o)       # chạy cả khi try đã return


print(doc_mot_o("8.2"), doc_mot_o("ERR"))

# %% [markdown]
# Hai dòng `da xu ly o` in ra trước, vì `finally` chạy xong rồi hàm mới trả giá trị về.

# %%
# 💻 Ví dụ: raise trong hàm, bắt ở nơi gọi
def doc_khoang_cach_m(o):
    kc = float(o)
    if kc < 0.1 or kc > 12.0:
        raise ValueError(f"khoang cach {kc} m ngoai tam LiDAR")
    return kc


for o in ["8.2", "-3.00"]:
    try:
        print(doc_khoang_cach_m(o))
    except ValueError as loi:
        print("bo qua:", loi)

# %% [markdown]
# `-3.0` đọc được thành số nên Python không tự báo lỗi. Hàm tự `raise` theo luật tầm đo
# LiDAR, còn nơi gọi quyết định bỏ qua dòng đó.

# %%
# 💻 Ví dụ: except trống nuốt lỗi gõ sai
o = "8.2"
try:
    so = flaot(o)          # gõ nhầm float thành flaot
except:                    # không ghi loại lỗi: bắt luôn NameError
    so = None
print(so)    # None

# %% [markdown]
# Ô `"8.2"` hoàn toàn đúng, nhưng kết quả là `None`, vì `except` trống đã giấu lỗi gõ sai
# tên hàm. Viết `except ValueError:` thì Python báo `NameError` ngay.

# %%
# 💻 Ví dụ: replace và upper
print("40,5".replace(",", "."), " n/a ".strip().upper())    # 40.5 N/A

# %% [markdown]
# Hai hàm đều trả chuỗi mới, chuỗi gốc giữ nguyên.

# %%
# 💻 Ví dụ: ghi file chữ
with open("vi_du_bao_cao.txt", "w") as f:
    f.write("so dong hong: 3\n")
    f.write("so dong tot: 97\n")
print(open("vi_du_bao_cao.txt").read())

# %% [markdown]
# Mỗi `f.write` cần `"\n"` ở cuối để xuống dòng. Ra khỏi khối `with` thì file tự đóng.

# %%
# 💻 Ví dụ: ghi file CSV
import csv

with open("vi_du_sach.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["thoi_gian_s", "toc_do_kmh"])     # dòng tiêu đề
    w.writerow([0.0, 0])
    w.writerow([0.1, 0])
print(open("vi_du_sach.csv").read())

# %% [markdown]
# `writerow` tự nối các phần tử bằng dấu phẩy và tự xuống dòng.

# %%
# 💻 Ví dụ: file không có
try:
    open("data/khong_co.csv")
except FileNotFoundError as loi:
    print("khong mo duoc:", loi)

# %% [markdown]
# Đọc file từ đường dẫn người dùng gõ vào thì nên bắt `FileNotFoundError`.

# %% [markdown]
# ### 🎯 Bài tập 1.1 — Đọc một ô số
#
# **Đầu vào:** tham số `chuoi` (str) là một ô của file log, do bộ chấm tự truyền vào. Bạn
# không cần khai báo dữ liệu.
#
# **Bạn viết:** hàm `doc_so(chuoi)`. Bỏ khoảng trắng hai đầu, đổi dấu phẩy thành dấu chấm (có
# kỹ thuật viên ghi số kiểu `40,5`), rồi ép sang `float` trong khối `try`.
#
# **Đầu ra:** trả về số `float`. Ép không được thì trả về `None`.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `doc_so("12.5")` | `12.5` |
# | `doc_so(" 7 ")` | `7.0` |
# | `doc_so("40,5")` | `40.5` |
# | `doc_so("N/A")` | `None` |
# | `doc_so("")` | `None` |
#
# **Bộ chấm:** gọi hàm 7 lần, gồm 5 trường hợp trên, `"ERR"` và `"-3.00"`.

# %%
def doc_so(chuoi):
    # TODO: strip, replace, rồi float trong try; lỗi ValueError thì trả về None
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_1_1(doc_so)

# %% [markdown]
# ### 📡 Bài tập 1.2 — Phân loại một dòng log
#
# **Đầu vào:** tham số `dong` (str) là một dòng của `data/nhat_ky_tho.csv` (có thể còn ký tự
# xuống dòng `\n` ở cuối), do bộ chấm tự truyền vào. Bạn không cần mở file. Một dòng tốt có
# 4 cột số: `thoi_gian_s,toc_do_kmh,khoang_cach_m,ax`.
#
# **Bạn viết:** hàm `phan_loai_dong(dong)`. Bỏ `\n`, cắt theo dấu phẩy, rồi trong khối `try`
# ép cả 4 cột (chỉ số `0` đến `3`) sang `float`. Dùng hai khối `except`.
#
# **Đầu ra:** trả về một trong ba chuỗi:
#
# | Trả về | Khi nào |
# |---|---|
# | `"THIEU_COT"` | gặp `IndexError`: dòng có ít hơn 4 cột |
# | `"SAI_SO"` | gặp `ValueError`: có ô không phải số |
# | `"OK"` | ép được cả 4 cột |
#
# Hàm chỉ xét định dạng. Số vô lý như khoảng cách `-3.00` vẫn là `"OK"`, việc đó để bài 1.3.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `phan_loai_dong("12.30,40,8.20,0.010\n")` | `"OK"` |
# | `phan_loai_dong("12.50,40")` | `"THIEU_COT"` |
# | `phan_loai_dong("12.60,N/A,8.20,0.010")` | `"SAI_SO"` |
# | `phan_loai_dong("thoi_gian_s,toc_do_kmh,khoang_cach_m,ax")` | `"SAI_SO"` |
# | `phan_loai_dong("16.10,2,-3.00,0.552")` | `"OK"` |
#
# **Bộ chấm:** gọi hàm 7 lần, gồm 5 trường hợp trên, một dòng chỉ còn 1 cột và một dòng có ô
# trống.

# %%
def phan_loai_dong(dong):
    # TODO: strip, split(","), ép 4 cột trong try, except IndexError, except ValueError, kết thúc bằng return
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_1_2(phan_loai_dong)

# %% [markdown]
# ### 🎯 Bài tập 1.3 — Kiểm tra giá trị hợp lý
#
# **Đầu vào:** tham số `toc_do_kmh` và `khoang_cach_m` (số) do bộ chấm tự truyền vào. Bạn
# không cần khai báo dữ liệu.
#
# **Bạn viết:** hàm `kiem_tra_mau(toc_do_kmh, khoang_cach_m)`, kiểm tra theo đúng thứ tự:
#
# 1. Tốc độ phải trong khoảng 0 đến 250 km/h (tính cả hai đầu). Sai thì
#    `raise ValueError("toc_do ngoai tam")`.
# 2. Khoảng cách phải trong khoảng 0.1 đến 12.0 m, tầm đo của LiDAR (tính cả hai đầu). Sai thì
#    `raise ValueError("khoang_cach ngoai tam")`.
#
# **Đầu ra:** hợp lệ thì trả về `True`. Không hợp lệ thì không trả về gì, mà `raise` lỗi với
# đúng câu thông báo ở trên.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `kiem_tra_mau(40, 8.2)` | `True` |
# | `kiem_tra_mau(0, 12.0)` | `True` |
# | `kiem_tra_mau(40, -3.0)` | `ValueError: khoang_cach ngoai tam` |
# | `kiem_tra_mau(900, 8.2)` | `ValueError: toc_do ngoai tam` |
# | `kiem_tra_mau(900, -3.0)` | `ValueError: toc_do ngoai tam` (cả hai sai thì báo tốc độ trước) |
#
# **Bộ chấm:** gọi hàm 8 lần, gồm cả hai đầu của mỗi khoảng, và so cả loại lỗi lẫn câu thông
# báo.

# %%
def kiem_tra_mau(toc_do_kmh, khoang_cach_m):
    # TODO: kiểm tra tốc độ rồi khoảng cách, sai thì raise ValueError, đúng thì return True
    pass  # Bỏ pass khi hoàn thiện hàm


# %%
kiem_tra_1_3(kiem_tra_mau)

# %% [markdown]
# ### 📡 Bài tập 1.4 — Làm sạch log thô
#
# **Đầu vào:** file `data/nhat_ky_tho.csv`, log thô 10 mẫu mỗi giây của cả chuyến xe 180 giây.
# Bạn tự mở file bằng `open`. Dòng đầu là tiêu đề. File có dòng bị cắt (mất điện), ô `N/A`,
# `ERR` hoặc để trống, giá trị vô lý, và 2 dòng tiêu đề lặp giữa file (log khởi động lại).
# Hai biến kết quả đã khởi tạo sẵn là `None` trong ô dưới.
#
# **Bạn viết:** đoạn code duyệt từng dòng (bỏ dòng tiêu đề đầu tiên bằng `next(f)`), và với
# mỗi dòng:
#
# 1. Gọi `phan_loai_dong` (bài 1.2). Khác `"OK"` thì đếm vào loại đó, sang dòng sau.
# 2. Dòng `"OK"` thì đổi 4 cột sang `float`, gọi `kiem_tra_mau` (bài 1.3) trong `try`. Gặp
#    `ValueError` thì đếm vào `"NGOAI_TAM"`, sang dòng sau.
# 3. Dòng qua được cả hai bước là dòng hợp lệ: đếm, và ghi 4 số của nó ra file mới.
#
# **Đầu ra:**
#
# - Biến `so_dong_hop_le` (int): số dòng hợp lệ.
# - Biến `so_loi_theo_loai` (dict): đúng ba khoá `"THIEU_COT"`, `"SAI_SO"`, `"NGOAI_TAM"`, giá
#   trị là số dòng mỗi loại.
# - File `nhat_ky_sach.csv` ở thư mục làm việc (cạnh thư mục `data/`, mở bằng
#   `open("nhat_ky_sach.csv", "w", newline="")`): dòng đầu là tiêu đề
#   `thoi_gian_s,toc_do_kmh,khoang_cach_m,ax`, sau đó là các dòng hợp lệ theo đúng thứ tự.
#
# **Ví dụ:** file chỉ có 5 dòng dữ liệu `0.00,0,12.00,0.000`, `0.10,0,12.00,-0.064`,
# `0.20,0`, `0.30,N/A,12.00,0.010`, `0.40,0,-3.00,0.020` cho `so_dong_hop_le = 2`,
# `so_loi_theo_loai = {"THIEU_COT": 1, "SAI_SO": 1, "NGOAI_TAM": 1}`, và file sạch có tiêu đề
# cùng 2 dòng đầu.
#
# **Bộ chấm:** so hai biến với đáp án tính từ `nhat_ky_tho.csv`, rồi mở lại `nhat_ky_sach.csv`
# bạn vừa ghi và so từng số.

# %%
so_dong_hop_le = None     # TODO
so_loi_theo_loai = None   # TODO

# ---------- Chỗ bạn viết ----------
# Khung cú pháp:
# so_dong_hop_le = 0
# so_loi_theo_loai = {"THIEU_COT": 0, "SAI_SO": 0, "NGOAI_TAM": 0}
# with open("data/nhat_ky_tho.csv") as f, open("nhat_ky_sach.csv", "w", newline="") as f_sach:
#     w = csv.writer(f_sach)
#     w.writerow(["thoi_gian_s", "toc_do_kmh", "khoang_cach_m", "ax"])
#     next(f)
#     for dong in f:
#         ...


# %%
kiem_tra_1_4(so_dong_hop_le, so_loi_theo_loai)

# %% [markdown]
# ---
# ## Bài 2 — Từ dict đến class
#
# Phần còn lại của tuần là lập trình hướng đối tượng (OOP). Ý chính: gói dữ liệu của một thứ
# (một điểm GPS, một chiếc lốp, một chiếc xe) cùng với các việc làm trên dữ liệu đó vào chung
# một chỗ. Bài này đi từ cách lưu bạn đã biết (tuple, dict) để thấy vì sao cần class.
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `class TenClass:` | định nghĩa class: một kiểu dữ liệu mới do bạn tự đặt. Thân class thụt vào 4 dấu cách | `class DiemGps:` |
# | `TenClass(...)` | tạo một object (còn gọi là instance) của class, tức một giá trị cụ thể thuộc kiểu đó | `p = DiemGps(0, 21.0045, 105.843)` |
# | `def __init__(self, ...):` | hàm khởi tạo: Python tự gọi ngay khi tạo object, để gán các thuộc tính ban đầu. Hai dấu gạch dưới mỗi bên | `def __init__(self, giay, vi_do, kinh_do):` |
# | `self` | tham số đầu tiên của hàm trong class, chính là object đang được tạo hoặc đang được dùng. Python tự truyền, bạn không truyền | `self.vi_do = vi_do` |
# | `self.ten = gia_tri` | tạo hoặc gán thuộc tính `ten` cho object | `self.giay = giay` |
# | `obj.ten` | đọc thuộc tính `ten` của object `obj` | `p.vi_do` → `21.0045` |
# | `ChuHoaDauTu` | quy ước đặt tên class: viết hoa chữ đầu mỗi từ, không gạch dưới | `DiemGps`, `MauCamBien` |
#
# #### ⚠️ Lỗi hay gặp
#
# - Quên `self.` khi gán trong `__init__` (`vi_do = vi_do`) thì giá trị chỉ là biến tạm của
#   hàm, object không có thuộc tính đó, đọc ra báo `AttributeError`.
# - `__init__` viết thiếu dấu gạch dưới (`_init_`, `init`) thì Python không tự gọi, tạo object
#   với tham số báo `TypeError`.
# - Tạo object thiếu tham số báo `TypeError: __init__() missing 1 required positional argument`.
# - Tên thuộc tính phải khớp từng chữ: gán `self.vi_do` thì đọc `p.vi_do`, không phải `p.vido`.

# %%
# 💻 Ví dụ: một điểm GPS lưu bằng tuple
diem = (113, 21.00733, 105.83817)      # (giây, vĩ độ, kinh độ)
print(diem[1])                          # 21.00733

# %% [markdown]
# Đọc được, nhưng phải nhớ cột `1` là vĩ độ. Đọc lại code sau một tuần thì `diem[1]` không
# nói gì.

# %%
# 💻 Ví dụ: cùng điểm đó lưu bằng dict
diem_dict = {"giay": 113, "vi_do": 21.00733, "kinh_do": 105.83817}
print(diem_dict["vi_do"])               # 21.00733

# %% [markdown]
# Tên khoá nói rõ đây là vĩ độ. Nhưng dict không biết một điểm GPS phải có những khoá nào.

# %%
# 💻 Ví dụ: dict gõ sai khoá
# print(diem_dict["vido"])   # Bỏ dấu # để thấy lỗi KeyError

# %% [markdown]
# Gõ sai khoá thì chỉ biết lúc chạy. Một dict khác thiếu khoá `"kinh_do"` cũng không ai chặn.

# %%
# 💻 Ví dụ: dữ liệu ở một nơi, hàm ở nơi khác
def mo_ta_diem(d):
    return f"giay {d['giay']}: ({d['vi_do']}, {d['kinh_do']})"


print(mo_ta_diem(diem_dict))

# %% [markdown]
# Hàm `mo_ta_diem` chỉ dùng được với dict có đúng ba khoá đó, nhưng nằm rời ở ngoài. Class gói
# chung cả dữ liệu lẫn hàm vào một chỗ.

# %%
# 💻 Ví dụ: class đầu tiên
class DiemGpsRong:
    pass                        # class chưa có gì


p = DiemGpsRong()               # tạo một object
p.vi_do = 21.00733              # gán thuộc tính bằng dấu chấm
print(p.vi_do, type(p))

# %% [markdown]
# `type(p)` cho biết `p` thuộc kiểu `DiemGpsRong`, một kiểu bạn vừa tự tạo.

# %%
# 💻 Ví dụ: object khác thiếu thuộc tính
q = DiemGpsRong()
# print(q.vi_do)   # Bỏ dấu # để thấy lỗi AttributeError

# %% [markdown]
# `q` chưa được gán `vi_do`. Gán tay từng object thì dễ sót, `__init__` giải quyết việc này.

# %%
# 💻 Ví dụ: __init__ và self
class DiemGps:
    def __init__(self, giay, vi_do, kinh_do):     # Python tự gọi khi tạo object
        self.giay = giay                          # self: chính object đang được tạo
        self.vi_do = vi_do
        self.kinh_do = kinh_do


p1 = DiemGps(113, 21.00733, 105.83817)
print(p1.giay, p1.vi_do, p1.kinh_do)

# %% [markdown]
# Vết chạy dòng `p1 = DiemGps(113, 21.00733, 105.83817)`:
#
# | Bước | Python làm gì | Kết quả |
# |---|---|---|
# | 1 | tạo một object rỗng kiểu `DiemGps` | object chưa có thuộc tính nào |
# | 2 | gọi `__init__`, gán `self` là object đó, `giay = 113`, `vi_do = 21.00733`, `kinh_do = 105.83817` | |
# | 3 | chạy `self.giay = giay` | object có thuộc tính `giay` là `113` |
# | 4 | chạy hai dòng còn lại | object có thêm `vi_do`, `kinh_do` |
# | 5 | `__init__` xong, object được gán vào `p1` | `p1.vi_do` là `21.00733` |
#
# Bạn truyền 3 giá trị, nhưng `__init__` có 4 tham số: `self` do Python tự truyền.

# %%
# 💻 Ví dụ: nhiều object từ một class
p2 = DiemGps(114, 21.00737, 105.83817)
p3 = DiemGps(115, 21.00739, 105.83817)
print(p1.giay, p2.giay, p3.giay)    # 113 114 115

# %% [markdown]
# Ba object, cùng khuôn `DiemGps`, mỗi object giữ giá trị riêng.

# %%
# 💻 Ví dụ: thiếu tham số khi tạo object
# DiemGps(113, 21.00733)   # Bỏ dấu # để thấy lỗi TypeError

# %% [markdown]
# `__init__` cần đủ `giay`, `vi_do`, `kinh_do`. Thiếu một là không tạo được object.

# %%
# 💻 Ví dụ: quên self khi gán
class DiemGpsQuenSelf:
    def __init__(self, giay, vi_do):
        self.giay = giay
        vi_do = vi_do            # quên self.: chỉ là biến tạm trong hàm


d = DiemGpsQuenSelf(113, 21.00733)
print(d.giay)
# print(d.vi_do)   # Bỏ dấu # để thấy lỗi AttributeError

# %% [markdown]
# Không có `self.` phía trước thì giá trị mất khi `__init__` chạy xong.

# %%
# 💻 Ví dụ: mọi giá trị đều là object
print(type(5), type("abc"), type([1, 2]), type(p1))

# %% [markdown]
# `int`, `str`, `list` cũng là class. Số `5` là một object của class `int`, giống `p1` là một
# object của class `DiemGps`.

# %%
# 💻 Ví dụ: tạo nhiều object từ list tuple
quy_dao_tho = [(0, 21.00451, 105.84297), (113, 21.00733, 105.83817), (114, 21.00737, 105.83817)]
cac_diem = [DiemGps(g, vd, kd) for g, vd, kd in quy_dao_tho]
print(len(cac_diem), cac_diem[1].vi_do)    # 3 21.00733

# %% [markdown]
# Mỗi tuple thành một object. Từ đây đọc `cac_diem[1].vi_do` thay cho `quy_dao_tho[1][1]`.

# %% [markdown]
# ### 🎯 Bài tập 2.1 — Class MauCamBien
#
# **Đầu vào:** bộ chấm tự tạo object bằng `MauCamBien(...)` với ba giá trị. Bạn không cần tạo
# object.
#
# **Bạn viết:** class `MauCamBien` có `__init__(self, thoi_gian_s, toc_do_kmh, khoang_cach_m)`,
# lưu ba tham số thành ba thuộc tính cùng tên.
#
# **Đầu ra:** mỗi object có ba thuộc tính `thoi_gian_s`, `toc_do_kmh`, `khoang_cach_m`.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `m = MauCamBien(113.0, 29, 7.36)` rồi `m.toc_do_kmh` | `29` |
# | `m.khoang_cach_m` | `7.36` |
# | `MauCamBien(5.0, 12, None).khoang_cach_m` | `None` |
#
# **Bộ chấm:** tạo 3 object, đọc đủ ba thuộc tính của mỗi object, và kiểm tra hai object
# không dính giá trị của nhau.

# %%
class MauCamBien:
    def __init__(self, thoi_gian_s, toc_do_kmh, khoang_cach_m):
        # TODO: gán ba tham số thành ba thuộc tính self.<ten> cùng tên
        pass  # Bỏ pass khi hoàn thiện


# %%
kiem_tra_2_1(MauCamBien)

# %% [markdown]
# ### 📡 Bài tập 2.2 — Danh sách mẫu của chuyến xe
#
# **Đầu vào:** hàm `doc_chuyen_xe()` viết sẵn. Nó đọc `data/khoang_cach_truoc.csv` và
# `data/obd.csv`, mỗi vòng `for` cho một giây của chuyến xe dưới dạng bốn giá trị:
#
# | Giá trị | Nghĩa |
# |---|---|
# | `t` | thời điểm, giây |
# | `khoang_cach` | khoảng cách phía trước (m), `None` nếu giây đó LiDAR không có mẫu hợp lệ |
# | `toc_do` | tốc độ (km/h) |
# | `pin` | mức pin (%) |
#
# Bạn không cần mở file. List `danh_sach_mau` đã khởi tạo sẵn là list rỗng trong ô dưới.
#
# **Bạn viết:** vòng `for t, khoang_cach, toc_do, pin in doc_chuyen_xe():`, mỗi vòng tạo một
# `MauCamBien(t, toc_do, khoang_cach)` và `append` vào `danh_sach_mau`. Chú ý thứ tự tham số
# của `MauCamBien`: thời gian, tốc độ, khoảng cách.
#
# **Đầu ra:** biến `danh_sach_mau`, list 181 object `MauCamBien`, phần tử thứ `i` là giây `i`.
#
# **Ví dụ:** phần tử đầu có `thoi_gian_s = 0`, `toc_do_kmh = 0`, `khoang_cach_m = 12.0`. Phần tử
# 113 (giây 113, ngay lúc phanh gấp vì vật cản) có `toc_do_kmh = 29`.
#
# **Bộ chấm:** kiểm tra độ dài, kiểu của từng phần tử, và ba thuộc tính ở giây 0, 113, 180.

# %%
from tests.tien_ich_du_lieu import doc_chuyen_xe

danh_sach_mau = []     # TODO: thêm đủ 181 object MauCamBien vào list này

# ---------- Chỗ bạn viết ----------


# %%
kiem_tra_2_2(danh_sach_mau)

# %% [markdown]
# ---
# ## Bài 3 — Phương thức
#
# Class ở Bài 2 mới giữ dữ liệu. Bài này thêm hành vi: các hàm đặt trong class, làm việc trên
# chính dữ liệu của object.
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `def ten(self, ...):` trong class | phương thức (method): hàm đặt trong class, tham số đầu luôn là `self` | `def ap_suat_bar(self):` |
# | `obj.ten(...)` | gọi phương thức trên object `obj`, Python tự truyền `obj` vào `self` | `lop.ap_suat_bar()` |
# | `obj.ten()` bằng `TenClass.ten(obj)` | hai cách gọi cho cùng kết quả, cách đầu là cách viết thường dùng | `LopXe.ap_suat_bar(lop)` |
# | `self.thuoc_tinh = ...` trong phương thức | phương thức đổi dữ liệu của object | `self.ap_suat_kpa += kpa` |
# | `self.phuong_thuc_khac()` | phương thức gọi phương thức khác của cùng object | `if self.can_bom():` |
# | trả `True` / `False` | quy ước cho phương thức có thể từ chối: làm được thì đổi dữ liệu và trả `True`, không thì giữ nguyên và trả `False` | `return False` |
#
# #### ⚠️ Lỗi hay gặp
#
# - Quên `self` ở dòng `def` thì gọi `obj.ten()` báo
#   `TypeError: ... takes 0 positional arguments but 1 was given`.
# - Trong phương thức, đọc thuộc tính phải có `self.`: viết `ap_suat_kpa` trống trơn báo
#   `NameError`.
# - Gọi `obj.ten` không có ngoặc tròn thì không chạy phương thức, chỉ lấy ra chính phương thức.
# - Phương thức từ chối thì phải `return False` trước khi đổi dữ liệu, không đổi rồi mới
#   kiểm tra.

# %%
# 💻 Ví dụ: phương thức đọc dữ liệu
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa

    def ap_suat_bar(self):                  # phương thức: hàm trong class, nhận self
        return self.ap_suat_kpa / 100


lop = LopXe("truoc_trai", 230)
print(lop.ap_suat_bar())    # 2.3

# %% [markdown]
# `ap_suat_bar` đọc `self.ap_suat_kpa` của chính object `lop` rồi đổi đơn vị.

# %%
# 💻 Ví dụ: Python tự truyền object vào self
print(lop.ap_suat_bar(), LopXe.ap_suat_bar(lop))    # 2.3 2.3

# %% [markdown]
# `lop.ap_suat_bar()` được Python đổi thành `LopXe.ap_suat_bar(lop)`, nên `self` chính là `lop`.

# %%
# 💻 Ví dụ: quên self ở dòng def
class LopQuenSelf:
    def ap_suat_bar():          # thiếu self
        return 2.3


# print(LopQuenSelf().ap_suat_bar())   # Bỏ dấu # để thấy lỗi TypeError

# %% [markdown]
# Python vẫn truyền object vào, nhưng phương thức không có chỗ nhận, nên báo thừa một tham số.

# %%
# 💻 Ví dụ: phương thức có tham số và giá trị mặc định
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa

    def can_bom(self, nguong_kpa=210):
        return self.ap_suat_kpa < nguong_kpa


lop = LopXe("sau_phai", 195)
print(lop.can_bom(), lop.can_bom(180))    # True False

# %% [markdown]
# Phương thức nhận tham số giống hàm thường, kể cả tham số mặc định.

# %%
# 💻 Ví dụ: phương thức đổi dữ liệu
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa

    def bom(self, kpa):
        self.ap_suat_kpa += kpa             # đổi thuộc tính của chính object


lop = LopXe("sau_phai", 195)
lop.bom(30)
print(lop.ap_suat_kpa)    # 225

# %% [markdown]
# `bom` không trả gì, nó sửa thẳng `ap_suat_kpa` của object `lop`.

# %%
# 💻 Ví dụ: phương thức có thể từ chối
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa

    def xa_hoi(self, kpa):
        if kpa > self.ap_suat_kpa:          # xả nhiều hơn đang có: từ chối
            return False
        self.ap_suat_kpa -= kpa
        return True


lop = LopXe("truoc_phai", 230)
print(lop.xa_hoi(500), lop.ap_suat_kpa)   # False 230
print(lop.xa_hoi(20), lop.ap_suat_kpa)    # True 210

# %% [markdown]
# Bị từ chối thì dữ liệu giữ nguyên và trả `False`. Nơi gọi biết ngay thao tác có thành công
# hay không.

# %%
# 💻 Ví dụ: phương thức gọi phương thức khác
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa

    def can_bom(self, nguong_kpa=210):
        return self.ap_suat_kpa < nguong_kpa

    def trang_thai(self):
        if self.can_bom():                  # gọi phương thức khác qua self
            return "CAN_BOM"
        return "OK"


print(LopXe("sau_trai", 195).trang_thai(), LopXe("sau_phai", 230).trang_thai())    # CAN_BOM OK

# %% [markdown]
# Trong class, gọi phương thức khác cũng phải qua `self.`, giống đọc thuộc tính.

# %%
# 💻 Ví dụ: kiểm tra cả bốn lốp
bon_lop = [LopXe("truoc_trai", 230), LopXe("truoc_phai", 228), LopXe("sau_trai", 195), LopXe("sau_phai", 231)]
for l in bon_lop:
    print(l.vi_tri, l.trang_thai())

# %% [markdown]
# Cùng một phương thức chạy trên từng object, mỗi object dùng dữ liệu của riêng nó.

# %% [markdown]
# ### 🎯 Bài tập 3.1 — Phương thức của MauCamBien
#
# **Đầu vào:** bộ chấm tự tạo `MauCamBien(...)` và gọi phương thức. Bạn không cần tạo object.
#
# **Bạn viết:** class `MauCamBien` viết lại trong ô dưới. Chép `__init__` của bài 2.1 vào chỗ
# đánh dấu, rồi thêm hai phương thức:
#
# - `toc_do_ms()`: đổi tốc độ sang m/s, $v' = \dfrac{v}{3.6}$, trong đó $v$ là `toc_do_kmh`, làm
#   tròn 2 chữ số.
# - `co_vat_can_gan(nguong=5.0)`: `True` khi `khoang_cach_m` khác `None` và nhỏ hơn hoặc bằng
#   `nguong`, ngược lại `False`.
#
# **Đầu ra:** giá trị hai phương thức trả về.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `MauCamBien(113.0, 36, 4.2).toc_do_ms()` | `10.0` |
# | `MauCamBien(113.0, 29, 7.36).toc_do_ms()` | `8.06` |
# | `MauCamBien(113.0, 36, 4.2).co_vat_can_gan()` | `True` |
# | `MauCamBien(113.0, 29, 7.36).co_vat_can_gan()` | `False` |
# | `MauCamBien(113.0, 29, 7.36).co_vat_can_gan(8.0)` | `True` |
# | `MauCamBien(5.0, 12, None).co_vat_can_gan()` | `False` |
#
# **Bộ chấm:** gọi 7 lần, gồm 6 trường hợp trên và khoảng cách đúng bằng ngưỡng `5.0`.

# %%
class MauCamBien:
    def __init__(self, thoi_gian_s, toc_do_kmh, khoang_cach_m):
        # TODO: chép phần thân __init__ của bài 2.1 vào đây
        pass

    def toc_do_ms(self):
        # TODO: trả về toc_do_kmh / 3.6, làm tròn 2 chữ số
        pass

    def co_vat_can_gan(self, nguong=5.0):
        # TODO: True khi khoang_cach_m khác None và <= nguong
        pass


# %%
kiem_tra_3_1(MauCamBien)

# %% [markdown]
# ### 🎯 Bài tập 3.2 — Class Pin
#
# **Đầu vào:** bộ chấm tự tạo `Pin(...)` và gọi phương thức theo thứ tự ở cột Ví dụ. Bạn không
# cần tạo object.
#
# **Bạn viết:** class `Pin` gồm:
#
# - `__init__(self, muc_pct)`: lưu mức pin (%) vào thuộc tính `muc_pct`.
# - `xa(luong)`: trừ `luong` khỏi `muc_pct`, nhưng không xuống dưới 0.
# - `sac(luong)`: cộng `luong` vào `muc_pct`, nhưng không vượt quá 100.
# - `can_sac()`: `True` khi `muc_pct` nhỏ hơn 15, ngược lại `False`.
#
# **Đầu ra:** `xa` và `sac` không cần trả gì, bộ chấm đọc thuộc tính `muc_pct` sau mỗi lần
# gọi. `can_sac` trả `True` hoặc `False`.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `p = Pin(15.8)` rồi `p.xa(1.0)` | `p.muc_pct` là `14.8` |
# | `p.can_sac()` | `True` |
# | `p.sac(90)` | `p.muc_pct` là `100` |
# | `p2 = Pin(3)` rồi `p2.xa(10)` | `p2.muc_pct` là `0` |
# | `Pin(15).can_sac()` | `False` |
#
# **Bộ chấm:** 5 kịch bản như bảng trên, thêm `Pin(50).can_sac()` và `Pin(14.9).can_sac()`.

# %%
class Pin:
    def __init__(self, muc_pct):
        # TODO
        pass

    def xa(self, luong):
        # TODO: trừ, không xuống dưới 0
        pass

    def sac(self, luong):
        # TODO: cộng, không vượt quá 100
        pass

    def can_sac(self):
        # TODO
        pass


# %%
kiem_tra_3_2(Pin)

# %% [markdown]
# ### 🎯 Bài tập 3.3 — Class Xe
#
# **Đầu vào:** bộ chấm tự tạo `Xe(...)` và gọi phương thức theo thứ tự ở cột Ví dụ. Bạn không
# cần tạo object.
#
# **Bạn viết:** class `Xe` gồm:
#
# - `__init__(self, bien_so, odo_km=0)`: lưu hai thuộc tính `bien_so`, `odo_km` (số km trên
#   đồng hồ).
# - `cap_nhat_odo(gia_tri)`: đồng hồ km không được quay lùi. `gia_tri` nhỏ hơn `odo_km` hiện tại
#   thì trả `False` và không đổi gì. Ngược lại gán `odo_km = gia_tri` và trả `True`.
# - `di_them(km)`: `km` âm thì trả `False` và không đổi gì. Ngược lại cộng vào `odo_km` và trả
#   `True`.
#
# **Đầu ra:** `True` hoặc `False` như trên, và thuộc tính `odo_km` sau mỗi lần gọi.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `Xe("30A-12345").odo_km` | `0` |
# | `xe = Xe("30A-12345", 120)` rồi `xe.cap_nhat_odo(50)` | `False`, `xe.odo_km` vẫn là `120` |
# | `xe.cap_nhat_odo(150)` | `True`, `xe.odo_km` là `150` |
# | `xe2 = Xe("30A-12345", 120)` rồi `xe2.di_them(1.3)` | `True`, `xe2.odo_km` là `121.3` |
# | `xe2.di_them(-2)` | `False`, `xe2.odo_km` vẫn là `121.3` |
#
# **Bộ chấm:** 7 kịch bản, mỗi kịch bản tạo một `Xe("30A-12345", 120)` mới rồi gọi lần lượt,
# gồm cả trường hợp `cap_nhat_odo` đúng bằng số hiện tại (vẫn nhận).

# %%
class Xe:
    def __init__(self, bien_so, odo_km=0):
        # TODO
        pass

    def cap_nhat_odo(self, gia_tri):
        # TODO: không cho quay lùi, trả True / False
        pass

    def di_them(self, km):
        # TODO: không nhận số âm, trả True / False
        pass


# %%
kiem_tra_3_3(Xe)

# %% [markdown]
# ---
# ## Bài 4 — Object đáng tin và dễ đọc
#
# Class ở Bài 3 vẫn cho tạo object với dữ liệu vô lý, và `print` một object chỉ ra một dòng
# địa chỉ bộ nhớ. Bài này sửa hai việc đó, rồi phân biệt dữ liệu dùng chung với dữ liệu riêng
# của từng object.
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `raise ValueError(...)` trong `__init__` | dữ liệu sai thì không cho tạo object | `if ap_suat_kpa < 0: raise ValueError("ap suat am")` |
# | `def __str__(self):` | trả về chuỗi dùng khi `print(obj)`, `str(obj)` hoặc đặt `obj` trong f-string | `return f"Lop {self.vi_tri}: {self.ap_suat_kpa} kPa"` |
# | thuộc tính class: gán ngay trong thân class | dùng chung cho mọi object của class, đọc bằng `TenClass.ten` | `so_lop_da_tao = 0` |
# | thuộc tính object: `self.ten = ...` trong `__init__` | riêng từng object | `self.vi_tri = vi_tri` |
# | list tạo trong `__init__` | mỗi object có list riêng | `self.nhat_ky = []` |
# | `_ten` | gạch dưới đầu tên là quy ước "chỉ dùng bên trong class, đừng sửa từ ngoài". Python không chặn | `self._so_lan_bom = 0` |
#
# #### ⚠️ Lỗi hay gặp
#
# - `__str__` phải `return` một chuỗi. Viết `print(...)` trong `__str__` thì `print(obj)` báo
#   `TypeError: __str__ returned non-string`.
# - Đặt list hoặc dict ở thân class (`nhat_ky = []`) thì mọi object dùng chung một list. List
#   riêng phải tạo trong `__init__`.
# - Gán `obj.ten_thuoc_tinh_class = ...` chỉ tạo thuộc tính riêng cho `obj`, không đổi giá trị
#   dùng chung. Đổi giá trị dùng chung thì gán qua `TenClass.ten`.

# %%
# 💻 Ví dụ: sửa thuộc tính từ ngoài
lop = LopXe("truoc_trai", 230)
lop.ap_suat_kpa = -50           # Python không chặn
print(lop.ap_suat_kpa, lop.trang_thai())    # -50 CAN_BOM

# %% [markdown]
# Áp suất âm là vô lý, nhưng object vẫn nhận và còn báo `CAN_BOM`.

# %%
# 💻 Ví dụ: raise trong __init__
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        if ap_suat_kpa < 0:
            raise ValueError("ap suat khong duoc am")
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa


try:
    LopXe("truoc_trai", -50)
except ValueError as loi:
    print("khong tao duoc:", loi)

# %% [markdown]
# Dữ liệu sai thì `__init__` dừng ở dòng `raise`, không có object nào được tạo ra.

# %%
# 💻 Ví dụ: print object khi chưa có __str__
print(LopXe("sau_phai", 220))

# %% [markdown]
# Python chỉ in tên class và địa chỉ bộ nhớ, không nói gì về chiếc lốp.

# %%
# 💻 Ví dụ: __str__
class LopXe:
    def __init__(self, vi_tri, ap_suat_kpa):
        if ap_suat_kpa < 0:
            raise ValueError("ap suat khong duoc am")
        self.vi_tri = vi_tri
        self.ap_suat_kpa = ap_suat_kpa

    def __str__(self):
        return f"Lop {self.vi_tri}: {self.ap_suat_kpa} kPa"


lop = LopXe("sau_phai", 220)
print(lop)                       # Lop sau_phai: 220 kPa
print(f"canh bao: {lop}")        # f-string cũng dùng __str__

# %% [markdown]
# `print`, `str(lop)` và f-string đều gọi `__str__`.

# %%
# 💻 Ví dụ: thuộc tính class dùng chung
class LopDem:
    so_lop_da_tao = 0                   # thuộc tính class: một giá trị cho cả class

    def __init__(self, vi_tri):
        self.vi_tri = vi_tri            # thuộc tính object: riêng từng lốp
        LopDem.so_lop_da_tao += 1


a, b, c = LopDem("truoc_trai"), LopDem("truoc_phai"), LopDem("sau_trai")
print(a.vi_tri, c.vi_tri, LopDem.so_lop_da_tao)    # truoc_trai sau_trai 3

# %% [markdown]
# `vi_tri` mỗi lốp một giá trị, `so_lop_da_tao` chỉ có một giá trị cho cả class.

# %%
# 💻 Ví dụ: hằng số dùng chung
class LopChuan:
    AP_SUAT_CHUAN_KPA = 230

    def __init__(self, ap_suat_kpa):
        self.ap_suat_kpa = ap_suat_kpa

    def thieu_bao_nhieu(self):
        return LopChuan.AP_SUAT_CHUAN_KPA - self.ap_suat_kpa


print(LopChuan(195).thieu_bao_nhieu(), LopChuan(228).thieu_bao_nhieu())    # 35 2

# %% [markdown]
# Hằng số của cả class đặt trong thân class, viết HOA theo quy ước hằng số.

# %%
# 💻 Ví dụ: list dùng chung (sai)
class XeNhatKySai:
    nhat_ky = []                        # list ở thân class: mọi xe dùng chung

    def __init__(self, bien_so):
        self.bien_so = bien_so

    def ghi(self, su_kien):
        self.nhat_ky.append(su_kien)


xe_a, xe_b = XeNhatKySai("30A-111"), XeNhatKySai("30A-222")
xe_a.ghi("phanh gap")
print(xe_b.nhat_ky)    # ['phanh gap']

# %% [markdown]
# Xe B chưa ghi gì mà nhật ký đã có `"phanh gap"` của xe A, vì cả hai cùng trỏ vào một list.

# %%
# 💻 Ví dụ: list riêng từng object (đúng)
class XeNhatKy:
    def __init__(self, bien_so):
        self.bien_so = bien_so
        self.nhat_ky = []               # tạo trong __init__: mỗi xe một list mới

    def ghi(self, su_kien):
        self.nhat_ky.append(su_kien)


xe_a, xe_b = XeNhatKy("30A-111"), XeNhatKy("30A-222")
xe_a.ghi("phanh gap")
print(xe_a.nhat_ky, xe_b.nhat_ky)    # ['phanh gap'] []

# %% [markdown]
# `__init__` chạy lại cho mỗi object, nên mỗi lần tạo xe là một list rỗng mới.

# %% [markdown]
# ### 🎯 Bài tập 4.1 — Pin kiểm tra dữ liệu và in được
#
# **Đầu vào:** bộ chấm tự tạo `Pin(...)`. Bạn không cần tạo object.
#
# **Bạn viết:** class `Pin` viết lại trong ô dưới. Chép class `Pin` của bài 3.2 vào, rồi thêm:
#
# - Trong `__init__`: `muc_pct` nhỏ hơn 0 hoặc lớn hơn 100 thì `raise ValueError`.
# - `__str__()`: trả về chuỗi `"Pin {muc_pct}%"`.
#
# **Đầu ra:** `Pin(x)` với `x` ngoài 0–100 thì gây `ValueError`. `str(pin)` trả về chuỗi như
# trên. Các phương thức của bài 3.2 vẫn đúng.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `Pin(120)` | `ValueError` |
# | `Pin(-1)` | `ValueError` |
# | `str(Pin(15.8))` | `"Pin 15.8%"` |
# | `str(Pin(100))` | `"Pin 100%"` |
#
# **Bộ chấm:** 6 kịch bản: 4 trường hợp trên, `str(Pin(0))`, và lại kịch bản `xa`, `can_sac`,
# `sac` của bài 3.2.

# %%
class Pin:
    # TODO: chép class Pin của bài 3.2 vào đây, thêm raise trong __init__ và phương thức __str__
    pass


# %%
kiem_tra_4_1(Pin)

# %% [markdown]
# ### 🎯 Bài tập 4.2 — Class NhatKyLoi
#
# **Đầu vào:** bộ chấm tự tạo **hai** object `NhatKyLoi` và gọi phương thức xen kẽ. Bạn không cần
# tạo object.
#
# **Bạn viết:** class `NhatKyLoi` gồm:
#
# - `__init__(self, ten_xe)`: lưu `ten_xe`, tạo thuộc tính `ban_ghi` là list rỗng riêng cho
#   object này.
# - `ghi(ma_loi, thoi_gian_s)`: thêm tuple `(ma_loi, thoi_gian_s)` vào cuối `ban_ghi`.
# - `so_lan(ma_loi)`: trả số phần tử trong `ban_ghi` có mã bằng `ma_loi`.
#
# **Đầu ra:** `ban_ghi` (list tuple) và giá trị `so_lan` trả về.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `a = NhatKyLoi("xe A")`, `b = NhatKyLoi("xe B")` | |
# | `a.ghi("P0113", 3.4)`, `a.ghi("P0113", 21.8)`, `b.ghi("C0035", 113.2)` | |
# | `a.so_lan("P0113")` | `2` |
# | `b.so_lan("P0113")` | `0` (không dính bản ghi của `a`) |
# | `a.ban_ghi` | `[("P0113", 3.4), ("P0113", 21.8)]` |
#
# **Bộ chấm:** 6 kịch bản, đúng như bảng trên, thêm `b.so_lan("C0035")`, `b.ban_ghi` và một
# nhật ký mới tạo.

# %%
class NhatKyLoi:
    def __init__(self, ten_xe):
        # TODO: lưu ten_xe, tạo self.ban_ghi là list rỗng
        pass

    def ghi(self, ma_loi, thoi_gian_s):
        # TODO
        pass

    def so_lan(self, ma_loi):
        # TODO
        pass


# %%
kiem_tra_4_2(NhatKyLoi)

# %% [markdown]
# ---
# ## Bài 5 — Object chứa object
#
# Một bộ bốn lốp, một chuyến xe nhiều mẫu cảm biến: object có thể giữ một list các object khác,
# và có phương thức làm việc trên cả list đó.
#
# #### 📖 Cú pháp
#
# | Cú pháp | Nghĩa | Ví dụ |
# |---|---|---|
# | `[x for x in ds if x.thuoc_tinh ...]` | lọc list object theo thuộc tính | `[l for l in cac_lop if l.can_bom()]` |
# | `self.danh_sach = []` rồi `self.danh_sach.append(obj)` | object giữ list các object khác | `self.cac_lop.append(lop)` |
# | `sorted(ds, key=ham)` | list mới xếp tăng dần theo giá trị `ham(x)` của từng phần tử. `ham` là hàm nhận một phần tử, viết tên hàm không có ngoặc tròn | `sorted(cac_lop, key=lay_ap_suat)` |
# | `max(ds, key=ham)`, `min(ds, key=ham)` | phần tử có `ham(x)` lớn nhất, nhỏ nhất. Nhiều phần tử bằng nhau thì lấy phần tử đầu tiên | `max(cac_lop, key=lay_ap_suat)` |
#
# #### ⚠️ Lỗi hay gặp
#
# - `sorted(ds, key=lay_ap_suat())` có ngoặc tròn sau tên hàm thì gọi hàm ngay, báo
#   `TypeError`. Viết `key=lay_ap_suat`.
# - `max(ds)` với list object không có `key` báo `TypeError`, vì Python không biết so hai chiếc
#   lốp bằng gì.
# - Object tạo ra trước khi định nghĩa lại class vẫn thuộc class cũ, không có phương thức mới.
#   Định nghĩa lại class thì tạo lại object.

# %%
# 💻 Ví dụ: lọc list object
cac_lop = [LopXe("truoc_trai", 230), LopXe("truoc_phai", 228), LopXe("sau_trai", 195), LopXe("sau_phai", 231)]
thap = [l for l in cac_lop if l.ap_suat_kpa < 210]
print([l.vi_tri for l in thap])    # ['sau_trai']

# %% [markdown]
# Lọc theo thuộc tính, rồi lấy ra `vi_tri` của các lốp còn lại.

# %%
# 💻 Ví dụ: object giữ list object
class BoLop:
    def __init__(self):
        self.cac_lop = []

    def them(self, lop):
        self.cac_lop.append(lop)

    def so_lop(self):
        return len(self.cac_lop)


bo = BoLop()
for l in cac_lop:
    bo.them(l)
print(bo.so_lop())    # 4

# %% [markdown]
# `bo.cac_lop` là list các object `LopXe`, `BoLop` chỉ giữ và đếm chúng.

# %%
# 💻 Ví dụ: phương thức duyệt các object bên trong
class BoLop:
    def __init__(self):
        self.cac_lop = []

    def them(self, lop):
        self.cac_lop.append(lop)

    def lop_can_bom(self):
        return [l.vi_tri for l in self.cac_lop if l.ap_suat_kpa < 210]


bo = BoLop()
for l in cac_lop:
    bo.them(l)
print(bo.lop_can_bom())    # ['sau_trai']

# %% [markdown]
# Phương thức của `BoLop` đọc thuộc tính của từng `LopXe` nó đang giữ.

# %%
# 💻 Ví dụ: sorted với key
def lay_ap_suat(lop):
    return lop.ap_suat_kpa


xep = sorted(cac_lop, key=lay_ap_suat)        # xếp theo ap_suat_kpa tăng dần
print([l.vi_tri for l in xep])    # ['sau_trai', 'truoc_phai', 'truoc_trai', 'sau_phai']

# %% [markdown]
# `sorted` gọi `lay_ap_suat` cho từng lốp để lấy con số so sánh, rồi xếp theo con số đó.

# %%
# 💻 Ví dụ: max và min với key
print(max(cac_lop, key=lay_ap_suat).vi_tri, min(cac_lop, key=lay_ap_suat).vi_tri)    # sau_phai sau_trai

# %% [markdown]
# `max` trả về cả object lốp, nên đọc tiếp được `.vi_tri`.

# %%
# 💻 Ví dụ: object giữ list dict, phương thức cộng dồn
class NhatKyPin:
    def __init__(self):
        self.ban_ghi = []       # list các dict, mỗi dict là một lần nạp hoặc xả

    def sac(self, luong, ly_do=""):
        self.ban_ghi.append({"thay_doi": luong, "ly_do": ly_do})

    def xa(self, luong, ly_do=""):
        self.ban_ghi.append({"thay_doi": -luong, "ly_do": ly_do})

    def muc_pin(self):
        tong = 0
        for bg in self.ban_ghi:
            tong += bg["thay_doi"]
        return tong


pin = NhatKyPin()
pin.sac(50, "sac qua dem")
pin.xa(20, "chay thu nghiem")
print(pin.muc_pin(), pin.ban_ghi)    # 30 [...]

# %% [markdown]
# `muc_pin` không lưu sẵn một con số, mỗi lần gọi nó cộng lại từ đầu `ban_ghi`. Dự án cuối tuần
# dùng đúng cách này.

# %% [markdown]
# ### 🎯 Bài tập 5.1 — Class ChuyenXe
#
# **Đầu vào:** bộ chấm tự tạo `ChuyenXe()` và vài mẫu có thuộc tính `toc_do_kmh`, rồi `them`
# vào. Bạn không cần tạo object.
#
# **Bạn viết:** class `ChuyenXe` gồm:
#
# - `__init__(self)`: tạo thuộc tính `danh_sach_mau` là list rỗng riêng cho chuyến này.
# - `them(mau)`: thêm `mau` vào cuối `danh_sach_mau`.
# - `so_mau()`: trả số mẫu đang có.
# - `toc_do_max()`: trả `toc_do_kmh` lớn nhất trong các mẫu. Chưa có mẫu nào thì trả `None`.
#
# **Đầu ra:** giá trị các phương thức trả về.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `ChuyenXe().so_mau()` | `0` |
# | `ChuyenXe().toc_do_max()` | `None` |
# | `cx = ChuyenXe()`, thêm 3 mẫu có `toc_do_kmh` là `0`, `65`, `42`, rồi `cx.so_mau()` | `3` |
# | `cx.toc_do_max()` | `65` |
#
# **Bộ chấm:** 4 kịch bản trên, thêm một kịch bản hai chuyến xe: thêm mẫu vào chuyến này thì
# chuyến kia vẫn 0 mẫu.

# %%
class ChuyenXe:
    def __init__(self):
        # TODO
        pass

    def them(self, mau):
        # TODO
        pass

    def so_mau(self):
        # TODO
        pass

    def toc_do_max(self):
        # TODO: None khi chưa có mẫu
        pass


# %%
kiem_tra_5_1(ChuyenXe)

# %% [markdown]
# ### 📡 Bài tập 5.2 — Phân tích chuyến xe bằng object
#
# **Đầu vào:** `doc_chuyen_xe()` (như bài 2.2) và class `MauCamBien` của bài 3.1. Biến
# `chuyen_xe` đã khởi tạo sẵn là `None` trong ô dưới.
#
# **Bạn viết:**
#
# 1. Class `ChuyenXe` viết lại: chép class của bài 5.1 vào, thêm hai phương thức:
#    - `giay_vat_can_gan()`: list `thoi_gian_s` của các mẫu có `co_vat_can_gan()` là `True`, theo
#      thứ tự.
#    - `mau_nhanh_nhat()`: trả về object mẫu có `toc_do_kmh` lớn nhất, dùng `max(..., key=...)`.
# 2. Tạo `chuyen_xe = ChuyenXe()`, rồi với mỗi giây của `doc_chuyen_xe()` tạo một
#    `MauCamBien(t, toc_do, khoang_cach)` và `them` vào. Phải tạo mẫu mới ở đây: các mẫu trong
#    `danh_sach_mau` của bài 2.2 thuộc class `MauCamBien` cũ, chưa có `co_vat_can_gan`.
#
# **Đầu ra:** biến `chuyen_xe` chứa 181 mẫu.
#
# **Ví dụ:** trên chuyến xe này, `chuyen_xe.giay_vat_can_gan()` bắt đầu bằng `[113, 114, 115, ...]`
# (vật cản xuất hiện ở giây 112.8, xe phanh gấp và đứng lại trước nó), và
# `chuyen_xe.mau_nhanh_nhat().toc_do_kmh` là `65`.
#
# **Bộ chấm:** gọi `chuyen_xe.so_mau()`, `chuyen_xe.giay_vat_can_gan()`, và đọc `thoi_gian_s`,
# `toc_do_kmh` của `chuyen_xe.mau_nhanh_nhat()`, so với đáp án tính từ dữ liệu.

# %%
chuyen_xe = None     # TODO

# ---------- Chỗ bạn viết ----------
# Khung cú pháp:
# def lay_toc_do(mau):
#     return mau.toc_do_kmh
#
# class ChuyenXe:
#     ...
#
# chuyen_xe = ChuyenXe()
# for t, khoang_cach, toc_do, pin in doc_chuyen_xe():
#     ...


# %%
kiem_tra_5_2(chuyen_xe)

# %% [markdown]
# ---
# ## Dự án tuần 3 — Budget App (Ứng dụng quản lý ngân sách)
#
# Đội xe chia ngân sách vận hành thành nhiều hạng mục (sạc điện, bảo dưỡng, phí đường...).
# Mỗi hạng mục có sổ giao dịch riêng: nạp tiền vào, rút ra chi tiêu, chuyển sang hạng mục khác.
# Dự án ghép mọi thứ của phần OOP: thiết kế class, giữ list giao dịch bên trong object (như
# `NhatKyPin`), phương thức có thể từ chối, phương thức gọi phương thức, và `__str__`.
#
# **Đầu vào:** bộ chấm tự tạo các object `HangMuc` và gọi phương thức. Bạn không cần tạo object.
#
# **Bạn viết:** class `HangMuc` (một hạng mục chi tiêu) gồm:
#
# | Phương thức | Việc phải làm |
# |---|---|
# | `__init__(self, ten)` | lưu `ten`, tạo `ledger` (sổ giao dịch) là list rỗng |
# | `nap_tien(self, so_tien, mo_ta="")` | thêm dict `{"so_tien": so_tien, "mo_ta": mo_ta}` vào `ledger` |
# | `rut_tien(self, so_tien, mo_ta="")` | đủ số dư thì thêm dict có `so_tien` âm (`-so_tien`) vào `ledger` và trả `True`. Không đủ thì trả `False`, **không đổi `ledger`** |
# | `chuyen_tien(self, hang_muc_khac, so_tien)` | gọi `self.rut_tien(...)`. Rút được thì gọi tiếp `hang_muc_khac.nap_tien(...)`. Trả về kết quả của việc rút |
# | `so_du(self)` | trả tổng `so_tien` của mọi giao dịch trong `ledger`, cộng dồn như `muc_pin` của `NhatKyPin` |
# | `__str__(self)` | trả về đúng định dạng `"{ten}: {so_du} VND"` |
#
# **Đầu ra:** giá trị các phương thức trả về, và chuỗi của `str(hang_muc)`.
#
# **Ví dụ:**
#
# | Lời gọi | Kết quả |
# |---|---|
# | `hm = HangMuc("An uong")`, `hm.nap_tien(500000)`, `hm.rut_tien(200000)`, rồi `hm.so_du()` | `300000` |
# | `hm2 = HangMuc("An uong")`, `hm2.nap_tien(100000)`, rồi `hm2.rut_tien(200000)` | `False`, `hm2.so_du()` vẫn là `100000` |
# | `a = HangMuc("Xang xe")`, `b = HangMuc("Sua chua")`, `a.nap_tien(300000)`, `a.chuyen_tien(b, 100000)` | `a.so_du()` là `200000`, `b.so_du()` là `100000` |
# | `g = HangMuc("Giai tri")`, `g.nap_tien(50000)`, rồi `str(g)` | `"Giai tri: 50000 VND"` |
#
# **Bộ chấm:** 5 kịch bản: nạp tiền, nạp rồi rút, rút vượt số dư, chuyển tiền giữa hai hạng mục,
# và chuỗi của `__str__`.
#
# `chuyen_tien` là chỗ mới nhất: một phương thức gọi phương thức của chính object mình
# (`self.rut_tien`), rồi gọi tiếp phương thức của một object `HangMuc` khác
# (`hang_muc_khac.nap_tien`).

# %%
class HangMuc:
    def __init__(self, ten):
        # TODO: lưu ten, khởi tạo ledger = []
        pass

    def nap_tien(self, so_tien, mo_ta=""):
        # TODO: thêm {"so_tien": so_tien, "mo_ta": mo_ta} vào ledger
        pass

    def rut_tien(self, so_tien, mo_ta=""):
        # TODO: nếu đủ số dư thì thêm giao dịch âm, trả True; không thì trả False
        pass

    def chuyen_tien(self, hang_muc_khac, so_tien):
        # TODO: gọi self.rut_tien(...), nếu thành công thì hang_muc_khac.nap_tien(...)
        pass

    def so_du(self):
        # TODO: cộng dồn so_tien của mọi giao dịch trong ledger
        pass

    def __str__(self):
        # TODO: trả về "{ten}: {so_du} VND"
        pass


# %%
kiem_tra_du_an(HangMuc)

# %% [markdown]
# Chạy thử `HangMuc` của bạn với ngân sách một tháng của đội xe, rồi vẽ số dư từng hạng mục.

# %%
from tests.tien_ich_du_lieu import ve_so_du_hang_muc

sac_dien = HangMuc("Sac dien")
bao_duong = HangMuc("Bao duong")
phi_duong = HangMuc("Phi duong")

sac_dien.nap_tien(3000000, "ngan sach thang")
sac_dien.rut_tien(1250000, "sac tai tram")
sac_dien.chuyen_tien(bao_duong, 500000)
bao_duong.rut_tien(320000, "thay ma phanh")
phi_duong.nap_tien(400000, "ngan sach thang")
phi_duong.rut_tien(150000, "qua tram thu phi")

ve_so_du_hang_muc([sac_dien, bao_duong, phi_duong])

# %% [markdown]
# ---
# ## Tổng kết tuần 3
#
# Chạy ô dưới để kiểm tra toàn bộ bài trong tuần.

# %%
ket_qua = [
    kiem_tra_1_1(doc_so),
    kiem_tra_1_2(phan_loai_dong),
    kiem_tra_1_3(kiem_tra_mau),
    kiem_tra_1_4(so_dong_hop_le, so_loi_theo_loai),
    kiem_tra_2_1(MauCamBien),
    kiem_tra_2_2(danh_sach_mau),
    kiem_tra_3_1(MauCamBien),
    kiem_tra_3_2(Pin),
    kiem_tra_3_3(Xe),
    kiem_tra_4_1(Pin),
    kiem_tra_4_2(NhatKyLoi),
    kiem_tra_5_1(ChuyenXe),
    kiem_tra_5_2(chuyen_xe),
    kiem_tra_du_an(HangMuc),
]

print(f"\nTONG KET TUAN 3: {sum(ket_qua)}/{len(ket_qua)} bai dat.")

# %% [markdown]
# ### Lưu bài và nộp bài
#
# Bản mở từ link là bản của repo, không lưu được bài làm. Vào
# `File > Save a copy in Drive` ngay từ đầu rồi làm trên bản trong Drive. Đóng tab khi
# chưa lưu thì bài làm trong phiên này mất.
#
# Để nộp bài:
#
# 1. Dùng repo bạn đã tạo từ template (chưa có thì tạo tại
#    https://github.com/momofdtt2k15kkk/15-weeks-of-military-training/generate, nên chọn
#    Private).
# 2. Ở bản trong Drive, vào `File > Save a copy in GitHub` (dòng này chỉ có trên bản
#    trong Drive), chọn repo của bạn, đường dẫn `week3/week_3.ipynb`, ghi commit
#    message dạng `week3: hoan thanh bai tap`.
# 3. Mở tab Actions của repo: dấu xanh là mọi bài đạt, dấu đỏ là còn bài sai.
