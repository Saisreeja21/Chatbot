from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://v6.exchangerate-api.com/v6/2eeef284d93c4cb0f6ca395a/latest/USD"
    response = requests.get(url)
    data = response.json()

    if source in data["conversion_rates"] and target in data["conversion_rates"]:
        source_to_usd_rate = data["conversion_rates"][source]
        target_to_usd_rate = data["conversion_rates"][target]

        # Calculate the conversion rate from source to target
        return target_to_usd_rate / source_to_usd_rate
    else:
        raise ValueError("Conversion rate not available for the specified currencies: {} to {}".format(source, target))


if __name__ == "__main__":
    app.run(debug=True)
