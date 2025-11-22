# AQUASense - AI-Powered Water Quality Solutions

**AQUASense** addresses the issue of growing underwater waste in oceans and seas. It offers three solutions: YoloV8 Algorithm-based underwater waste detection, a rule-based classifier for aquatic life habitat assessment, and a Machine Learning model for water classification as fit for use or not fit. The first model was trained on a dataset of 5000 images, while the second model used chemical properties guidelines from US EPA and WHO. The third model was trained on a dataset with over 6 million rows, providing reliable water classification results.

## Features

- Can detect underwater waste based on input images.
- Classifies water as potable or not based on chemical properties of water
- Classifies water as habitual for aquatic life or not.

## Architecture of YoloV8

YoloV8 is a state-of-the-art object detection model that uses deep learning to identify and locate objects in images.

## Tech Stack

- Python
- Dark Channel Prior Algorithm (for image denoising)
- YoloV8 (from Ultralytics)
- XGBoost Classifier
- Streamlit (for web interface)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the model files are in the correct directories:
   - `models/Underwater_Waste_Detection_YoloV8/60_epochs_denoised.pt`
   - `models/Water_Potability/xgboost_without_source_month.pkl`

## Usage

Run the main application:
```bash
streamlit run main_app.py
```

The application will open in your browser with a sidebar navigation menu.

## Project Structure

- `main_app.py` - Main Streamlit application with navigation
- `app.py` - Underwater waste detection module
- `app2.py` - Water potability test module
- `rule_based_classifier.py` - Aquatic life habitat assessment module
- `inference.py` - YOLO model inference functions
- `dark_channel_prior.py` - Image denoising algorithm
- `models/` - Pre-trained model files
- `test_data/` - Test datasets
- `assets/` - Image assets for the application
