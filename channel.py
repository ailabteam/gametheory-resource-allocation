# channel.py

import numpy as np
import config

def db_to_linear(db_value):
    """Chuyển đổi từ dB sang dạng tuyến tính (linear)."""
    return 10**(db_value / 10)

def linear_to_db(linear_value):
    """Chuyển đổi từ linear sang dB."""
    return 10 * np.log10(linear_value)

def get_satellite_path_loss(distance_m, freq_hz):
    """
    Tính suy hao trong không gian tự do (Free Space Path Loss - FSPL).
    
    Args:
        distance_m (float): Khoảng cách (mét).
        freq_hz (float): Tần số (Hz).
        
    Returns:
        float: Suy hao đường truyền (dạng linear, không phải dB).
    """
    # FSPL (linear) = (4 * pi * d * f / c)^2
    lambda_val = config.SPEED_OF_LIGHT / freq_hz
    fspl = (4 * np.pi * distance_m / lambda_val)**2
    return fspl

def get_satellite_channel_gain(sat_pos, ground_pos):
    """
    Tính toán độ lợi kênh tổng hợp cho liên kết Vệ tinh - Mặt đất.
    Độ lợi = G_tx * G_rx / PathLoss / AdditionalLoss
    
    Args:
        sat_pos (tuple): Tọa độ 3D của vệ tinh.
        ground_pos (tuple): Tọa độ 2D của thiết bị mặt đất, giả sử z=0.
        
    Returns:
        float: Độ lợi kênh (dạng linear).
    """
    ground_pos_3d = (ground_pos[0], ground_pos[1], 0)
    distance = np.linalg.norm(np.array(sat_pos) - np.array(ground_pos_3d))
    
    # Tính suy hao đường truyền
    path_loss_linear = get_satellite_path_loss(distance, config.SAT_DOWNLINK_FREQ)
    
    # Chuyển đổi các giá trị gain từ dB sang linear
    sat_antenna_gain_linear = db_to_linear(config.SAT_ANTENNA_GAIN_DB)
    user_antenna_gain_linear = db_to_linear(config.USER_ANTENNA_GAIN_DB)
    rain_fading_linear = db_to_linear(config.RAIN_FADING_DB)
    
    # Tổng độ lợi kênh
    # Giả sử liên kết là từ vệ tinh xuống người dùng
    channel_gain = (sat_antenna_gain_linear * user_antenna_gain_linear) / (path_loss_linear * rain_fading_linear)
    
    return channel_gain

def get_terrestrial_path_loss(distance_m):
    """
    Tính suy hao đường truyền cho mạng mặt đất theo mô hình 3GPP UMi-LoS.
    
    Args:
        distance_m (float): Khoảng cách (mét).
        
    Returns:
        float: Suy hao đường truyền (dạng linear).
    """
    if distance_m < 10: # Tránh log(0)
        distance_m = 10
        
    # Công thức Path Loss (dB)
    pl_db = (config.TERRA_PATH_LOSS_A * np.log10(distance_m) + 
             config.TERRA_PATH_LOSS_B + 
             config.TERRA_PATH_LOSS_C * np.log10(config.TERRESTRIAL_FREQ / 1e9))
             
    return db_to_linear(pl_db)

def get_terrestrial_channel_gain(pos1, pos2):
    """
    Tính toán độ lợi kênh tổng hợp cho liên kết Mặt đất - Mặt đất.
    
    Args:
        pos1 (tuple): Tọa độ 2D của điểm 1.
        pos2 (tuple): Tọa độ 2D của điểm 2.
        
    Returns:
        float: Độ lợi kênh (dạng linear).
    """
    distance = np.linalg.norm(np.array(pos1) - np.array(pos2))
    
    # Tính suy hao
    path_loss_linear = get_terrestrial_path_loss(distance)
    
    # Chuyển đổi gain từ dB sang linear
    terra_antenna_gain_linear = db_to_linear(config.TERRA_ANTENNA_GAIN_DB)
    user_antenna_gain_linear = db_to_linear(config.USER_ANTENNA_GAIN_DB)
    
    # Giả sử liên kết là từ trạm mặt đất xuống người dùng
    channel_gain = (terra_antenna_gain_linear * user_antenna_gain_linear) / path_loss_linear
    
    return channel_gain
