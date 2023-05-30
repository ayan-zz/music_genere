from flask import Flask, render_template, jsonify
from src.components.data_ingestion import data_ingestion
from src.components.data_transformation import data_transformation

# Initialize your Flask application
app = Flask(__name__)
app.template_folder = 'templates'
# Define your home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define your API endpoint
@app.route('/data', methods=['GET'])
def get_data():

    obj=data_ingestion()
    raw_data=obj.initiate_data_ingestion()

    transformation_obj=data_transformation()
    results=transformation_obj.initiate_data_trasformation(raw_data)
   
    return render_template("result.html",results=results)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
