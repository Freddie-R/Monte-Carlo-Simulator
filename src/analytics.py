import numpy as np

def calculate_stats(price_paths: np.ndarray):
    # Takes final prices and cacluates key stats

    # Get final row
    final_prices = price_paths[-1, :]

    # Calculate stats
    mean_value = np.mean(final_prices)
    median_value = np.median(final_prices)

    # Calculate risk bounds
    p5 = np.percentile(final_prices, 5)
    p95 = np.percentile(final_prices, 95)

    return {
        "mean_value": mean_value,
        "median_value": median_value,
        "p5": p5,
        "p95": p95,
        "final_prices": final_prices
    }