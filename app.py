import os
from functools import wraps
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


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


@app.route("/")
def home():
    return render_template("index.html", destinations=DESTINATIONS)


@app.route("/destinations")
def destinations():
    return render_template(
        "destinations.html",
        destinations=DESTINATIONS
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not supabase:
            flash("Database not configured.")
            return redirect(url_for("register"))

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or len(password) < 6:
            flash("Enter valid details. Password must be at least 6 characters.")
            return redirect(url_for("register"))

        try:
            existing = supabase.table("users").select("id").eq(
                "email", email
            ).execute()

            if existing.data:
                flash("Email already registered.")
                return redirect(url_for("register"))

            result = supabase.table("users").insert({
                "name": name,
                "email": email,
                "password": generate_password_hash(password)
            }).execute()

            flash("Registration successful. Please login.")
            return redirect(url_for("login"))

        except Exception as e:
            print(e)
            flash("Registration failed.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not supabase:
            flash("Database not configured.")
            return redirect(url_for("login"))

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        try:
            result = supabase.table("users").select("*").eq(
                "email", email
            ).execute()

            if result.data:
                user = result.data[0]

                if check_password_hash(user["password"], password):
                    session["user_id"] = user["id"]
                    session["name"] = user["name"]

                    return redirect(url_for("dashboard"))

            flash("Invalid email or password.")

        except Exception as e:
            print(e)
            flash("Login failed.")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        name=session.get("name")
    )


@app.route("/booking", methods=["GET", "POST"])
@login_required
def booking():
    if request.method == "POST":
        if not supabase:
            flash("Database not configured.")
            return redirect(url_for("booking"))

        try:
            destination = request.form.get("destination")
            hotel = request.form.get("hotel")
            check_in = request.form.get("check_in")
            check_out = request.form.get("check_out")
            persons = int(request.form.get("persons", 1))

            if persons < 1 or not all([
                destination, hotel, check_in, check_out
            ]):
                raise ValueError("Please complete all booking fields.")

            if check_out <= check_in:
                raise ValueError("Check-out must be after check-in.")

            result = supabase.table("bookings").insert({
                "user_id": session["user_id"],
                "destination": destination,
                "hotel": hotel,
                "check_in": check_in,
                "check_out": check_out,
                "persons": persons
            }).execute()

            flash("Hotel booking saved successfully!")
            return redirect(url_for("booking"))

        except Exception as e:
            print(e)
            flash(str(e))

    return render_template(
        "booking.html",
        destinations=DESTINATIONS
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
