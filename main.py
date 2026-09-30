from src.models import SimulationAsset, AssetVariable
from src.engine import run_simulation
from src.analytics import calculate_stats

# 1. Setup and run simulation
house = SimulationAsset(name="House", initial_value=300000.0)
house.add_varibes(AssetVariable("Rental Income", 0.10, 0.03))
house.add_varibes(AssetVariable("Maintenance", -0.02, 0.01))

paths = run_simulation(house, years=1.0, n_steps=252, n_paths=1000)

# 2. Get analytics
stats = calculate_stats(paths)

print(f"Mean Value: £{stats['mean_value']:,.2f}")
print(f"Median Value (50th %): £{stats['median_value']:,.2f}")
print(f"5th Percentile (Risk):  £{stats['p5']:,.2f}")
print(f"95th Percentile (Gain): £{stats['p95']:,.2f}")