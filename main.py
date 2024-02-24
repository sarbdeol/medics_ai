from flask import Flask, render_template, request,session, jsonify, redirect, url_for
import openai
import json
from bs4 import BeautifulSoup
from train import check_query
import requests
import yfinance as yf
from data_get import get_forex
import re,os
from datetime import datetime
from flask_session import Session
from google_bard_api import user_msg
from google_search import google_search
from data import check_sentance
# from place_project_bid import sample_place_project_bid




# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')
# from google_bard_api import user_msg
app = Flask(__name__)
API_URL = "http://13.49.0.68:5000/cbdctracker_scraper"
# Set your OpenAI API key
openai.api_key = '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'
json_file_path = "firms_data.json"
cbdc_file_path='cbdc.json'
# Open the JSON file for reading
with open(json_file_path, "r") as file:
    # Read the contents of the file
    firms_data = json.load(file)
# Open the JSON file for reading
with open(cbdc_file_path, "r") as file:
    # Read the contents of the file
    cbdc_data = json.load(file)

currency_codes = [
        'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN',
        'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL',
        'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY',
        'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP',
        'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP',
        'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
        'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD',
        'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD',
        'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA',
        'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR',
        'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN',
        'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF',
        'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SPL',
        'SRD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP',
        'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS',
        'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER',
        'ZAR', 'ZMW', 'ZWD'
    ]

intructions='''ASK RUEDEX specializes in providing real-time financial updates, focusing on CBDCs (Central Bank Digital Currencies), FCA (Financial Conduct Authority) regulated firms, forex (foreign exchange) rates, and cryptocurrency rates. It delivers factual information, avoiding speculation and financial advice. Below are the capabilities and instructions for using ASK RUEDEX effectively:

 **CBDC Updates:** To get the latest information on Central Bank Digital Currencies, please provide the specific country you are interested in. Example query: "What's the latest update on the CBDC in [Country]?"

 **FCA Firms:** For information on firms regulated by the Financial Conduct Authority, mention the firm's name. Example query: "Is [Firm Name] regulated by the FCA?"

 **Forex Rates:** ASK RUEDEX can dynamically retrieve live forex exchange rates. To get the most accurate rate, specify the from and to currencies, the countries involved, and the amount you wish to convert. Example query: "What is the exchange rate from [From Currency] to [To Currency] for [Amount] from [From Country] to [To Country]?"

 **Crypto Rates:** For the latest cryptocurrency rates, provide the specific crypto asset you are interested in. Example query: "What's the current rate for [Crypto Asset]?"

To ensure ASK RUEDEX can retrieve this information, it has been enabled with internet access capabilities. When asking for forex rates, ASK RUEDEX will dynamically construct a URL based on the provided details to fetch live rates from reliable sources.

**Note:** ASK RUEDEX clarifies when data is unavailable or cannot provide updated information, ensuring users have clear expectations.

**Usage Instructions:**
- Be specific with your queries to ensure accurate retrieval of information.
- For forex rates, the dynamic URL construction format is: `https://www.monito.com/en/compare/transfer/{from_country}/{to_country}/{from_currency}/{to_currency}/{amount}`. This format is used internally to fetch the latest rates.
- Ensure to provide all necessary details for your query as per the examples given.

Remember, ASK RUEDEX is here to provide real-time financial information at your fingertips!
'''

# Function to get stock information using yfinance
def get_stock_info(symbol):
    stock_data = yf.Ticker(symbol)
    info = stock_data.info
    return info
# Function to get cryptocurrency prices
def get_bitcoin_price(coin):
    url = f"https://coinmarketcap.com/currencies/{coin}/"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        price_element = soup.find("span", class_="sc-f70bb44c-0 jxpCgO base-text")
        if price_element:
            coin_price = price_element.get_text(strip=True)
            print(coin_price)
            return coin_price
        else:
            print("Bitcoin price not found on the webpage.")
            return None
    else:
        print("Failed to fetch webpage data.")
        return None



@app.route('/')
def index():
    return render_template('chat.html')
@app.route('/exchanges/<exchange_name>')
def exchange(exchange_name):
    url = f"https://api.coingecko.com/api/v3/exchanges/{exchange_name}"

    payload = {}
    headers = {
        'Cookie': '__cf_bm=75cxtdvhpMZ1Z.3km5_LJ71c9hKGkZlm1RYwjDcbaA8-1708767959-1.0-AStyAoTVjVrmKf+tDkVVeRC+OlS5v65iPxatKADUjdZD3+anvDaExEuqelyRBIwV/HBcwnI6R2YP/2I3hZe2T4c='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    binance_data = response.json()
    print(binance_data)
    return render_template('table.html', binance_data=binance_data)
def rewrite(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0.5,
        "max_tokens": 2000,
        "messages": [
                    {"role": "system", "content": f"Today date is {today_date}"},
                    {"role": "user","content": f"Re write {user_message}"},
                    {"role": "system","content": "if there is url under the message then  make it under <a> tag</a> and bold black color and also bold text which is after ###  (eg :### Introduction to CBDCs\n\n)"},
                    {"role": "system","content": "make this type of text  -** ** under <a> text </a>"}]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }
    response = requests.post(url, headers=headers, data=payload)
    output = json.loads(response.text)
    print(output)
    try:
        output=output['choices'][0]['message']['content']
    except:
        # output=user_msg(user_message)
        output='Something Went Wrong\n Try to Refresh Page'
    return output
def gpt(user_message,role):
    print(user_message)
    qauta=False
    if qauta:
        
        output=google_search(user_message)
        output=rewrite(output)
        
    else:
        # print(role)
        # If the user is not asking for cryptocurrency price, use OpenAI API
        url = "https://api.openai.com/v1/chat/completions"
        payload = json.dumps({
            "model": "gpt-3.5-turbo-0125",#"gpt-4-0125-preview",
            "temperature": 0.5,
            "max_tokens": 4096,
            "messages": [
                        {"role": "system", "content": f"intructions :{intructions}"},
                        {"role": "system", "content": f"Today date is {today_date}"},
                        {"role": "user","content": user_message},
                        {"role": "system","content": "if there is url under the message then  make it under <a href='url'> url </a> and bold black color and also bold text which is after ###  (eg :### Introduction to CBDCs\n\n)"},
                        {"role": "system","content": "dont repeat user query"},
                        {"role": "system","content": role}]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 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'
        }
        response = requests.post(url, headers=headers, data=payload)
        output = json.loads(response.text)
        print(output)
        try:
            output=output['choices'][0]['message']['content']
        except:
            # output=user_msg(user_message)
            output='Something Went Wrong\n Try to Refresh Page'
    return output


import re

def format_text(text):
    # Bold text within double asterisks
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Underline text within double underscores
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
    
    # Replace new lines with <br> tags
    text = text.replace('\n', '<br>')
    
    return text
def get_country_name(country):
    # Function to get entries based on country
    with open(cbdc_file_path, "r") as file:
        # Read the contents of the file
        cbdc_data = json.load(file)
    country_data = []
    for entry in cbdc_data:
        if entry.get('country').lower() == country.lower():
            print('find country')
            print(entry)
            country_data.append(entry)
        else:
            country_data.append('country data not available yet')
    return country_data

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    global intructions,currency_codes
    section=request.get_json().get('section')
    # Save section in session
    if section:
        session['section'] = section
    print('session',session['section'])
    user_message1 = request.get_json().get('userMessage')
    print(user_message1)
    if user_message1:
        # Log the user query
        user_message=check_sentance(user_message1)
        print(user_message)
        label_gpe=user_message.get('GPE')
        label_org=user_message.get('ORG')
        log_data = {'user_query': user_message1}
       
    else:
        label_gpe=''
        label_org=''
        user_message1=''
        log_data = {'user_query': section}
    
    


    ############# cbdc sections
    if label_gpe:
        cbdc_data=get_country_name(label_gpe)
        role=f"Here is CBDCs country data {cbdc_data}, Analyze the data and share as updates ."
        output=gpt(f'{user_message1}',role)
        # Log the AI response
        log_data['ai_response'] = output
        with open('user_queries_log.json', 'a') as log_file:
            json.dump(log_data, log_file)
            log_file.write('\n')
        try:
            output=format_text(output)
        except:
            output=output
        return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})
    elif session['section']=='Query Central Bank Digital Currencies' or label_org and any(keyword in user_message1.lower() for keyword in ['cbdc','banks','bank','central','digital','Query Central Bank Digital Currencies']):
            role=f"Ask user which cbdc country data he wants"
            output=gpt(f'{user_message1}',role)
            # Log the AI response
            log_data['ai_response'] = output
            with open('user_queries_log.json', 'a') as log_file:
                json.dump(log_data, log_file)
                log_file.write('\n')
            try:
                output=format_text(output)
            except:
                output=output
            return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})
    
    
    
    
    #### FCA 
    elif session['section']=='Query FCA registered digital asset companies' or any(keyword in user_message1.lower() for keyword in ['Ltd','LTD','Limited','firm','company','fca','assets']):
        role=f"Ask user to provide full Firm name for checking if its registered or not in FCA registered digital asset companies ,If user provide name then check here is data {firms_data}"
        output=gpt(f'{user_message1}',role)
        with open('user_queries_log.json', 'a') as log_file:
            log_data['ai_response'] = output
            log_file.write('\n')
        try:
            output=format_text(output)
        except:
            output=output
        return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})
    


    # FOREX
    

    elif session['section']=='Ask for live forex rates' or any(keyword in user_message1.lower() for keyword in ['forex','usd','inr','eur','gbp']) or any(keyword2 == user_message1.upper() for keyword2 in currency_codes):
        print('forex')
        role="ask user for one time from/to currency and add parameter to this url  https://www.monito.com/en/compare/transfer/{from_country}/{to_country}/{from_currency}/{to_currency}/1 amount always 1 and return url and no confirm again (usa will be us) and use same correncies country codes for to and from country"
        output=gpt(f'{user_message1}',role)
        with open('user_queries_log.json', 'a') as log_file:
            log_data['ai_response'] = output
            json.dump(log_data, log_file)
            log_file.write('\n')
        if 'https://www.monito.com' in output:
        

            # Given text containing the UR
            # Define a regex pattern to match URLs
            url_pattern = r'https?://(?:www\.)?monito\.com/\S+'

            # Find URLs in the text using regex
            urls = re.findall(url_pattern, output)

            # Check if any URLs were found
            if urls:
                # Assuming there is only one URL in the text, extract the first one
                extracted_url = urls[0].replace('"','').replace(')**','').replace('**','').replace(')','').replace('%20','')
                
            else:
                print("No URL found in the text.")
            try:
                extracted_url=extracted_url.split("'")[0]
            except:
                extracted_url=extracted_url.split("]")[0]
            else:
                extracted_url=extracted_url
            print(extracted_url)
            output =get_forex(extracted_url)
            
            # output=user_msg(output,'')
            output=gpt(f'{output} \n\n\n provide info in well format ','if there is any url then attach it in anchor tag ')
            try:
                output=format_text(output)
            except:
                output=output
            with open('user_queries_log.json', 'a') as log_file:
                log_data['ai_response'] = output
                json.dump(log_data, log_file)
                log_file.write('\n')
            return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>').replace('###', '-->')})
    
    
    elif session['section'] =='Ask who is selling crypto asset as what rate' or any(keyword in user_message1.lower() for keyword in ['crypto','bitcoin','crypto asset','current rate','current price']):
        role="Ask user to provide crypto exchange name \n\n eg : (Binance)"
        # Load exchange data from JSON file
        if user_message1:
            with open('exchange_names.json', 'r') as f:
                exchange_data = json.load(f)
            matched_exchange = None
            for exchange in exchange_data:
                if  user_message1.lower() in exchange["name"].lower():
                    matched_exchange = exchange
                    break

            # If a matching exchange is found, use its ID to get the table
            if matched_exchange:
                exchange_id = matched_exchange["id"]
            # Check if "binance" is in the user's message
            
                # Provide a clickable link to the Binance exchange page
                output = f'<a href="{url_for("exchange", exchange_name=exchange_id)}">Sure, here is the link to view {exchange["name"]}</a>'
                return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})
            else:
                output='No exchange found in our records'
        else:
            output=gpt(section,role)
        return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})
    elif user_message1=='ruedex':
        print(intructions)
        try:
            intructions=format_text(intructions)
        except:
            intructions=intructions
        return jsonify({'aiResponse': intructions.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})
    
    
    else:
        with open('user_queries_log.json', 'r') as log_file1:
            # Parse the JSON data
            lines = log_file1.readlines()

            # Parse the last line as JSON
            last_output = json.loads(lines[-1]) # Assuming the data is stored as a list

            # Now you can work with the last row
            print(last_output)
        output=gpt(f'{user_message1}',f'this is answer of your last query {last_output}')
        log_data['ai_response'] = output
        with open('user_queries_log.json', 'a') as log_file:
            
            json.dump(log_data, log_file)
            log_file.write('\n')
        return jsonify({'aiResponse': output.replace('\n', '<br>').replace('* **', '<strong>').replace('**', '</strong>')})



if __name__ == '__main__':
    
    app.secret_key = os.urandom(24)  # Use a more secure method to generate a secret key
    app.config['SESSION_TYPE'] = 'filesystem'  # Choose an appropriate session type
    Session(app)
    app.run(debug=True)
