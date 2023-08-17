from flask import Blueprint, request, jsonify, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, status = 'success'), 200
    return jsonify(message='Invalid email or password'), 401

@auth.route('/logout')  # This route can be removed since you won't need it with JWT
def logout():
    # Logout logic if needed
    return redirect(url_for('auth.login'))  # Redirect to the login page

@auth.route('/api/sign-up', methods=['POST'])
def sign_up():
    email = request.json.get('email')
    first_name = request.json.get('firstName')
    password1 = request.json.get('password')

    new_user = User(email=email, first_name=first_name, password=generate_password_hash(
        password1, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify(access_token=access_token, status='success'), 201

# Other auth routes (like reset password, etc.) can be adapted in a similar manner.
