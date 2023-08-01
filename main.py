from flask import Flask, render_template, request
import mysql.connector
import requests

app = Flask(__name__)

# For connecting to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="Mortgage Rate" 
)

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        search_option = request.form["search_option"]
        if search_option == "mortgage_rate30":
            return render_template("mortgage_rate30.html")
        elif search_option == "mortgage_rate15":
            return render_template("mortgage_rate15.html")
        elif search_option == "realtime":
            response = requests.get("https://api.stlouisfed.org/fred/release?release_id=473&realtime_end=9999-12-31&api_key=66e31b592e4db5531a48c87f68841a89&file_type=json")
            if response.status_code == 200:
                realtime_data = response.json()
                return render_template("realtime_data.html", data=realtime_data)
            else:
                print(f"Failed to fetch data. Status Code: {response.status_code}")

    return render_template("index.html")

def get_mortgage_rate30(selected_date):
    query = "SELECT `Rate-30-US` FROM `Mortgage_Rate30` WHERE `Date` <= %s ORDER BY `Date` DESC LIMIT 1"
    cursor.execute(query, (selected_date,))
    mortgage_rate = cursor.fetchone()
    return mortgage_rate[0] if mortgage_rate else None

def get_mortgage_rate15(selected_date):
    query = "SELECT `Rate-15-US` FROM `Mortgage_Rate15` WHERE `Date` <= %s ORDER BY `Date` DESC LIMIT 1"
    cursor.execute(query, (selected_date,))
    mortgage_rate = cursor.fetchone()
    return mortgage_rate[0] if mortgage_rate else None


@app.route("/mortgage_rate30", methods=["POST"])
def mortgage_rate30_lookup():
    if request.method == "POST":
        year = request.form["year"]
        month = request.form["month"]
        selected_date = f"{year}-{month}-01"  # Add the day "01" for the first day of the selected month
        mortgage_rate30 = get_mortgage_rate30(selected_date)
        return render_template("mortgage_rate30.html", selected_year=year, selected_month=month, mortgage_rate30=mortgage_rate30)

@app.route("/mortgage_rate15", methods=["POST"])
def mortgage_rate15_lookup():
    if request.method == "POST":
        year = request.form["year"]
        month = request.form["month"]
        selected_date = f"{year}-{month}-01"  # Add the day "01" for the first day of the selected month
        mortgage_rate15 = get_mortgage_rate15(selected_date)
        return render_template("mortgage_rate15.html", selected_year=year, selected_month=month, mortgage_rate15=mortgage_rate15)
    
if __name__ == "__main__":
    app.run(debug=True)


