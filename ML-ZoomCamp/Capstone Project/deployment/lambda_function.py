import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor

# defining preprocessing function
preprocessor = create_preprocessor('xception', target_size=(300, 300))

# defining of model
interpreter = tflite.Interpreter(model_path='cutlery-prod.tflite')
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

# defining of classes to predict from
classes = ['cup', 'fork', 'glass', 'knife', 'plate', 'spoon']

def predict(url):
    X = preprocessor.from_url(url)
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    float_predictions = preds[0].tolist()
    max_value = max(float_predictions)
    max_index = float_predictions.index(max_value)
    return classes[max_index]

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result
