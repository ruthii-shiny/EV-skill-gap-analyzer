# app.py
# EV Skill Gap Analyzer 🚗⚡
# Hackathon-ready prototype

import spacy
import pandas as pd
import plotly.express as px
import json

# -----------------------------
# 1. Load NLP model
# -----------------------------
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# 2. Define EV Skill Ontology
# -----------------------------
required_skills = {
    "battery_management",
    "power_electronics",
    "embedded_systems",
    "high_voltage_safety",
    "charging_infrastructure",
    "thermal_management",
    "iot_connectivity",
    "ai_diagnostics",
    "sustainability_practices"
}

# -----------------------------
# 3. Load Sample Workforce Profiles
# -----------------------------
with open("data/sample_profiles.json") as f:
    profiles = json.load(f)

# -----------------------------
# 4. Extract Skills via NLP
# -----------------------------
def extract_skills(text):
    doc = nlp(text.lower())
    return {token.text.replace(" ", "_") for token in doc if not token.is_stop}

# -----------------------------
# 5. Gap Analysis
# -----------------------------
results = []
for profile in profiles:
    employee_skills = extract_skills(profile["skills"])
    gaps = required_skills - employee_skills
    results.append({
        "name": profile["name"],
        "current_skills": list(employee_skills),
        "missing_skills": list(gaps)
    })

df = pd.DataFrame(results)

# -----------------------------
# 6. Visualization
# -----------------------------
gap_counts = df.explode("missing_skills")["missing_skills"].value_counts().reset_index()
gap_counts.columns = ["Skill", "Number of Employees Missing"]

fig = px.bar(
    gap_counts,
    x="Skill",
    y="Number of Employees Missing",
    title="EV Skill Gaps in Workforce",
    color="Number of Employees Missing",
    text_auto=True
)

fig.show()

# -----------------------------
# 7. Recommendation Engine
# -----------------------------
def recommend_courses(skill):
    course_map = {
        "battery_management": "Battery Management Systems - Coursera",
        "power_electronics": "Power Electronics for EVs - Udemy",
        "embedded_systems": "Embedded Systems Design - edX",
        "high_voltage_safety": "High Voltage Safety Training - OEM Academy",
        "charging_infrastructure": "EV Charging Infra Basics - LinkedIn Learning",
        "thermal_management": "Thermal Systems in EVs - Coursera",
        "iot_connectivity": "IoT for Smart Mobility - Udemy",
        "ai_diagnostics": "AI in Automotive Diagnostics - edX",
        "sustainability_practices": "Sustainable Manufacturing - Coursera"
    }
    return course_map.get(skill, "General EV Training")

print("\n--- Recommendations ---")
for gap in results[0]["missing_skills"]:
    print(f"Skill Gap: {gap} → Suggested Course: {recommend_courses(gap)}")
