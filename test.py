import pdfplumber
import re
import pandas as pd
import requests
import json,time

# Replace with the actual path to your PDF file
pdf_path = "invoices.pdf" 

# Initialize a list to store product information
product_info = []
invoice_info = []
total_products_info = []
def rewrite(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0.5,
        "max_tokens": 2000,

        "messages": [
            # {
            #     "role": "user",
            #     "content": "company Address, Delivery Address, Billing Address in one line only, no need in sub JSON."
            # },
                    {
                "role": "user",
                "content":"i want only these fields ,{Total Products: "",Total Discount:""}\n "f"I want mention keys and values in JSON from the below text only not other data if not then stay empty: \n {user_message}",
            }
            # {
            #     "role": "user",
            #     "content": f"INVOICE :DATE\tINVOICE NO\tDelivery Address\tBilling Address\t\tInvoice Date\tOrder Reference\tPayment Method\tOrder date\t\tShipping Costs\tTotal (Tax excl.)\tTotal Tax\tTotal \n I want mention keys and values in JSON from the below text only not other data: \n {user_message}"
            # }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
    }
    response = requests.post(url, headers=headers, data=payload)
    output = json.loads(response.text)
    # print(output)
    return output['choices'][0]['message']['content']

# Open the PDF and extract the data
with pdfplumber.open(pdf_path) as pdf:
    pages = pdf.pages# Adjust as needed
    for i, page in enumerate(pages):
        text = page.extract_text()
        # print(text)
        json_data = rewrite(text)
        
        data = json.loads(json_data)
        
        total_products_info.append(data)
      
        print(data)
              
        # print(total_products_info)
        print(f"Processing page: {i+1}")
        time.sleep(1)
# print(invoice_info)
# Convert invoice information to DataFrame for sheet 1
# df_invoice = pd.DataFrame(invoice_info)
# print(total_products_info)
# Convert total products information to DataFrame for sheet 2
df_total_products = pd.DataFrame(total_products_info)

# Define the Excel writer and the output path
excel_path = 'output2.xlsx'
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    # Write invoice DataFrame to sheet 1
    # df_invoice.to_excel(writer, sheet_name='shhet1', index=False)
    
    # Write total products DataFrame to sheet 2
    df_total_products.to_excel(writer, sheet_name='sheet 2', index=False)

print(f'Data extracted and written to {excel_path}')