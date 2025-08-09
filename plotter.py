# plotter.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Thiết lập chung cho đồ thị ---
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "Times New Roman"],
    "font.size": 12
})
sns.set_theme(style="whitegrid", palette="deep", font_scale=1.2)

# --- Các hàm vẽ ---

def plot_figure_1_welfare_and_principal(df):
    """
    Vẽ Figure 1:
    - Subplot (a): Social Welfare
    - Subplot (b): Principal's Utility
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Subplot (a): Social Welfare
    sns.lineplot(data=df, x='Num TOs', y='Social Welfare', hue='Scenario', 
                 style='Scenario', markers=True, dashes=False, ax=axes[0])
    axes[0].set_title('(a) Social Welfare', fontsize=14)
    axes[0].set_xlabel('Number of Terrestrial Operators (TOs)')
    axes[0].set_ylabel('Total Social Welfare')
    axes[0].legend(title='Scheme')
    axes[0].set_ylim(bottom=0)

    # Subplot (b): Principal's Utility
    sns.lineplot(data=df, x='Num TOs', y='Principal Utility', hue='Scenario', 
                 style='Scenario', markers=True, dashes=False, ax=axes[1])
    axes[1].set_title('(b) Principal\'s Utility', fontsize=14)
    axes[1].set_xlabel('Number of Terrestrial Operators (TOs)')
    axes[1].set_ylabel('Total Principal\'s Utility')
    axes[1].axhline(0, color='black', linestyle='--', linewidth=1)
    
    # Sửa lỗi: Kiểm tra sự tồn tại của legend trước khi xóa
    if axes[1].get_legend() is not None:
        axes[1].get_legend().remove()
    
    plt.tight_layout(pad=1.5)
    filepath = os.path.join('results', 'figure_1_welfare_principal.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 1 saved to '{filepath}'")

def plot_figure_2_utility_breakdown_and_efficiency(df):
    """
    Vẽ Figure 2:
    - Subplot (a): Agents' Utility
    - Subplot (b): Efficiency Loss
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Subplot (a): Agents' Utility
    sns.lineplot(data=df, x='Num TOs', y='Agents Utility', hue='Scenario', 
                 style='Scenario', markers=True, dashes=False, ax=axes[0])
    axes[0].set_title('(a) Agents\' Utility', fontsize=14)
    axes[0].set_xlabel('Number of Terrestrial Operators (TOs)')
    axes[0].set_ylabel('Total Agents\' Utility')
    axes[0].legend(title='Scheme')
    axes[0].set_ylim(bottom=0)

    # Subplot (b): Efficiency Analysis
    centralized_welfare = df[df['Scenario'] == 'Centralized Optimal'][['Num TOs', 'Social Welfare']]
    centralized_welfare = centralized_welfare.rename(columns={'Social Welfare': 'Centralized Welfare'})
    plot_data = pd.merge(df, centralized_welfare, on='Num TOs')
    plot_data['Efficiency Loss'] = 1 - (plot_data['Social Welfare'] / plot_data['Centralized Welfare'])
    data_for_loss_plot = plot_data[plot_data['Scenario'].isin(['Proposed (Contract-based)', 'Equal Allocation'])]
    
    sns.lineplot(data=data_for_loss_plot, x='Num TOs', y='Efficiency Loss', hue='Scenario',
                 style='Scenario', markers=True, dashes=False, ax=axes[1])
    
    axes[1].set_title('(b) Efficiency Loss compared to Centralized Optimal', fontsize=14)
    axes[1].set_xlabel('Number of Terrestrial Operators (TOs)')
    axes[1].set_ylabel('Efficiency Loss Ratio')
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter('{:.0%}'.format))
    
    # =====================================================================
    # SỬA LỖI Ở ĐÂY
    # =====================================================================
    # Sửa lỗi: Kiểm tra sự tồn tại của legend trước khi xóa
    if axes[1].get_legend() is not None:
        axes[1].get_legend().remove()
        
    axes[1].set_ylim(bottom=-0.1)
    
    plt.tight_layout(pad=1.5)
    filepath = os.path.join('results', 'figure_2_agents_efficiency.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure 2 saved to '{filepath}'")

if __name__ == '__main__':
    results_file = os.path.join('results', 'simulation_results.csv')
    
    if not os.path.exists(results_file):
        print(f"Error: Results file not found at '{results_file}'")
        print("Please run main.py first to generate the results.")
    else:
        main_df = pd.read_csv(results_file)
        main_df['Scenario'] = main_df['Scenario'].replace({
            'Contract Theory': 'Proposed (Contract-based)',
            'Centralized': 'Centralized Optimal',
            'Equal Allocation': 'Equal Allocation'
        })
        
        plot_figure_1_welfare_and_principal(main_df)
        plot_figure_2_utility_breakdown_and_efficiency(main_df)
        
        print("\nAll figures have been generated successfully.")
