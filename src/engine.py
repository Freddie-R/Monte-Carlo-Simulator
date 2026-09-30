import numpy as np
from src.models import SimulationAsset

def run_simulation(
        asset: SimulationAsset
        years = 1,
        n_steps = 252,
        n_paths
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
    drift = (net_expected_return - 0.5*(net_variance ** 2)) * dt
    sd_shock = net_standard_deviation * np.sqrt(dt)

    # 5. Generate random normal shocks matrix (n_steps, n_paths)
    random_shocks = np.random.normal(0,1, size=(n_steps, ))