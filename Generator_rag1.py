import docx
from docx import Document
import faiss
from sentence_transformers import SentenceTransformer
import random
import numpy as np
import os
import json
import re

class Generator_lease(self,section_texts,index,query,model):
    def __init__(self) -> None:
        self.section_texts =section_texts
        self.index= index
        self.query= query
        self.google_model= model
    
    ''' 
    def lease_generator(self):
        # Load the embeddings and FAISS index
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        index = faiss.read_index("faiss_index.bin")  # Assuming you saved embeddings to a FAISS index
    '''   
    # Function to embed text using your chosen embedding model
    def embed_text(self,text):
        # Implement your embedding logic here
        embedding = embedding_model.encode(text)  # Replace with actual embedding logic
        return np.array(embedding)  # Ensure it's a numpy array

    # Function to retrieve similar sections based on a query
    def retrieve_similar_sections(query, index, your_documents, k):
        # Embed the query
        query_embedding = embed_text(self.query)
        print("Shape of Query Embedding:", query_embedding.shape)

        # Perform a search on the FAISS index
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)

        # Handle empty results
        if len(indices[0]) == 0:
            return ["No relevant sections found."]
        
        # Retrieve matched sections
        matched_sections = [your_documents[idx] for idx in indices[0] if idx < len(self.section_texts)]
        print(matched_sections,"Sections found")
        return matched_sections

    # Function to generate a response using the Google Gen AI model
    def generate_response(self, query, index, your_documents):
        # Retrieve the sections
        matched_sections = retrieve_similar_sections(self.query, self.index, self.section_texts, k=1)

        context = "\n\n".join(matched_sections)
        combined_input = f"Use these new details Query: {query} and refer to the \n\nContext:\n{context} to write a new agreement"
        print("Input to model:", combined_input)

        # Generate response using the Google Gen AI model
        response = self.google_model.generate_content(combined_input)
        return response
