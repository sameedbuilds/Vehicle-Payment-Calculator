import streamlit as st
from supabase import create_client
import pandas as pd

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="View Records")
st.title("📋 Vehicle Records")

# Month & Year filter
col1, col2 = st.columns(2)
month = col1.selectbox("Select Month", list(range(1, 13)), index=0)
year = col2.number_input("Select Year", min_value=2024, max_value=2030, value=2026)

if st.button("Load Records"):
    response = supabase.table("vehicle_records") \
        .select("*") \
        .gte("created_at", f"{year}-{month:02d}-01") \
        .lt("created_at", f"{year}-{month+1:02d}-01" if month < 12 else f"{year+1}-01-01") \
        .execute()

    data = response.data

    if data:
        df = pd.DataFrame(data)
        df = df.drop(columns=["id", "created_at"], errors="ignore")
        st.dataframe(df, use_container_width=True)

        st.write("## Summary")
        st.success(f"💸 Total Cost: Rs {df['Total_cost'].sum():,.2f}")
        st.info(f"💰 Total Revenue: Rs {df['Company_Cost'].sum():,.2f}")
        profit = df['Profit'].sum()
        if profit >= 0:
            st.success(f"📈 Total Profit: Rs {profit:,.2f}")
        else:
            st.error(f"📉 Total Loss: Rs {abs(profit):,.2f}")
    else:
        st.warning("No records found for this month.")
