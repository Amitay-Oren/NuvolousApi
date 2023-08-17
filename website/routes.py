# Import necessary modules and packages
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash
from website.models import User, Note, Feedback  # Import your User model
from website import db  # Import your SQLAlchemy instance

# Create a Blueprint for your API routes
api = Blueprint('api', __name__)

# Define a route for user login
@api.route('/login', methods=['POST'])
def login():
    # Get email and password from the JSON request
    email = request.json.get('email')
    password = request.json.get('password')

    # Query the database for the user
    user = User.query.filter_by(email=email).first()

    # Check user credentials and create an access token if valid
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid email or password'), 401

# Define a route for getting user profile
@api.route('/profile', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_profile():
    # Get the user's identity from the token
    user_id = get_jwt_identity()
    
    # Query the database for the user
    user = User.query.get(user_id)

    # Return user profile data as JSON
    return jsonify(email=user.email, first_name=user.first_name), 200

# Define a route for getting user notes
@api.route('/notes', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_notes():
    # Get the user's identity from the token
    user_id = get_jwt_identity()
    
    # Query the database for the user
    user = User.query.get(user_id)

    # Create a list of notes with relevant data
    notes = [{'id': note.id, 'data': note.data, 'date': note.date} for note in user.notes]

    # Return notes data as JSON
    return jsonify(notes=notes), 200

# Define a route for creating a new note
@api.route('/notes', methods=['POST'])
@jwt_required()  # Requires a valid JWT token
def create_note():
    # Get the user's identity from the token
    user_id = get_jwt_identity()
    
    # Query the database for the user
    user = User.query.get(user_id)

    # Get note data from the JSON request
    data = request.json.get('data')

    # Create a new note and add it to the database
    new_note = Note(data=data, user_id=user.id)
    db.session.add(new_note)
    db.session.commit()

    # Return success message as JSON
    return jsonify(message='Note created successfully'), 201

# Define a route for submitting feedback
@api.route('/feedback', methods=['POST'])
@jwt_required()  # Requires a valid JWT token
def submit_feedback():
    # Get the user's identity from the token
    user_id = get_jwt_identity()
    
    # Get feedback content from the JSON request
    content = request.json.get('content')

    # Create new feedback and add it to the database
    new_feedback = Feedback(user_id=user_id, content=content)
    db.session.add(new_feedback)
    db.session.commit()

    # Return success message as JSON
    return jsonify(message='Feedback submitted successfully'), 201



# Define a route for submitting feedback
@api.route('/test', methods=['GET'])
def test():

    return jsonify('Test success'), 200
