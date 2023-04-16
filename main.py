from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from flask_cors import CORS
import os

import onnxruntime

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
    model_path = 'Models/model_' + nomBus+'_sens'+ sens + '.onnx'
    # verify the model exists
    if not os.path.exists(model_path):
        return 'Model not found', 404

    model = load_model(model_path)

    # get the data from the POST request.
    data = request.form.to_dict()
    # convert data into a dataframe
    data.update((x, [y]) for x, y in data.items())
    data_df = pd.DataFrame.from_dict(data)
    # Convert the dataframe to a numpy array (if needed by the model)
    input_data = data_df.to_numpy().astype(np.float32)

    # Get predictions
    result = run_model(model, input_data)
    return result


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=5001)
