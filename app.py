from flask import Flask, render_template, request, jsonify
from database.db_operations import get_samples_by_criteria

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    criteria = request.json
    samples = get_samples_by_criteria(criteria)
    return jsonify(samples)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
