from flask import Flask, g # g stands for global variable
from flask_cors import CORS
from flask_login import LoginManager
import models # all the classes and functions are methods on the models object
# name of file is models
# import the blueprint
from api.user import user
############################ DOG BLUEPRINt 
# from api.dog import dog 
DEBUG = True
PORT = 8000
login_manager = LoginManager() # sets up the ability to set up the sesssion
# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__, static_url_path="", static_folder="static")
# const app = express()
app.secret_key = 'RLAKJDRANDOM STRING' # app.use(session({secret_key: 'sdajfds'}))
login_manager.init_app(app) # sets up the session on the app
@login_manager.user_loader # decorator #current_user, or load anything from
# the session
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
# CORS(dog, origins=['http://localhost:3000'], supports_credentials=True)
# setsup the blueprint (controller) in the server file
app.register_blueprint(user)
### REGISTER DOG BLUEPRINT 
# app.register_blueprint(dog)
@app.before_request # givin to us by flask @
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
  
@app.after_request # given to us by flask @
def after_request(response):
    ###Close the database connection after each request####
    g.db.close()
    return response
# The default URL ends in / ("my-website.com/").
@app.route('/') #decorator, anything with the @ is a decorator, and its a function
# before a function
def index(): #name this method whatever
    return 'hi' # res.send in express
# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT) #app.listen in express