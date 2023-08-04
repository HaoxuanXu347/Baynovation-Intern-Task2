from flask import Flask, render_template, request, redirect
import mysql.connector
import requests

app = Flask(__name__)

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="Mortgage Rate" 
)

cursor = db.cursor()

@app.route("/")
def home():
    if request.method == "POST":
            response  = requests.get("https://api.stlouisfed.org/fred/release?release_id=473&realtime_end=9999-12-31&api_key=66e31b592e4db5531a48c87f68841a89&file_type=json")
            response1 = requests.get("https://api.stlouisfed.org/fred/series?series_id=OBMMIVA30YF&realtime_end=9999-12-31&api_key=66e31b592e4db5531a48c87f68841a89&file_type=json")
            response2 = requests.get("https://api.stlouisfed.org/fred/series?series_id=OBMMIFHA30YF&realtime_end=9999-12-31&api_key=66e31b592e4db5531a48c87f68841a89&file_type=json")
            response3 = requests.get("https://api.stlouisfed.org/fred/series?series_id=MORTGAGE30US&realtime_end=9999-12-31&api_key=66e31b592e4db5531a48c87f68841a89&file_type=json")
            response4 = requests.get("https://api.stlouisfed.org/fred/series?series_id=MORTGAGE15US&realtime_end=9999-12-31&api_key=66e31b592e4db5531a48c87f68841a89&file_type=json")
            if response.status_code == 200 and response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200 and response4.status_code == 200:
                realtime_data  = response.json()
                realtime_data1 = response1.json()
                realtime_data2 = response2.json()
                realtime_data3 = response3.json()
                realtime_data4 = response4.json()

                return render_template("realtime_data.html", data=realtime_data, data1=realtime_data1, 
                                    data2=realtime_data2, data3=realtime_data3, data4=realtime_data4)
        
            
    return render_template("index.html")


#-------------------------Zillow Current Mortgage Rate-----------------------
@app.route('/Zillow_CurrentRate', methods=["GET", "POST"])
def zillow_rates():
    if request.method == 'POST':
        state_abbreviation = request.form['stateAbbreviation']
        property_value = request.form['propertyValue']
        loan_amount = request.form['loanAmount']

        api_url = f"https://mortgageapi.zillow.com/getCurrentRates?partnerId=RD-QVHNTHG&queries.1.propertyBucket.location.stateAbbreviation={state_abbreviation}&queries.1.propertyBucket.propertyValue={property_value}&queries.1.propertyBucket.loanAmount={loan_amount}"

        response = requests.get(api_url)
        if response.status_code == 200:
            zillow_data = response.json()
            return render_template("Zillow_CurrentRate.html", zillow_data=zillow_data)
        else:
            error_message = f"Failed to fetch data from the API. Status Code: {response.status_code}, Response Content: {response.text}"
            return error_message

    return render_template("Zillow_CurrentRate.html")

#-------------------------30-Year Mortgage Rates-----------------------
@app.route("/mortgage_rate30", methods=["POST"])
def get_mortgage_rate30():
    year = request.form["year"]
    month = request.form["month"]
    selected_date = f"{year}-{month}-01"  # Add the day "01" for the first day of the selected month
    query = "SELECT `Rate-30-US` FROM `Mortgage_Rate30` WHERE `Date` <= %s ORDER BY `Date` DESC LIMIT 1"
    cursor.execute(query, (selected_date,))
    mortgage_rate30 = cursor.fetchone()
    return render_template("mortgage_rate30.html", selected_year=year, selected_month=month, mortgage_rate30=mortgage_rate30)

@app.route("/mortgage_rate30")
def mortgage_rate30_lookup():
    return render_template("mortgage_rate30.html")

#-------------------------15-Year Mortgage Rates-----------------------
@app.route("/mortgage_rate15", methods=["POST"])
def get_mortgage_rate15(selected_date):
    year = request.form["year"]
    month = request.form["month"]
    selected_date = f"{year}-{month}-01"  # Add the day "01" for the first day of the selected month
    query = "SELECT `Rate-15-US` FROM `Mortgage_Rate15` WHERE `Date` <= %s ORDER BY `Date` DESC LIMIT 1"
    cursor.execute(query, (selected_date,))
    mortgage_rate15 = cursor.fetchone()
    return render_template("mortgage_rate15.html", selected_year=year, selected_month=month, mortgage_rate15=mortgage_rate15)

@app.route("/mortgage_rate15")
def mortgage_rate15_lookup():
   return render_template("mortgage_rate15.html")
    
if __name__ == "__main__":
    app.run(debug=True)


