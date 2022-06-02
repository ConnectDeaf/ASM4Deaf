from email.policy import default
from flask import Flask, render_template, request, send_file, send_from_directory, Response, session, redirect, url_for, flash, jsonify
from itsdangerous import base64_encode
from flask_sqlalchemy import SQLAlchemy
from my_config import *
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from datauri import DataURI
from datetime import timedelta
from faceswap.openCV.videoFaceSwap.videoFaceSwapping import swap
import json
import aux_
import time
import base64
import os
import hashlib



app = Flask(__name__)
app.secret_key = SESSION_ENCRYPTION_SECRET_KEY
app.permanent_session_lifetime = timedelta(days=USER_SESSION_LIFETIME_IN_DAYS)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_USER_PASSWORD}@{DB_IP_ADDRESS}/{DB_TABLENAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

############################### 
## DECLARING DATABASE TABLES ##
###############################
class UsersModel(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key = True)
    Email = db.Column(db.String(300), primary_key = True) 
    PwdSaltedDigest = db.Column(db.LargeBinary)
    IsVerified = db.Column(db.Integer, default=0)
    
    def __init__(self, Email, PwdSaltedDigest):
        self.Email = Email
        self.PwdSaltedDigest = PwdSaltedDigest

class SignerRacesModel(db.Model):
    __tablename__ = 'signerraces'
 
    RaceID = db.Column(db.Integer, primary_key = True)
    RaceName = db.Column(db.String(50)) 
    BodyParts_gifs = db.relationship('BodyPartsModel', backref='signerraces', lazy=True)
    #fullbody_gifs = db.relationship('FullbodysModel', backref='signerraces', lazy=True)
    
    def __init__(self, RaceName):
        self.RaceName = RaceName

class SignLanguagesModel(db.Model):
    __tablename__ = 'signlanguages'
 
    LanguageID = db.Column(db.Integer, primary_key = True)
    LanguageName = db.Column(db.String(50))
    BodyParts_gifs = db.relationship('BodyPartsModel', backref='signlanguages', lazy=True)
    #fullbody_gifs = db.relationship('FullbodysModel', backref='signlanguages', lazy=True)
    
    def __init__(self, LanguageName):
        self.LanguageName = LanguageName

class BodyPartsModel(db.Model):
    __tablename__ = 'bodyparts'
 
    BodyPartID = db.Column(db.Integer, primary_key = True)
    Keywords = db.Column(db.String(200))
    FileName = db.Column(db.String(1000))
    RaceID = db.Column(db.Integer, db.ForeignKey('signerraces.RaceID'), nullable=False)
    LanguageID = db.Column(db.Integer, db.ForeignKey('signlanguages.LanguageID'), nullable=False)
    PartType = db.Column(db.String(1))#'h' or 't'
    
    def __init__(self, Keywords, FileName, RaceID, LanguageID, PartType):
        self.Keywords = Keywords
        self.FileName = FileName
        self.RaceID = RaceID
        self.LanguageID = LanguageID
        self.PartType = PartType
        

##############################################################
##               CREATING THE SITE ENDPOINTS                ##
##############################################################
#NOTE: The GET endpoint versions return the pages for th UI,
#        the POST endpoint versions do the actual work
##############################################################

@app.route('/users/register', methods=["POST", "GET"])
@app.route('/users/register/', methods=["POST", "GET"])
def register_user():
    '''
        adds an unverified user to the database;
        the administrator needs to login to the database to verify the user later on
    '''  
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            email = request_data['email']
            password = request_data["password"]
        except:
                return "Incorect parameters!", 400

        try:
            #hash password
            salt = os.urandom(32)
            pwd_digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            salted_digest = salt + pwd_digest
        except:
            return "Failed to process (hash) password!", 500

        existence_check_user = UsersModel.query.filter_by(Email=email).first()
        if existence_check_user:
            return "User with this email already exists!", 403

        try:
            #add new unverified user to the database
            new_user_record = UsersModel(email, salted_digest)
            db.session.add(new_user_record)
            db.session.commit()
        except:
            return "Failed store user data into database", 500

        flash("Thak you for your registration! An administrator will examine your request soon.")
        return redirect(url_for("login")), 200
    else:
        if "user" in session:
            flash("You cannot register while you are logged in!", "info")
            return redirect(url_for("login")), 403
        return render_template("register.html"), 200
    

@app.route('/users/login', methods=["POST", "GET"])
@app.route('/users/login/', methods=["POST", "GET"])
def login():

    if request.method == 'POST':
        try:
            request_data = request.get_json()
            email = request_data['email']
            password = request_data["password"]
        except:
                return "Incorect parameters!", 400


        #check if the user is already logged in with another account
        if "user" in session:
            return f"You are logged in with another email ({session['user']})," + \
                            f" please logout and try again with this one!", 403

        #retrieve user data from the database
        found_user = UsersModel.query.filter_by(Email=email).first()
        if not found_user:
            return f"This user ({email}) does not exist!", 404
    
        if not found_user.IsVerified:
            return "This user has not been unverified yet!", 403

        stored_salt = found_user.PwdSaltedDigest[:32]
        stored_salted_digest = found_user.PwdSaltedDigest[32:]

        try:
            #hash password
            pwd_digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt, 100000)
        except:
            return "Failed to hash password", 500

        if not stored_salted_digest == pwd_digest:
            return "Incorrect password!", 403

        #create a permanent session for user
        session.permanent = True
        session["user"] = email

        flash("User successfully logged in!", "info")
        return "User successfully logged in!", 200
    else:
        if "user" in session:
            flash("Already logged in!", "info")
            return redirect(url_for("add_new")), 200
        return render_template("login.html"), 200
            

@app.route("/users/logout", methods=["GET"])
@app.route("/users/logout/", methods=["GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("Succesfully logged out!", "info")
    else:
        flash("User already logged out!", "info")
    return redirect(url_for("login")), 200


@app.route("/users/remove/<email>", methods=["PUT"])#pending
def remove_user(email):
    return "removed", 200
    
@app.route("/users/verify/<email>", methods=["PUT"])#pending
def verify_user(email):
    return "verified", 200


@app.route("/users/manage", methods=["GET"])
@app.route("/users/manage/", methods=["GET"])
def manage_users():
    if not "user" in session:
        flash("You need to log in to access the Managae Users page!", "info")
        return redirect(url_for("login")), 403

    users =  UsersModel.query.order_by(UsersModel.Email.asc()).all()
    users = [[u.UserID, u.Email, u.IsVerified] for u in users]
    return render_template("users.html", users=users), 200


@app.route('/gifs/new', methods=["POST", "GET"])
@app.route('/gifs/new/', methods=["POST", "GET"])
def add_new():
    '''
        stores the uploaded gif to the filesystem and creates the necessary database entry.
        (it does not check for duplicates- I don't see a way to automatically check for duplicates)
    '''

    #regardless of method, check if user is logged in
    if not "user" in session:
        flash("You need to log in to access the Add New GIF page!", "info")
        return redirect(url_for("login")), 403

    if request.method == "POST":
        try:

            gif_type = request.form['gif_type']
            
            try:
                if request.form['new_language_toggle']:
                    try:
                        #insert the new language into the database
                        sign_language_name = request.form["new_language"].lower()
                        for lang in SignLanguagesModel.query.all():
                            if lang.LanguageName == sign_language_name:
                                return "Sign language already exists!", 400
                        new_language_record = SignLanguagesModel(sign_language_name)
                        db.session.add(new_language_record)
                        db.session.commit()
                        sign_language = new_language_record.LanguageID
                    except:
                        return "Failed to create new sign language!", 500
            except:
                sign_language = request.form["sign_languages"]

            signer_race = request.form["signer_race"]
            keywords = request.form["keywords"]
        except:
            return "Incorect parameters!", 400
        
        try:
            if gif_type == "head":
                save_directory = GIF_FILEPATH_ROOT + "heads/"
                unique_filename_prefix = "head"
            elif gif_type == "torso":
                save_directory = GIF_FILEPATH_ROOT + "torsos/"
                unique_filename_prefix = "torso"
            
            unique_filename_suffix = str(int(time.time()))
            unique_filename = f"{unique_filename_prefix}_{unique_filename_suffix}{GIF_FILE_FORMAT}"

            filepath = aux_.save_gif_on_the_file_system(request, save_directory, unique_filename)

            if gif_type == "head":
                new_gif_record = BodyPartsModel(keywords, unique_filename, signer_race, sign_language, 'h')
            elif gif_type == "torso":
                new_gif_record = BodyPartsModel(keywords, unique_filename, signer_race, sign_language, 't')
  
            db.session.add(new_gif_record)
            db.session.commit()
        except:
            aux_.delete_gif_file_from_file_system(filepath)            
            return "Failed to store the GIF!", 500

        return "Successfully stored the GIF!", 201
    else:
        #retrieve sign languages and signer races from the database
        races =  SignerRacesModel.query.all()
        races = [[r.RaceID, r.RaceName] for r in races]
       
        languages =  SignLanguagesModel.query.all()
        languages = [[l.LanguageID, l.LanguageName] for l in languages]
        
        return render_template("new-gif.html", races=races, languages=languages), 200


@app.route('/gifs/retrieve', methods=['POST','GET'])
@app.route('/gifs/retrieve/', methods=['POST', 'GET'])
def get_urls_for():
    '''
        queries the database (using the provided gif type, language and array of keywords)
        and returns a list of relative ids and filenames (to be used for subsequent calls to
        retrieve the GIFs- or simply put together the URL and use in an img html element).
    '''

    #regardless of method, check if user is logged in
    if not "user" in session:
        flash("You need to log in to access the Add New GIF page!", "info")
        return redirect(url_for("login")), 403


    if request.method == 'POST':
        try:
            request_data = request.get_json()
            sign_language = request_data['sign_language']
            gif_type = request_data["gif_type"]
            keywords = request_data["keywords"]
        except:
                return "Incorect parameters!", 400

        try:
            query_str = aux_.prepare_database_keyword_query(sign_language, gif_type, keywords)
            gifs_dict_array = aux_.create_dictionary_array_from_cursor_results(db.engine.execute(query_str))
            augmented_response = { "gif_type" : gif_type,
                                   "gif_matches" : gifs_dict_array}
            return jsonify(augmented_response), 200
        except:
            return "Failed to perform database query.", 500

    else:
        languages =  SignLanguagesModel.query.all()
        languages = [[l.LanguageID, l.LanguageName] for l in languages]
        
        return render_template("query-gif.html", languages=languages), 200


@app.route('/gifs/retrieve/<gif_type>/<path:path>', methods=["GET"])
def retrieve(gif_type, path):
    '''
        returns GIF files
    '''
    if "user" in session:
        return send_from_directory(f'{GIF_FILEPATH_ROOT}/{gif_type}', path)
    else:
        return "Forbidden Access", 403


@app.route('/gifs/faceswap/openCV', methods=["GET"])
def faceswap():
    '''
        creates and returns the requested faceswap using the openCV/DYI faceswapping tool (tool 1)
    '''
    if "user" in session:
        if request.args.get('gif_filename') == None or request.args.get('head_photo') == None:
            return "Incorect arguments!", 400

        gif_filename = request.args.get('gif_filename')
        head_photo = request.args.get('head_photo')

        gif_fullpath = f'{GIF_FILEPATH_ROOT}/{gif_filename}'
        head_photo_fullpath = f'{HEADPHOTOS_FILEPATH_ROOT}/{head_photo}'
        
        unique_filename_prefix = "swap"
        unique_filename_suffix = str(int(time.time()))
        unique_filename = f"{unique_filename_prefix}_{unique_filename_suffix}{SWAPS_FILE_FORMAT}"
        result_fullpath = f"{SWAPS_FILEPATH_ROOT}/{unique_filename}"

        try:
            swap(DETECTOR_FULLPATH, gif_fullpath, head_photo_fullpath, result_fullpath)       
        except e:
            return "Failed to faceswap!", 500

        try:
            return send_from_directory(SWAPS_FILEPATH_ROOT, unique_filename), 200
        except:
            return "Failed to retrieve faceswap video file.", 500
    else:
        return "Forbidden Access", 403

    pass


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
