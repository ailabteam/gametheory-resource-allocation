# main.py

import matplotlib.pyplot as plt
import config
import geometry
import os # Thêm thư viện os để làm việc với thư mục
import numpy as np

def visualize_deployment(satellite_pos, to_positions, all_users, filename="deployment.png"):
    """
    Vẽ sơ đồ phân bố mạng và lưu thành file ảnh.
    
    Args:
        satellite_pos (tuple): Tọa độ vệ tinh.
        to_positions (list): Danh sách tọa độ các TO.
        all_users (list): Danh sách tọa độ tất cả người dùng.
        filename (str): Tên file để lưu hình ảnh.
    """
    plt.figure(figsize=(10, 10))
    
    # Vẽ các trạm mặt đất (TOs)
    to_x = [pos[0] for pos in to_positions]
    to_y = [pos[1] for pos in to_positions]
    plt.scatter(to_x, to_y, c='red', marker='s', s=100, label='Terrestrial Operators (TOs)')
    
    # Vẽ người dùng
    user_x = [pos[0] for pos in all_users]
    user_y = [pos[1] for pos in all_users]
    plt.scatter(user_x, user_y, c='blue', marker='.', s=10, label='Users')
    
    # Vẽ hình chiếu của vệ tinh
    sat_proj_x, sat_proj_y, _ = satellite_pos
    plt.scatter(sat_proj_x, sat_proj_y, c='green', marker='*', s=200, label=f'Satellite Projection (z={config.SAT_ALTITUDE/1000}km)')
    
    # Thiết lập đồ thị
    plt.title('Network Deployment Scenario')
    plt.xlabel('X-coordinate (meters)')
    plt.ylabel('Y-coordinate (meters)')
    plt.xlim(0, config.AREA_WIDTH)
    plt.ylim(0, config.AREA_HEIGHT)
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # --- THAY ĐỔI QUAN TRỌNG ---
    # Tạo thư mục results nếu chưa có
    if not os.path.exists('results'):
        os.makedirs('results')
        
    # Lưu hình ảnh
    filepath = os.path.join('results', filename)
    plt.savefig(filepath, dpi=300) # dpi=300 cho chất lượng cao
    plt.close() # Đóng figure để giải phóng bộ nhớ
    
    print(f"Deployment visualization saved to '{filepath}'")


if __name__ == '__main__':
    # --- Bước 1: Tạo kịch bản mạng ---
    
    # Lấy vị trí vệ tinh tại thời điểm t=1 giây
    current_satellite_pos = geometry.get_satellite_position(time_t=1)
    
    # Phân bố các TOs
    to_positions = geometry.deploy_terrestrial_operators(config.NUM_TO)
    
    # Phân bố người dùng cho mỗi TO
    all_users = []
    for to_pos in to_positions:
        # Giả định số người dùng của mỗi TO là ngẫu nhiên xung quanh giá trị trung bình
        num_users_this_to = np.random.poisson(config.USERS_PER_TO)
        users = geometry.deploy_users_around_to(to_pos, num_users_this_to, config.TO_CELL_RADIUS)
        all_users.extend(users)
        
    # --- Bước 2: Trực quan hóa ---
    print(f"Deployed {len(to_positions)} TOs.")
    print(f"Deployed {len(all_users)} users.")
    print(f"Satellite position at t=1s: {current_satellite_pos}")
    
    visualize_deployment(current_satellite_pos, to_positions, all_users)
