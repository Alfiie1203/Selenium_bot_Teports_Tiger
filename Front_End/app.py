import json
from flask import Flask, render_template, jsonify, request
import sys
import os

# Add home directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Back_End.routes import tiger_processes

# Create the Flask application
app = Flask(__name__,
    template_folder='Template', 
    static_url_path='/Template', 
    static_folder='Template' 
)

app.config['DEBUG'] = True 
app.register_blueprint(tiger_processes, url_prefix='/')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)