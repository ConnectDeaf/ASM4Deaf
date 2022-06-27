from email.policy import default
from flask import Flask, render_template, request, send_file, send_from_directory, Response, session, redirect, url_for, flash, jsonify
from itsdangerous import base64_encode
from flask_sqlalchemy import SQLAlchemy
from my_config import *
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from datauri import DataURI
from datetime import timedelta
# from faceswap.openCV.videoFaceSwap.videoFaceSwapping import swap
import json
import aux_
import time
import base64
import os
import hashlib
import shutil



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
    Videos = db.relationship('VideosModel', backref='signerraces', lazy=True)
    
    def __init__(self, RaceName):
        self.RaceName = RaceName

class SignLanguagesModel(db.Model):
    __tablename__ = 'signlanguages'
 
    LanguageID = db.Column(db.Integer, primary_key = True)
    LanguageName = db.Column(db.String(50))
    Videos = db.relationship('VideosModel', backref='signlanguages', lazy=True)
    
    def __init__(self, LanguageName):
        self.LanguageName = LanguageName

class VideosModel(db.Model):
    __tablename__ = 'videos'
 
    VideoID = db.Column(db.Integer, primary_key = True)
    Keywords = db.Column(db.String(200))
    FileName = db.Column(db.String(1000))
    RaceID = db.Column(db.Integer, db.ForeignKey('signerraces.RaceID'), nullable=False)
    LanguageID = db.Column(db.Integer, db.ForeignKey('signlanguages.LanguageID'), nullable=False)
    
    def __init__(self, Keywords, FileName, RaceID, LanguageID):
        self.Keywords = Keywords
        self.FileName = FileName
        self.RaceID = RaceID
        self.LanguageID = LanguageID
        
class ImagesModel(db.Model):
    __tablename__ = 'images'
 
    ImageID = db.Column(db.Integer, primary_key = True)
    FileName = db.Column(db.String(1000))
    
    def __init__(self, FileName):
        self.FileName = FileName
    

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
            return redirect(url_for("add_new_video")), 200
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

@app.route("/users/remove/<email>", methods=["DELETE"])
def remove_user(email):

    if not "user" in session:
        flash("You must be logged in to remove a user!", "info")
        return redirect(url_for("login")), 403

    if session["user"] == email:
        return "You cannot remove yourself! This is to ensure that at least one person has access to this web UI.", 400

    UsersModel.query.filter_by(Email=email).delete()
    db.session.commit()

    return "User successfully removed!", 200
    
@app.route("/users/verify/<email>", methods=["PUT"])
def verify_user(email):
    if not "user" in session:
        flash("You must be logged in to verify a user!", "info")
        return redirect(url_for("login")), 403

    UsersModel.query.filter_by(Email=email).first().IsVerified = 1
    db.session.commit()

    return "User has been verified!", 200
    
@app.route("/users/manage", methods=["GET"])
@app.route("/users/manage/", methods=["GET"])
def manage_users():
    if not "user" in session:
        flash("You need to log in to access the Manage Users page!", "info")
        return redirect(url_for("login")), 403
    users =  UsersModel.query.order_by(UsersModel.UserID.asc()).all()
    users = [[u.UserID, u.Email, u.IsVerified] for u in users]
    return render_template("users.html", users=users), 200

###########################

@app.route('/media/videos/new', methods=["POST", "GET"])
@app.route('/media/videos/new/', methods=["POST", "GET"])
def add_new_video():
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
            save_directory = MEDIA_FILEPATH_ROOT + "videos/"
            thumbnail_save_directory = MEDIA_FILEPATH_ROOT + "thumbnails/video_thumbnails/"
            filename_prefix = "video"
            
            unique_filename_suffix = str(int(time.time()))
            unique_filename = f"{filename_prefix}_{unique_filename_suffix}{VIDEO_FILE_FORMAT}"

            filepath = aux_.save_on_the_file_system(request, "GIFfile" , save_directory, unique_filename)
            thumbnail_filepath = f"{thumbnail_save_directory}{unique_filename}"
            shutil.copy(filepath, thumbnail_filepath)

            new_gif_record = VideosModel(keywords, unique_filename, signer_race, sign_language)
            
            db.session.add(new_gif_record)
            db.session.commit()
        except:
            try:
                aux_.delete_file_from_file_system(filepath)
                aux_.delete_file_from_file_system(thumbnail_filepath)
            except:
                pass

            return "Failed to store the GIF!", 500

        return "Successfully stored the GIF!", 201
    else:
        #retrieve sign languages and signer races from the database
        races =  SignerRacesModel.query.all()
        races = [[r.RaceID, r.RaceName] for r in races]
       
        languages =  SignLanguagesModel.query.all()
        languages = [[l.LanguageID, l.LanguageName] for l in languages]
        
        return render_template("new-video.html", races=races, languages=languages), 200

@app.route('/media/videos/retrieve/original/<path:path>', methods=["GET"])
def retrieve_video_original(path):
    '''
        returns video files
    '''
    if "user" in session:
        return send_from_directory(f'{MEDIA_FILEPATH_ROOT}/videos/', path)
    else:
        return "Forbidden Access", 403

@app.route('/media/videos/retrieve/thumbnail/<path:path>', methods=["GET"])
def retrieve_video_thumbnail(path):
    '''
        returns video files
    '''
    if "user" in session:
        return send_from_directory(f'{MEDIA_FILEPATH_ROOT}/thumbnails/video_thumbnails/', path)
    else:
        return "Forbidden Access", 403

@app.route('/media/videos/retrieve', methods=['POST','GET'])
@app.route('/media/videos/retrieve/', methods=['POST', 'GET'])
def query_video_filenames():
    '''
        queries the database (using the provided language and array of keywords)
        and returns a list of relative ids and filenames (to be used for subsequent calls to
        simply put together the URL and use as a source in a video html element).
    '''

    #regardless of method, check if user is logged in
    if not "user" in session:
        flash("You need to log in to access the Add New GIF page!", "info")
        return redirect(url_for("login")), 403


    if request.method == 'POST':
        try:
            request_data = request.get_json()
            sign_language = request_data['sign_language']
            keywords = request_data["keywords"]
        except:
                return "Incorect parameters!", 400

        try:
            query_str = aux_.prepare_database_keyword_query(sign_language, keywords)
            gifs_dict_array = aux_.create_dictionary_array_from_cursor_results(db.engine.execute(query_str))
            augmented_response = { "gif_matches" : gifs_dict_array}

            return jsonify(augmented_response), 200
        except:
            return "Failed to perform database query.", 500

    else:
        languages =  SignLanguagesModel.query.all()
        languages = [[l.LanguageID, l.LanguageName] for l in languages]
        
        return render_template("query-video.html", languages=languages), 200

@app.route('/media/videos/retrieve/all_filenames', methods=["GET"])
@app.route('/media/videos/retrieve/all_filenames/', methods=["GET"])
def get_all_video_filenames():
    '''
        Retrieves the filenames of all the available videos from the database.
        These filenames must be appended to the URL for video retrieval.
    '''
    
    if "user" in session:
        all_videos =  VideosModel.query.all()
        all_videos = [v.FileName for v in all_videos]
        return jsonify(all_videos), 200
    else:
        return "Forbidden Access", 403

@app.route('/media/videos/retrieve/keywords', methods=["GET"])
@app.route('/media/videos/retrieve/keywords/', methods=["GET"])
def get_all_video_keywords():
    '''
        Retrieves all the available keywords from the database. (no duplicates or empty strings)
    '''
    
    if "user" in session:
        keywords =  VideosModel.query.all()
        keywords_with_duplicates = ""
        for k in keywords:
            keywords_with_duplicates += k.Keywords + ','
        
        keywords_with_duplicates = keywords_with_duplicates.split(',')
        keywords_no_duplicates =  list(filter(None, list(dict.fromkeys(keywords_with_duplicates))))

        return jsonify(keywords_no_duplicates), 200
    else:
        return "Forbidden Access", 403
 
###########################

@app.route('/media/images/retrieve/originals/<path:path>', methods=["GET"])
def retrieve_image_original(path):
    '''
        returns image files
    '''
    if "user" in session:
        return send_from_directory(f'{MEDIA_FILEPATH_ROOT}/images/', path)
    else:
        return "Forbidden Access", 403

@app.route('/media/images/retrieve/thumbnails/<path:path>', methods=["GET"])
def retrieve_image_thumbnail(path):
    '''
        returns image files
    '''
    if "user" in session:
        return send_from_directory(f'{MEDIA_FILEPATH_ROOT}/thumbnails/image_thumbnails/', path)
    else:
        return "Forbidden Access", 403

@app.route('/media/images/new', methods=["POST", "GET"])
@app.route('/media/images/new/', methods=["POST", "GET"])
def add_new_image():
    '''
        stores the uploaded image to the filesystem and creates the necessary database entry.
        (it does not check for duplicates- I don't see a way to automatically check for duplicates)
    '''

    #regardless of method, check if user is logged in
    if not "user" in session:
        flash("You need to log in to access the Add New Image page!", "info")
        return redirect(url_for("login")), 403

    if request.method == "POST":

        try:
            save_directory = MEDIA_FILEPATH_ROOT + "images/"
            thumbnail_save_directory = MEDIA_FILEPATH_ROOT + "thumbnails/image_thumbnails/"
            filename_prefix = "image"
            
            unique_filename_suffix = str(int(time.time()))
            unique_filename = f"{filename_prefix}_{unique_filename_suffix}{IMAGE_FILE_FORMAT}"

            filepath = aux_.save_on_the_file_system(request, "Imagefile", save_directory, unique_filename)
            thumbnail_filepath = f"{thumbnail_save_directory}{unique_filename}"
            shutil.copy(filepath, thumbnail_filepath)

            new_image_record = ImagesModel(unique_filename)
            
            db.session.add(new_image_record)
            db.session.commit()
        except:
            try:
                aux_.delete_file_from_file_system(filepath)
                aux_.delete_file_from_file_system(thumbnail_filepath)
            except:
                pass

            return "Failed to store the image!", 500

        return "Successfully stored the image!", 201
    else:
        return render_template("new-image.html"), 200

@app.route('/media/images/retrieve', methods=["GET"])
@app.route('/media/images/retrieve/', methods=["GET"])#PENDING
def query_image_filenames():
    '''
        Retrieves the filenames of all the available images from the database.
        These filenames must be appended to the URL for image retrieval.
    '''
    
    if "user" not in session:
        return "Forbidden Access", 403

    #get all the image names from the database
    all_images =  ImagesModel.query.all()
    all_images = [i.FileName for i in all_images]

    #PENDING TO pass the related information to the template so it can render the images

    return render_template("all-images.html"), 200
    
@app.route('/media/images/retrieve/all_filenames', methods=["GET"])
@app.route('/media/images/retrieve/all_filenames/', methods=["GET"])
def get_all_image_filenames():
    '''
        Retrieves the filenames of all the available images from the database.
        These filenames must be appended to the URL for image retrieval.
    '''
    
    if "user" in session:
        all_images =  ImagesModel.query.all()
        all_images = [i.FileName for i in all_images]
        return jsonify(all_images), 200
    else:
        return "Forbidden Access", 403

###########################

# @app.route('/faceswap/openCV', methods=["GET"]) #PENDING
# def faceswap_with_ids():
#     '''
#         creates and returns the requested faceswap using the openCV/DYI faceswapping tool (tool 1)
#     '''
#     if "user" in session:
#         if request.args.get('gif_filename') == None or request.args.get('head_photo') == None:
#             return "Incorect arguments!", 400


#         ## PENDING ## : GET IDs + USE DB & PASSED IDs TO GET IMAGE AND VIDEO NAMEs
#         gif_filename = request.args.get('gif_filename')
#         head_photo = request.args.get('head_photo')

#         gif_fullpath = f'{GIF_FILEPATH_ROOT}/{gif_filename}'
#         head_photo_fullpath = f'{HEADPHOTOS_FILEPATH_ROOT}/{head_photo}'
#         ###############
        
#         unique_filename_prefix = "swap"
#         unique_filename_suffix = str(int(time.time()))
#         unique_filename = f"{unique_filename_prefix}_{unique_filename_suffix}{SWAPS_FILE_FORMAT}"
#         result_fullpath = f"{SWAPS_FILEPATH_ROOT}/{unique_filename}"

#         try:
#             swap(DETECTOR_FULLPATH, gif_fullpath, head_photo_fullpath, result_fullpath)       
#         except e:
#             return "Failed to faceswap!", 500

#         try:
#             return send_from_directory(SWAPS_FILEPATH_ROOT, unique_filename), 200
#         except:
#             return "Failed to retrieve faceswap video file.", 500
#     else:
#         return "Forbidden Access", 403

# @app.route('/faceswap/openCV', methods=["POST"]) #PENDING
# def faceswap_with_user_image():
#     '''
#         creates and returns the requested faceswap using the openCV/DYI faceswapping tool (tool 1)
#         faceswapping image is the user's face (they took a picture of themselves)
#     '''
#     if "user" in session:
#         if request.args.get('gif_filename') == None or request.args.get('head_photo') == None:
#             return "Incorect arguments!", 400

#         gif_filename = request.args.get('gif_filename')
#         head_photo = request.args.get('head_photo')

#         ## PENDING ## : RETRIEVE THE USER'S FACE-FILE + USE DB & PASSED ID TO GET THE VIDEO NAME
#         gif_fullpath = f'{GIF_FILEPATH_ROOT}/{gif_filename}'
#         head_photo_fullpath = f'{HEADPHOTOS_FILEPATH_ROOT}/{head_photo}'
#         ###############
        
#         unique_filename_prefix = "swap"
#         unique_filename_suffix = str(int(time.time()))
#         unique_filename = f"{unique_filename_prefix}_{unique_filename_suffix}{SWAPS_FILE_FORMAT}"
#         result_fullpath = f"{SWAPS_FILEPATH_ROOT}/{unique_filename}"

#         try:
#             swap(DETECTOR_FULLPATH, gif_fullpath, head_photo_fullpath, result_fullpath)       
#         except e:
#             return "Failed to faceswap!", 500

#         try:
#             return send_from_directory(SWAPS_FILEPATH_ROOT, unique_filename), 200
#         except:
#             return "Failed to retrieve faceswap video file.", 500
#     else:
#         return "Forbidden Access", 403



if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
