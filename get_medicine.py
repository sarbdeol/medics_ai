import spacy,json

# Preprocessing: Store data in a dictionary
# Load data from the JSON file
with open('bnf.json', 'r') as file:
    medicine_data = json.load(file)

# Preprocess the loaded data and store it in a dictionary
medicine_dict = {medicine["Name"]: medicine for medicine in medicine_data}
# Load English language model
nlp = spacy.load("en_core_web_sm")

# Define a function to process user queries
def process_query(query):
    
    doc = nlp(query)

    for ent in doc.ents:
        print(ent.text)
        medicine_name = ent.text
        if medicine_name in medicine_dict:
            data=get_info(medicine_name, query)
            print(data)
            return data
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

