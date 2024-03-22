import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import difflib
# Load the saved model
model = tf.keras.models.load_model("tensor_models/firms/firm_registration_model.keras")

# Load the word index from the tokenizer
with open('tensor_models/firms/word_index.json', 'r') as f:
    word_index = json.load(f)

# Load the firm data
with open('tensor_models/firms/firms_data.json', 'r') as f:
    firms_data = json.load(f)

# Function to check if a firm is registered and return registration status with date
def check_registration(firm_name):
    # Tokenize the input
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.word_index = word_index
    query_seq = tokenizer.texts_to_sequences([firm_name])
    query_padded = pad_sequences(query_seq, maxlen=10, padding='post')

    # Make prediction
    prediction = model.predict(query_padded)

    # Threshold for classification
    threshold = 0.5

    # Determine the registration status based on the prediction
    if prediction[0][0] >= threshold:
        # Find the closest matching firm name
        matches = difflib.get_close_matches(firm_name.lower(), [entry["Firm Name"].lower() for entry in firms_data], n=1, cutoff=0.6)
        if matches:
            # Find the firm data
            for entry in firms_data:
                if entry["Firm Name"].lower() == matches[0]:
                    
                    return f'{entry["Firm Name"]} is a registered firm with the Financial Conduct Authority. It was registered on {entry["Date"]}'
        else:
            return "Not Found", None
    else:
        # Check for partial matches
        for entry in firms_data:
            if firm_name.lower() in entry["Firm Name"].lower():
                return f'{entry["Firm Name"]} is a registered firm with the Financial Conduct Authority. It was registered on {entry["Date"]}'

    return "Not Found", None