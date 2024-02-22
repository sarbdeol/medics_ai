import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_cryptocurrency_name(user_query):
    # Tokenization
    tokens = word_tokenize(user_query)

    # Part-of-Speech Tagging
    pos_tags = pos_tag(tokens)

    # Extract cryptocurrency names from the user query based on POS tags
    cryptocurrency_names = []
    for word, tag in pos_tags:
        if tag.startswith('NN') or 'NNP' in tag:  # Select nouns and proper nouns as cryptocurrency names
            cryptocurrency_names.append(word.lower())  # Convert to lowercase for consistency
    
    # Remove "price" if it exists in the list
    cryptocurrency_names = [name for name in cryptocurrency_names if name != 'price' or name != 'rates']
    
    return cryptocurrency_names

# # Sample user query
# user_query = "I want selling rates of bitcoin "

# # Extract cryptocurrency names from the user query
# cryptocurrencies = extract_cryptocurrency_name(user_query)

# # Print extracted cryptocurrency names
# print("Extracted Cryptocurrencies:", cryptocurrencies)


def check_query(user_query):
# Sample user query
    # user_query = "What is the price of bitcoin?"

    # Extract cryptocurrency names from the user query
    cryptocurrencies = extract_cryptocurrency_name(user_query.replace('rate',''))
   
    # Print extracted cryptocurrency names
    print("Extracted Cryptocurrencies:", cryptocurrencies[0])
    return cryptocurrencies[0]


# check_query(user_query)