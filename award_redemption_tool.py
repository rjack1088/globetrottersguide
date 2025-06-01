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
    total_effective_cost = cash_required_with_bags + (points_used * (benchmark / 100))
    savings = cash_price - total_effective_cost

    if savings < 0 or val_wo_bag < benchmark:
        assessment = "Poor redemption"
    elif val_wo_bag <= benchmark + 0.2:
        assessment = "Good redemption"
    else:
        assessment = "Great redemption!"

    return val_with_bag, val_wo_bag, assessment, benchmark, savings


st.set_page_config(page_title="Points vs. Cash Flight Tool")

st.title("✈️ Points vs. Cash Flight Comparison Tool")
st.write(
    "Use this tool to help you decide whether to book a flight with points/miles or cash, "
    "based on airline-specific redemption benchmarks."
)

with st.form("flight_form"):
    flight_name = st.text_input("Flight Name or Route", placeholder="Example: JFK to LHR")

    cash_price_str = st.text_input("Cash Price (USD, excluding bag fees)", placeholder="e.g. 425.00")
    taxes_fees_str = st.text_input("Taxes & Fees on Award Ticket (USD)", placeholder="e.g. 57.60")
    bag_fees_str = st.text_input("Bag Fees (USD, if applicable)", placeholder="e.g. 70.00")
    points_used_str = st.text_input("Points or Miles Required", placeholder="e.g. 32000")

    program = st.selectbox("Select Airline Loyalty Program", list(POINT_VALUATIONS.keys()))
    submitted = st.form_submit_button("Compare")

if submitted:
    try:
        cash_price = float(cash_price_str)
        taxes_fees = float(taxes_fees_str)
        bag_fees = float(bag_fees_str)
        points_used = int(points_used_str)

        val_with_bag, val_wo_bag, assessment, benchmark, savings = evaluate_redemption(
            cash_price, points_used, taxes_fees, bag_fees, program
        )

        st.markdown("### 🧾 Results")
        st.write(f"**Flight:** {flight_name}")
        st.write(f"**Program:** {program}")
        st.write(f"**Benchmark Redemption Value:** {benchmark:.2f}¢/point")
        st.write(f"**Redemption Value w/o Bag Fees:** {val_wo_bag:.2f}¢/point")
        st.write(f"**Redemption Value w/ Bag Fees:** {val_with_bag:.2f}¢/point")
        st.write(f"**Estimated Savings vs. Paying Cash:** ${savings:.2f}")
        st.write(f"**Assessment:** {assessment}")

    except ValueError:
        st.error("Please enter valid numbers in all fields.")