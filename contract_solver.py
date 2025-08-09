# contract_solver.py

import numpy as np
import config

class Contract:
    """
    Đại diện cho một hợp đồng trong menu: (R, P)
    R: Lượng tài nguyên được cấp (ví dụ: băng thông Hz)
    P: Khoản thanh toán (một đơn vị tiền tệ ảo)
    """
    def __init__(self, resource, payment):
        self.R = resource
        self.P = payment

    def __repr__(self):
        return f"Contract(R={self.R/1e6:.2f} MHz, P={self.P:.2f})"

def get_agent_utility(contract, agent_type_theta):
    """
    Tính lợi ích (utility) của một Agent (TO) khi chấp nhận một hợp đồng.
    Utility = Lợi ích từ tài nguyên - Chi phí phải trả
    
    Args:
        contract (Contract): Hợp đồng (R, P).
        agent_type_theta (float): "Type" (hiệu quả) của Agent.
    
    Returns:
        float: Giá trị lợi ích của Agent.
    """
    # Lợi ích của TO là thông lượng tăng thêm mà nó có được từ tài nguyên vệ tinh.
    # Sử dụng hàm log để thể hiện lợi ích cận biên giảm dần (diminishing returns).
    # theta * log(1 + R) là một dạng phổ biến.
    # Chúng ta chuẩn hóa R để tránh giá trị log quá lớn.
    normalized_resource = contract.R / 1e6 # Chuẩn hóa theo MHz
    
    utility = agent_type_theta * np.log(1 + normalized_resource) - contract.P
    return utility

def get_principal_utility(contract, agent_type_theta):
    """
    Tính lợi ích (utility) của Principal (SO) khi một Agent chấp nhận hợp đồng.
    Utility = Doanh thu - Chi phí hoạt động
    
    Args:
        contract (Contract): Hợp đồng (R, P) mà Agent đã chọn.
        agent_type_theta (float): "Type" của Agent đã chọn hợp đồng đó.
    
    Returns:
        float: Giá trị lợi ích của Principal.
    """
    # Doanh thu là khoản thanh toán P
    revenue = contract.P
    
    # Chi phí hoạt động của vệ tinh
    normalized_resource = contract.R / 1e6 # Chuẩn hóa theo MHz
    operational_cost = (config.SAT_COST_C1 * normalized_resource + 
                        config.SAT_COST_C2 * normalized_resource**2)
    
    utility = revenue - operational_cost
    return utility

def design_optimal_contracts_skeleton():
    """
    Bộ khung (skeleton) cho hàm thiết kế hợp đồng tối ưu.
    Hiện tại chỉ trả về một menu hợp đồng giả định để kiểm tra.
    
    Returns:
        dict: Một menu hợp đồng, key là tên type, value là đối tượng Contract.
    """
    print("WARNING: Using a placeholder contract menu. Not optimized.")
    
    # Đây là một menu hợp đồng "ngây thơ" để chúng ta kiểm tra.
    # Hợp đồng cho loại 'low': cấp ít tài nguyên, giá thấp.
    # Hợp đồng cho loại 'high': cấp nhiều tài nguyên, giá cao.
    
    # Giả sử chúng ta thiết kế bằng tay
    # Dành cho low_efficiency
    R_low = 10e6 # 10 MHz
    P_low = 0.5 * np.log(1 + R_low/1e6) * 0.8 # Trả 80% lợi ích
    
    # Dành cho high_efficiency
    R_high = 30e6 # 30 MHz
    P_high = 1.0 * np.log(1 + R_high/1e6) * 0.9 # Trả 90% lợi ích
    
    contract_menu = {
        'low_efficiency': Contract(resource=R_low, payment=P_low),
        'high_efficiency': Contract(resource=R_high, payment=P_high)
    }
    
    return contract_menu
