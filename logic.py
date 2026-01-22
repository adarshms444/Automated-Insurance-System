import google.generativeai as genai
from pinecone import Pinecone
import requests 
import os

class SurakshaBrain:
    def __init__(self, gemini_key, deepgram_key, pinecone_key, index_name):
        # Initialize Gemini (FIXED: Uses 1.5-flash, 2.5 does not exist yet)
        genai.configure(api_key=gemini_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=pinecone_key)
        self.index = self.pc.Index(index_name)
        
        # Store Deepgram Key
        self.deepgram_key = deepgram_key

    def get_rag_context(self, query):
        """Searches Pinecone for relevant policy details."""
        try:
            # Embed Query
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = response['embedding']
            
            # Search Index
            results = self.index.query(
                vector=query_embedding,
                top_k=3, 
                include_metadata=True
            )
            
            context = ""
            sources = []
            for match in results['matches']:
                if 'metadata' in match:
                    context += f"- {match['metadata'].get('text', '')}\n"
                    sources.append(match['metadata'].get('category', 'General'))
            
            return context, list(set(sources))
        except Exception as e:
            return str(e), []

    def transcribe_audio(self, audio_bytes):
        """
        Converts Voice to Text using Deepgram.
        Returns ONLY the transcript string.
        """
        try:
            url = "https://api.deepgram.com/v1/listen"
            
            params = {
                "model": "nova-2",
                "smart_format": "true",
                "detect_language": "true" 
            }
            
            headers = {
                "Authorization": f"Token {self.deepgram_key}",
                "Content-Type": "audio/wav" 
            }
            
            response = requests.post(url, headers=headers, params=params, data=audio_bytes)
            
            if response.status_code == 200:
                data = response.json()
                # Return just the text
                transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
                return transcript
            else:
                return f"Error: Deepgram API returned {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_response(self, query, context, lang_code="en"):
        """
        Generates answer. 
        """
        prompt = f"""
        You are SurakshaConnect, a smart insurance advisor for rural India.
        
        CONTEXT FROM OFFICIAL DOCUMENTS:
        {context}
        
        USER QUESTION: "{query}"
        
        INSTRUCTIONS:

         PHASE 1: SURVEY (Do this first if details are missing)
        - If the user just says "I want insurance", DO NOT recommend yet.
        - Ask 2-3 specific questions based on the 'Eligibility' section in the context (e.g., "What crop do you grow?", "How old are you?", "Do you own land?").
        
        PHASE 2: RECOMMENDATION (Do this if user gave details)
        - clearly state the **Policy Name** that fits them best.
        - List 3 **Key Benefits** using the exact numbers from the context.
        
        PHASE 3: THE HOOK (Simple Story/Analogy) - **CRITICAL STEP**
        - After the facts, add a section called "💡 **Why you need this (Simple Story)**"
        - Use these specific analogies based on the policy type:
          - **Crop Insurance:** "Think of this policy like a **Helmet for your Farm** ⛑️. Just like a helmet saves your head in a fall, this saves your income when the rain fails."
          - **Health Insurance:** "Think of this like a **Magic Purse** 👛. You put small coins in it now, but if you get sick, it opens up to pay the big hospital bills automatically."
          - **Life Insurance:** "Think of this as a **Backup Father** 🛡️. If something happens to you, this policy steps in to pay your children's school fees and house rent."
        
        PHASE 4: THE CLOSE (Sales Push)
        - End with a strong, encouraging question: "It costs less than a cup of tea per day. Shall I create your policy ID now?"
        
        Answer:
        """
        
        response = self.model.generate_content(prompt)
        return response.text