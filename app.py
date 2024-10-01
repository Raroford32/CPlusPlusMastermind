from flask import Flask, render_template, request, jsonify
from database.db_operations import get_samples_by_criteria, get_project_structures, get_project_details

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    criteria = request.json
    samples = get_samples_by_criteria(criteria)
    return jsonify(samples)

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = get_project_structures()
    return jsonify(projects)

@app.route('/project/<int:project_id>', methods=['GET'])
def get_project_details(project_id):
    project = get_project_details(project_id)
    return jsonify(project)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
