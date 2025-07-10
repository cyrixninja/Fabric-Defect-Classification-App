# Fabric Defect Classification

This project is a Flask web application for classifying Fabric defects using a pre-trained deep learning model. The application allows users to upload images of Fabric, which are then processed and classified based on the trained model.

## Project Structure

```
Fabric-defect-classification
├── app.py                     # Main entry point of the Flask application
├── models                     # Directory containing the trained model
│   └── Fabric_defect_model.h5 # Trained model for Fabric defect classification
├── static                     # Directory for static files
│   ├── css                    # Directory for CSS files
│   │   └── style.css          # Styles for the web application
│   ├── js                     # Directory for JavaScript files
│   │   └── main.js            # Client-side functionality
│   └── uploads                # Directory for temporarily storing uploaded images
├── templates                  # Directory for HTML templates
│   ├── index.html             # Homepage template with image upload form
│   └── result.html            # Template for displaying classification results
├── utils                      # Directory for utility functions
│   └── preprocessing.py        # Functions for image preprocessing
├── requirements.txt           # List of dependencies for the application
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd Fabric-defect-classification
   ```

2. **Install the required dependencies:**
   It is recommended to create a virtual environment before installing the dependencies.
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   python app.py
   ```
   The application will start on `http://127.0.0.1:5000/`.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Use the upload form to select an image of Fabric.
3. Click the "Upload" button to submit the image for classification.
4. The results will be displayed on a new page, showing the predicted defect class and confidence level.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.