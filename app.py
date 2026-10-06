import pandas as pd
import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE

from logic import SEED, cost_per_late_order, choose_best_promise

STEP = 5  # promises are tested in five-minute steps


def money(amount):
    """Format dollars with the sign before the $, e.g. −$127.40."""
    sign = "−" if round(amount, 2) < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


@st.cache_data
def run_choose_best_promise(zone, time_block, promises, refund, churn, margin):
    """Cached wrapper so repeated clicks with the same inputs are instant."""
    costs = {"refund": refund, "churn_orders": churn, "margin": margin}
    return choose_best_promise(zone, time_block, list(promises), costs)


st.set_page_config(page_title="Rosa's Delivery Promise", page_icon="🍕")
st.title("🍕 Rosa's Pizza: Best Delivery Promise")
st.write(
    "Pick a zone and time block, the range of promises to test and the cost figures. "
    "The app simulates four weeks of orders for each promise and recommends the one "
    "with the highest net profit (order profit minus the cost of late orders)."
)

st.sidebar.header("1. Where and when")
zone = st.sidebar.selectbox("Zone", ZONES, index=ZONES.index("Far West"))
time_block = st.sidebar.selectbox(
    "Time block", TIME_BLOCKS, index=TIME_BLOCKS.index("Fri/Sat eve")
)

st.sidebar.header("2. Promises to test (minutes)")
min_p = st.sidebar.number_input("Minimum promise", min_value=5, max_value=240, value=20, step=STEP)
max_p = st.sidebar.number_input("Maximum promise", min_value=5, max_value=240, value=90, step=STEP)
st.sidebar.caption(f"Promises are tested every {STEP} minutes.")

st.sidebar.header("3. Costs")
margin = st.sidebar.number_input(
    "Profit margin per order ($)", min_value=0.0, value=float(COSTS["margin"]), step=0.5
)
churn = st.sidebar.number_input(
    "Future orders lost per late order", min_value=0.0, value=float(COSTS["churn_orders"]), step=0.1
)
refund = st.sidebar.number_input(
    "Refund cost per late order ($)", min_value=0.0, value=float(COSTS["refund"]), step=0.5
)
st.sidebar.caption(
    f"Total cost per late order: **${cost_per_late_order(refund, churn, margin):,.2f}**"
)

if st.button("Find Best Promise", type="primary"):
    if min_p >= max_p:
        st.error("The minimum promise must be smaller than the maximum promise.")
        st.stop()
    if (max_p - min_p) < STEP:
        st.error(f"The range must cover at least one {STEP}-minute step.")
        st.stop()

    promises = tuple(range(int(min_p), int(max_p) + 1, STEP))

    with st.spinner("Simulating four weeks of orders for each promise..."):
        best_result, results = run_choose_best_promise(
            zone, time_block, promises, refund, churn, margin
        )

    st.subheader(f"Recommendation for {zone}, {time_block}")
    col1, col2 = st.columns(2)
    col1.metric("Recommended promise", f"{best_result['promise']} min")
    col2.metric("Net profit over four weeks", f"${best_result['net_profit']:,.2f}")

    current = next((r for r in results if r["promise"] == PROMISE), None)
    if current is not None:
        gain = round(best_result["net_profit"] - current["net_profit"], 2)
        if gain > 0:
            change = f"increases net profit by {money(gain)}"
        elif gain < 0:
            change = f"decreases net profit by {money(-gain)}"
        else:
            change = "does not change net profit"
        # st.text shows plain text, so "$" is not read as math markup
        st.text(
            f"Today's {PROMISE}-minute promise earns {money(current['net_profit'])}, "
            f"so the recommendation {change}."
        )

    if best_result["promise"] in (promises[0], promises[-1]):
        st.warning(
            f"The best promise ({best_result['promise']} min) is at the edge of the range "
            "you tested. The true best may lie outside it, so try widening the range."
        )

    table = pd.DataFrame(results)
    table["late_pct"] = table["late_orders"] / table["orders"] * 100
    table = table.rename(columns={
        "promise": "Promise (min)",
        "orders": "Orders",
        "late_orders": "Late orders",
        "late_pct": "Late %",
        "net_profit": "Net profit ($)",
    })[["Promise (min)", "Orders", "Late orders", "Late %", "Net profit ($)"]]

    st.write("**Net profit by promise**")
    st.line_chart(table, x="Promise (min)", y="Net profit ($)")

    st.write("**Comparison of promises**")
    st.dataframe(
        table.style.format({"Net profit ($)": "${:,.2f}", "Late %": "{:.1f}%"})
        .highlight_max(subset=["Net profit ($)"], color="#d4edda"),
        hide_index=True,
        width="stretch",
    )
    st.caption(f"Simulation uses a fixed seed ({SEED}), so results match the notebook.")
else:
    st.info("Set the inputs in the sidebar, then click **Find Best Promise**.")
