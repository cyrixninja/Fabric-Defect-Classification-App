from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import os
import numpy as np
import tensorflow as tf
import uuid
import time
import json
from datetime import datetime
from utils.preprocessing import load_and_preprocess_image, predict_defect

app = Flask(__name__)
app.secret_key = 'Textile_defect_analysis_key'

# Define the upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create required directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/history', exist_ok=True)
os.makedirs('static/images/defects', exist_ok=True)

# Load the trained model
model = None
try:
    model = tf.keras.models.load_model('models/textile_defect_model.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

# Class mapping based on your folder structure
CLASS_INDICES = {
    0: 'vertical',
    1: 'defect_free', 
    2: 'hole', 
    3: 'horizontal',
    4: 'lines',
    5: 'stain'
}

# Defect information for UI display
DEFECT_INFO = {
    'defect_free': {
        'description': 'No defects detected in the textile. The material passes quality control standards.',
        'recommendation': 'This textile can proceed to the next stage of production.',
        'severity': 'None'
    },
    'hole': {
        'description': 'Physical gaps or perforations in the textile that compromise its integrity.',
        'recommendation': 'Remove affected section and inspect surrounding areas for potential spreading issues.',
        'severity': 'High'
    },
    'horizontal': {
        'description': 'Horizontal creases or folds that disrupt the textile pattern and structure.',
        'recommendation': 'Apply controlled steaming and tension to remove creases before further processing.',
        'severity': 'Medium'
    },
    'lines': {
        'description': 'Linear marks that run across the textile, often caused by mechanical issues in the loom.',
        'recommendation': 'Inspect loom settings and tension. textile may require reprocessing or downgrading.',
        'severity': 'Medium'
    },
    'stain': {
        'description': 'Discoloration or spots on the textile surface caused by oils, chemicals, or foreign materials.',
        'recommendation': 'Attempt spot cleaning if appropriate for textile type, or cut and discard affected sections.',
        'severity': 'Medium'
    },
    'Vertical': {
        'description': 'Vertical creases or folds that disrupt the textile pattern and structure.',
        'recommendation': 'Apply horizontal tension and steam treatment to remove creases before further processing.',
        'severity': 'Medium'
    }
}

@app.route('/')
def index():
    return render_template('index.html', 
                          title="textile Defect Classifier",
                          defect_types=list(CLASS_INDICES.values()))

# Update your predict route with these changes
@app.route('/predict', methods=['POST'])
def predict():
    print("Predict route accessed")
    
    if 'file' not in request.files:
        print("No file part in the request")
        flash('No file part in the request', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        print("No file selected")
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    print(f"File received: {file.filename}")
    
    try:
        # Generate unique filename
        unique_filename = f"{str(uuid.uuid4())}{os.path.splitext(file.filename)[1]}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        print(f"Saving file to: {file_path}")
        
        file.save(file_path)
        
        # Path relative to the static folder for display
        display_path = os.path.join('uploads', unique_filename)
        
        # Make prediction
        if model is None:
            print("Model not loaded")
            flash('Model not loaded. Please try again later.', 'error')
            return redirect(url_for('index'))
            
        print("Making prediction")
        predicted_class, confidence, all_probabilities = predict_defect(model, file_path, CLASS_INDICES)
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Prepare alternative predictions for low confidence
        # Get indices of top 3 predictions
        top_indices = np.argsort(all_probabilities)[::-1][:3]
        
        # Create list of alternatives with their probabilities
        alternatives = []
        low_confidence = confidence < 0.7  # Define low confidence as below 70%
        
        if low_confidence:
            # Create list of top 3 predictions with their classes and probabilities
            for idx in top_indices:
                class_name = CLASS_INDICES[idx]
                prob = float(all_probabilities[idx])
                if class_name != predicted_class:  # Don't include the main prediction
                    alternatives.append({
                        'class': class_name,
                        'confidence': prob,
                        'info': DEFECT_INFO.get(class_name, {
                            'description': 'Information not available.',
                            'recommendation': 'Consult with a textile specialist.',
                            'severity': 'Unknown'
                        })
                    })
        
        # Save to history
        history_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': timestamp,
            'image': display_path,
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'probabilities': {class_name: float(prob) for class_name, prob in zip(CLASS_INDICES.values(), all_probabilities)}
        }
        
        # Load existing history or create new
        history_file = 'static/history/analysis_history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        # Add new entry and save
        history.append(history_entry)
        with open(history_file, 'w') as f:
            json.dump(history, f)
        
        # Get defect information
        defect_info = DEFECT_INFO.get(predicted_class, {
            'description': 'Information not available for this defect type.',
            'recommendation': 'Consult with a textile specialist.',
            'severity': 'Unknown'
        })
        
        print(f"Prediction complete: {predicted_class} with {confidence} confidence")
        
        # Render result template
        return render_template('result.html',
                              title="Detection Results",
                              predicted_class=predicted_class,
                              confidence=confidence,
                              image_file=display_path,
                              probabilities=list(zip(CLASS_INDICES.values(), all_probabilities)),
                              defect_info=defect_info,
                              timestamp=timestamp,
                              low_confidence=low_confidence,
                              alternatives=alternatives)
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        flash(f'Error in processing: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    history_file = 'static/history/analysis_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    return render_template('history.html', 
                          title="Analysis History",
                          history=history)

@app.route('/about')
def about():
    return render_template('about.html', title="About")

if __name__ == '__main__':
    print("Starting Flask application")
    app.run(debug=True)