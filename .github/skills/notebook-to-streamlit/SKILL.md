---
name: notebook-to-streamlit
description: Turn the Part II logic in 722_Assignment1.ipynb (Rosa's Pizza delivery promise) into a Streamlit app, with calculation functions in logic.py and the interface in app.py. Use when building or updating the Streamlit app from the notebook.
---

# Notebook to Streamlit

Move the decision logic from `722_Assignment1.ipynb` into a Streamlit app **without changing what it computes**. The notebook is the source of truth; the app is only an interface around it. For the same inputs, the app must give exactly the same numbers as the notebook.

## 1. Read the notebook first

Read `722_Assignment1.ipynb` and find the two functions the app reuses:

- `cost_per_late_order(refunds, churn, margin)` (Part II(a)): returns `refunds + churn * margin`.
- `choose_best_promise(zone, time_block, promises, costs)` (Part II(b)): for each promise, calls `delivery_times(zone, time_block, promise, seed=1)`, counts orders and late orders (`times > promise`), computes `net_profit = orders * margin - late_orders * cost_per_late_order(...)`, and returns `(best_result, results)`, where each result is a dict with keys `promise`, `orders`, `late_orders`, `net_profit`. Raises `ValueError` when `promises` is empty.

Note their exact names, parameters, return values and the constants they use.

## 2. Import the starter package; never recreate the simulator

- Import from the instructor's package exactly as the notebook does:
  `from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times`
- Do **not** write your own `delivery_times`, random delivery model, or copies of `ZONES`, `TIME_BLOCKS`, `COSTS` or `PROMISE`.
- `requirements.txt` must include the starter line `git+https://github.com/zhouy185/rosa-starter.git` (plus `streamlit`, `numpy`, `pandas`).
- Drop notebook-only code: `!pip install` lines, `print` tables, test and exploration cells.

## 3. `logic.py`: calculation functions only

- Contains the starter import, `numpy`, `cost_per_late_order` and `choose_best_promise`, copied with the **same names, parameters, formulas and return format** as the notebook.
- **Keep `seed=1`.** Every `delivery_times` call uses `seed=1`, as in the notebook. A module constant `SEED = 1` is fine if its value stays 1.
- **Call `delivery_times` separately for each candidate promise**, inside the loop, passing that promise. The promise changes demand and therefore delivery times, so never reuse one array of times across promises or compute it once outside the loop.
- A late order is `time > promise` (strictly greater), as in the notebook.
- No `streamlit` import and no UI code in `logic.py`, so it can be tested and imported on its own.

## 4. `app.py`: interface only

- Import the functions: `from logic import cost_per_late_order, choose_best_promise` (and the starter constants it needs for widget options and defaults).
- No calculation formulas in `app.py`; any number shown must come from the `logic.py` functions.
- Widgets, with the notebook's values as defaults:
  - zone and time block: `st.selectbox` from `ZONES` and `TIME_BLOCKS` (default "Far West", "Fri/Sat eve")
  - promises to try: shortest, longest and step (default 20, 90, 5, giving `range(20, 95, 5)` as in the notebook)
  - refund, churn orders and margin: `st.number_input`, defaults from `COSTS`; build a `costs` dict with keys `refund`, `churn_orders`, `margin` to pass to `choose_best_promise`
  - run the calculation on an `st.button` click
- Results for a decision-maker:
  - Lead with the recommended promise and its net profit (`st.metric`), compared with today's `PROMISE`.
  - Show a chart of net profit against the promise and a table of every promise tried (orders, late orders, late %, net profit).
  - Warn if the best promise is at the edge of the range tried (as the notebook does).
  - Validate inputs (e.g. shortest < longest, step > 0) with `st.error` instead of crashing.
- `@st.cache_data` may wrap calls in `app.py` for speed, but must not change the logic or the seed.

## 5. Check before finishing

- Run `python -c "from logic import *; ..."` with the notebook inputs ("Far West", "Fri/Sat eve", promises 20–90 step 5, `COSTS`) and confirm the result matches the notebook: best promise **55 minutes**, net profit **$1,212.40**; at 45 minutes, net profit **-$127.40** (210 orders, 77 late). Cost per late order is **$26.20**.
- Run `streamlit run app.py` and confirm the default inputs show the same numbers.
- No personal information in the repository.
