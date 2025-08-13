# plotter_final.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# --- Thiết lập chung cho đồ thị chất lượng cao ---
DPI = 600
plt.rcParams.update({
    "text.usetex": False, # Đặt là False nếu không cài LaTeX trên máy
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8
})
sns.set_theme(style="whitegrid", palette="muted")

def plot_figure_1_social_welfare(df):
    """Vẽ Figure 1: So sánh Lợi ích Xã hội (Social Welfare)."""
    plt.figure(figsize=(5, 3.5))
    
    ax = sns.lineplot(data=df, x='Num TOs', y='Social Welfare', hue='Scenario', 
                 style='Scenario', markers=True, dashes=False, lw=2)
    
    ax.set_title('Overall System Performance', fontsize=12, weight='bold')
    ax.set_xlabel('Number of Terrestrial Operators (TOs)', weight='bold')
    ax.set_ylabel('Total Social Welfare', weight='bold')
    ax.legend(title='Scheme')
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=df['Num TOs'].min())
    
    plt.tight_layout()
    filepath = os.path.join('results', 'figure_1_social_welfare.png')
    plt.savefig(filepath, dpi=DPI)
    plt.close()
    print(f"Figure 1 saved to '{filepath}'")

def plot_figure_2_utility_breakdown(df):
    """Vẽ Figure 2: Phân rã lợi ích (Principal vs. Agents)."""
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.5), sharey=False)
    
    fig.suptitle('Utility Distribution Analysis', fontsize=12, weight='bold')

    # Subplot (a): Principal's Utility
    sns.lineplot(data=df, x='Num TOs', y='Principal Utility', hue='Scenario', 
                 style='Scenario', markers=True, dashes=False, lw=2, ax=axes[0], legend=False)
    axes[0].set_title('(a) Satellite Operator\'s Utility', fontsize=10)
    axes[0].set_xlabel('Number of TOs', weight='bold')
    axes[0].set_ylabel('Total Utility')
    axes[0].axhline(0, color='k', linestyle='--', linewidth=1, alpha=0.7)

    # Subplot (b): Agents' Utility
    sns.lineplot(data=df, x='Num TOs', y='Agents Utility', hue='Scenario', 
                 style='Scenario', markers=True, dashes=False, lw=2, ax=axes[1])
    axes[1].set_title('(b) Terrestrial Operators\' Utility', fontsize=10)
    axes[1].set_xlabel('Number of TOs', weight='bold')
    axes[1].set_ylabel('') # Xóa label trục y để tránh lặp
    axes[1].set_ylim(bottom=0)
    
    # Tạo legend chung
    handles, labels = axes[1].get_legend_handles_labels()
    axes[1].get_legend().remove()
    fig.legend(handles, labels, title='Scheme', loc='upper right', bbox_to_anchor=(0.99, 0.85))

    plt.tight_layout(rect=[0, 0, 1, 0.95]) # Điều chỉnh để không bị che bởi suptitle
    filepath = os.path.join('results', 'figure_2_utility_breakdown.png')
    plt.savefig(filepath, dpi=DPI)
    plt.close(fig)
    print(f"Figure 2 saved to '{filepath}'")

def plot_figure_3_efficiency_loss(df):
    """Vẽ Figure 3: Phân tích Tổn thất Hiệu quả (Efficiency Loss)."""
    # Chuẩn bị dữ liệu
    centralized_welfare = df[df['Scenario'] == 'Centralized Optimal'][['Num TOs', 'Social Welfare']]
    centralized_welfare = centralized_welfare.rename(columns={'Social Welfare': 'Centralized Welfare'})
    plot_data = pd.merge(df, centralized_welfare, on='Num TOs')
    plot_data['Efficiency Loss'] = 1 - (plot_data['Social Welfare'] / plot_data['Centralized Welfare'])
    data_for_loss_plot = plot_data[plot_data['Scenario'].isin(['Proposed (Contract-based)', 'Equal Allocation'])]
    
    plt.figure(figsize=(5, 3.5))
    ax = sns.lineplot(data=data_for_loss_plot, x='Num TOs', y='Efficiency Loss', hue='Scenario',
                 style='Scenario', markers=True, dashes=False, lw=2)
    
    ax.set_title('Efficiency Loss due to Sub-optimal Allocation', fontsize=12, weight='bold')
    ax.set_xlabel('Number of Terrestrial Operators (TOs)', weight='bold')
    ax.set_ylabel('Efficiency Loss Ratio', weight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0%}'.format))
    ax.legend(title='Scheme')
    ax.set_ylim(bottom=-0.1, top=0.7)
    
    plt.tight_layout()
    filepath = os.path.join('results', 'figure_3_efficiency_loss.png')
    plt.savefig(filepath, dpi=DPI)
    plt.close()
    print(f"Figure 3 saved to '{filepath}'")

def generate_latex_tables(df):
    """Tạo mã LaTeX cho 2 table."""
    print("\n--- Generating LaTeX Tables ---\n")
    
    # --- Table 1: Snapshot at N=20 ---
    snapshot_df = df[df['Num TOs'] == 20].copy()
    snapshot_df = snapshot_df[['Scenario', 'Principal Utility', 'Agents Utility', 'Social Welfare']]
    
    latex_table1 = snapshot_df.to_latex(
        index=False,
        float_format="%.2f",
        caption="Performance Snapshot at N=20 Terrestrial Operators.",
        label="tab:snapshot",
        column_format="lrrr",
        header=['Scheme', 'Principal Utility', 'Agents Utility', 'Social Welfare'],
        position='!t'
    )
    
    print("--- LaTeX Code for Table 1 ---")
    print(latex_table1)
    
    # --- Table 2: Per-Agent Social Welfare (Scalability) ---
    df['Per-Agent Welfare'] = df['Social Welfare'] / df['Num TOs']
    pivot_df = df.pivot(index='Scenario', columns='Num TOs', values='Per-Agent Welfare')
    
    latex_table2 = pivot_df.to_latex(
        float_format="%.2f",
        caption="Per-Agent Social Welfare vs. Number of TOs.",
        label="tab:scalability",
        position='!t'
    )

    print("\n--- LaTeX Code for Table 2 ---")
    print(latex_table2)


if __name__ == '__main__':
    results_file = os.path.join('results', 'simulation_results.csv')
    
    if not os.path.exists(results_file):
        print(f"Error: Results file not found at '{results_file}'")
    else:
        main_df = pd.read_csv(results_file)
        main_df['Scenario'] = main_df['Scenario'].replace({
            'Contract Theory': 'Proposed (Contract-based)',
            'Centralized': 'Centralized Optimal',
            'Equal Allocation': 'Equal Allocation'
        })
        
        # Vẽ các figure
        plot_figure_1_social_welfare(main_df)
        plot_figure_2_utility_breakdown(main_df)
        plot_figure_3_efficiency_loss(main_df)
        
        # Tạo mã LaTeX cho table
        generate_latex_tables(main_df)
        
        print("\nAll figures and table codes have been generated successfully.")
