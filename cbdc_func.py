import json
import requests
from datetime import datetime
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load JSON data
with open('cbdc.json', 'r') as file:
    data = json.load(file)

# Extract country names from the data
country_names = set(entry['country'].lower() for entry in data)

# # Define the label dictionary
# label_dict = {'Research': 0, 'Pilot': 1, 'Proof of concept': 2, 'Launched': 3, 'Cancelled': 4}

# # Load the encoder used for preprocessing
# encoder = joblib.load('encoder.pkl')

# # Load the model
# model = tf.keras.models.load_model('cbdc_model.keras')

# def preprocess_input(input_data):
#     # Preprocess user input to match the format used for training the model

#     input_feature = [
#         input_data['country'], 
#         input_data['central_bank'], 
#         input_data['digital_currency'], 
#         input_data['type_']
#     ]
#     input_feature_encoded = encoder.transform([input_feature]).toarray()
#     return input_feature_encoded

def preprocess_user_input(user_input):
    # Convert the user input to lowercase
    user_input = user_input.lower()
    
    # Define keywords related to CBDCs
    cbdc_keywords = ['cbdc', 'central bank digital currency', 'digital currency','about','want','to','know']

    for keyword in cbdc_keywords:
        if keyword in user_input:
            user_input = user_input.replace(keyword, '').strip()
    
    # Initialize variables to store extracted country and additional keywords
    country = None
    additional_keywords = []
    
    # Check for country name as complete word
    similar_countries = [country for country in country_names if user_input in country]
    if similar_countries:
        print('Similar countries found:', similar_countries)
        country=similar_countries[0]
    
    # If country is not found, check for country name as substring
    if country is None:
        for country_name in country_names:
            
            if country_name in user_input:
                country = country_name
                break
    
    
    
    return country

def format_entry_details_html(entry_details):
    # Format the entry details into HTML format
    formatted_details = f"<p><strong>Status:</strong> {entry_details['CBCD_status']} ({entry_details['type_']} CBDC)</p>"
    formatted_details += f"<p><strong>Country:</strong> {entry_details['country']}</p>"
    formatted_details += f"<p><strong>Central Bank:</strong> {entry_details['central_bank']}</p>"
    formatted_details += f"<p><strong>Digital Currency:</strong> {entry_details['digital_currency']}</p>"
    formatted_details += f"<p><strong>Description:</strong> {entry_details['description']}</p>"
    formatted_details += f"<p><strong>More Info:</strong> <a href=\"{entry_details['url']}\">{entry_details['url']}</a></p>"
    return formatted_details

def query_entry_by_country(input_country):
    # Find the corresponding entry in the data
    country_entry = next((entry for entry in data if entry['country'].lower() == input_country), None)

    if country_entry:
        return country_entry
    else:
        return "Country not found"

def get_cbdc_news(url):
    # Make a GET request to fetch the data
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON
        parsed_data = response.json()

        # Extract relevant information
        content = parsed_data['content']
        news_info = []

        for item in content:
            title = item['abstract']
            created_timestamp = item['created'] / 1000  # Convert milliseconds to seconds
            created_date = datetime.utcfromtimestamp(created_timestamp).strftime('%Y-%m-%d')  # Format created date
            news_info.append({'Update': title, 'Date': created_date})

        # Format news into HTML
        news_html = "<ul>"
        for news in news_info:
            news_html += f"<li>{news['Update']} - {news['Date']}</li>"
        news_html += "</ul>"

        return news_html

    else:
        return "<p>No CBDC updates found</p>"

def get_country_name(country):
    print('country:',country)
    cbdc_data = data

    country_data = []
    for entry in cbdc_data:
        if ' ' in country :
        
            # Split the country input and get the last word
            country_parts = country.split()
            last_word = country_parts[-1].lower().strip()
            # print('last_word',last_word)
            # Check if the last word matches with the last word in the entry's country or digital currency
            if last_word in entry.get('country').lower() or last_word == entry.get('country').lower() or last_word in entry.get('digital_currency').lower():
                print('find')
                tag = entry.get('country').replace('england', 'united_kingdom').replace('uk', 'united_kingdom').lower().replace(' ', '_')
                currency = entry.get('digital_currency').lower().replace(' ', '_')
                url = f'https://cbdctracker.org/api/news?page=0&size=5&tags={tag}-{currency}'
                cbdc_news_html = get_cbdc_news(url)
            
                return cbdc_news_html
        else:
            #print(country.lower().strip() , entry.get('country').lower())
            if country.lower().strip() in entry.get('country').lower() or country.lower().strip() in  entry.get('digital_currency').lower():
                print('find country')
                tag=entry.get('country').replace('england','united_kingdom').replace('uk','united_kingdom').lower().replace(' ','_')
                currency=entry.get('digital_currency').lower().replace(' ','_')
                url=f'https://cbdctracker.org/api/news?page=0&size=5&tags={tag}-{currency}'
                cbdc_news_html=get_cbdc_news(url)
                #print(entry)

                
                return cbdc_news_html
            else:
                cbdc_news_html='cbdc updates not found'

        
    return "<p>CBDC updates: No updates found</p>", "<p>CBDC data: Country data not available</p>"


# user_input = input("what you want to know about cbdc")
def user_cbdc_input(user_input):
    # Preprocess the user input country
    country = preprocess_user_input(user_input)

    # Query the entry by country
    country_entry = query_entry_by_country(country)

    if country_entry != "Country not found":
        # Format the entry details into HTML
        formatted_details_html = format_entry_details_html(country_entry)
        print('formatted_details_html',formatted_details_html)
        # Get CBDC news for the country
        cbdc_news_html = get_country_name(country)
        print('cbdc_news_html',cbdc_news_html)
        # Preprocess the user input and make prediction using the model
        # input_data = {'country': country, 'central_bank': '', 'digital_currency': '', 'type_': ''}
        # preprocessed_input = preprocess_input(input_data)
        # prediction = model.predict(preprocessed_input)
        # predicted_status = list(label_dict.keys())[np.argmax(prediction)]

        print("Details for", user_input + ":")
        # print("Predicted CBDC Status:", predicted_status)
        result=f"<p><strong>Here is the latest update on the Central Bank Digital Currency (CBDC) in {country}</strong></p> \n {cbdc_news_html} \n {formatted_details_html}"
        # print(result)
        return result
    # else:
    #     print("Country not found")
# user_cbdc_input('united states of america')
