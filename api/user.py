# this is like the controller in express
import models
# obviously the models, models.Dog, models.User
import os
import sys
import secrets
from PIL import Image
### ignoring at the moment  
from flask import Blueprint, request, jsonify, url_for, send_file
# Blueprint - they record opertions to execute,
# thier controllers
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict # from peewee
# first argument, is the blueprint name
# second arg - is its import name
# 3 arg = this is what every route in the blueprint
# should start with much app.use('/api/v1', fruitsController)
# this will have to be registered in the app.py file
user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():
    print(request)
    print(type(request))
    # this is how we grab the image being sent over
    # this has the form info in teh dict
    # we change the request object into a dictionary so
    # we can see inside it
    payload = request.form.to_dict()

    payload['email'].lower() # make emails all lower case!
    try:
        # check to see if the email exist, if it does let the user know
        models.User.get(models.User.email == payload['email'])# query
        # trying to find a user by thier email
        #if models.User.get exists then respond to the client
        return jsonify(data={}, status={"code": 401, "message": "A user with that name or email exists"})
    except models.DoesNotExist: # boolean on the model
        # otherwise create and register the user
        # hash password using bcrypt
        payload['password'] = generate_password_hash(payload['password'])
        # function that will save the image as a static asset in our static
        # save_picture is helper function we will create
        # add the image property to payload dictionary and
        #  save the file_path of our image in the db
        ## Create the ROw in the sql table
        user = models.User.create(**payload) # the spread operator in javascript
        # same as above this is the longhand
        # user = models.User.create(username=payload['username'], password=payload['password'])
        # start the user session
        login_user(user) # login_user is from flask_login, will set user id in session
        # we can't send back a class we can only send back dicts, lists
        user_dict = model_to_dict(user)
        # make our response object jsonifyable
        # lists, hashs, simple datatype like number bools,
        # NO class or instance of class
        # remove the password, client doesn't need to know
        del user_dict['password']
        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '<-payload')
    user = models.User.get(models.User.username == payload['username'])
    user_dict = model_to_dict(user)
    print(user_dict, 'user_dict in login route')
    if(check_password_hash(user_dict['password'], payload['password'])):
        login_user(user)
        del user_dict['password']
        print(current_user, '<-current user')
        print(user_dict, '<-user_dict')
        return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
    else:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})