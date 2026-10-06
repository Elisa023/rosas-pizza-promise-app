# Rosa's Pizza: Best Delivery Promise

A Streamlit app that recommends the delivery promise (in minutes) with the highest simulated net profit over four weeks, for a chosen zone and time block.

**Net profit = orders × margin − late orders × (refund + future orders lost × margin)**

The calculations in `logic.py` come from `722_Assignment1.ipynb` (Part II), use the instructor's `starter` simulator, and keep `seed=1`, so the app matches the notebook. `app.py` is the interface.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Inputs
- Zone and time block
- Minimum and maximum promise (tested in 5-minute steps; default 20–90)
- Profit margin per order, future orders lost per late order, refund per late order (defaults from `COSTS`)
