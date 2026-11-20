import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "change-this-secret")


# SUPABASE DATABASE
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# TOURIST DESTINATIONS
DESTINATIONS = [

    {
        "name": "Ooty",
        "location": "Nilgiris",
        "description": "Beautiful hill station with tea gardens.",
        "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358"
    },

    {
        "name": "Kodaikanal",
        "location": "Dindigul",
        "description": "Princess of Hill Stations.",
        "image": "https://images.unsplash.com/photo-1589307357647-7f7f4f6f5f7d"
    },

    {
        "name": "Madurai",
        "location": "Madurai",
        "description": "Famous for Meenakshi Amman Temple.",
        "image": "https://images.unsplash.com/photo-1600100397608-1b6b6e4c6e0c"
    },

    {
        "name": "Rameswaram",
        "location": "Ramanathapuram",
        "description": "Famous spiritual and coastal destination.",
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944"
    },

    {
        "name": "Kanyakumari",
        "location": "Kanyakumari",
        "description": "Beautiful sunrise and sunset destination.",
        "image": "https://images.unsplash.com/photo-1589307357647-7f7f4f6f5f7d"
    },

    {
        "name": "Thanjavur",
        "location": "Thanjavur",
        "description": "Famous for Brihadeeswarar Temple.",
        "image": "https://images.unsplash.com/photo-1606293926075-69a00db196d8"
    }

]


# HOME PAGE
@app.route("/")
def home():

    return render_template(
        "index.html",
        destinations=DESTINATIONS
    )


# DESTINATIONS PAGE
@app.route("/destinations")
def destinations():

    return render_template(
        "destinations.html",
        destinations=DESTINATIONS
    )


# BOOKING PAGE
@app.route("/booking", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        if not supabase:
            flash("Database not configured.")
            return redirect(url_for("booking"))

        try:

            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()

            destination = request.form.get("destination")
            hotel = request.form.get("hotel")

            check_in = request.form.get("check_in")
            check_out = request.form.get("check_out")

            persons = int(request.form.get("persons", 1))

            if not all([
                name,
                email,
                phone,
                destination,
                hotel,
                check_in,
                check_out
            ]):
                raise ValueError("Please complete all fields.")

            if persons < 1:
                raise ValueError("Persons must be at least 1.")

            if check_out <= check_in:
                raise ValueError("Check-out must be after check-in.")

            result = supabase.table("bookings").insert({

                "name": name,
                "email": email,
                "phone": phone,
                "destination": destination,
                "hotel": hotel,
                "check_in": check_in,
                "check_out": check_out,
                "persons": persons

            }).execute()

            flash("Booking submitted successfully!")

            return redirect(url_for("booking"))

        except Exception as e:

            print("BOOKING ERROR:", e)

            flash(str(e))

    return render_template(
        "booking.html",
        destinations=DESTINATIONS
    )


# RUN APPLICATION
if __name__ == "__main__":

    app.run(debug=True)
