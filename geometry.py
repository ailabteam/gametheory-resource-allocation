# geometry.py

import numpy as np
import config

def deploy_terrestrial_operators(num_operators):
    """
    Phân bố ngẫu nhiên các trạm mặt đất (TOs/gNBs) trong khu vực mô phỏng.
    Mỗi TO được biểu diễn bằng tọa độ (x, y).
    
    Args:
        num_operators (int): Số lượng TO cần phân bố.
        
    Returns:
        list: Danh sách các tuple tọa độ (x, y) của các TO.
    """
    to_positions_x = np.random.uniform(0, config.AREA_WIDTH, num_operators)
    to_positions_y = np.random.uniform(0, config.AREA_HEIGHT, num_operators)
    return list(zip(to_positions_x, to_positions_y))

def deploy_users_around_to(to_position, num_users, cell_radius):
    """
    Phân bố ngẫu nhiên người dùng trong một cell (hình tròn) xung quanh một TO.
    
    Args:
        to_position (tuple): Tọa độ (x, y) của TO.
        num_users (int): Số lượng người dùng cần phân bố.
        cell_radius (float): Bán kính của cell.
        
    Returns:
        list: Danh sách các tuple tọa độ (x, y) của người dùng.
    """
    to_x, to_y = to_position
    # Kỹ thuật phân bố điểm ngẫu nhiên đều trong hình tròn
    radius = cell_radius * np.sqrt(np.random.uniform(0, 1, num_users))
    angle = 2 * np.pi * np.random.uniform(0, 1, num_users)
    
    user_x = to_x + radius * np.cos(angle)
    user_y = to_y + radius * np.sin(angle)
    
    return list(zip(user_x, user_y))

def get_satellite_position(time_t):
    """
    Tính toán vị trí của vệ tinh tại một thời điểm t.
    Giả định vệ tinh bay thẳng theo trục x ở độ cao không đổi.
    
    Args:
        time_t (float): Thời điểm (giây).
        
    Returns:
        tuple: Tọa độ 3D (x, y, z) của vệ tinh.
    """
    # Vệ tinh bay ngang qua giữa khu vực mô phỏng
    x_pos = (config.SAT_VELOCITY * time_t) % config.AREA_WIDTH
    y_pos = config.AREA_HEIGHT / 2
    z_pos = config.SAT_ALTITUDE
    return (x_pos, y_pos, z_pos)

def calculate_distance(pos1, pos2):
    """
    Tính khoảng cách Euclidean giữa hai điểm (có thể là 2D hoặc 3D).
    
    Args:
        pos1 (tuple): Tọa độ điểm 1.
        pos2 (tuple): Tọa độ điểm 2.
        
    Returns:
        float: Khoảng cách giữa hai điểm.
    """
    p1 = np.array(pos1)
    p2 = np.array(pos2)
    return np.linalg.norm(p1 - p2)
