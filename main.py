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
    # (Hàm này không thay đổi, giữ nguyên)
    plt.figure(figsize=(10, 10))
    to_x = [pos[0] for pos in to_positions]
    to_y = [pos[1] for pos in to_positions]
    plt.scatter(to_x, to_y, c='red', marker='s', s=100, label='Terrestrial Operators (TOs)')
    user_x = [pos[0] for pos in all_users]
    user_y = [pos[1] for pos in all_users]
    plt.scatter(user_x, user_y, c='blue', marker='.', s=10, label='Users')
    sat_proj_x, sat_proj_y, _ = satellite_pos
    plt.scatter(sat_proj_x, sat_proj_y, c='green', marker='*', s=200, label=f'Satellite Projection (z={config.SAT_ALTITUDE/1000}km)')
    plt.title('Network Deployment Scenario')
    plt.xlabel('X-coordinate (meters)')
    plt.ylabel('Y-coordinate (meters)')
    plt.xlim(0, config.AREA_WIDTH)
    plt.ylim(0, config.AREA_HEIGHT)
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    if not os.path.exists('results'):
        os.makedirs('results')
    filepath = os.path.join('results', filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"Deployment visualization saved to '{filepath}'")

def run_simulation():
    """Hàm chính để chạy toàn bộ quá trình mô phỏng."""
    
    print("--- Step 1: Deploying Network ---")
    # (Phần này không thay đổi, giữ nguyên)
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
    visualize_deployment(current_satellite_pos, to_positions, all_users_list)
    
    print("--- Step 2: Channel Module Sanity Check ---")
    # (Phần này không thay đổi, giữ nguyên)
    if config.NUM_TO > 0 and all_users_by_to.get(0):
        first_to_pos = to_positions[0]
        first_user_pos = all_users_by_to[0][0]
        sat_to_user_gain = channel.get_satellite_channel_gain(current_satellite_pos, first_user_pos)
        terra_to_user_gain = channel.get_terrestrial_channel_gain(first_to_pos, first_user_pos)
        print(f"Satellite -> User Channel Gain: {channel.linear_to_db(sat_to_user_gain):.2f} dB")
        print(f"Terrestrial TO -> User Channel Gain: {channel.linear_to_db(terra_to_user_gain):.2f} dB\n")

    print("--- Step 3: Contract Theory Simulation ---")
    contract_menu = contract_solver.design_optimal_contracts()
    
    if not contract_menu:
        print("Could not generate an optimal contract menu. Exiting simulation.")
        return

    print("Principal offers an OPTIMIZED menu of contracts:")
    for type_name, contract in contract_menu.items():
        print(f"  - For '{type_name}' agents: {contract}")

    agent_types_list = list(config.AGENT_TYPES.keys())
    agent_type_probs = [config.AGENT_TYPES[t]['prob'] for t in agent_types_list]
    assigned_types = np.random.choice(agent_types_list, size=config.NUM_TO, p=agent_type_probs)
    
    total_principal_utility = 0
    total_agents_utility = 0
    
    print("\nAgents start choosing contracts...")
    for i in range(config.NUM_TO):
        my_true_type_name = assigned_types[i]
        my_true_theta = config.AGENT_TYPES[my_true_type_name]['theta']
        
        # =====================================================================
        # DEBUG BLOCK: In chi tiết quá trình ra quyết định
        # =====================================================================
        if i == 0: # Chỉ in chi tiết cho agent đầu tiên để tránh spam
            print(f"\n--- DEBUGGING AGENT {i} (True Type: {my_true_type_name}, Theta: {my_true_theta}) ---")
        
        best_contract_for_me = None
        max_utility_for_me = 0.0
        chosen_contract_name = "Not Participating"
        
        for offered_type, contract_option in contract_menu.items():
            # Tính toán lợi ích
            utility = contract_solver.get_agent_utility(contract_option, my_true_theta)
            
            if i == 0: # In chi tiết
                print(f"  - Considering contract for '{offered_type}':")
                print(f"    - Contract Details: R={contract_option.R/1e6:.4f} MHz, P={contract_option.P:.4f}")
                print(f"    - Calculated Utility: {utility:.15f}") # In với độ chính xác cao
                print(f"    - Current Max Utility: {max_utility_for_me:.15f}")
            
            # Thay đổi điều kiện so sánh, cho phép chọn hợp đồng có lợi ích bằng
            if utility >= max_utility_for_me:
                # Thêm một kiểm tra nhỏ để ưu tiên hợp đồng có lợi hơn nếu utility bằng nhau
                # (ví dụ, nếu cả hai đều là 0, nó sẽ không cập nhật trừ khi có lợi hơn)
                if abs(utility - max_utility_for_me) > 1e-9 or utility > 0:
                     max_utility_for_me = utility
                     best_contract_for_me = contract_option
                     chosen_contract_name = offered_type
                     if i == 0:
                         print("    - DECISION: This is better. Updating choice.")
                else:
                     if i == 0:
                         print("    - DECISION: Utility is not strictly greater. Sticking with current choice.")
            else:
                 if i == 0:
                    print("    - DECISION: Not better. Ignoring.")
        
        if i == 0:
            print(f"--- END DEBUGGING AGENT {i} ---")
        # =====================================================================
        # END DEBUG BLOCK
        # =====================================================================

        print(f"  - TO {i:02d} (True Type: '{my_true_type_name.ljust(15)}') chooses contract for '{chosen_contract_name.ljust(15)}'. "
              f"Utility: {max_utility_for_me:.3f}")

        if best_contract_for_me is not None:
            total_agents_utility += max_utility_for_me
            principal_utility_from_this_agent = contract_solver.get_principal_utility(best_contract_for_me, my_true_theta)
            total_principal_utility += principal_utility_from_this_agent

    print("\n--- Simulation Summary ---")
    print(f"Total Principal (Satellite) Utility: {total_principal_utility:.2f}")
    print(f"Total Agents (Terrestrial) Utility: {total_agents_utility:.2f}")
    print(f"Total System Welfare (Sum of Utilities): {total_principal_utility + total_agents_utility:.2f}")

if __name__ == '__main__':
    run_simulation()
