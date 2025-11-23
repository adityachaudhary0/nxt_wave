import streamlit as st
import pandas as pd
import os
import joblib
import numpy as np
from llm_advisor import get_ai_advice

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
test_df_path = os.path.join(base_dir, 'test_data', 'test_df')
test_df = pd.read_csv(test_df_path)

# Define the features and their types
features = {
    'pH': float,
    'Iron': float,
    'Nitrate': float,
    'Chloride': float,
    'Lead': float,
    'Zinc': float,
    'Color': str,
    'Turbidity': float,
    'Fluoride': float,
    'Copper': float,
    'Odor': float,
    'Sulfate': float,
    'Chlorine': float,
    'Manganese': float,
    'Total Dissolved Solids': float,
}

# Define the target variable
target_variable = 'Target'

# Define the color options
color_options = ['Colorless', 'Faint Yellow', 'Light Yellow', 'Near Colorless', 'Yellow', 'NaN']

quality = []
# Create a Streamlit app
def app2():
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
                💧 Water Potability Test Model
            </h1>
            <p style='color: #666; font-size: 1.1rem;'>Machine Learning Model Trained on 6+ Million Data Points</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Load the pretrained model pipeline
    model_path = os.path.join(base_dir, 'models', 'Water_Potability', 'xgboost_without_source_month.pkl')
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        # Try alternative path
        alt_path = os.path.join(base_dir, 'models', 'Water_Potability', 'xgboost_pipeline.pkl')
        try:
            model = joblib.load(alt_path)
        except FileNotFoundError:
            st.error("""
                ⚠️ **Model file not found.** 
                
                Please ensure the model file exists at:
                - `models/Water_Potability/xgboost_without_source_month.pkl` or
                - `models/Water_Potability/xgboost_pipeline.pkl`
            """)
            return
    
    # Info section
    st.info("""
        📋 **Model Information**: This XGBoost model classifies water as fit for drinking/irrigation (0) or 
        not suitable (1) based on 15 chemical and physical parameters. Enter values below or use random sample data.
    """)
    
    # Create input widgets for each feature
    st.markdown("### 📝 Enter Water Quality Parameters")
    
    inputs = {}
    
    # Group parameters logically
    st.markdown("#### Basic Chemical Properties")
    col1, col2, col3, col4 = st.columns(4)
    basic_params = ['pH', 'Iron', 'Nitrate', 'Chloride']
    for i, param in enumerate(basic_params):
        with [col1, col2, col3, col4][i]:
            inputs[param] = st.number_input(
                f'**{param}**', 
                value=0.0, 
                step=0.1, 
                format='%.2f',
                key=f'potability_{param}',
                help=f"Enter {param} value"
            )
    
    st.markdown("#### Heavy Metals & Trace Elements")
    col1, col2, col3, col4 = st.columns(4)
    metal_params = ['Lead', 'Zinc', 'Copper', 'Manganese']
    for i, param in enumerate(metal_params):
        with [col1, col2, col3, col4][i]:
            inputs[param] = st.number_input(
                f'**{param}**', 
                value=0.0, 
                step=0.1, 
                format='%.2f',
                key=f'potability_{param}',
                help=f"Enter {param} value"
            )
    
    st.markdown("#### Physical Properties")
    col1, col2, col3 = st.columns(3)
    physical_params = ['Turbidity', 'Total Dissolved Solids']
    for i, param in enumerate(physical_params):
        with [col1, col2, col3][i]:
            inputs[param] = st.number_input(
                f'**{param}**', 
                value=0.0, 
                step=0.1, 
                format='%.2f',
                key=f'potability_{param}',
                help=f"Enter {param} value"
            )
    
    st.markdown("#### Other Parameters")
    col1, col2, col3, col4, col5 = st.columns(5)
    other_params = ['Fluoride', 'Sulfate', 'Chlorine', 'Color', 'Odor']
    for i, param in enumerate(other_params):
        with [col1, col2, col3, col4, col5][i]:
            if param == 'Color':
                inputs[param] = st.selectbox(
                    f'**{param}**', 
                    options=color_options,
                    key=f'potability_{param}',
                    help=f"Select {param}"
                )
            else:
                inputs[param] = st.number_input(
                    f'**{param}**', 
                    value=0.0, 
                    step=0.1, 
                    format='%.2f',
                    key=f'potability_{param}',
                    help=f"Enter {param} value"
                )
    
    st.markdown("---")
    
    # Buttons with better styling
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col2:
        predict_btn = st.button('🔍 Predict Potability', use_container_width=True, type='primary')
    
    with col3:
        random_btn = st.button('🎲 Use Random Sample', use_container_width=True)
    
    with col4:
        ask_ai_btn = st.button('🤖 Ask AI for Advice', use_container_width=True)
    
    # Check if inputs are provided (not all zeros and not default values)
    def has_inputs(inputs_dict):
        """Check if user has entered any meaningful values"""
        # Check numeric values (not zero) and non-empty strings
        for key, value in inputs_dict.items():
            if key == 'Color':
                if value and value != 'NaN':
                    return True
            elif isinstance(value, (int, float)):
                if float(value) != 0.0:
                    return True
            elif value:
                return True
        return False
    
    # AI Advice Button Logic
    if ask_ai_btn:
        if not has_inputs(inputs):
            st.warning("⚠️ **Please provide input values first!** Enter water quality parameters above before asking for AI advice.")
        else:
            st.markdown("---")
            st.markdown("### 🤖 AI-Powered Improvement Advice")
            
            with st.spinner("Analyzing water parameters and generating recommendations..."):
                # Convert inputs to float values for advice
                inputs_for_advice = {k: float(v) if isinstance(v, (int, float)) else v for k, v in inputs.items()}
                advice = get_ai_advice(inputs_for_advice, assessment_type="potability", use_llm=True)
                
                if advice:
                    st.markdown("""
                        <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                   border-radius: 10px; color: white; margin-top: 1rem;'>
                            <h3 style='color: white; margin-top: 0;'>💡 Expert Recommendations</h3>
                            <div style='color: rgba(255,255,255,0.95); line-height: 1.8; white-space: pre-wrap;'>
                    """, unsafe_allow_html=True)
                    st.markdown(advice)
                    st.markdown("</div></div>", unsafe_allow_html=True)
                else:
                    st.info("💡 AI advice is currently unavailable. Using rule-based recommendations.")
                    rule_based_advice = get_ai_advice(inputs_for_advice, assessment_type="potability", use_llm=False)
                    st.markdown(f"""
                        <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                   border-radius: 10px; color: white; margin-top: 1rem;'>
                            <h3 style='color: white; margin-top: 0;'>💡 Expert Recommendations</h3>
                            <div style='color: rgba(255,255,255,0.95); line-height: 1.8; white-space: pre-wrap;'>
                                {rule_based_advice}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Prediction logic
    if predict_btn:
        data = pd.DataFrame(inputs, index=range(0, 1), columns=inputs.keys())
        # Use pipeline's predict method directly
        prediction = model.predict(data)
        prediction_label = int(prediction[0]) if hasattr(prediction, '__iter__') else int(prediction)
        quality.append(prediction_label)
        
        st.markdown("---")
        st.markdown("### 📊 Prediction Result")
        
        if prediction_label == 0:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>✅ Water is Fit for Use</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water is suitable for both drinking and irrigation purposes according to the ML model.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>⚠️ Water is Not Fit for Use</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water is not suitable for drinking or irrigation purposes. 
                        Some parameters may exceed safe limits.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # AI Advice Section
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Improvement Advice")
        
        with st.spinner("Analyzing water parameters and generating recommendations..."):
            # Convert inputs to float values for advice
            inputs_for_advice = {k: float(v) if isinstance(v, (int, float)) else v for k, v in inputs.items()}
            advice = get_ai_advice(inputs_for_advice, assessment_type="potability", use_llm=True)
            
            if advice:
                st.markdown("""
                    <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               border-radius: 10px; color: white; margin-top: 1rem;'>
                        <h3 style='color: white; margin-top: 0;'>💡 Expert Recommendations</h3>
                        <div style='color: rgba(255,255,255,0.95); line-height: 1.8; white-space: pre-wrap;'>
                """, unsafe_allow_html=True)
                st.markdown(advice)
                st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.info("💡 AI advice is currently unavailable. Using rule-based recommendations.")
                rule_based_advice = get_ai_advice(inputs_for_advice, assessment_type="potability", use_llm=False)
                st.markdown(f"""
                    <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               border-radius: 10px; color: white; margin-top: 1rem;'>
                        <h3 style='color: white; margin-top: 0;'>💡 Expert Recommendations</h3>
                        <div style='color: rgba(255,255,255,0.95); line-height: 1.8; white-space: pre-wrap;'>
                            {rule_based_advice}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    if random_btn:
        data = test_df.sample(n=1)
        data_display = data.drop(['Target'], axis=1, errors='ignore')
        
        st.markdown("---")
        st.markdown("### 🎲 Random Sample Data")
        st.dataframe(data_display, use_container_width=True, hide_index=True)
        
        # Use pipeline's predict method directly
        prediction = model.predict(data_display)
        prediction_label = int(prediction[0]) if hasattr(prediction, '__iter__') else int(prediction)
        quality.append(prediction_label)
        
        st.markdown("### 📊 Prediction Result")
        
        if prediction_label == 0:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>✅ Water is Fit for Use</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water is suitable for both drinking and irrigation purposes according to the ML model.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>⚠️ Water is Not Fit for Use</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water is not suitable for drinking or irrigation purposes. 
                        Some parameters may exceed safe limits.
                    </p>
                </div>
            """, unsafe_allow_html=True)