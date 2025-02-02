from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import tensorflow as tf
from PIL import Image
import numpy as np
import io

# Your list of class labels
class_labels = [
    "apple", "banana", "beetroot", "bell pepper", "cabbage", "capsicum",
    "carrot", "cauliflower", "chilli pepper", "corn", "cucumber", "eggplant", 
    "garlic", "ginger", "grapes", "jalepeno", "kiwi", "lemon", "lettuce", 
    "mango", "onion", "orange", "paprika", "pear", "peas", "pineapple", 
    "pomegranate", "potato", "raddish", "soy beans", "spinach", "sweetcorn", 
    "sweetpotato", "tomato", "turnip", "watermelon"
]


# predicted_class_name = class_labels[predicted_class]
# print(predicted_class_name)

# Load the saved model
model = tf.keras.models.load_model('C:\D\Programming\Learning\AIML\Fruit&Veg_recognition\Final app\model api\Fruit_Veg_recognition/fruit&vegetable_model.h5')

class PredictFoodView(APIView):         
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            # Get the uploaded image
            image_file = request.FILES['image']
            
            print(f"Received file: {image_file.name}")  # Log file name for debugging

            # Open the image and preprocess it
            image = Image.open(image_file).convert('RGB')
            image = image.resize((224, 224))  # Resize to match the model's input
            image_array = np.array(image) / 255.0  # Normalize
            image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
            
            # Make a prediction
            predictions = model.predict(image_array)
            predicted_class = np.argmax(predictions, axis=1)[0]
            predicted_class_name = class_labels[predicted_class]
            # Return the prediction as a response
            #return Response({'predicted_class': int(predicted_class)}, status=200)
            return Response({'predicted_class': predicted_class_name}, status=200)
        
        except Exception as e:
            return Response({'error': str(e)}, status=400)
