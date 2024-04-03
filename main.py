from flask import Flask, render_template, request,session, jsonify, redirect, url_for
import openai
import json
from bs4 import BeautifulSoup

import requests
import spacy,json
import re,os
from datetime import datetime
from flask_session import Session
# from google_bard_api import user_msg
from google_search import google_search

# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')
# from google_bard_api import user_msg
app = Flask(__name__)

# Set your OpenAI API key
# openai.api_key = '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'
import spacy,json

# Preprocessing: Store data in a dictionary
# Load data from the JSON file
with open('bnf.json', 'r') as file:
    medicine_data = json.load(file)

# Preprocess the loaded data and store it in a dictionary
medicine_dict = {medicine["Name"]: medicine for medicine in medicine_data}
# Load English language model
nlp = spacy.load("en_core_web_sm")


intructions='''
you are a specielist doctor.
'''


# Define a function to process user queries


@app.route('/')
def index():
    return render_template('chat.html')

def rewrite(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0.5,
        "max_tokens": 2000,
        "messages": [
                    {"role": "system", "content": f"Today date is {today_date}"},
                    {"role": "user","content": f"Re write {user_message}"},
                    
        ]
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
                        {"role": "system","content": "dont repeat user query and give response in bullet points"},
                        {"role": "user","content": str(user_message).strip()},
                        {"role": "system","content": role}
            ]
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
    
    # Replace new lines with '' tags
    text = text.replace('\n', "<br>")
    
    return text



# Define a function to process user queries
def process_query(query):
    doc = nlp(query)
    print(doc.ents)
    for ent in doc.ents:
        
        medicine_name = ent.text
        if medicine_name in medicine_dict:
            return get_info(medicine_name, query)
    return "Sorry, I couldn't find information for that medicine."

# Define a function to retrieve information based on the user query type
def get_info(medicine_name, query):
    if "overdose" in query.lower():
        return medicine_dict[medicine_name]["Overdose"]
    elif "side effect" in query.lower() or "side effects" in query.lower():
        return medicine_dict[medicine_name]["Side_effects"]
    elif "caution" in query.lower() or "precaution" in query.lower() or "warning" in query.lower():
        return medicine_dict[medicine_name]["Cautions"]
    elif "unlicensed use" in query.lower() or "unlicensed" in query.lower():
        return medicine_dict[medicine_name]["Unlicensed_use"]
    else:
        return "Please specify whether you are asking about overdose, side effects, cautions, or unlicensed use."




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

    log_data = {'user_query': section}
    
    
    if session['section']=='Query Medicines Doses and warning':
        if user_message1:
            # user_message1=user_message1.lower().strip()
            
            print('calling')
            output=process_query(user_message1)#gpt(f'{user_message1}','answer query based on previous chat')
            # Log the AI response
           
            if 'Sorry' in output:
                output=gpt(f'{user_message1}','Give information')
                
            try:
                output=format_text(output.replace('\n', "<br>").replace('* **', '<strong>').replace('**', '</strong>').replace('```html','').replace('```',''))
            except:
                output=output
            return jsonify({'aiResponse': output})
        else:

            role=f"Ask user which Query Medicines he wants"
            output=gpt(f'{session["section"]}',role)
            # output='Please specify the country for which you would like to receive the latest CBDC update.'
            # Log the AI response
            
            # try:
            #     output=format_text(output)
            # except:
            #     output=output
            return jsonify({'aiResponse': output.replace('\n', "<br>").replace('* **', '<strong>').replace('**', '</strong>').replace('```html','').replace('```','')})

    
    
    if session['section']=='Query CPD Points':
        if user_message1:
            if 'doctor' in user_message1:
                print('doctor')
                output='Doctor cpd points are 70 CPD points,40 CPD points,35 CPD points,25 CPD points,15 CPD points,10 CPD points'
                
            elif 'health' in user_message1:
                print('health')
                output='Health worker cpd points are 70 CPD points,40 CPD points,35 CPD points,25 CPD points,15 CPD points,10 CPD points'
                
            elif 'nurse' in user_message1:
                print('nurse')
                output='Nurse cpd points are 70 CPD points,40 CPD points,35 CPD points,25 CPD points,15 CPD points,10 CPD points'
            return jsonify({'aiResponse': output.replace('\n', "<br>").replace('* **', '<strong>').replace('**', '</strong>').replace('```html','').replace('```','')})
        else:

            role=f"Ask user which CPD point he want to know doctor,nurse,Health worker"
            output=gpt(f'{session["section"]}',role)
            # output='Please specify the country for which you would like to receive the latest CBDC update.'
            # Log the AI response
            
            # try:
            #     output=format_text(output)
            # except:
            #     output=output
            return jsonify({'aiResponse': output.replace('\n', "<br>").replace('* **', '<strong>').replace('**', '</strong>').replace('```html','').replace('```','')})

    if session['section']=='Query Jobs':
        if user_message1:
            try:
                user_message1=user_message1.split()[0]
            except:
                user_message1=user_message1
            # URL of the jobs API
            api_url = "http://51.21.132.235:5000/nhs_data"
            
            try:
                # Make a request to the API
                response = requests.get(api_url)
                # Raise an exception if the request was unsuccessful
                response.raise_for_status()
                
                # Convert the response to JSON format
                jobs_data = response.json()
                matches = []
                # Search for the job by title
                for job in jobs_data:
                    if user_message1.lower() in job["job"].lower():
                        print(f"Job Title: {job['job']}")
                        print(f"Job URL: {job['url']}")
                        job_title = job['job']
                        job_location = job['location']
                        job_url = job['url']
                        # Add the formatted job information to the matches list
                        matches.append(f"Title: <strong>{job_title}</strong><br>Location: <strong>{job_location}</strong><br>Apply link : <a href='{job_url}'>Apply here</a><br><br>")
                            # Exit after finding the first match
                if matches:
                    output = "".join(matches)
                else:
                    output = 'No jobs found with the specified title.'
                return jsonify({'aiResponse': output.replace('\n', "<br>").replace('* **', '<strong>').replace('**', '</strong>').replace('```html','').replace('```','')})
                # print("No jobs found with the specified title.")
            
            except requests.exceptions.RequestException as e:
                print(f"Error accessing the API:")

           

        else:
            role=f"Ask user which medical job he want to search"
            output=gpt(f'{session["section"]}',role)
            # output='Please specify the country for which you would like to receive the latest CBDC update.'
            # Log the AI response
            
            try:
                output=format_text(output)
            except:
                output=output
            return jsonify({'aiResponse': output.replace('\n', "<br>").replace('* **', '<strong>').replace('**', '</strong>').replace('```html','').replace('```','')})


if __name__ == '__main__':
    
    app.secret_key = os.urandom(24)  # Use a more secure method to generate a secret key
    app.config['SESSION_TYPE'] = 'filesystem'  # Choose an appropriate session type
    Session(app)
    # app.run(debug=True,port=5000)
    app.run(host='0.0.0.0', port=5000,debug=True)










