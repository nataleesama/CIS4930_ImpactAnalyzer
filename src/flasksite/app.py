from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/predict')
def predict():
   return render_template('predict.html')

@app.route('/cluster')
def cluster():
   return render_template('cluster.html')

@app.route('/anomalies')
def anomalies():
   return render_template('anomalies.html')

if __name__ == '__main__':
   app.run(debug = True)