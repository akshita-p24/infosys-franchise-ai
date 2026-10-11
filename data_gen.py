"""Generate realistic sample data for all 7 agents into ./data/*.csv
Run once:  python data_gen.py
"""
import os
import numpy as np, pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
rng = np.random.default_rng(42)

CITIES = ["Guwahati","Shillong","Kolkata","Bengaluru","Hyderabad","Chennai",
          "Pune","Mumbai","Delhi","Jaipur","Lucknow","Bhubaneswar"]
QUALITY = [1.35,0.7,1.15,1.4,1.05,0.95,1.1,1.25,0.55,0.85,0.65,0.9]  # drives tiers later

def generate(force=False):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not force and os.path.exists(os.path.join(DATA_DIR, "sales.csv")):
        return
    outlets = pd.DataFrame({
        "outlet_id": [f"O{i+1:02d}" for i in range(12)],
        "outlet_name": [f"FranchiseOps {c}" for c in CITIES],
        "city": CITIES, "quality": QUALITY,
        "opened": pd.date_range("2019-01-01", periods=12, freq="5MS").strftime("%Y-%m-%d"),
    })
    # ---- sales (daily, 180 days)
    days = pd.date_range(end=pd.Timestamp.today().normalize(), periods=180)
    rows = []
    for _, o in outlets.iterrows():
        for i, d in enumerate(days):
            wk = 1.25 if d.dayofweek >= 5 else 1.0
            trend = 1 + (o.quality - 1) * 0.0008 * i
            orders = max(20, int(rng.normal(180 * o.quality * wk * trend, 15)))
            avg_ticket = rng.normal(260 + 30 * o.quality, 15)
            rows.append([o.outlet_id, d, orders, int(orders * rng.uniform(.9, 1.1)),
                         round(orders * avg_ticket, 2),
                         round(rng.normal(32 - 3 * o.quality, 1.5), 1),     # food_cost_pct
                         round(max(0.5, rng.normal(7 - 2.5 * o.quality, 1)), 1)])  # wastage_pct
    sales = pd.DataFrame(rows, columns=["outlet_id","date","orders","customers",
                                        "revenue","food_cost_pct","wastage_pct"])
    # ---- inventory
    items = ["Flour","Cooking Oil","Chicken","Paneer","Rice","Tomatoes","Cheese","Packaging","Spices","Milk"]
    inv = []
    for _, o in outlets.iterrows():
        for it in items:
            usage = rng.uniform(5, 40)
            reorder = usage * 4
            stock = max(0, rng.normal(reorder * (1.2 + (o.quality - 1) * .5), reorder * .5))
            inv.append([o.outlet_id, it, round(stock,1), round(reorder,1),
                        round(usage,1), round(rng.uniform(30, 400),1)])
    inventory = pd.DataFrame(inv, columns=["outlet_id","item","stock","reorder_level",
                                           "daily_usage","unit_cost"])
    # ---- staff
    roles = ["Cashier","Cook","Server","Supervisor","Delivery"]
    st_rows, sid = [], 1
    for _, o in outlets.iterrows():
        for _ in range(10):
            att = float(np.clip(rng.normal(80 + 10 * (o.quality - 1) * 2, 8), 40, 100))
            perf = float(np.clip(rng.normal(65 + 20 * (o.quality - 1), 12), 20, 100))
            ten = int(rng.integers(1, 60))
            risk = (100 - att) / 100 + (100 - perf) / 150 + (1 / (ten + 3))
            st_rows.append([f"S{sid:03d}", o.outlet_id, f"Staff {sid}", rng.choice(roles),
                            round(att,1), round(perf,1), ten, int(rng.random() < risk * .6)])
            sid += 1
    staff = pd.DataFrame(st_rows, columns=["staff_id","outlet_id","name","role",
                                           "attendance_pct","performance_score",
                                           "tenure_months","left_company"])
    # ---- marketing
    channels = ["Instagram","Google Ads","Facebook","Email","Flyers","Influencer"]
    mk = []
    for k in range(40):
        o = outlets.sample(1, random_state=int(rng.integers(1e6))).iloc[0]
        ch = rng.choice(channels); spend = rng.uniform(5000, 60000)
        roi = rng.uniform(.6, 4.5) * (0.8 + o.quality * .3)
        mk.append([f"C{k+1:03d}", o.outlet_id, ch, round(spend,0), round(spend*roi,0),
                   int(rng.integers(50, 900))])
    marketing = pd.DataFrame(mk, columns=["campaign_id","outlet_id","channel","spend",
                                          "revenue_generated","new_customers"])
    # ---- feedback
    pos = ["Great food and quick service","Loved the ambience","Staff were very friendly",
           "Fresh and tasty, will come again","Excellent value for money"]
    neg = ["Service was very slow","Food arrived cold","The place was not clean",
           "Staff were rude","Order was wrong and no refund","Too expensive for the portion"]
    fb = []
    for _, o in outlets.iterrows():
        for _ in range(60):
            good = rng.random() < (0.45 + 0.3 * (o.quality - .5))
            fb.append([o.outlet_id, days[int(rng.integers(len(days)))].strftime("%Y-%m-%d"),
                       int(np.clip(round(rng.normal(4.2 if good else 2.2, .7)), 1, 5)),
                       rng.choice(pos if good else neg)])
    feedback = pd.DataFrame(fb, columns=["outlet_id","date","rating","comment"])
    # ---- audits
    au = []
    for _, o in outlets.iterrows():
        for m in range(6):
            au.append([o.outlet_id, (pd.Timestamp.today() - pd.DateOffset(months=m)).strftime("%Y-%m-%d"),
                       round(float(np.clip(rng.normal(70 + 25 * (o.quality - 1), 6), 35, 100)),1),
                       int(max(0, rng.normal(6 - 4 * (o.quality - 1), 2)))])
    audits = pd.DataFrame(au, columns=["outlet_id","date","compliance_score","open_issues"])

    for name, df in [("outlets",outlets),("sales",sales),("inventory",inventory),
                     ("staff",staff),("marketing",marketing),("feedback",feedback),
                     ("audits",audits)]:
        df.to_csv(os.path.join(DATA_DIR, f"{name}.csv"), index=False)

if __name__ == "__main__":
    generate(force=True)
    print("Sample data written to", DATA_DIR)