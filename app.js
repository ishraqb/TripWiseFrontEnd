var sampleFlights = {
  cheapest: { airline: "Budget Air", price: 480, duration: "8h 45m" },
  balanced: { airline: "Skyline", price: 720, duration: "7h 30m" },
  premium: { airline: "Prestige Airways", price: 1850, duration: "7h 05m" }
};

var sampleHotels = {
  cheapest: { name: "City Hostel Central", pricePerNight: 65, rating: "7.8" },
  balanced: { name: "Garden View Hotel", pricePerNight: 140, rating: "8.6" },
  premium: { name: "The Grand Palace", pricePerNight: 380, rating: "9.4" }
};

var planTypes = [
  { name: "Cheapest", tier: "cheapest" },
  { name: "Balanced", tier: "balanced" },
  { name: "Experience-Focused", tier: "premium" }
];

var form = document.getElementById("trip-form");
var results = document.getElementById("results");
var errorBox = document.getElementById("error");

function countNights(startValue, endValue) {
  var start = new Date(startValue);
  var end = new Date(endValue);
  var oneDay = 1000 * 60 * 60 * 24;
  var difference = (end - start) / oneDay;
  return Math.round(difference);
}

function makeRow(labelText, valueText) {
  var row = document.createElement("div");
  row.className = "row";

  var label = document.createElement("span");
  label.className = "label";
  label.textContent = labelText;

  var value = document.createElement("span");
  value.textContent = valueText;

  row.appendChild(label);
  row.appendChild(value);
  return row;
}

function makeSectionTitle(text) {
  var title = document.createElement("div");
  title.className = "section-title";
  title.textContent = text;
  return title;
}

function buildCard(planType, nights, budget) {
  var flight = sampleFlights[planType.tier];
  var hotel = sampleHotels[planType.tier];

  var baseCost = flight.price + hotel.pricePerNight * nights;
  var activityBudget = budget - baseCost;

  var card = document.createElement("div");
  card.className = "card";

  var heading = document.createElement("h3");
  heading.textContent = planType.name;
  card.appendChild(heading);

  if (activityBudget < 0) {
    var warning = document.createElement("div");
    warning.className = "warning";
    warning.textContent = "This plan goes over budget before activities.";
    card.appendChild(warning);
  }

  card.appendChild(makeSectionTitle("Flight"));
  card.appendChild(makeRow(flight.airline, "$" + flight.price));
  card.appendChild(makeRow("Duration", flight.duration));

  card.appendChild(makeSectionTitle("Hotel"));
  card.appendChild(makeRow(hotel.name, "$" + hotel.pricePerNight + " / night"));
  card.appendChild(makeRow("Rating", hotel.rating));

  card.appendChild(makeSectionTitle("Costs"));
  card.appendChild(makeRow("Base cost", "$" + baseCost));

  var budgetRow = makeRow(
    activityBudget < 0 ? "Over budget by" : "Activity budget",
    "$" + Math.abs(activityBudget)
  );
  budgetRow.className = "row " + (activityBudget < 0 ? "over" : "under");
  card.appendChild(budgetRow);

  return card;
}

form.addEventListener("submit", function (event) {
  event.preventDefault();
  errorBox.textContent = "";
  results.innerHTML = "";

  var destination = document.getElementById("destination").value;
  var startValue = document.getElementById("start-date").value;
  var endValue = document.getElementById("end-date").value;
  var budget = Number(document.getElementById("budget").value);

  if (destination === "" || startValue === "" || endValue === "" || budget <= 0) {
    errorBox.textContent = "Please fill in destination, both dates, and a budget.";
    return;
  }

  var nights = countNights(startValue, endValue);
  if (nights <= 0) {
    errorBox.textContent = "The return date must be after the departure date.";
    return;
  }

  var title = document.createElement("h2");
  title.className = "results-title";
  title.textContent = "Your trip to " + destination + " (" + nights + " nights)";
  results.appendChild(title);

  for (var i = 0; i < planTypes.length; i++) {
    var card = buildCard(planTypes[i], nights, budget);
    results.appendChild(card);
  }
});
