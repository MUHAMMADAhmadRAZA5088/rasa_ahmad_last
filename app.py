import requests

from flask import Flask, render_template, request

app = Flask(__name__)



@app.route("/")
def get_all_properties():
   
    BASE_ID = "appn9mV0cCoqtZEz2"
    TABLE_NAME = "tblAhTLF08BeGQ4vf"
    API_KEY = "patRY4Vyt9FQ2ZtZn.f7eaa7841e12ccab916f74790ca10f8a1ed1704721cdf846b52aa2135ae4c181"

    # URL for the Airtable API
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

    # Headers including API key
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    

@app.route("/address")
def get_property_by_address():

    BASE_ID = "appn9mV0cCoqtZEz2"
    TABLE_NAME = "tblAhTLF08BeGQ4vf"
    API_KEY = "patRY4Vyt9FQ2ZtZn.f7eaa7841e12ccab916f74790ca10f8a1ed1704721cdf846b52aa2135ae4c181"

    # URL for the Airtable API
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

    # Define your filter formula using the SEARCH() function
    search_term = '8228 Bellgave Pl'
    filter_formula = f"SEARCH('{search_term}', {{Address}})"

    # Set up the headers with your API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Create a parameters dictionary with the filter formula
    params = {
        'filterByFormula': filter_formula
    }

    # Send a GET request to retrieve records where the 'Address' field contains 'Lahore'
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data


@app.route("/id")
def get_property_by_id():

    BASE_ID = "appn9mV0cCoqtZEz2"
    TABLE_NAME = "tblAhTLF08BeGQ4vf"
    API_KEY = "patRY4Vyt9FQ2ZtZn.f7eaa7841e12ccab916f74790ca10f8a1ed1704721cdf846b52aa2135ae4c181"
    
    # Define the Airtable API endpoint URL
    record_id = 'recQrBHmKh6SFx1l3'  # Replace with the actual record ID you want to retrieve

    # URL for the Airtable API
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}/{record_id}"

    # Set up the headers with your API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Send a GET request to retrieve records where the 'Address' field contains 'Lahore'
    response = requests.get(url, headers=headers,)

    if response.status_code == 200:
        data = response.json()
        return data

if __name__ == "__main__":
        app.run(debug=True)