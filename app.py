from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.models import load_model
import numpy as np
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads/'
model = load_model('jambu_pepaya_class_model.h5')

class_dict = {0: 'Jambu', 1: 'Pepaya'}

def predict_label(img_path):
    query = cv2.imread(img_path)
    output = query.copy()
    query = cv2.resize(query, (32, 32))
    q = []
    q.append(query)
    q = np.array(q, dtype='float') / 255.0
    q_pred = model.predict(q)
    predicted_bit = q_pred * 10
    print(predicted_bit)
    if(predicted_bit < 1):
        predicted_bit = 0
    if(predicted_bit > 1):
        predicted_bit = 1

    return class_dict[predicted_bit]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(img_path)
            prediction = predict_label(img_path)
            return render_template('index.html', uploaded_image=image.filename, prediction=prediction)

    return render_template('index.html')

@app.route('/display/<filename>')
def send_uploaded_image(filename=''):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)