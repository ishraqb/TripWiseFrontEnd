import git
import os

from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import TripForm
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    nights = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    travelers = db.Column(db.Integer, nullable=False)
    style = db.Column(db.String(100))
    interests = db.Column(db.String(200))

    def __repr__(self):
        return f"Trip('{self.destination}', {self.nights} nights)"


with app.app_context():
    db.create_all()

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
        trip = Trip(
            destination=form.destination.data,
            nights=nights,
            budget=form.budget.data,
            travelers=form.travelers.data,
            style=form.style.data,
            interests=form.interests.data,
        )
        db.session.add(trip)
        db.session.commit()
        return render_template("results.html", plans=plans,
                               destination=form.destination.data, nights=nights)
    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
