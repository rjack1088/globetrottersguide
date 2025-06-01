import streamlit as st

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

def evaluate_redemption(cash_price, points_used, taxes_fees, bag_fees, program):
    cash_required_with_bags = taxes_fees + bag_fees
    val_with_bag = round((cash_price - cash_required_with_bags) / points_used * 100, 2)
    val_wo_bag = round((cash_price - taxes_fees) / points_used * 100, 2)

    benchmark = POINT_VALUATIONS.get(program, 1.0)
    pt_cash_value = round(points_used * (benchmark / 100), 2)
    total_effective_cost = round(cash_required_with_bags + pt_cash_value, 2)
    savings = round(cash_price - total_effective_cost, 2)

    if savings < 0 or val_wo_bag < benchmark:
        assessment = "Poor redemption"
    elif val_wo_bag <= benchmark + 0.2:
        assessment = "Good redemption"
    else:
        assessment = "Great redemption!"

    return {
        "val_with_bag": val_with_bag,
        "val_wo_bag": val_wo_bag,
        "benchmark": benchmark,
        "savings": savings,
        "total_effective_cost": total_effective_cost,
        "pt_cash_value": pt_cash_value,
        "assessment": assessment
    }

# ---- Streamlit UI ----

st.set_page_config(page_title="Points vs Cash Flight Tool", layout="centered")

st.title("✈️ Points vs Cash Flight Redemption Tool")
st.write("Find out whether it's a good deal to use your miles or pay cash for your next flight.")

with st.form("flight_form"):
    flight_name = st.text_input("Flight Name or Route", "Example: JFK to LAX")
    cash_price = st.number_input("Cash Price of Ticket (exclude bag fees)", min_value=0.0, step=10.0)
    taxes_fees = st.number_input("Taxes & Fees on Award Ticket", min_value=0.0, step=1.0)
    bag_fees = st.number_input("Bag Fees (if applicable)", min_value=0.0, step=1.0)
    points_used = st.number_input("Points Required for Award Ticket", min_value=1, step=100)
    program = st.selectbox("Select Airline Loyalty Program", list(POINT_VALUATIONS.keys()))

    submitted = st.form_submit_button("Evaluate Redemption")

if submitted:
    results = evaluate_redemption(cash_price, points_used, taxes_fees, bag_fees, program)

    st.subheader(f"Results for {flight_name}")
    st.write(f"**Cash Price:** ${cash_price:.2f}")
    st.write(f"**Points Required:** {points_used:,}")
    st.write(f"**Value Per Point (with bag fees):** {results['val_with_bag']}¢")
    st.write(f"**Value Per Point (excluding bag fees):** {results['val_wo_bag']}¢")
    st.write(f"**Benchmark for {program}:** {results['benchmark']}¢")
    st.write(f"**Cash Value of Points Used:** ${results['pt_cash_value']:.2f}")
    st.write(f"**Total Effective Cost (points + cash):** ${results['total_effective_cost']:.2f}")
    st.write(f"**Savings Compared to Cash Price:** ${results['savings']:.2f}")

    st.success(f"**Assessment:** {results['assessment']}")