import docx
from docx import Document
import faiss
from sentence_transformers import SentenceTransformer
import random
import numpy as np
import os
import json
import re

class Retrieval_Docs:
    def __init__(self) -> None:
        self.data= None
        self.section_texts=[]
        self.index=[]
    
    def document_to_json(self,model,lease_document):
        # Load document
        doc = Document(lease_document)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        print(full_text)

        #use google gen ai to organise the document in sections
        prompt ="Please organize the following rental agreement text in its original format and wordings into the sections: Parties Involved, Lease Term, Rent Amount, Deposit and Fees, Tenant Obligations, Special Conditions. Important to Keep the sentences as they are from the document dont change original text and style. If a section is missing, leave it blank."
        response =model.generate_content("Organize the rental agreement text into specific sections." +  prompt + full_text)
        
        # Define section names
        sections = ["Parties Involved", "Lease Term", "Rent Amount", "Deposit and Fees", "Tenant Obligations", "Special Conditions"]

        # Initialize dictionary for JSON structure
        self.data = {"file_name": "TestAgreement1", "content": {section: "" for section in sections}}

        # Parse the text
        for section in sections:
            # Regex to match each section header and capture text until the next header or end of document
            pattern = rf"\*\*{section}\*\*\n\n(.+?)(?=\*\*|$)"
            match = re.search(pattern, response.text, re.DOTALL)
            if match:
                # Strip any extra whitespace and newlines
                self.data["content"][section] = match.group(1).strip()

        # Save to JSON file
        with open("organized_agreement.json", "w") as f:
            json.dump(self.data, f, indent=2)

        print("JSON file created successfully!")
        
        #start the indexing of file
        index = self.embedd_doc_to_index(self.data)
        return (index,self.section_texts)
        

    
    def embedd_doc_to_index(self, data):
        self.data=data
        # Extract section text
        sections = list(self.data["content"].keys())
        section_texts = list(self.data["content"].values())
        
        # Initialize the embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')  # Choose any model compatible with your needs

        # Generate embeddings for each section
        section_embeddings = model.encode(section_texts)
        
        # Choose an appropriate index type (FlatL2 is a good starting point)
        index = faiss.IndexFlatL2(section_embeddings.shape[1])  

        # Add your embeddings to the index
        index.add(section_embeddings.astype('float32')) 

        # Save the index to a file
        faiss.write_index(index, "faiss_index.bin")
        print(sections, section_texts, section_embeddings)
        self.section_texts =s ection_texts
        return index, self.section_texts
        
        
        
        
