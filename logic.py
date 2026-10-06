"""Calculation functions from 722_Assignment1.ipynb (Part II).

Copied from the notebook without changing the formulas, so the app gives
the same numbers. No Streamlit code here.
"""
import numpy as np
from starter import delivery_times

SEED = 1  # same fixed seed as the notebook


def cost_per_late_order(refunds, churn, margin):
    lost_future_profit = churn * margin
    Total_cost = refunds + lost_future_profit

    return Total_cost


def choose_best_promise(zone, time_block, promises, costs):
    if len(promises) == 0:
        raise ValueError("Please provide at least one promise to test.")

    late_cost = cost_per_late_order(
        costs["refund"],
        costs["churn_orders"],
        costs["margin"]
    )

    results = []

    for promise in promises:
        # simulate each promise separately: the promise changes demand
        times = delivery_times(
            zone, time_block, promise, seed=SEED
        )

        number_of_orders = len(times)
        number_of_late_orders = int(np.sum(times > promise))

        order_profit = number_of_orders * costs["margin"]
        total_late_cost = number_of_late_orders * late_cost
        net_profit = order_profit - total_late_cost

        results.append({
            "promise": promise,
            "orders": number_of_orders,
            "late_orders": number_of_late_orders,
            "net_profit": net_profit
        })

    best_result = max(
        results,
        key=lambda result: result["net_profit"]
    )

    return best_result, results
