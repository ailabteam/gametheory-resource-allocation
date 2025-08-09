# main.py

import os
import numpy as np
import matplotlib.pyplot as plt

# Import các module tự định nghĩa
import config
import geometry
import channel
import contract_solver

def visualize_deployment(satellite_pos, to_positions, all_users, filename="deployment.png"):
    """
    Vẽ sơ đồ phân bố mạng và lưu thành file ảnh.
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
    
    # Tạo thư mục results nếu chưa có
    if not os.path.exists('results'):
        os.makedirs('results')
        
    # Lưu hình ảnh
    filepath = os.path.join('results', filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
    
    print(f"Deployment visualization saved to '{filepath}'")


def run_simulation():
    """Hàm chính để chạy toàn bộ quá trình mô phỏng."""
    
    # =================================================================
    # Bước 1: Tạo kịch bản mạng
    # =================================================================
    print("--- Step 1: Deploying Network ---")
    current_satellite_pos = geometry.get_satellite_position(time_t=1)
    to_positions = geometry.deploy_terrestrial_operators(config.NUM_TO)
    
    all_users_by_to = {}
    all_users_list = []
    
    for i, to_pos in enumerate(to_positions):
        num_users_this_to = np.random.poisson(config.USERS_PER_TO)
        users = geometry.deploy_users_around_to(to_pos, num_users_this_to, config.TO_CELL_RADIUS)
        all_users_by_to[i] = users
        all_users_list.extend(users)
        
    print(f"Deployed {len(to_positions)} TOs and {len(all_users_list)} users.")
    print(f"Satellite position at t=1s: {current_satellite_pos}\n")
    
    # =================================================================
    # Bước 2: Trực quan hóa (tùy chọn)
    # =================================================================
    visualize_deployment(current_satellite_pos, to_positions, all_users_list)
    
    # =================================================================
    # Bước 3: Kiểm tra Module Kênh truyền (để xác thực)
    # =================================================================
    print("--- Step 2: Channel Module Sanity Check ---")
    if config.NUM_TO > 0 and all_users_by_to.get(0):
        first_to_pos = to_positions[0]
        first_user_pos = all_users_by_to[0][0]
        
        sat_to_user_gain = channel.get_satellite_channel_gain(current_satellite_pos, first_user_pos)
        terra_to_user_gain = channel.get_terrestrial_channel_gain(first_to_pos, first_user_pos)
        
        print(f"Satellite -> User Channel Gain: {channel.linear_to_db(sat_to_user_gain):.2f} dB")
        print(f"Terrestrial TO -> User Channel Gain: {channel.linear_to_db(terra_to_user_gain):.2f} dB\n")

    # =================================================================
    # Bước 4: Mô phỏng Lý thuyết Hợp đồng
    # =================================================================
    print("--- Step 3: Contract Theory Simulation ---")
    
    # 1. Principal (SO) thiết kế và công bố menu hợp đồng
    # Hiện tại chúng ta đang dùng một menu giả định từ bộ khung
    contract_menu = contract_solver.design_optimal_contracts_skeleton()
    print("Principal offers a menu of contracts:")
    for type_name, contract in contract_menu.items():
        print(f"  - For '{type_name}' agents: {contract}")

    # 2. Các Agents (TOs) được gán "type" một cách ngẫu nhiên
    agent_types_list = list(config.AGENT_TYPES.keys())
    agent_type_probs = [config.AGENT_TYPES[t]['prob'] for t in agent_types_list]
    assigned_types = np.random.choice(agent_types_list, size=config.NUM_TO, p=agent_type_probs)
    
    total_principal_utility = 0
    total_agents_utility = 0
    
    print("\nAgents start choosing contracts...")
    # 3. Mỗi Agent lựa chọn hợp đồng tối ưu cho mình
    for i in range(config.NUM_TO):
        to_id = i
        my_true_type_name = assigned_types[i]
        my_true_theta = config.AGENT_TYPES[my_true_type_name]['theta']
        
        best_contract_for_me = None
        max_utility_for_me = -np.inf
        chosen_contract_name = "None"
        
        # Duyệt qua tất cả các hợp đồng trong menu để tìm ra cái tốt nhất
        for offered_type, contract_option in contract_menu.items():
            utility = contract_solver.get_agent_utility(contract_option, my_true_theta)
            
            if utility > max_utility_for_me:
                max_utility_for_me = utility
                best_contract_for_me = contract_option
                chosen_contract_name = offered_type
        
        # Kiểm tra điều kiện Tham gia Cá nhân (Individual Rationality - IR)
        if max_utility_for_me >= 0:
            print(f"  - TO {to_id:02d} (True Type: '{my_true_type_name}') chooses contract for '{chosen_contract_name}'. "
                  f"Utility: {max_utility_for_me:.2f}")
            
            total_agents_utility += max_utility_for_me
            
            principal_utility_from_this_agent = contract_solver.get_principal_utility(best_contract_for_me, my_true_theta)
            total_principal_utility += principal_utility_from_this_agent
        else:
            print(f"  - TO {to_id:02d} (True Type: '{my_true_type_name}') chooses to NOT participate.")

    # 4. In kết quả tổng hợp
    print("\n--- Simulation Summary ---")
    print(f"Total Principal (Satellite) Utility: {total_principal_utility:.2f}")
    print(f"Total Agents (Terrestrial) Utility: {total_agents_utility:.2f}")
    print(f"Total System Welfare (Sum of Utilities): {total_principal_utility + total_agents_utility:.2f}")


if __name__ == '__main__':
    run_simulation()
