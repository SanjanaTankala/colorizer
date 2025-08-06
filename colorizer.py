
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

# Load model without compiling to avoid optimizer compatibility issues
model = load_model('models/model (1).h5', compile=False)

def colorize_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (512, 512))
    image_input = image.astype('float32') / 255.0
    image_input = image_input.reshape((1, 512, 512, 1))
    output = model.predict(image_input)
    output = output[0].reshape((512, 512, 3))
    output = (output * 255).astype('uint8')
    
    # Handle different file extensions
    base_path = os.path.splitext(image_path)[0]
    output_path = base_path + '_colorized.jpg'
    cv2.imwrite(output_path, output)
    return output_path
