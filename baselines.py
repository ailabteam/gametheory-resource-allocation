# baselines.py

import numpy as np
import config
from scipy.optimize import minimize

def solve_centralized_optimal():
    """
    Baseline 1: Tối ưu Tập trung (Social Planner).
    Giả định: Có một bộ điều khiển toàn tri, biết hết type của các agent.
    Mục tiêu: Tối đa hóa TỔNG LỢI ÍCH XÃ HỘI (System Welfare), 
             tức là (Lợi ích từ tài nguyên của Agent) - (Chi phí của Principal).
    """
    try:
        theta_low = config.AGENT_TYPES['low_efficiency']['theta']
        prob_low = config.AGENT_TYPES['low_efficiency']['prob']
        theta_high = config.AGENT_TYPES['high_efficiency']['theta']
        prob_high = config.AGENT_TYPES['high_efficiency']['prob']
    except (KeyError, AttributeError):
        print("ERROR: AGENT_TYPES not defined correctly in config.py")
        return None, None

    def objective_function(R):
        """
        Hàm mục tiêu: - Tổng lợi ích xã hội kỳ vọng.
        R = [R_l, R_h] (R tính theo MHz)
        """
        R_l, R_h = R

        # Lợi ích xã hội từ agent loại low
        agent_benefit_l = theta_low * np.log(1 + R_l)
        principal_cost_l = config.SAT_COST_C1 * R_l + config.SAT_COST_C2 * R_l**2
        welfare_l = agent_benefit_l - principal_cost_l

        # Lợi ích xã hội từ agent loại high
        agent_benefit_h = theta_high * np.log(1 + R_h)
        principal_cost_h = config.SAT_COST_C1 * R_h + config.SAT_COST_C2 * R_h**2
        welfare_h = agent_benefit_h - principal_cost_h
        
        expected_welfare = prob_low * welfare_l + prob_high * welfare_h
        return -expected_welfare

    # Ràng buộc: R >= 0
    bounds = [(0, None), (0, None)]
    initial_guess = [5.0, 10.0]
    options = {'maxiter': 1000, 'ftol': 1e-9}
    
    result = minimize(objective_function, initial_guess, method='SLSQP', bounds=bounds, options=options)
    
    if result.success:
        R_l_opt_mhz, R_h_opt_mhz = result.x
        # Trả về lượng tài nguyên tối ưu cho mỗi type
        return max(0, R_l_opt_mhz), max(0, R_h_opt_mhz)
    else:
        print(f"ERROR: Centralized optimization failed! {result.message}")
        return None, None

def solve_equal_allocation(num_agents):
    """
    Baseline 2: Phân bổ Đồng đều (Equal Allocation).
    Chia đều tổng tài nguyên cho tất cả các agent.
    """
    # Lấy tổng tài nguyên từ config (giả sử là băng thông)
    # Chuyển về MHz để nhất quán
    total_resource_mhz = config.TOTAL_SAT_RESOURCE_B_HZ / 1e6
    
    if num_agents == 0:
        return 0
        
    resource_per_agent_mhz = total_resource_mhz / num_agents
    return resource_per_agent_mhz
