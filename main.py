# main.py

import os
import numpy as np
import pandas as pd # Thêm pandas để quản lý kết quả
import matplotlib.pyplot as plt

# Import các module tự định nghĩa
import config
import geometry
import channel
import contract_solver
import baselines # Import module mới

def run_simulation_for_one_scenario(scenario_name, num_agents):
    """
    Hàm này chạy mô phỏng cho MỘT kịch bản (ví dụ: 'Contract Theory' hoặc 'Centralized').
    Trả về tổng lợi ích của Principal và Agents.
    """
    # Gán ngẫu nhiên type cho các agent
    agent_types_list = list(config.AGENT_TYPES.keys())
    agent_type_probs = [config.AGENT_TYPES[t]['prob'] for t in agent_types_list]
    assigned_types = np.random.choice(agent_types_list, size=num_agents, p=agent_type_probs)

    total_principal_utility = 0
    total_agents_utility = 0
    
    # Phân bổ tài nguyên dựa trên kịch bản
    if scenario_name == 'Contract Theory':
        contract_menu = contract_solver.design_optimal_contracts()
        if not contract_menu: return None, None
        
        for i in range(num_agents):
            my_true_type_name = assigned_types[i]
            my_true_theta = config.AGENT_TYPES[my_true_type_name]['theta']
            
            # Agent lựa chọn hợp đồng
            best_utility = 0.0
            chosen_contract = None
            for _, contract_option in contract_menu.items():
                utility = contract_solver.get_agent_utility(contract_option, my_true_theta)
                if utility > best_utility:
                    best_utility = utility
                    chosen_contract = contract_option
            
            if chosen_contract:
                total_agents_utility += best_utility
                total_principal_utility += contract_solver.get_principal_utility(chosen_contract, my_true_theta)

    elif scenario_name == 'Centralized':
        R_l_opt, R_h_opt = baselines.solve_centralized_optimal()
        if R_l_opt is None: return None, None
        
        # Phân bổ tài nguyên và tính lợi ích
        for i in range(num_agents):
            my_true_type_name = assigned_types[i]
            my_true_theta = config.AGENT_TYPES[my_true_type_name]['theta']
            
            R_alloc = R_l_opt if my_true_type_name == 'low_efficiency' else R_h_opt
            
            # Trong kịch bản tập trung, không có thanh toán (P=0). 
            # Lợi ích của agent chính là lợi ích từ tài nguyên.
            # Lợi ích của principal là chi phí (âm).
            temp_contract = contract_solver.Contract(resource=R_alloc * 1e6, payment=0)
            
            agent_benefit = contract_solver._calculate_utility_from_resource(my_true_theta, R_alloc)
            principal_cost = (config.SAT_COST_C1 * R_alloc + config.SAT_COST_C2 * R_alloc**2)

            total_agents_utility += agent_benefit
            total_principal_utility -= principal_cost # Chi phí là lợi ích âm

    elif scenario_name == 'Equal Allocation':
        R_alloc = baselines.solve_equal_allocation(num_agents)
        # Giả sử Principal không thu tiền trong kịch bản ngây thơ này
        # hoặc thu một mức giá cố định không đáng kể (P=0)
        
        for i in range(num_agents):
            my_true_type_name = assigned_types[i]
            my_true_theta = config.AGENT_TYPES[my_true_type_name]['theta']
            
            temp_contract = contract_solver.Contract(resource=R_alloc * 1e6, payment=0)
            agent_benefit = contract_solver.get_agent_utility(temp_contract, my_true_theta)
            
            if agent_benefit > 0: # Agent chỉ tham gia nếu có lợi
                total_agents_utility += agent_benefit
                total_principal_utility += contract_solver.get_principal_utility(temp_contract, my_true_theta)

    return total_principal_utility, total_agents_utility


def plot_results(df):
    """Vẽ đồ thị từ DataFrame kết quả."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Lấy danh sách các kịch bản đã chạy
    scenarios = df['Scenario'].unique()
    
    metrics = {
        'Principal Utility': 'Principal Utility',
        'Agents Utility': 'Agents Utility',
        'Social Welfare': 'Social Welfare'
    }
    
    for ax, (title, metric) in zip(axes, metrics.items()):
        for scenario in scenarios:
            subset = df[df['Scenario'] == scenario]
            ax.plot(subset['Num TOs'], subset[metric], marker='o', linestyle='-', label=scenario)
        ax.set_xlabel('Number of Terrestrial Operators')
        ax.set_ylabel(f'Total {title}')
        ax.set_title(f'{title} vs. Number of TOs')
        ax.legend()
        ax.set_ylim(bottom=0) # Đảm bảo trục y bắt đầu từ 0
    
    plt.tight_layout()
    filepath = os.path.join('results', 'performance_comparison.png')
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"Performance comparison plot saved to '{filepath}'")


if __name__ == '__main__':
    # --- Thiết lập Mô phỏng ---
    num_simulation_runs = 20 # Chạy 20 lần cho mỗi điểm dữ liệu để lấy trung bình
    num_tos_range = [5, 10, 15, 20, 25, 30] # Khảo sát số lượng TOs
    scenarios_to_run = ['Contract Theory', 'Centralized', 'Equal Allocation']
    
    all_results = []
    
    # --- Vòng lặp Mô phỏng chính ---
    for n_tos in num_tos_range:
        print(f"\n--- Running simulations for {n_tos} TOs ---")
        for scenario in scenarios_to_run:
            # Lưu kết quả của từng lần chạy để tính trung bình và độ lệch chuẩn
            run_principal_utils = []
            run_agents_utils = []
            
            for _ in range(num_simulation_runs):
                p_util, a_util = run_simulation_for_one_scenario(scenario, n_tos)
                if p_util is not None:
                    run_principal_utils.append(p_util)
                    run_agents_utils.append(a_util)
            
            # Tính giá trị trung bình
            avg_p_util = np.mean(run_principal_utils) if run_principal_utils else 0
            avg_a_util = np.mean(run_agents_utils) if run_agents_utils else 0
            
            # Lưu kết quả
            all_results.append({
                'Scenario': scenario,
                'Num TOs': n_tos,
                'Principal Utility': avg_p_util,
                'Agents Utility': avg_a_util,
                'Social Welfare': avg_p_util + avg_a_util
            })
            print(f"  - Scenario '{scenario}': Social Welfare = {avg_p_util + avg_a_util:.2f}")

    # --- Xử lý và Trực quan hóa Kết quả ---
    results_df = pd.DataFrame(all_results)
    print("\n--- Simulation Results (Averaged) ---")
    print(results_df)
    
    # Lưu kết quả ra file CSV
    results_df.to_csv('results/simulation_results.csv', index=False)
    print("\nResults saved to 'results/simulation_results.csv'")
    
    # Vẽ đồ thị
    plot_results(results_df)
