"""
AI-Powered Water Quality Advisor
Provides intelligent water quality improvement advice using free APIs or rule-based system
"""

import streamlit as st
import requests
import os
from typing import Dict, Optional

# Option 1: Google Gemini API (FREE tier - 60 requests/minute)
# Get free API key from: https://aistudio.google.com/app/apikey
# No credit card required!

# Option 2: Hugging Face Inference API (FREE, no key needed)
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

def get_water_quality_advice_gemini(water_params: Dict[str, float], assessment_type: str = "aquatic", api_key: Optional[str] = None) -> Optional[str]:
    """
    Get water quality advice using Google Gemini API (FREE tier)
    
    Args:
        water_params: Dictionary of water quality parameters
        assessment_type: "aquatic" or "potability"
        api_key: Gemini API key (optional, can be set in Streamlit secrets)
    
    Returns:
        Advice string or None if API fails
    """
    # Default API key (can be overridden by secrets or environment variable)
    DEFAULT_API_KEY = "AIzaSyAHgKT76yU7qKQ76-uCxDdR-0YcStFhs0k"
    
    # Try to get API key from Streamlit secrets or environment first (more secure)
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", None)
        except:
            pass
        
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY", None)
        
        # Use default if nothing else is set
        if not api_key:
            api_key = DEFAULT_API_KEY
    
    if not api_key:
        return None
    
    try:
        # Format parameters
        params_text = "\n".join([f"{key}: {value}" for key, value in water_params.items()])
        
        if assessment_type == "aquatic":
            prompt = f"""As a water quality expert, analyze these water parameters for aquatic life habitat:
{params_text}

Based on US EPA and WHO standards, provide:
1. Which parameters are problematic (if any)
2. Specific, actionable advice to improve water quality
3. Recommended treatment methods
4. Priority actions

Keep response concise (3-4 sentences) and practical."""
        else:
            prompt = f"""As a water quality expert, analyze these water parameters for human consumption:
{params_text}

Based on WHO drinking water standards, provide:
1. Which parameters are problematic (if any)
2. Specific, actionable advice to improve water quality
3. Recommended treatment methods
4. Priority actions

Keep response concise (3-4 sentences) and practical."""
        
        # Call Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text.strip()
        
        return None
        
    except Exception as e:
        return None


def get_water_quality_advice_hf(water_params: Dict[str, float], assessment_type: str = "aquatic") -> Optional[str]:
    """
    Get water quality advice using Hugging Face Inference API (FREE, no key needed)
    Fallback option if Gemini is not available
    """
    try:
        params_text = ", ".join([f"{key}: {value}" for key, value in water_params.items()])
        
        if assessment_type == "aquatic":
            prompt = f"Water quality for aquatic life. Parameters: {params_text}. What improvements are needed?"
        else:
            prompt = f"Water quality for drinking. Parameters: {params_text}. What improvements are needed?"
        
        headers = {"Content-Type": "application/json"}
        payload = {"inputs": prompt}
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return result[0]['generated_text']
        
        return None
        
    except:
        return None


def get_water_quality_advice_rule_based(water_params: Dict[str, float], assessment_type: str = "aquatic") -> str:
    """
    Fallback rule-based advisor if LLM is unavailable
    Provides advice based on parameter thresholds
    """
    advice_parts = []
    
    # Define thresholds based on US EPA/WHO standards
    thresholds = {
        "aquatic": {
            "pH": (6.5, 9.0),
            "Iron": (0, 0.3),
            "Nitrate": (0, 10),
            "Chloride": (0, 250),
            "Lead": (0, 0.015),
            "Zinc": (0, 5),
            "Turbidity": (0, 5),
            "Fluoride": (0.7, 1.5),
            "Copper": (0, 1.3),
            "Sulfate": (0, 250),
            "Chlorine": (0, 4.0),
            "Manganese": (0, 0.05),
            "Total Dissolved Solids": (0, 500)
        },
        "potability": {
            "pH": (6.5, 8.5),
            "Iron": (0, 0.3),
            "Nitrate": (0, 10),
            "Chloride": (0, 250),
            "Lead": (0, 0.01),
            "Zinc": (0, 3),
            "Turbidity": (0, 1),
            "Fluoride": (0.7, 1.5),
            "Copper": (0, 2),
            "Sulfate": (0, 250),
            "Chlorine": (0, 4),
            "Manganese": (0, 0.05),
            "Total Dissolved Solids": (0, 500)
        }
    }
    
    thresholds_dict = thresholds.get(assessment_type, thresholds["aquatic"])
    
    # Check each parameter
    issues = []
    for param, value in water_params.items():
        if param in thresholds_dict:
            min_val, max_val = thresholds_dict[param]
            if value < min_val or value > max_val:
                issues.append((param, value, min_val, max_val))
    
    if not issues:
        return "✅ All parameters are within acceptable ranges. The water quality is good. Maintain regular monitoring and standard filtration practices."
    
    # Generate advice for issues
    advice_parts.append("⚠️ **Issues Detected:**")
    
    priority_actions = []
    for param, value, min_val, max_val in issues:
        if value < min_val:
            advice_parts.append(f"• **{param}** ({value}) is below minimum ({min_val}).")
            priority_actions.append(get_treatment_advice(param, "low"))
        elif value > max_val:
            advice_parts.append(f"• **{param}** ({value}) exceeds maximum ({max_val}).")
            priority_actions.append(get_treatment_advice(param, "high"))
    
    advice_parts.append("\n**Recommended Actions:**")
    for action in set(priority_actions):  # Remove duplicates
        advice_parts.append(f"• {action}")
    
    return "\n".join(advice_parts)


def get_treatment_advice(parameter: str, issue_type: str) -> str:
    """Get specific treatment advice for a parameter"""
    treatments = {
        "pH": {
            "low": "Add alkaline substances (lime, soda ash) to raise pH",
            "high": "Add acid (sulfuric acid, CO2 injection) to lower pH"
        },
        "Iron": {
            "high": "Use oxidation filtration, aeration, or iron removal filters"
        },
        "Nitrate": {
            "high": "Use reverse osmosis, ion exchange, or biological denitrification"
        },
        "Lead": {
            "high": "Install lead removal filters, use reverse osmosis, or replace lead pipes"
        },
        "Turbidity": {
            "high": "Use coagulation, flocculation, and sedimentation followed by filtration"
        },
        "Total Dissolved Solids": {
            "high": "Use reverse osmosis, distillation, or deionization"
        },
        "Chloride": {
            "high": "Use reverse osmosis or distillation"
        },
        "Fluoride": {
            "low": "Add fluoride through fluoridation systems",
            "high": "Use activated alumina, reverse osmosis, or bone char filters"
        }
    }
    
    if parameter in treatments and issue_type in treatments[parameter]:
        return treatments[parameter][issue_type]
    return f"Consult a water treatment specialist for {parameter} {issue_type} levels"


def get_ai_advice(water_params: Dict[str, float], assessment_type: str = "aquatic", use_llm: bool = True) -> str:
    """
    Main function to get AI advice - tries Gemini first, then Hugging Face, then rule-based
    
    Args:
        water_params: Dictionary of water quality parameters
        assessment_type: "aquatic" or "potability"
        use_llm: Whether to try LLM API (default True)
    
    Returns:
        Advice string
    """
    if use_llm:
        # Try Gemini API first (best quality)
        gemini_advice = get_water_quality_advice_gemini(water_params, assessment_type)
        if gemini_advice:
            return gemini_advice
        
        # Fallback to Hugging Face API
        hf_advice = get_water_quality_advice_hf(water_params, assessment_type)
        if hf_advice:
            return hf_advice
    
    # Final fallback to rule-based advice (always works)
    return get_water_quality_advice_rule_based(water_params, assessment_type)

