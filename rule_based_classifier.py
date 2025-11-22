import streamlit as st
import pandas as pd
import os

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))


def is_habitable(pH, Iron, Nitrate, Chloride, Lead, Zinc, Turbidity, Fluoride, Copper, Sulfate, Chlorine, Manganese,
                 Total_Dissolved_Solids):
    if pH >= 6.5 and pH <= 9.0 and Iron < 0.3 and Nitrate < 10 and Chloride < 250 and Lead < 0.015 and Zinc < 5 and Turbidity < 5 and Fluoride >= 0.7 and Fluoride <= 1.5 and Copper < 1.3 and Sulfate < 250 and Chlorine < 4.0 and Manganese < 0.05 and Total_Dissolved_Solids < 500:
        return 0
    else:
        return 1


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
    'Turbidity': float,
    'Fluoride': float,
    'Copper': float,
    'Sulfate': float,
    'Chlorine': float,
    'Manganese': float,
    'Total Dissolved Solids': float,
}

quality_aquatic = []

def rbc():
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
                🐠 Water Quality Assessment for Aquatic Life
            </h1>
            <p style='color: #666; font-size: 1.1rem;'>Based on US EPA and WHO Guidelines</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info section
    st.info("""
        📋 **Assessment Criteria**: This model evaluates water quality parameters against US EPA and WHO standards 
        to determine if the water is suitable for aquatic life habitat. Enter the chemical properties below or 
        use random sample data to test.
    """)
    
    # Input form with better styling
    st.markdown("### 📝 Enter Water Quality Parameters")
    
    inputs = {}
    
    # Group parameters into sections
    st.markdown("#### Basic Parameters")
    col1, col2, col3, col4 = st.columns(4)
    basic_params = ['pH', 'Iron', 'Nitrate', 'Chloride']
    for i, param in enumerate(basic_params):
        with [col1, col2, col3, col4][i]:
            inputs[param] = st.number_input(
                f'**{param}**', 
                value=0.0, 
                step=0.1, 
                format='%.2f',
                key=f'aquatic_{param}',
                help=f"Enter {param} value"
            )
    
    st.markdown("#### Heavy Metals")
    col1, col2, col3, col4 = st.columns(4)
    metal_params = ['Lead', 'Zinc', 'Copper', 'Manganese']
    for i, param in enumerate(metal_params):
        with [col1, col2, col3, col4][i]:
            inputs[param] = st.number_input(
                f'**{param}**', 
                value=0.0, 
                step=0.1, 
                format='%.2f',
                key=f'aquatic_{param}',
                help=f"Enter {param} value"
            )
    
    st.markdown("#### Other Parameters")
    col1, col2, col3, col4, col5 = st.columns(5)
    other_params = ['Turbidity', 'Fluoride', 'Sulfate', 'Chlorine', 'Total Dissolved Solids']
    for i, param in enumerate(other_params):
        with [col1, col2, col3, col4, col5][i]:
            inputs[param] = st.number_input(
                f'**{param}**', 
                value=0.0, 
                step=0.1, 
                format='%.2f',
                key=f'aquatic_{param}',
                help=f"Enter {param} value"
            )
    
    st.markdown("---")
    
    # Buttons with better styling
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        predict_btn = st.button('🔍 Assess Water Quality', use_container_width=True, type='primary')
    
    with col3:
        random_btn = st.button('🎲 Use Random Sample', use_container_width=True)
    
    # Prediction logic
    if predict_btn:
        inputs_list = list(inputs.values())
        is_good = is_habitable(*inputs_list)
        quality_aquatic.append(is_good)
        
        st.markdown("---")
        st.markdown("### 📊 Assessment Result")
        
        if is_good == 0:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>✅ Water Quality is Habitable</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water meets US EPA and WHO standards for aquatic life habitat.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>⚠️ Water Quality is Not Habitable</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water does not meet the required standards for aquatic life habitat. 
                        Some parameters exceed safe limits.
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    if random_btn:
        data = test_df.sample(n=1)
        data_copy = data.copy()
        data_display = data_copy.drop(['Target', 'Color', 'Odor'], axis=1, errors='ignore')
        
        st.markdown("---")
        st.markdown("### 🎲 Random Sample Data")
        st.dataframe(data_display, use_container_width=True, hide_index=True)
        
        # Extract values in correct order
        inputs_list = [
            data_display['pH'].values[0],
            data_display['Iron'].values[0],
            data_display['Nitrate'].values[0],
            data_display['Chloride'].values[0],
            data_display['Lead'].values[0],
            data_display['Zinc'].values[0],
            data_display['Turbidity'].values[0],
            data_display['Fluoride'].values[0],
            data_display['Copper'].values[0],
            data_display['Sulfate'].values[0],
            data_display['Chlorine'].values[0],
            data_display['Manganese'].values[0],
            data_display['Total Dissolved Solids'].values[0]
        ]
        
        is_good = is_habitable(*inputs_list)
        quality_aquatic.append(is_good)
        
        st.markdown("### 📊 Assessment Result")
        
        if is_good == 0:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>✅ Water Quality is Habitable</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water meets US EPA and WHO standards for aquatic life habitat.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>⚠️ Water Quality is Not Habitable</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        The water does not meet the required standards for aquatic life habitat. 
                        Some parameters exceed safe limits.
                    </p>
                </div>
            """, unsafe_allow_html=True)
