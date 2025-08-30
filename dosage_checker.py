# Import required libraries
from fastapi import FastAPI, Request
from typing import List, Dict
import streamlit as st
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI(title="AI Medical Prescription Verification")

# HuggingFace pipeline for NLP extraction (assume model is trained for medical info extraction)
nlp = pipeline("ner", model="your-medical-ner-model")

# Simulated drug interaction database (for demonstration)
drug_interactions = {
    ("DrugA", "DrugB"): "Increased risk of bleeding",
    ("DrugC", "DrugD"): "May cause heart issues"
}

# Sample age-specific dosage map
dosage_recommendations = {
    ("DrugA", "adult"): "20mg once daily",
    ("DrugA", "child"): "10mg once daily"
}
# Endpoint: Detect Drug Interactions
@app.post("/detect_interactions/")
async def detect_interactions(drugs: List[str]):
    interactions = []
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            key = (drugs[i], drugs[j])
            if key in drug_interactions:
                interactions.append({"drugs": key, "interaction": drug_interactions[key]})
    return {"interactions": interactions}

# Endpoint: Recommend Dosage
@app.post("/recommend_dosage/")
async def recommend_dosage(drug: str, age_group: str):
    key = (drug, age_group)
    dosage = dosage_recommendations.get(key, "Consult doctor for dosage")
    return {"drug": drug, "age_group": age_group, "dosage": dosage}
# Endpoint: Extract Info from Medical Text
@app.post("/extract_info/")
async def extract_info(text: str):
    results = nlp(text)
    extracted_info = [{"entity": res['entity'], "value": res['word']} for res in results]
    return {"extracted_info": extracted_info}

# Streamlit Frontend (Sample Usage)
def main():
    st.title("AI Medical Prescription Verification")
    drugs = st.text_input("Enter drugs (comma separated):").split(",")
    if st.button("Check Interactions"):
        response = detect_interactions(drugs)
        st.json(response)

    drug = st.text_input("Drug name for dosage:")
    age_group = st.selectbox("Age group:", ["adult", "child"])
    if st.button("Get Dosage"):
        response = recommend_dosage(drug, age_group)
        st.json(response)

    text = st.text_area("Paste medical text:")
    if st.button("Extract Drug Info"):
        response = extract_info(text)
        st.json(response)

if _name_ == "_main_":
    main()
