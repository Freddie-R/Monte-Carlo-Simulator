import numpy as np
from src.models import SimulationAsset

def run_simulation(
        asset: SimulationAsset,
        years = 1,
        n_steps = 252,
        n_paths = 1000
        ):
    # runs a monte carlo simulation
    
    # check if the asset has varibles
    if not asset.variables:
        raise ValueError("The asset has no varibles")

    # 1. Sum expected returns
    net_expected_return = sum(var.expected_return for var in asset.variables)

    # 2. Sum standard deviations (variences sum for independent varibles)
    net_variance = sum(var.standard_deviation ** 2 for var in asset.variables)
    net_standard_deviation = np.sqrt(net_variance)

    # 3. Calulate time steps
    dt = years / n_steps

    # 4. Geometric brownian motion with correction
    #drift = (net_expected_return - 0.5*(net_variance ** 2)) * dt
    drift = (net_expected_return) * dt
    sd_shock = net_standard_deviation * np.sqrt(dt)

    # 5. Generate random normal shocks matrix (n_steps, n_paths)
    random_shocks = np.random.normal(0,1, size=(n_steps, n_paths))

    # 6. Calulate dailiy growth factors for all paths
    step_returns = np.exp(drift + sd_shock*random_shocks)

    # 7. Contrusct the full price matrix using cumaltive product
    initial_row = np.ones((1, n_paths)) * asset.initial_value
    price_paths = np.vstack([initial_row, asset.initial_value * np.cumprod(step_returns, axis=0)])

    return price_paths

