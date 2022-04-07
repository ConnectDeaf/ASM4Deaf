from email.policy import default
from flask import Flask, render_template, request, send_file, send_from_directory, Response, session
from itsdangerous import base64_encode
from requests_toolbelt import MultipartEncoder
from flask_sqlalchemy import SQLAlchemy
from my_config import GIF_FILEPATH_ROOT
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from datauri import DataURI
import json
import aux_
import time
import base64
import os
import hashlib


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://test_user:test_pass@localhost/asm4deaf"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

############################### 
## DECLARING DATABASE TABLES ##
###############################
class UsersModel(db.Model):
    __tablename__ = 'users'

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

@app.route('/users/register', methods=["POST"])#pending (currently only able to be used only via Postman- for testing)
@app.route('/users/register/', methods=["POST"])
def register_user():
    '''
        adds an unverified user to the database;
        the administrator needs to login to the database to verify the user later on
    '''  

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
        return "Failed to hash password", 500

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

    return "Unverified user successfully added to the database", 200
    

@app.route('/users/login', methods=["POST", "GET"])#pending (user sessions + might possibly change)
@app.route('/users/login/', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        
        try:
            request_data = request.get_json()
            email = request_data['email']
            password = request_data["password"]
        except:
                return "Incorect parameters!", 400

        #retrieve user data from the database
        found_user = UsersModel.query.filter_by(Email=email).first()
        if not found_user:
            return "User not found", 404
        
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

        return "Successfully logged in!", 200

    else:
        return render_template("login.html")


@app.route('/gifs/new', methods=["POST", "GET"])#pending (user sessions)
@app.route('/gifs/new/', methods=["POST", "GET"])
def add_new():
    '''
        stores the uploaded gif to the filesystem and creates the necessary database entry.
        (it does not check for duplicates- I don't see a way to automatically check for duplicates)
    '''
    if request.method == "POST":
         
        try:
            gif_type = request.form['gif_type']
            sign_language = request.form["sign_languages"]
            signer_race = request.form["signer_race"]
            keywords = request.form["keywords"]
        except:
            return "Incorect parameters!", 400
        
        try:
            if gif_type == "head":
                save_directory = GIF_FILEPATH_ROOT + "heads\\"
                unique_filename_prefix = "head"
            elif gif_type == "torso":
                save_directory = GIF_FILEPATH_ROOT + "torsos\\"
                unique_filename_prefix = "torso"
            
            unique_filename_suffix = str(int(time.time()))
            unique_filename = f"{unique_filename_prefix}_{unique_filename_suffix}.gif"

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


@app.route("/gifs/retrieve", methods=["POST"])#pending (everything)
@app.route("/gifs/retrieve/", methods=["POST"])
def retrieve():
    '''
        retrieves multiple GIFs from the database using their type and id
    '''
    
    filename = "torso_1648734447.gif"
    DOWNLOAD_DIRECTORY = GIF_FILEPATH_ROOT + "torsos\\"
    f1 = DOWNLOAD_DIRECTORY + filename
    f2 = f1

    filenames = [f1, f2]
    

    #RETURN MULTIPLE FILES - OPTION 1: MULTIPART ENCODED FILE
    # files_dict = {}
    # for fn_index in range(len(filenames)):
    #     files_dict[f'f_{fn_index}'] = (filenames[fn_index], open(f1, 'rb'), 'text/plain')
    # m = MultipartEncoder(files_dict)
    # return Response(m.to_string(), mimetype=m.content_type), 200
    
    #RETURN MULTIPLE FILES - OPTION 2: json with Base64 strings (can also return the URIs instead of Base64 encoding)
    # type = "heads"
    # files_dict = {
    #     "heads" : [],
    #     "torsos": [],
    #     "fullbodys": []
    # }
    # for fn_index in range(len(filenames)):
    #     file_data_as_str = base64.b64encode(open(filenames[fn_index], 'rb').read()).decode("ascii")
    #     file = {
    #         "id" : f'dummy_{fn_index}',
    #         "data": file_data_as_str
    #     }

    #     files_dict[type].append(file)
    # return json.dumps(files_dict), 200

    #RETURN MULTIPLE FILES - OPTION 3: ZIP FILE
    # memory_file = BytesIO()
    # with ZipFile(memory_file, 'w') as zf:
    #     for fn in filenames:
    #         zf.write(fn)
    # memory_file.seek(0)
    # return send_file(memory_file, attachment_filename='result.zip', as_attachment=True)
    return


@app.route('/gifs/query', methods=['POST','GET'])#pending (everything)
@app.route('/gifs/query/', methods=['POST', 'GET'])
def query():
    '''
        searches the database (using the provided gif type, language and array of keywords)
        and returns a list of relative ids.
    '''

    #NOTE TO SELF: get the "array of keywords" in the same manner as the csv from add_new function
    #            (json stringify before returning it!)
    #            Can also use the same method as for adding tags (for searching them this time)
    #            at the front end.
    #  SOS: will have to test this function from Postman!

    if request.method == 'POST':
        # form fields presence-check (type, language, keywords)
        ## PENDING

        #query the database to find relevant GIFs (get the GIF ids)
        ## the table to be queried is determined by the GIF type
        ## PENDING

        #retrieve and return the related image Ids
        ##PENDING
        
        return "something - PENDING", 200
    else:
        return render_template("query-gif.html"), 200



if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)