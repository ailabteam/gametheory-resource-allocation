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
