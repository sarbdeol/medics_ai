"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
from datetime import datetime
import json
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
# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')
import google.generativeai as genai
intructions='''ASK RUDEX specializes in providing real-time financial updates, focusing on CBDCs (Central Bank Digital Currencies), FCA (Financial Conduct Authority) regulated firms, forex (foreign exchange) rates, and cryptocurrency rates. It delivers factual information, avoiding speculation and financial advice. Below are the capabilities and instructions for using ASK RUDEX effectively:

 **CBDC Updates:** To get the latest information on Central Bank Digital Currencies, please provide the specific country you are interested in. Example query: "What's the latest update on the CBDC in [Country]?"

 **FCA Firms:** For information on firms regulated by the Financial Conduct Authority, mention the firm's name. Example query: "Is [Firm Name] regulated by the FCA?"

 **Forex Rates:** ASK RUDEX can dynamically retrieve live forex exchange rates. To get the most accurate rate, specify the from and to currencies, the countries involved, and the amount you wish to convert. Example query: "What is the exchange rate from [From Currency] to [To Currency] for [Amount] from [From Country] to [To Country]?"

 **Crypto Rates:** For the latest cryptocurrency rates, provide the specific crypto asset you are interested in. Example query: "What's the current rate for [Crypto Asset]?"

To ensure ASK RUDEX can retrieve this information, it has been enabled with internet access capabilities. When asking for forex rates, ASK RUDEX will dynamically construct a URL based on the provided details to fetch live rates from reliable sources.

**Note:** ASK RUDEX clarifies when data is unavailable or cannot provide updated information, ensuring users have clear expectations.

**Usage Instructions:**
- Be specific with your queries to ensure accurate retrieval of information.
- For forex rates, the dynamic URL construction format is: `https://www.monito.com/en/compare/transfer/{from_country}/{to_country}/{from_currency}/{to_currency}/{amount}`. This format is used internally to fetch the latest rates.
- Ensure to provide all necessary details for your query as per the examples given.

Remember, ASK RUDEX is here to provide real-time financial information at your fingertips!
'''
genai.configure(api_key="AIzaSyDQhNTTLDd8QNuGJIvCGjGq2CFA0NSSTFQ")
def user_msg(user_msg):
    print('google api')
    # print(user_msg)
    # Set up the model
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    
    convo = model.start_chat(history=[
  {"role": "user",
  "parts": [f"{user_msg}"]},
  {
    "role": "model",
    "parts": ["Re Write the message if there is information data"]
  },
  {"role": "user",
  "parts": [f"{user_msg}"]},
  {
    "role": "model",
    "parts": ["**CBDC: New In PDF**\n\n* **Bank for International Settlements (BIS): Central Bank Digital Currencies: An Updated Assessment**\nhttps://www.bis.org/publ/othp33.pdf\n\n* **International Monetary Fund (IMF): Central Bank Digital Currencies: A Survey of the Literature**\nhttps://www.imf.org/en/Publications/WP/Issues/2022/02/16/Central-Bank-Digital-Currencies-A-Survey-of-the-Literature-517965\n\n* **World Bank: Digital Currencies: A New Frontier for Central Banks**\nhttps://documents1.worldbank.org/curated/en/938221633133971482/pdf/Digital-Currencies-A-New-Frontier-for-Central-Banks.pdf\n\n* **Bank of England: Central Bank Digital Currency: Opportunities and Challenges**\nhttps://www.bankofengland.co.uk/-/media/boe/files/speech/2022/central-bank-digital-currency-opportunities-and-challenges.pdf\n\n* **Federal Reserve: Money and Payments: The U.S. Dollar in the Age of Digital Transformation**\nhttps://www.federalreserve.gov/publications/money-and-payments/money-and-payments-20220119.htm\n\n* **European Central Bank: Report on a Digital Euro**\nhttps://www.ecb.europa.eu/pub/pdf/other/ecb.repdigitaEURO21102023~8381a8b516.en.pdf\n\n* **Bank of Canada: Project Jasper: Exploring a Retail Central Bank Digital Currency in Canada**\nhttps://www.bankofcanada.ca/2022/04/project-jasper-exploring-retail-central-bank-digital-currency-canada/\n\n* **Reserve Bank of Australia: CBDC Pilot Report: Exploring the Use of a Central Bank Digital Currency in Australia**\nhttps://www.rba.gov.au/publications/rdp/2023/2023-01.html\n\n* **People's Bank of China: White Paper on Digital Currency/Electronic Payment**\nhttp://www.pbc.gov.cn/en/goutongjiaoliu/113456/113479/index.html\n\n* **Central Bank of Nigeria: eNaira: A New Digital Currency for Nigeria**\nhttps://www.cbn.gov.ng/Out/2021/CCD/eNaira%20-%20A%20New%20Digital%20Currency%20for%20Nigeria.pdf\n\nThese PDF reports provide a comprehensive overview of the latest developments, challenges, and opportunities related to central bank digital currencies (CBDCs). They cover topics such as the motivations for issuing CBDCs, the different design choices and technologies involved, the potential benefits and risks of CBDCs, and the implications for monetary policy, financial stability, and cross-border payments."]
  },
  {"role": "user",
  "parts": [f"{user_msg}"]},
  {"role": "model",
  "parts": ["ASK RUDEX specializes in real-time financial updates: CBDCs (Central Bank Digital Currencies), FCA firms, forex, and crypto rates. It focuses on delivering factual information, avoiding speculation and advice. For forex rates, ASK RUDEX dynamically constructs a URL (https://www.monito.com/en/compare/transfer/{from_country}/{to_country}/{from_currency}/{to_currency}/{amount}) based on user queries to provide live exchange rates. It prompts users for specific details (firm name for FCA queries, country for CBDC updates, and crypto asset for rates) and uses resources like CoinMarketCap for crypto rates, ensuring accuracy and timeliness. ASK RUDEX clarifies when data is unavailable or cannot provide updated information."]},
  {"role": "user",
  "parts": [f"forex price"]},
  {"role": "model",
  "parts": ["if user asks for forex price then ask user for from to currency and you will use this website to get price https://www.monito.com/en/compare/transfer/gb/in/inr/gbp/1 and use country (eg :gb,in ) in code using currency provide my user"]},
  {"role": "user",
  "parts": [f"firm data"]},
  {"role": "model", 
  "parts": [f"Here is firm data {firms_data} give answer to user query which he wants to know \n dont share same data which is in json format just give him answer in appropriate way.\n if firm not found then answer its not registered"]},
  {"role": "user",
  "parts": [f" CBDCs (Central Bank Digital Currencies)"]},
  {"role":"model",
  "parts":[f"Here is CBDCs (Central Bank Digital Currencies) country wise data {cbdc_data},Ask user which cbdc country related info he wants, Give user Anser after Analyze the data.Give answer in your way dont send json format just share as information ."]},
  {"role": "user",
  "parts": [f"query"]},
  {"role": "model", 
  "parts": [f"{intructions}"]},
  {"role": "user",
  "parts": [f"today date"]},
  {"role": "model", 
  "parts": [f"Today date is {today_date}"]},
  {"role": "user",
  "parts": [f"for content share"]},
  {"role": "model",
  "parts": ["if there is url under the message then  make it under <a href='URL'> text </a> and bold black color and also bold text which is after ###  (eg :### Introduction to CBDCs\n\n)"]},
  {"role": "user",
  "parts": [f"for content share in response"]},
  {"role": "model",
  "parts": ["make every link under <a href='URL'> text </a> mostly share in html so it will show perfect in web page and also make bold tag like  **text:** i want int <strong>text</strong> "]},
  {
      "role":"user",
      "parts":["if text like [Bank for International Settlements: Central Bank Digital Currencies](https://www.bis.org/cbdc/) then make it like this <a href='https://www.bis.org/cbdc/'>Bank for International Settlements: Central Bank Digital Currencies<a/> apply all related to this type text and  **text:** i want int <strong>text</strong>"]
  },
  {
      "role":"model",
      "parts":["[Bank for International Settlements: Central Bank Digital Currencies](https://www.bis.org/cbdc/) then make it like this <a href='https://www.bis.org/cbdc/'>Bank for International Settlements: Central Bank Digital Currencies<a/> apply all related to this type text"]
  }

])
    convo.send_message(user_msg)
    
    print(convo.last.text)
    return convo.last.text
    

# user_msg('what is stock price of acc today')