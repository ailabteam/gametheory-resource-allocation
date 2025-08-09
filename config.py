# config.py

# --- Tham số Mô phỏng ---
AREA_WIDTH = 20000  # Chiều rộng khu vực mô phỏng (mét), 20km
AREA_HEIGHT = 20000 # Chiều cao khu vực mô phỏng (mét), 20km
NUM_TO = 10         # Số lượng Nhà mạng Mặt đất (Terrestrial Operators)
USERS_PER_TO = 15   # Số lượng người dùng trung bình cho mỗi TO
TO_CELL_RADIUS = 1000 # Bán kính phủ sóng của một TO (mét)

# --- Tham số Vệ tinh ---
SAT_ALTITUDE = 600000 # Độ cao quỹ đạo vệ tinh LEO (mét), 600km
SAT_VELOCITY = 7500   # Vận tốc vệ tinh (m/s)

# --- Tham số Vật lý ---
SPEED_OF_LIGHT = 3e8 # Tốc độ ánh sáng (m/s)

# --- Tham số Kênh truyền & Tần số ---
# Sử dụng băng tần Ka cho vệ tinh (ví dụ)
SAT_UPLINK_FREQ = 27e9   # 27 GHz
SAT_DOWNLINK_FREQ = 17e9 # 17 GHz

# Sử dụng băng tần Sub-6GHz cho mạng mặt đất (ví dụ)
TERRESTRIAL_FREQ = 3.5e9 # 3.5 GHz

# Công suất phát
SAT_TRANS_POWER_W = 20    # Công suất phát của chùm vệ tinh (Watt) - 43 dBm
TERRA_TRANS_POWER_W = 5     # Công suất phát của trạm mặt đất (Watt) - 37 dBm
USER_TRANS_POWER_W = 0.2  # Công suất phát của người dùng (Watt) - 23 dBm

# Độ lợi Antenna
SAT_ANTENNA_GAIN_DB = 50  # dBi (cho chùm hẹp)
TERRA_ANTENNA_GAIN_DB = 15 # dBi
USER_ANTENNA_GAIN_DB = 3   # dBi

# Công suất tạp âm
NOISE_POWER_W = 1e-12 # -90 dBm, ví dụ

# --- Tham số Mô hình Kênh truyền ---
# Mô hình suy hao cho liên kết mặt đất (Terrestrial)
# PL(d) = A * log10(d) + B + C * log10(fc/5) + X
# Tham số cho mô hình 3GPP UMi (Urban Micro) - Line of Sight
TERRA_PATH_LOSS_A = 22.0
TERRA_PATH_LOSS_B = 28.0
TERRA_PATH_LOSS_C = 20.0

# Suy hao do mưa cho liên kết vệ tinh (sử dụng mô hình đơn giản)
RAIN_FADING_DB = 5 # dB, một giá trị suy hao trung bình, sẽ nâng cấp sau

# --- Tham số Bài toán Hợp đồng & Game Theory ---
# Tổng tài nguyên mà Vệ tinh có thể phân bổ (ví dụ: băng thông)
# Giả sử là 100 MHz
TOTAL_SAT_RESOURCE_B_HZ = 100e6

# Định nghĩa các "Type" của TOs. Type ở đây đại diện cho hiệu quả chuyển đổi
# tài nguyên thành thông lượng của một TO. TO "tốt" có thể tạo ra nhiều 
# throughput hơn từ cùng một lượng băng thông.
# (theta, probability)
AGENT_TYPES = {
    'low_efficiency': {
        'theta': 0.5,  # Có thể tạo ra 0.5 bps/Hz cho mỗi đơn vị tài nguyên chuẩn hóa
        'prob': 0.5    # 50% TOs là loại này
    },
    'high_efficiency': {
        'theta': 1.0,  # Có thể tạo ra 1.0 bps/Hz cho mỗi đơn vị tài nguyên chuẩn hóa
        'prob': 0.5    # 50% TOs là loại này
    }
}

# Chi phí hoạt động của Vệ tinh khi phân bổ tài nguyên
# Ví dụ: chi phí năng lượng. Giả sử nó là một hàm bậc hai của tài nguyên được cấp phát.
# cost = c1 * R + c2 * R^2
SAT_COST_C1 = 0.01
SAT_COST_C2 = 0.005
