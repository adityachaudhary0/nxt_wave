import streamlit as st
import app
import app2
import rule_based_classifier as rbc
from inference import garbage
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Custom CSS for modern UI
st.set_page_config(
    page_title="AQUASense",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 3rem;
    }
    
    /* Title styling */
    h1 {
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Card-like containers */
    .stContainer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    
    /* Success/Error messages */
    .stSuccess {
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
    }
    
    .stError {
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
    }
    
    /* Image containers */
    .image-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Sidebar navigation */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

labels = ['Mask', 'can', 'cellphone', 'electronics', 'gbottle', 'glove', 'metal', 'misc', 'net', 'pbag', 'pbottle',
          'plastic', 'rod', 'sunglasses', 'tire']

def main():
    # Enhanced sidebar with icons
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: white; margin: 0;'>🌊 AQUASense</h1>
            <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0;'>AI-Powered Water Quality Solutions</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    selected_model = st.sidebar.radio(
        'Navigate to:',
        ['Home', 'Underwater Waste Detection Model',
         'Water Quality Assessment Model',
         'Water Potability Test Model', 'Generated Report'],
        label_visibility="collapsed"
    )
    # display appropriate content based on selected model
    if selected_model == 'Home':
        # Hero Section
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
                <div style='padding: 2rem 0;'>
                    <h1 style='font-size: 3.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                               margin-bottom: 1rem;'>🌊 AQUASense</h1>
                    <p style='font-size: 1.3rem; color: #555; line-height: 1.8;'>
                        Advanced AI-Powered Solutions for Water Bodies Conservation and Water Quality Assessment
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        yacht_image = os.path.join(base_dir, 'assets', 'yacht.jpg')
        if os.path.exists(yacht_image):
            st.image(yacht_image, caption="Protecting our Water Bodies with AI technology")
        
        st.markdown("---")
        
        # Features Section
        st.markdown("### 🎯 Our Solutions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           border-radius: 10px; color: white; height: 100%;'>
                    <h3 style='color: white; margin-top: 0;'>🔍 Waste Detection</h3>
                    <p style='color: rgba(255,255,255,0.9);'>
                        YOLOv8-based underwater waste detection trained on 5,000+ images for accurate identification 
                        of marine debris including plastics, metals, and other pollutants.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                           border-radius: 10px; color: white; height: 100%;'>
                    <h3 style='color: white; margin-top: 0;'>🐠 Aquatic Life Assessment</h3>
                    <p style='color: rgba(255,255,255,0.9);'>
                        Rule-based classifier using US EPA and WHO guidelines to assess water quality 
                        for aquatic life habitat suitability.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                           border-radius: 10px; color: white; height: 100%;'>
                    <h3 style='color: white; margin-top: 0;'>💧 Potability Testing</h3>
                    <p style='color: rgba(255,255,255,0.9);'>
                        Machine Learning model trained on 6+ million data points to classify water as 
                        fit for drinking, irrigation, or not suitable.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Stats Section
        st.markdown("### 📊 Project Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Training Images", "5,000+", "YOLOv8 Model")
        with col2:
            st.metric("Data Points", "6M+", "Potability Model")
        with col3:
            st.metric("Waste Categories", "15", "Detected Types")
        with col4:
            st.metric("Standards", "US EPA & WHO", "Guidelines Used")
    elif selected_model == 'Underwater Waste Detection Model':
        app.app()
    elif selected_model == 'Water Quality Assessment Model':
        rbc.rbc()
    elif selected_model == 'Water Potability Test Model':
        app2.app2()
    elif selected_model == 'Generated Report':
        st.markdown("""
            <div style='text-align: center; padding: 2rem 0;'>
                <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    📊 Generated Report
                </h1>
                <p style='color: #666; font-size: 1.1rem;'>Comprehensive analysis of all detections and assessments</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Waste Detection Statistics
        st.markdown("### 🗑️ Waste Detection Statistics")
        occurrences = [garbage.count(labels[i]) for i in range(len(labels))]
        
        if sum(occurrences) > 0:
            col1, col2 = st.columns([2, 1])
            with col1:
                plt.figure(figsize=(10, 8))
                sns.set_style("whitegrid")
                colors_bar = sns.color_palette("husl", len(labels))
                bars = plt.barh(labels, occurrences, color=colors_bar)
                plt.xlabel("Occurrences", fontsize=12, fontweight='bold')
                plt.ylabel("Waste Labels", fontsize=12, fontweight='bold')
                plt.title("Frequency of Detected Waste Types", fontsize=14, fontweight='bold', pad=20)
                plt.grid(axis='x', alpha=0.3)
                # Add value labels on bars
                for i, (bar, val) in enumerate(zip(bars, occurrences)):
                    if val > 0:
                        plt.text(val + 0.1, i, str(val), va='center', fontweight='bold')
                plt.tight_layout()
                st.pyplot(plt)
                plt.close()
            
            with col2:
                total_detections = sum(occurrences)
                most_common_idx = occurrences.index(max(occurrences)) if max(occurrences) > 0 else 0
                st.metric("Total Detections", total_detections)
                st.metric("Most Common", labels[most_common_idx], f"{max(occurrences)} times")
                st.metric("Unique Types", sum(1 for x in occurrences if x > 0))
        else:
            st.info("📝 No waste detections yet. Run some detections in the Underwater Waste Detection Model to see statistics here.")
        
        st.markdown("---")
        
        # Water Quality for Aquatic Life
        st.markdown("### 🐠 Water Quality for Aquatic Life Habitat")
        quality_aquatic = rbc.quality_aquatic
        counts = [quality_aquatic.count(0), quality_aquatic.count(1)]
        
        if len(quality_aquatic) == 0:
            st.warning("⚠️ Please run some inference on water quality for aquatic life habitat to see statistics here.")
        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                ans = max(set(quality_aquatic), key=quality_aquatic.count)
                labels_h = ['Habitual', 'Not Habitual']
                habitual = labels_h[ans]
                colors = ['#28a745', '#dc3545']
                sns.set_style("whitegrid")
                fig, ax = plt.subplots(figsize=(8, 8))
                wedges, texts, autotexts = ax.pie(counts, labels=labels_h, colors=colors, autopct='%1.1f%%', 
                                                   startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
                ax.set_title('Water Quality Distribution for Aquatic Life', fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.markdown(f"""
                    <div style='padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               border-radius: 10px; color: white; margin-top: 2rem;'>
                        <h3 style='color: white;'>Overall Assessment</h3>
                        <p style='font-size: 1.5rem; color: white; font-weight: bold;'>
                            {habitual}
                        </p>
                        <p style='color: rgba(255,255,255,0.9);'>
                            Based on {len(quality_aquatic)} assessment(s)
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Water Potability
        st.markdown("### 💧 Water Quality for Potability")
        data = app2.quality
        counts_pot = [data.count(0), data.count(1)]
        
        if len(data) == 0:
            st.warning("⚠️ Please run some inference on water potability assessment to see statistics here.")
        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                ans_pot = max(set(data), key=data.count)
                labels_wqa = ['Fit for use', 'Polluted']
                qwa = labels_wqa[ans_pot]
                colors_pot = ['#17a2b8', '#ffc107']
                sns.set_style("whitegrid")
                fig2, ax2 = plt.subplots(figsize=(8, 8))
                wedges2, texts2, autotexts2 = ax2.pie(counts_pot, labels=labels_wqa, colors=colors_pot, 
                                                      autopct='%1.1f%%', startangle=90,
                                                      textprops={'fontsize': 12, 'fontweight': 'bold'})
                ax2.set_title('Water Potability Distribution', fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close()
            
            with col2:
                st.markdown(f"""
                    <div style='padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                               border-radius: 10px; color: white; margin-top: 2rem;'>
                        <h3 style='color: white;'>Overall Assessment</h3>
                        <p style='font-size: 1.5rem; color: white; font-weight: bold;'>
                            {qwa}
                        </p>
                        <p style='color: rgba(255,255,255,0.9);'>
                            Based on {len(data)} assessment(s)
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Final Conclusion
            if len(quality_aquatic) > 0 and sum(occurrences) > 0:
                st.markdown("### 📋 Executive Summary")
                most_common_waste = labels[occurrences.index(max(occurrences))] if max(occurrences) > 0 else "None"
                waste_count = max(occurrences) if max(occurrences) > 0 else 0
                
                st.markdown(f"""
                    <div style='padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               border-radius: 15px; color: white; margin: 2rem 0;'>
                        <h2 style='color: white; margin-top: 0;'>🎯 Key Findings</h2>
                        <p style='font-size: 1.2rem; line-height: 1.8; color: rgba(255,255,255,0.95);'>
                            In the recent analysis, the most frequently detected type of waste is 
                            <strong>{most_common_waste}</strong> (detected {waste_count} time(s)). 
                            The water quality assessment indicates that the water is <strong>{habitual.lower()}</strong> 
                            for aquatic life habitat and <strong>{qwa.lower()}</strong> for human use.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning('Please select a model from the sidebar.')

main()
