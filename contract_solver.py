# contract_solver.py

import numpy as np
import config
from scipy.optimize import minimize

NUMERICAL_STABILITY_EPSILON = 1e-9

class Contract:
    def __init__(self, resource, payment):
        self.R = resource
        self.P = payment

    def __repr__(self):
        return f"Contract(R={self.R/1e6:.2f} MHz, P={self.P:.2f})"

def _calculate_utility_from_resource(theta, R_mhz):
    return theta * np.log(1 + R_mhz + NUMERICAL_STABILITY_EPSILON)

def get_agent_utility(contract, agent_type_theta):
    normalized_resource = contract.R / 1e6
    if normalized_resource < 0: 
        normalized_resource = 0
    utility = _calculate_utility_from_resource(agent_type_theta, normalized_resource) - contract.P
    return utility

def get_principal_utility(contract, agent_type_theta):
    revenue = contract.P
    normalized_resource = contract.R / 1e6
    if normalized_resource < 0:
        normalized_resource = 0
    operational_cost = (config.SAT_COST_C1 * normalized_resource + 
                        config.SAT_COST_C2 * normalized_resource**2)
    utility = revenue - operational_cost
    return utility

def design_optimal_contracts():
    try:
        theta_low = config.AGENT_TYPES['low_efficiency']['theta']
        prob_low = config.AGENT_TYPES['low_efficiency']['prob']
        theta_high = config.AGENT_TYPES['high_efficiency']['theta']
        prob_high = config.AGENT_TYPES['high_efficiency']['prob']
    except (KeyError, AttributeError):
        print("ERROR: AGENT_TYPES not defined correctly in config.py")
        return None

    def objective_function(x):
        R_l, P_l, R_h, P_h = x
        cost_l = config.SAT_COST_C1 * R_l + config.SAT_COST_C2 * R_l**2
        util_l = P_l - cost_l
        cost_h = config.SAT_COST_C1 * R_h + config.SAT_COST_C2 * R_h**2
        util_h = P_h - cost_h
        expected_utility = prob_low * util_l + prob_high * util_h
        return -expected_utility

    def constraint_ir_low(x):
        return _calculate_utility_from_resource(theta_low, x[0]) - x[1]

    def constraint_ir_high(x):
        return _calculate_utility_from_resource(theta_high, x[2]) - x[3]

    def constraint_ic_low(x):
        u_l_l = _calculate_utility_from_resource(theta_low, x[0]) - x[1]
        u_l_h = _calculate_utility_from_resource(theta_low, x[2]) - x[3]
        return u_l_l - u_l_h

    def constraint_ic_high(x):
        u_h_h = _calculate_utility_from_resource(theta_high, x[2]) - x[3]
        u_h_l = _calculate_utility_from_resource(theta_high, x[0]) - x[1]
        # =====================================================================
        # SỬA LỖI QUAN TRỌNG: Siết chặt ràng buộc IC-high
        # Yêu cầu U_h(h) phải lớn hơn U_h(l) một chút.
        # =====================================================================
        return (u_h_h - u_h_l) - 1e-6 # Thêm một khoảng đệm an toàn

    constraints = [
        {'type': 'ineq', 'fun': constraint_ir_low},
        {'type': 'ineq', 'fun': constraint_ir_high},
        {'type': 'ineq', 'fun': constraint_ic_low},
        {'type': 'ineq', 'fun': constraint_ic_high}
    ]
    
    bounds = [(0, None), (None, None), (0, None), (None, None)]
    initial_guess = [5.0, 1.0, 10.0, 2.0]
    options = {'maxiter': 1000, 'ftol': 1e-9}
    
    result = minimize(objective_function, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints, options=options)
    
    if result.success:
        R_l_opt_mhz, P_l_opt, R_h_opt_mhz, P_h_opt = result.x
        R_l_opt_mhz = max(0, R_l_opt_mhz)
        R_h_opt_mhz = max(0, R_h_opt_mhz)

        optimal_menu = {
            'low_efficiency': Contract(resource=R_l_opt_mhz * 1e6, payment=P_l_opt),
            'high_efficiency': Contract(resource=R_h_opt_mhz * 1e6, payment=P_h_opt)
        }
        return optimal_menu
    else:
        print(f"ERROR: Optimization failed! {result.message}")
        print(f"Final solution attempted: {result.x}")
        return None

def design_optimal_contracts_skeleton():
    pass
