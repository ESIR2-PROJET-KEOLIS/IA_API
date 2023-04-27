import time
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from flask_cors import CORS
import os

import onnxruntime


from sys import stdout
from loguru import logger as log

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


def load_model(model_path):
    # Load the ONNX model into the runtime
    sess = onnxruntime.InferenceSession(model_path)
    return sess


def run_model(sess, input_array):
    # Run the model with the input array
    output = sess.run(None, {'input': input_array})
    return output[1][0]


# Load the model


@app.route('/predict/Nombus=<nomBus>&Sens=<sens>', methods=['POST'])
def predict(nomBus, sens):

    model_name = 'model_' + nomBus + '_sens' + sens
    if model_name not in models:
        log.error("Model not found")
        return 'Model not found', 404
    model = models[model_name]
    log.info("Model found : " + model_name)

    # get the data from the POST request.
    data = request.form.to_dict()

    # convert data into a dataframe
    data.update((x, [y]) for x, y in data.items())

    data_df = pd.DataFrame.from_dict(data)
    # Convert the dataframe to a numpy array (if needed by the model)

    input_data = data_df.to_numpy().astype(np.float32)

    # Get predictions
    result = run_model(model, input_data)
    log.info(result)

    return result


if __name__ == '__main__':

    log.remove()
    log.add(stdout, format="{time} {level} {message}", level="INFO")
    log.add("./logs/IA.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="1 week",
            retention="1 month", level="DEBUG")

    log.info("Loading models")
    models = {}
    model_dir = 'Models/'
    for file in os.listdir(model_dir):
        if file.endswith(".onnx"):
            model_path = os.path.join(model_dir, file)
            model_name = file.split('.')[0]
            models[model_name] = load_model(model_path)

    log.info("Models loaded")
    log.info(models)

    log.info("Starting server")
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)
