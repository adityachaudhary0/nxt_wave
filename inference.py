from ultralytics import YOLO
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)
import torch
import cv2
import os

labels = ['Mask', 'can', 'cellphone', 'electronics', 'gbottle', 'glove', 'metal', 'misc', 'net', 'pbag', 'pbottle',
        'plastic', 'rod', 'sunglasses', 'tire']

garbage = []

def detect(image):
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'models', 'Underwater_Waste_Detection_YoloV8', '60_epochs_denoised.pt')
    model = YOLO(model_path)
    results = model(image)
    class_list = []
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
        class_list = boxes.cls.tolist()
    int_list = [int(num) for num in class_list]
    class_names = [labels[i] for i in int_list]
    garbage.extend(class_names)
    res_plotted = results[0].plot()
    return res_plotted, class_names

# cv2.imshow('res', res_plotted)
# cv2.waitKey(0)
# cv2.destroyAllWindows()