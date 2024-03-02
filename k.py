from keras.models import load_model
import cv2
import numpy as np

# Step 1: Load the OCR model
model = load_model(r'c:\Users\yassi\Downloads\ar_numbers_v6.h5')

# Step 2: Prepare input image
image = cv2.imread(r'C:\Users\yassi\Desktop\egyptian id project\runs\detect\predict2\crops\national_id\21.jpg')
# Convert the image to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Resize the image to match the expected input shape of the model
image_resized = cv2.resize(image_gray, (64, 64))
# Reshape the image to add batch and channel dimensions
image_reshaped = np.expand_dims(image_resized, axis=0)  # Add batch dimension
image_reshaped = np.expand_dims(image_reshaped, axis=-1)  # Add channel dimension

# Step 3: Make predictions
predictions = model.predict(image_reshaped)

# Step 4: Post-process output
# Process predictions to convert them into human-readable text
# Example: text = postprocess_predictions(predictions)

print("Predicted text:", predictions)  # Print or use the predicted text
