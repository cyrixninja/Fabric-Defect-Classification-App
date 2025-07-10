import tensorflow as tf
import numpy as np

def load_and_preprocess_image(image_path, img_height=224, img_width=224):
    """
    Load and preprocess a single image for prediction
    """
    # Load the image
    img = tf.keras.preprocessing.image.load_img(
        image_path, target_size=(img_height, img_width)
    )
    
    # Convert to array and add batch dimension
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Normalize pixel values
    img_array = img_array / 255.0
    
    return img_array

def predict_defect(model, image_path, class_indices):
    """
    Predict the defect class for a single image
    """
    # Preprocess the image
    processed_img = load_and_preprocess_image(image_path)
    
    # Make prediction
    predictions = model.predict(processed_img)
    predicted_class_idx = np.argmax(predictions[0])
    
    # Get the class name directly from class_indices dict
    predicted_class = class_indices[predicted_class_idx]
    confidence = float(predictions[0][predicted_class_idx])
    
    return predicted_class, confidence, predictions[0]