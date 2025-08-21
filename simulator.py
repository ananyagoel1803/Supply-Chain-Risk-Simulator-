import pandas as pd

def load_data(path="data/supply_chain_risk_simulator_refined.xlsx"):
    return pd.read_excel(path)

def simulate_risks(df, demand_surge=0.0, supplier_delay=0, transport_increase=0.0):
    sim_df = df.copy()
    sim_df["UnitsOrdered"] = (sim_df["UnitsOrdered"] * (1 + demand_surge)).astype(int)
    sim_df["LeadTimeDays"] = sim_df["LeadTimeDays"] + supplier_delay
    sim_df["TransportCost"] = sim_df["TransportCost"] * (1 + transport_increase)
    sim_df["DeliveryDate"] = sim_df["OrderDate"] + pd.to_timedelta(sim_df["LeadTimeDays"], unit="D")
    sim_df["TotalCost"] = sim_df["CostPerUnit"] * sim_df["UnitsOrdered"] + sim_df["TransportCost"]
    sim_df["OnTime"] = sim_df["LeadTimeDays"].apply(lambda x: "Yes" if x <= 7 else "No")
    return sim_df

def calculate_kpis(dataset):
    return {
        "Average Lead Time (days)": round(dataset["LeadTimeDays"].mean(), 2),
        "On-Time Delivery %": round((dataset["OnTime"].value_counts(normalize=True).get("Yes", 0) * 100), 2),
        "Total Cost ($)": round(dataset["TotalCost"].sum(), 2)
    }
