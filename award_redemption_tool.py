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

AIRLINE_CHOICES = list(POINT_VALUATIONS.keys())

st.set_page_config(page_title="Points vs. Cash Tool", layout="wide")
st.title("✈️ Award Redemption Value Tool")

st.markdown("""
Use this tool to compare whether a flight is a better deal when booked with **cash** or **points**.
Simply enter your flight details and get a quick analysis.
""")

num_flights = st.number_input("How many flights would you like to compare?", min_value=1, max_value=5, step=1, value=1)

flights = []

for i in range(num_flights):
    st.subheader(f"Flight {i + 1} Details")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Flight Name or Route", placeholder="Example: JFK-LHR", key=f"name_{i}")
        base_cash_price = st.text_input("Cash Price (excluding bag fees)", placeholder="e.g. 750.00", key=f"cash_price_{i}")
        taxes_fees = st.text_input("Taxes and Fees on Award Ticket", placeholder="e.g. 80.00", key=f"taxes_fees_{i}")
        bag_fees = st.text_input("Bag Fees", placeholder="e.g. 60.00", key=f"bag_fees_{i}")

    with col2:
        points_used = st.text_input("Points Required", placeholder="e.g. 20000", key=f"points_used_{i}")
        program = st.selectbox("Loyalty Program", AIRLINE_CHOICES, key=f"program_{i}")

    try:
        flight = {
            "name": name,
            "cash_price": float(base_cash_price),
            "taxes_fees": float(taxes_fees),
            "bag_fees": float(bag_fees),
            "points_used": int(points_used),
            "program": program
        }
        flights.append(flight)
    except ValueError:
        st.warning(f"Please complete all fields with valid numbers for Flight {i + 1}.")

def evaluate_redemption(cash_price, points_used, taxes_fees, bag_fees, program):
    cash_required_with_bags = taxes_fees + bag_fees
    val_with_bag = round((cash_price - cash_required_with_bags) / points_used * 100, 2)
    val_wo_bag = round((cash_price - taxes_fees) / points_used * 100, 2)
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
        redemption_efficiency = round(base_cash_price - total_effective_cost, 2)
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
            "redemption_efficiency": redemption_efficiency,
            "val_with_bag": val_with_bag,
            "val_wo_bag": val_wo_bag,
            "assessment": assessment,
            "benchmark": point_value
        })

    results.sort(key=lambda x: x["val_with_bag"], reverse=True)
    return results

if st.button("Compare Flights"):
    if len(flights) == num_flights:
        results = compare_flights(flights)
        st.subheader("Comparison Results")
        st.write("Higher redemption value (¢/point) is better.")
        st.dataframe(results)
    else:
        st.error("Please fill in all required fields for all flights.")