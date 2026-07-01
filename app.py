from flask import Flask, render_template, flash, request
from forms import TripForm
import git

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-any-random-string"

SAMPLE_FLIGHTS = {
    "cheapest": {"airline": "Budget Air", "price": 480, "duration": "8h 45m"},
    "balanced": {"airline": "Skyline", "price": 720, "duration": "7h 30m"},
    "premium": {"airline": "Prestige Airways", "price": 1850, "duration": "7h 05m"},
}
SAMPLE_HOTELS = {
    "cheapest": {"name": "City Hostel Central", "price": 65, "rating": "7.8"},
    "balanced": {"name": "Garden View Hotel", "price": 140, "rating": "8.6"},
    "premium": {"name": "The Grand Palace", "price": 380, "rating": "9.4"},
}
PLAN_TIERS = [
    ("Cheapest", "cheapest"),
    ("Balanced", "balanced"),
    ("Experience-Focused", "premium"),
]

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/TripWiseFrontEnd/TripWiseFrontEnd')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

def build_plans(nights, budget):
    plans = []
    for name, tier in PLAN_TIERS:
        flight = SAMPLE_FLIGHTS[tier]
        hotel = SAMPLE_HOTELS[tier]
        base_cost = flight["price"] + hotel["price"] * nights
        activity_budget = budget - base_cost
        plans.append({
            "name": name,
            "flight": flight,
            "hotel": hotel,
            "base_cost": base_cost,
            "activity_budget": activity_budget,
            "over_budget": activity_budget < 0,
        })
    return plans


@app.route("/", methods=["GET", "POST"])
def home():
    form = TripForm()
    if form.validate_on_submit():
        nights = (form.end_date.data - form.start_date.data).days
        if nights <= 0:
            flash("Return date must be after the departure date.")
            return render_template("home.html", form=form)
        plans = build_plans(nights, form.budget.data)
        return render_template("results.html", plans=plans,
                               destination=form.destination.data, nights=nights)
    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
