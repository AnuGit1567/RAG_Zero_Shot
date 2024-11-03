#import pandas as pd
import random
import numpy as np
import os
import Retrieval_Rag1
import google.generativeai as genai
import Generator_rag1
google_api_key ="your google api key"

def initiate_google_genai(key):   
    os.environ['GOOGLE_API_KEY'] = google_api_key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model_google = genai.GenerativeModel('gemini-1.5-flash')
    return model_google

if __name__ =="__main__":
    model_google= initiate_google_genai(google_api_key)
    text_embeddings = Retrieval_Rag1.Retrieval_Docs()
    index, section_texts= text_embeddings.document_to_json(model_google,"funnyagree.docx")
    
    new_details_for_lease =" **tenant name:** Smith of 2nd floor\
    **Rent Amount:** The monthly rent is $1,200.\
    **Deposit and Fees:** A security deposit of $200 is required.\
    lease duration is 2nd decemeber 2024 for 1 year, landlord name is Peanuts the King , Address is 1 King Street"
    query = new_details_for_lease  # Example query
   
    lease_generator= Generator_rag1.Generator_lease()
    response = lease_generator.generate_response(query, index, section_texts,model_google)
    print(response.text)



print("done")