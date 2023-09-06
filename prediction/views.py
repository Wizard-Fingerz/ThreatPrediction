from django.shortcuts import render
from .models import cnn_predict  # Replace 'your_module' with the actual module containing cnn_predict
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PredictionForm  # Replace with the actual form you create
from tensorflow.keras.models import load_model
import numpy as np

# Load your pre-trained Keras model
model_path = 'model/dumped.keras'  # Replace with the actual path to your model
cnn_model = load_model(model_path)


# def predict(request):
#     if request.method == 'POST':
#         protocol = request.POST.get('protocol')
#         sourcePort = request.POST.get('sourcePort')
#         destPort = request.POST.get('destPort')
#         size = request.POST.get('size')
#         seqNumber = request.POST.get('seqNumber')
#         ackNumber = request.POST.get('ackNumber')

#         # Ensure that all input values are valid and properly formatted.
#         # You may need to perform data validation and conversion here.

#         # Prepare the input data for your machine learning model
#         input_data = [protocol, sourcePort, destPort, size, seqNumber, ackNumber]

#         # Make predictions using the model
#         predictions = cnn_predict(input_data)
#         print(predictions)

#         # You can then pass the predictions to your template to display them
#         context = {'predictions': predictions}

#         return render(request, 'predict.html', context)

#     return render(request, 'predict.html')


class_labels = {
    0: 'benign',
    1: 'malicious',  # Replace with the actual label for the other class
}


# Define a view to handle predictions
def predict(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            protocol = float(request.POST.get('protocol'))
            sourcePort = float(request.POST.get('sourcePort'))
            destPort = float(request.POST.get('destPort'))
            size = float(request.POST.get('size'))
            seqNumber = float(request.POST.get('seqNumber'))
            ackNumber = float(request.POST.get('ackNumber'))


            # Preprocess the input data
            input_data = np.array([protocol, sourcePort, destPort, size, seqNumber, ackNumber])
            input_data = input_data.reshape(1, 6, 1, 1)  # Reshape to match model input shape

            # Make predictions using the model
            predictions = cnn_model.predict(input_data)
            prediction_result = predictions[0][0]  # Extract the prediction result
            predicted_class = class_labels[int(round(predictions[0][0]))]

            # You can pass the class label to your template for display
            context = {'predicted_class': predicted_class}

            return render(request, 'predict.html', context)

    else:
        form = PredictionForm()  # Create a new instance of the form if it's a GET request

    return render(request, 'forms.html', {'form': form})

# Add any other views or functions as needed for your application
