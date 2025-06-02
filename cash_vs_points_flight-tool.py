import streamlit as st
import pandas as pd

POINT_VALUATIONS = {
    "Aegean Miles+Bonus": 1.3,
    "Air Canada Aeroplan": 1.45,
    "Air France KLM Flying Blue": 1.3,
    "Alaska Airlines Mileage Plan": 1.53,
    "American Airlines AAdvantage": 1.49,
    "ANA Mileage Club": 1.4,
    "Asiana Airlines Asiana Club Miles": 1.6,
    "Avianca LifeMiles": 1.38,
    "Avios": 1.27,
    "Cathay Pacific Asia Miles": 1.23,
    "Delta Air Lines SkyMiles": 1.15,
    "Emirates Skywards": 1.17,
    "Etihad Guest": 1.23,
    "Frontier Airlines Frontier Miles": 1.07,
    "Hawaiian Airlines Hawaiian Miles": 1.2,
    "Japan Airlines Mileage Bank": 1.3,
    "JetBlue TrueBlue": 1.31,
    "Korean Air SkyPass": 1.53,
    "Lufthansa Miles & More": 1.27,
    "Qantas Frequent Flyer": 1.3,
    "Singapore Airlines KrisFlyer": 1.35,
    "Southwest Airlines Rapid Rewards": 1.3,
    "Spirit Airlines Free Spirit": 1.1,
    "Turkish Airlines Miles&Smiles": 1.3,
    "United Airlines MileagePlus": 1.22,
    "Virgin Atlantic Flying Club": 1.33
}

AIRLINE_CHOICES = list(POINT_VALUATIONS.keys())

def safe_float(val):
    try:
        return float(val)
    except:
        return 0.0

def safe_int(val):
    try:
        return int(val)
    except:
        return 0

def evaluate_redemption(cash_price, points_used, taxes_fees, bag_fees, program):
    cash_required_with_bags = taxes_fees + bag_fees
    val_with_bag = round((cash_price - cash_required_with_bags) / points_used * 100, 2) if points_used else 0
    val_wo_bag = round((cash_price - taxes_fees) / points_used * 100, 2) if points_used else 0
    benchmark = POINT_VALUATIONS.get(program, 1.0)
    total_effective_cost = cash_required_with_bags + (points_used * (benchmark / 100))
    savings = cash_price - total_effective_cost

    if savings < 0:
        assessment = "Poor redemption"
    elif val_wo_bag < benchmark:
        assessment = "Poor redemption"
    elif val_wo_bag <= benchmark + 0.2:
        assessment = "Good redemption"
    else:
        assessment = "Great redemption!"

    return val_with_bag, val_wo_bag, assessment

def compare_flights(flights):
    results = []
    for flight in flights:
        name = flight["name"]
        base_cash_price = flight["cash_price"]
        bag_fees = flight["bag_fees"]
        taxes_fees = flight["taxes_fees"]
        points_used = flight["points_used"]
        program = flight["program"]

        cash_price_with_bags = base_cash_price + bag_fees
        cash_required = taxes_fees + bag_fees
        point_value = POINT_VALUATIONS.get(program, 1.0)
        point_dollar_value = points_used * (point_value / 100)
        total_effective_cost = round(cash_required + point_dollar_value, 2)
        savings = round(base_cash_price - total_effective_cost, 2)
        pt_cash_value = round(points_used * (point_value / 100), 2)

        val_with_bag, val_wo_bag, assessment = evaluate_redemption(
            base_cash_price, points_used, taxes_fees, bag_fees, program
        )

        results.append({
            "name": name,
            "cash_price": cash_price_with_bags,
            "cash_required": cash_required,
            "points_used": points_used,
            "pt_cash_value": pt_cash_value,
            "point_dollar_value": round(point_dollar_value, 2),
            "total_effective_cost": total_effective_cost,
            "redemption_efficiency": savings,
            "val_with_bag": val_with_bag,
            "val_wo_bag": val_wo_bag,
            "assessment": assessment,
            "benchmark": point_value
        })

    results.sort(key=lambda x: x["val_with_bag"], reverse=True)
    return results

def main():
    st.set_page_config(page_title="Points vs Cash Flight Tool", page_icon="✈️")

    st.markdown("""
    <style>
    .table-container {
        overflow-x: auto;
        width: 100%;
    }
    .table-container table {
        width: 100%;
        white-space: nowrap;
    }
    div[class*="stNumberInput"] > div[class*="stVerticalBlock"] > div[class*="stHorizontalBlock"] {
        display: none;
    }
    div[role="tooltip"] {
        display: none !important;
    }
    .stDataFrame {
        overflow-x: auto !important;
        overflow-y: auto !important;
    }
    .stDataFrame > div {
        overflow-x: auto !important;
        overflow-y: auto !important;
    }
    .dataframe {
        width: 100%;
        table-layout: fixed;
        word-wrap: break-word;
        white-space: normal !important;
    }
    .dataframe th {
        white-space: normal !important;
        text-align: left;
        word-wrap: break-word;
    }
    .dataframe td {
        white-space: normal !important;
        text-align: left;
        word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("# ✈️ Points vs Cash Flight Tool")
    st.write("Use this tool to compare whether a flight is a better deal when booked with cash or points. Simply enter your flight details and get a quick analysis.")

    mode = st.radio(
        "Choose mode:",
        ("Single Flight", "Compare Multiple Flights"),
        index=0,
        horizontal=True
    )
    num_flights = 1 if mode == "Single Flight" else st.number_input("Number of flights to compare", min_value=2, max_value=10, value=2, step=1)

    flights = []

    for i in range(num_flights):
        st.markdown(f"### Flight {i + 1}")
        name = st.text_input(f"Flight Name or Route (e.g., NYC to LAX)", key=f"name_{i}")

        base_cash_price = safe_float(
            st.text_input(
                f"Cash Price (excl. bag fees) [$] (e.g., 299.99)",
                key=f"cash_price_{i}",
                on_change=None
            )
        )

        taxes_fees = safe_float(
            st.text_input(
                f"Taxes and Fees on Reward Ticket [$] (e.g., 25.00)",
                key=f"taxes_fees_{i}",
                on_change=None
            )
        )

        bag_fees = safe_float(
            st.text_input(
                f"Bag Fees (if applicable) [$] (e.g., 35.00)",
                key=f"bag_fees_{i}",
                on_change=None
            )
        )

        points_used = safe_int(
            st.text_input(
                f"Points Required (e.g., 15000)",
                key=f"points_used_{i}",
                on_change=None
            )
        )

        program = st.selectbox(f"Loyalty Program", AIRLINE_CHOICES, key=f"program_{i}")

        flights.append({
            "name": name,
            "cash_price": base_cash_price,
            "taxes_fees": taxes_fees,
            "bag_fees": bag_fees,
            "points_used": points_used,
            "program": program
        })

    if st.button("Calculate" if mode == "Single Flight" else "Compare Flights"):
        if mode == "Single Flight":
            flight = flights[0]
            val_with_bag, val_wo_bag, assessment = evaluate_redemption(
                flight["cash_price"], flight["points_used"],
                flight["taxes_fees"], flight["bag_fees"], flight["program"]
            )
            
            base_cash_price = flight["cash_price"]
            bag_fees = flight["bag_fees"]
            taxes_fees = flight["taxes_fees"]
            points_used = flight["points_used"]
            program = flight["program"]

            cash_price_with_bags = base_cash_price + bag_fees
            cash_required = taxes_fees + bag_fees
            point_value = POINT_VALUATIONS.get(program, 1.0)
            point_dollar_value = round(points_used * (point_value / 100), 2)
            total_effective_cost = round(cash_required + point_dollar_value, 2)
            savings = round(base_cash_price - total_effective_cost, 2)
            pt_cash_value = round(points_used * (point_value / 100), 2)

            st.write(f"### Detailed Results for {flight['name']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Pricing Breakdown")
                st.write(f"**Base Cash Price:** ${base_cash_price:.2f}")
                st.write(f"**Bag Fees:** ${bag_fees:.2f}")
                st.write(f"**Taxes & Fees:** ${taxes_fees:.2f}")
                st.write(f"**Cash Price with Bags:** ${cash_price_with_bags:.2f}")
            
            with col2:
                st.write("### Points Analysis")
                st.write(f"**Points Used:** {points_used}")
                st.write(f"**Loyalty Program:** {program}")
                st.write(f"**Point Value:** {point_value}¢")
                st.write(f"**Points Cash Value:** ${pt_cash_value:.2f}")
            
            st.write("### Redemption Efficiency")
            st.write(f"**Redemption Value with Bags:** {val_with_bag:.2f}¢ per point")
            st.write(f"**Redemption Value without Bags:** {val_wo_bag:.2f}¢ per point")
            st.write(f"**Total Effective Cost:** ${total_effective_cost:.2f}")
            st.write(f"**Estimated Savings:** ${savings:.2f}")
            st.write(f"**Assessment:** **{assessment}**")
        else:
            results = compare_flights(flights)
            st.write("### Flight Comparison Results")
            
            df = pd.DataFrame([
                {
                    "Flight": r["name"],
                    "Req Award Cash": f"${r['cash_required']:.2f}",
                    "Pt Cash Value": f"${r['pt_cash_value']:.2f}",
                    "Total Cost": f"${r['total_effective_cost']:.2f}",
                    "Savings": f"${r['redemption_efficiency']:.2f}",
                    "Redemption Value w/ Bags (¢)": f"{r['val_with_bag']:.2f}",
                    "Redemption Value w/o Bags (¢)": f"{r['val_wo_bag']:.2f}",
                    "Benchmark (¢)": f"{r['benchmark']:.2f}",
                    "Assessment": r["assessment"]
                }
                for r in results
            ])
            
            column_config = {
                "Flight": st.column_config.TextColumn(width="large"),
                "Req Award Cash": st.column_config.TextColumn(width="small"),
            }
            
            st.dataframe(
                df, 
                use_container_width=True,
                hide_index=True,
                column_config=column_config
            )

if __name__ == "__main__":
    main()
