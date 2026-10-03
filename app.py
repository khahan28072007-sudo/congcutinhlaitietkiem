import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 CÔNG CỤ TÍNH LÃI GỬI TIẾT KIỆM_HỒ NGỌC KHẢ HÂN")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=10000000.0,
        step=100000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

hinh_thuc_lai = st.radio(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH LÃI
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    # Chuyển lãi suất năm sang dạng thập phân
    r = lai_suat / 100

    # Kỳ hạn tính theo năm
    so_nam = ky_han / 12

    # Xác định số kỳ nhận lãi
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_ky = ky_han
        lai_suat_ky = r / 12

    elif hinh_thuc_nhan_lai == "Hàng quý":
        so_ky = ky_han / 3
        lai_suat_ky = r / 4

    else:
        so_ky = 1
        lai_suat_ky = r * so_nam

    # =========================
    # LÃI ĐƠN
    # =========================
    if hinh_thuc_lai == "Lãi đơn":

        # Tổng tiền lãi
        tong_lai = tien_gui * r * so_nam

        # Lãi mỗi kỳ nhận được
        if hinh_thuc_nhan_lai == "Hàng tháng":
            lai_dinh_ky = tien_gui * r / 12

        elif hinh_thuc_nhan_lai == "Hàng quý":
            lai_dinh_ky = tien_gui * r / 4

        else:
            lai_dinh_ky = tong_lai

        tong_tien = tien_gui + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Hàng tháng
        if hinh_thuc_nhan_lai == "Hàng tháng":
            so_ky = ky_han
            lai_suat_ky = r / 12

            tong_tien = tien_gui * (1 + lai_suat_ky) ** so_ky
            tong_lai = tong_tien - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_ky

        # Hàng quý
        elif hinh_thuc_nhan_lai == "Hàng quý":
            so_ky = ky_han / 3
            lai_suat_ky = r / 4

            tong_tien = tien_gui * (1 + lai_suat_ky) ** so_ky
            tong_lai = tong_tien - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_ky

        # Cuối kỳ
        else:
            tong_tien = tien_gui * (1 + r * so_nam)
            tong_lai = tong_tien - tien_gui
            lai_dinh_ky = tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Đã tính toán xong!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            dinh_dang_tien(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        dinh_dang_tien(tong_tien)
    )

    st.divider()

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================
    st.subheader("📝 Chi tiết khoản gửi")

    st.write(f"**Số tiền gửi:** {dinh_dang_tien(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Phương pháp tính:** {hinh_thuc_lai}")

    if hinh_thuc_lai == "Lãi đơn":
        st.info(
            "Lãi đơn: tiền lãi được tính dựa trên số tiền gốc ban đầu "
            "và không cộng lãi vào vốn để tính lãi tiếp."
        )
    else:
        st.info(
            "Lãi kép: tiền lãi được cộng vào vốn, sau đó tiếp tục "
            "được sử dụng để tính lãi cho các kỳ tiếp theo."
        )

    # =========================
    # CÔNG THỨC
    # =========================
    with st.expander("📐 Xem công thức tính"):

        if hinh_thuc_lai == "Lãi đơn":
            st.latex(
                r"I = P \times r \times t"
            )
            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất năm, "
                "t là số năm gửi."
            )

        else:
            st.latex(
                r"A = P(1+r)^n"
            )
            st.write(
                "Trong đó: P là tiền gốc, r là lãi suất mỗi kỳ, "
                "n là số kỳ nhập lãi."
            )
