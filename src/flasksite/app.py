from flask import Flask, render_template, url_for
import numpy as np

# have to go one level up to access our modules
import sys
import os
sys.path.append(os.path.abspath('..'))
from visualizer import Visualizer
from data_processor import DataProcessor
from algorithms import CustomPrecipitationPredictor, custom_clustering, detect_anomalies

app = Flask(__name__)

# Load and preprocess data
processor = DataProcessor("../../data/climate_data.json")
processor.load_data()
processor.clean_data()
x, y = processor.get_features_and_target() # get dates and values

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/predict')
def predict():
   return render_template('predict.html')

@app.route('/cluster')
def cluster():
    data = list(zip(x, y))
    labels = custom_clustering(np.array(data), n_clusters=2)
    clustergraph = Visualizer.plot_clustered_data(data, labels.tolist())
    print("Type of clustergraph:", type(clustergraph))
    return render_template('cluster.html', clustergraph=clustergraph)

@app.route('/anomalies')
def anomalies():
   return render_template('anomalies.html')

@app.route('/data')
def data():
   return render_template('data.html')

if __name__ == '__main__':
   app.run(debug = True)
