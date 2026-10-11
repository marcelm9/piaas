import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURE THE DATABASE
# We use an environment variable 'DATABASE_URL' so you can easily point 
# your 3 Docker worker VMs to the dedicated PostgreSQL VM later.
# Fallback is a local SQLite file for testing before you set up Docker.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///local_test.db' 
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DEFINE THE DATABASE MODEL
class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(100), nullable=False)
    stream_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database tables if they don't exist
with app.app_context():
    db.create_all()

# EMBEDDED HTML TEMPLATE (Keeps the project to a single Python file)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NERDS uc - Wild Cam Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        .form-group { margin-bottom: 15px; }
        input[type="text"] { width: 100%; padding: 8px; box-sizing: border-box; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h1>NERDS uc - Wild Cam Tracker</h1>
        
        <h3>Log a New Sighting</h3>
        <form action="{{ url_for('add_observation') }}" method="POST">
            <div class="form-group">
                <label>Animal Name:</label>
                <input type="text" name="animal_name" placeholder="e.g., Brown Bear" required>
            </div>
            <div class="form-group">
                <label>Stream Location:</label>
                <input type="text" name="stream_name" placeholder="e.g., Brooks Falls Cam 1" required>
            </div>
            <button type="submit">Submit Sighting</button>
        </form>

        <h3>Observation Log</h3>
        <table>
            <tr>
                <th>ID</th>
                <th>Animal</th>
                <th>Stream</th>
                <th>Timestamp (UTC)</th>
            </tr>
            {% for obs in observations %}
            <tr>
                <td>{{ obs.id }}</td>
                <td>{{ obs.animal_name }}</td>
                <td>{{ obs.stream_name }}</td>
                <td>{{ obs.timestamp.strftime('%Y-%m-%d %H:%M:%S') }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="4">No observations logged yet.</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

# ROUTES
@app.route('/')
def index():
    # Fetch all observations from the database, ordered by newest first
    observations = Observation.query.order_by(Observation.timestamp.desc()).all()
    return render_template_string(HTML_TEMPLATE, observations=observations)

@app.route('/add', methods=['POST'])
def add_observation():
    # Get data from the form
    animal = request.form.get('animal_name')
    stream = request.form.get('stream_name')
    
    if animal and stream:
        # Save to database
        new_obs = Observation(animal_name=animal, stream_name=stream)
        db.session.add(new_obs)
        db.session.commit()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # host='0.0.0.0' is REQUIRED for Docker. It tells Flask to listen on all network interfaces.
    app.run(host='0.0.0.0', port=8000)
