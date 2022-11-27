from io import BytesIO
from urllib import request
from PIL import Image
import tflite_runtime.interpreter as tflite
import numpy as np

# import model into global variable
interpreter = tflite.Interpreter(model_path='dino-vs-dragon-v2.tflite')
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']



def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_image(img):
    return (np.array([np.array(img)]) * 1./255).astype(np.float32)

def predict(url):
    img = download_image(url)
    img = prepare_image(img,(150,150))
    X = preprocess_image(img)
    interpreter.set_tensor(input_index,X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    if preds >= 0.5:
        out = 'dragon'
    else:
        out = 'dino'
    return {out:float(preds)}

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result
