from flask import Flask, render_template, url_for, redirect
import numpy as np
import json
from plotly.io import to_html

# have to go one level up to access our modules
import sys
import os
sys.path.append(os.path.abspath('..'))
from visualizer import Visualizer
from data_processor import DataProcessor
from algorithms import CustomPrecipitationPredictor

app = Flask(__name__)


miamiProcessor = DataProcessor("../../data/miamiData.json")
orlandoProcessor = DataProcessor("../../data/orlandoData.json")
tallahasseeProcessor = DataProcessor("../../data/tallahasseeData.json")
    
miamiProcessor.load_data()
miamiProcessor.clean_data()
mx, my = miamiProcessor.get_features_and_target() # get dates and values
mz = miamiProcessor.get_precipitation()
    
orlandoProcessor.load_data()
orlandoProcessor.clean_data()
ox, oy = orlandoProcessor.get_features_and_target()
oz = orlandoProcessor.get_precipitation()
    
tallahasseeProcessor.load_data()
tx, ty = tallahasseeProcessor.get_features_and_target()
tz = tallahasseeProcessor.get_precipitation()
tx_unnorm = tallahasseeProcessor.unnormalized_date()

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/predict')
def predict():
    tallahasseeProcessor = DataProcessor("../../data/tallahasseeData.json")
    tallahasseeProcessor.load_data()
    tx, ty = tallahasseeProcessor.get_features_and_target()
    tx_unnorm = tallahasseeProcessor.unnormalized_date()

    model = CustomPrecipitationPredictor()
    model.fit(tx, ty)
    predictions = model.predict(tx)

    fig = Visualizer.plot_precipitation_trend_html(tx_unnorm, ty.tolist(), predictions.tolist())
    plot_html = to_html(fig, full_html=False, include_plotlyjs='cdn')
    return render_template("predict.html", plot=plot_html)


@app.route('/cluster')
def cluster():
    data = list(zip(x, y))
    labels = custom_clustering(np.array(data), n_clusters=2)
    clustergraph = Visualizer.plot_clustered_data(data, labels.tolist())
    print("Type of clustergraph:", type(clustergraph))
    return render_template('cluster.html', clustergraph=clustergraph)

@app.route('/anomalies')
def anomalies():
    model = CustomPrecipitationPredictor()

    # Prepare station data dictionary
    station_data = {
        'Tallahassee': {
            'values': tz,
            'anomalies': model.detect_anomalies(tx, tz)[0]
        },
        'Miami': {
            'values': mz,
            'anomalies': model.detect_anomalies(mx, mz)[0]
        },
        'Orlando': {
            'values': oz,
            'anomalies': model.detect_anomalies(ox, oz)[0]
        }
    }
    plot_html = Visualizer.plot_anomalies_to_html(station_data)  # call your function
    return render_template('anomalies.html', plot_html = plot_html)


@app.route('/algorithms')
def algorithms():
    return render_template("algorithms.html")

if __name__ == '__main__':
    app.run(debug = True)
