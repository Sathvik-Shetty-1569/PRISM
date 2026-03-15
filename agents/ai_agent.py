import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_summary(df):
    prompt = f"""
    You are a sharp data analyst. Analyze this dataset and give a brutal, 
    concise report in exactly this format:

    **What this dataset is about:** (1 sentence)
    **3 key observations:** (bullet points, specific numbers)
    **Biggest data quality issue:** (1 sentence)  
    **Best ML task for this data:** (classification/regression/clustering + why)

    Dataset info:
    - Shape: {df.shape}
    - Columns: {df.columns.tolist()}
    - Types: {df.dtypes.astype(str).to_dict()}
    - Missing: {df.isnull().sum().to_dict()}
    - Sample: {df.head(3).to_dict()}
    - Stats: {df.describe().to_dict()}
    """
    response = model.generate_content(prompt)
    return response.text

def generate_code(question, columns, chat_history=[]):
    history_text = ""
    if chat_history:
        history_text = "Previous questions in this session:\n"
        for q in chat_history[-3:]:  # last 3 questions
            history_text += f"- {q}\n"

    prompt = f"""
        You are a data scientist with memory of this session.
        
        A pandas dataframe named df is already loaded.
        Dataset columns: {columns}
        
        {history_text}
        
        Current question: {question}
        
        Rules:
        - Do NOT use import statements
        - pandas is available as pd
        - matplotlib is available as plt
        - Only output Python code, nothing else
    """
    response = model.generate_content(prompt)
    return response.text