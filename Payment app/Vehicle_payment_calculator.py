import streamlit as st
from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.set_page_config(page_title="Vehicle Payment Calculator")

st.title("🚚 Vehicle Payment Calculator")
st.subheader("Made By Sameed Hassan")

# Session state to store all entries
if "entries" not in st.session_state:
    st.session_state.entries = []

st.write("## Vehicle Information")

col1, col2 = st.columns(2)

vehicle_num = col1.number_input(
    "Vehicle Number",
    min_value=0,
    step=1
)

weight = col2.number_input(
    "Enter Vehicle Weight",
    min_value=0.0,
    step=0.1
)

unit = col1.selectbox(
    "Select Unit",
    ["Kg", "Mund"]
)

st.write("## Rates")

col3, col4 = st.columns(2)

broker_rate = col3.number_input(
    "Broker Rate (Rs per Mund)",
    min_value=0.0,
    step=0.1
)

company_rate = col4.number_input(
    "Company Rate (Rs per Mund)",
    min_value=0.0,
    step=0.1
)

if st.button("Add Entry"):

    # Convert weight to mund if entered in kg
    weight_in_mund = weight

    if unit == "Kg":
        weight_in_mund = weight / 40

    # Calculations
    buying_cost = weight_in_mund * broker_rate
    selling_revenue = weight_in_mund * company_rate

    total_cost = buying_cost

    profit = selling_revenue - total_cost

    # Save entry
    st.session_state.entries.append({
        "Vehicle No": vehicle_num,
        "Weight (Mund)": round(weight_in_mund, 2),
        "Broker Cost": round(buying_cost, 2),
        "Total Cost": round(total_cost, 2),
        "Company Revenue": round(selling_revenue, 2),
        "Profit": round(profit, 2)
    })
    supabase.table("vehicle_records").insert({
    "Vehicle_no": vehicle_num,
    "Weight_mund": round(weight_in_mund, 2),
    "Broker_cost": round(buying_cost, 2),
    "Total_cost": round(total_cost, 2),
    "Company_Cost": round(selling_revenue, 2),
    "Profit": round(profit, 2)
}).execute()

    st.success("Entry added successfully!")

# Display all entries
if st.session_state.entries:

    st.write("## All Entries")

    st.table(st.session_state.entries)

    grand_cost = sum(entry["Total Cost"]
                     for entry in st.session_state.entries)

    grand_revenue = sum(entry["Company Revenue"]
                        for entry in st.session_state.entries)

    grand_profit = sum(entry["Profit"]
                       for entry in st.session_state.entries)

    st.write("## Summary")

    st.success(f"💸 Total Amount Spent: Rs {grand_cost:,.2f}")
    st.info(f"💰 Total Revenue: Rs {grand_revenue:,.2f}")

    if grand_profit >= 0:
        st.success(f"📈 Total Profit: Rs {grand_profit:,.2f}")
    else:
        st.error(f"📉 Total Loss: Rs {abs(grand_profit):,.2f}")

    col1, col2 = st.columns(2)

    if col1.button("Remove Last Entry"):
        st.session_state.entries.pop()
        st.rerun()

    if col2.button("Clear All Entries"):
        st.session_state.entries = []
        st.rerun()
        
