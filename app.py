import cv2
import streamlit as st
import numpy as np
import dark_channel_prior as dcp
import inference as inf
import pandas as pd
from collections import Counter

# Function to remove noise from an image
def remove_noise(image):
    # Replace this with your noise removal code
    processed_image, alpha_map = dcp.haze_removal(image, w_size=15, a_omega=0.95, gf_w_size=200, eps=1e-6)
    return processed_image


# Function to perform object detection on an image
def detect_objects(image):
    # Replace this with your object detection code
    # Make sure the output image has bounding boxes around the detected objects
    output_image, class_names = inf.detect(image)
    return output_image, class_names


# Main function for Streamlit app
def app():
    # Header with gradient
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
                🔍 Underwater Waste Detection Model
            </h1>
            <p style='color: #666; font-size: 1.1rem;'>Powered by YOLOv8 Deep Learning Algorithm</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info box
    st.info("📸 Upload an underwater image to detect and identify waste materials. The model can identify 15 different types of waste including plastics, metals, and other debris.")
    
    # Allow the user to upload an image
    file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"], 
                            help="Supported formats: JPG, JPEG, PNG")
    
    # Process the input and display the output
    if file is not None:
        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Upload and process image
        status_text.text("📤 Uploading and processing image...")
        progress_bar.progress(20)
        
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        input_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        input_image = cv2.resize(input_image, (416, 416))
        
        progress_bar.progress(40)
        status_text.text("✅ Image processed successfully")
        
        # Display input image
        st.markdown("### 📥 Input Image")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(input_image, caption="Original underwater image")
        
        st.markdown("---")
        
        # Step 2: Remove noise
        status_text.text("🔧 Removing noise and enhancing image quality...")
        progress_bar.progress(60)
        
        processed_image = remove_noise(input_image)
        
        progress_bar.progress(80)
        status_text.text("✅ Image enhancement completed")
        
        # Display processed image
        st.markdown("### ✨ Enhanced Image (Noise Removed)")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(processed_image, caption="Enhanced image after noise removal")
        
        st.markdown("---")
        
        # Step 3: Run detection
        status_text.text("🤖 Running YOLOv8 model for object detection...")
        progress_bar.progress(90)
        
        output_image, class_names = detect_objects(processed_image)
        
        progress_bar.progress(100)
        status_text.text("✅ Detection completed!")
        
        # Display output image
        st.markdown("### 🎯 Detection Results")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(output_image, caption="Detected objects with bounding boxes")
        
        # Results summary
        st.markdown("---")
        st.markdown("### 📊 Detection Summary")
        
        if len(class_names) == 0:
            st.markdown("""
                <div style='padding: 2rem; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           border-radius: 15px; color: white; text-align: center;'>
                    <h2 style='color: white; margin: 0;'>✅ Water is Clear!</h2>
                    <p style='font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-top: 1rem;'>
                        No waste materials were detected in this image. The water appears to be clean.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Count occurrences
            waste_counts = Counter(class_names)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"""
                    <div style='padding: 1.5rem; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                               border-radius: 10px; color: white;'>
                        <h3 style='color: white; margin-top: 0;'>⚠️ Waste Detected!</h3>
                        <p style='font-size: 1.1rem; color: rgba(255,255,255,0.9);'>
                            <strong>{len(class_names)}</strong> object(s) detected
                        </p>
                        <p style='font-size: 1.1rem; color: rgba(255,255,255,0.9);'>
                            <strong>{len(waste_counts)}</strong> unique type(s)
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Detected Waste Types:**")
                for waste_type, count in waste_counts.items():
                    st.markdown(f"- **{waste_type}**: {count} time(s)")
            
            # Detailed breakdown
            st.markdown("#### 📋 Detailed Breakdown")
            waste_df = pd.DataFrame(list(waste_counts.items()), columns=['Waste Type', 'Count'])
            st.dataframe(waste_df, use_container_width=True, hide_index=True)
        
        # Clear progress
        progress_bar.empty()
        status_text.empty()




