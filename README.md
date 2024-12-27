Run the web app by changing directory to demo

and run manage.py

python demo/manage.py runserver

# PPE Detector: A Django-Based Personal Protective Equipment Detection App

## Overview
The **PPE Detector** is a Django application that utilizes a webcam feed to detect whether individuals are wearing mandatory Personal Protective Equipment (PPE) such as helmets and safety vests. It employs real-time object detection using advanced computer vision techniques to ensure compliance with safety standards.

---

## Features
- **Real-Time Detection**: Utilizes webcam input for live detection.
- **PPE Classification**: Detects the presence of helmets and safety vests.
- **Alerts**: Provides visual or audio alerts for non-compliance.
- **User-Friendly Interface**: Simple and intuitive interface built with Django.
- **Scalability**: Modular design allows adding more PPE categories in the future.

---

## Installation and Setup

### Prerequisites
Ensure the following are installed on your system:
- Python 3.8+
- Django 4.0+
- OpenCV
- TensorFlow or PyTorch (depending on the model used)
- Web browser with webcam access

 
