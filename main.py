from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Enter your MySQL password here
    database="Mortgage Rate"  # Enclose the database name in backticks
)

cursor = db.cursor()

def get_mortgage_rate(selected_date):
    query = "SELECT `Rate-30-US` FROM `Mortgage_Rate` WHERE `Date` <= %s ORDER BY `Date` DESC LIMIT 1"
    cursor.execute(query, (selected_date,))
    mortgage_rate = cursor.fetchone()
    return mortgage_rate[0] if mortgage_rate else None

@app.route("/", methods=["GET", "POST"])
def mortgage_rate_lookup():
    if request.method == "POST":
        year = request.form["year"]
        month = request.form["month"]
        selected_date = f"{year}-{month}-01"  # Add the day "01" for the first day of the selected month
        mortgage_rate = get_mortgage_rate(selected_date)
        return render_template("index.html", selected_year=year, selected_month=month, mortgage_rate=mortgage_rate)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


