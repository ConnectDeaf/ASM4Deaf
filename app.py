from flask import Flask, render_template, request, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from my_config import FILEPATH_ROOT
from datauri import DataURI
import json
import aux_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://test_user:test_pass@localhost/asm4deaf"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

############################### 
## DECLARING DATABASE TABLES ##
###############################
class SignerRacesModel(db.Model):
    __tablename__ = 'signerraces'
 
    RaceID = db.Column(db.Integer, primary_key = True)
    RaceName = db.Column(db.String(50)) 
    head_gifs = db.relationship('HeadsModel', backref='signerraces', lazy=True)
    #torso_gifs = db.relationship('TorsosModel', backref='signerraces', lazy=True)
    #fullbody_gifs = db.relationship('FullbodysModel', backref='signerraces', lazy=True)
    
    def __init__(self, RaceName):
        self.RaceName = RaceName
 
    def __repr__(self):
        return f"RaceID: {self.RaceID}, RaceName :{self.RaceName}"

class SignLanguagesModel(db.Model):
    __tablename__ = 'signlanguages'
 
    LanguageID = db.Column(db.Integer, primary_key = True)
    LanguageName = db.Column(db.String(50))
    #head_gifs = db.relationship('HeadsModel', backref='signerraces', lazy=True)
    #torso_gifs = db.relationship('TorsosModel', backref='signerraces', lazy=True)
    #fullbody_gifs = db.relationship('FullbodysModel', backref='signerraces', lazy=True)
    
    def __init__(self, LanguageName):
        self.LanguageName = LanguageName
 
    def __repr__(self):
        return f"LanguageID: {self.LanguageID}, LanguageName :{self.LanguageName}"

class HeadsModel(db.Model):
    __tablename__ = 'heads'
 
    HeadID = db.Column(db.Integer, primary_key = True)
    Keywords = db.Column(db.String(200))
    VideoURL = db.Column(db.String(1000))
    RaceID = db.Column(db.Integer, db.ForeignKey('signerraces.RaceID'), nullable=False)
    LanguageID = db.Column(db.Integer, db.ForeignKey('signlanguages.LanguageID'), nullable=False)
    
    def __init__(self, Keywords, VideoURL, RaceID, LanguageID):
        self.Keywords = Keywords
        self.VideoURL = VideoURL
        self.RaceID = RaceID
        self.LanguageID = LanguageID
        
 
    def __repr__(self):
        return f"HeadID: {self.HeadID}, Keywords: {self.Keywords}, VideoURL: {self.VideoURL}, RaceID: {self.RaceID}, LanguageID: {self.LanguageID}"



#################################
## CREATING THE SITE ENDPOINTS ##
#################################
@app.route('/new', methods=["POST", "GET"])
@app.route('/new/', methods=["POST", "GET"])
def add_new():
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
                save_directory = FILEPATH_ROOT + "heads\\"
            elif gif_type == "torso":
                save_directory = FILEPATH_ROOT + "torsos\\"
            else:
                save_directory = FILEPATH_ROOT + "fullbodys\\"
                
            filepath = aux_.save_gif_on_the_file_system(request, save_directory)

            ### YET UNFINISHED
            head = HeadsModel(keywords, filepath, signer_race, sign_language)
            db.session.add(head)
            db.session.commit()
            auto_generated_id = head.HeadID
            ###
        except:
            return "Failed to store the GIF!", 500

        #return status message
        return "Successfully stored the GIF!", 201
    else:
        #retrieve sign languages and signer races from the database
        races =  SignerRacesModel.query.all()
        races = [[r.RaceID, r.RaceName] for r in races]
       
        languages =  SignLanguagesModel.query.all()
        languages = [[l.LanguageID, l.LanguageName] for l in languages]
        
        return render_template("new-gif.html", races=races, languages=languages), 200
  



@app.route('/login', methods=["POST", "GET"])#pending
@app.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == 'POST': 
        pass
    else:
        return render_template("login.html")


@app.route('/search', methods=['GET'])#pending
@app.route('/search/', methods=['GET'])
def search():
    
    # form fields presence-check (return the necessary status codes if not correct)
    ## PENDING (type, keywords, gif file)

    # get GIF type (according to which the rest of the steps into this function 
    #                           will be performed or skipped)
    ## PENDING
    
    #query the database to find relevant GIFs (get the GIF ids and local paths)
    ## the table to be queried is determined by the GIF type
    ## PENDING: will it be a one keyword search or many??

    #retrieve and return the related image Ids??


    filepath = FILEPATH_ROOT + "heads\\"
    keywords = "dummy,keyword,csv,list"

    # FOR search-gif.html PAGE! (to be moved)
    #create GIF data URI for preview page
    gif_uri = DataURI.from_file(filepath)
    #return preview page
    return render_template("search-gif.html", keywords=keywords, gif_uri=gif_uri)



@app.route("/retrieve", methods=["GET"])#pending
def retrieve():
    
    #(example) http://10.16.20.182:5000/retrieve?type=heads&id=3
    type = request.args.get('type', None)
    id = request.args.get('id', None)


    #have not yet tried the following 
    # + I want to learn how to render proper image files into an HTML document
    #       (not sure if this is posible with my current setup though)
    
    #DOWNLOAD_DIRECTORY = FILEPATH_ROOT + "heads\\"
    #return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    ## https://medium.com/analytics-vidhya/receive-or-return-files-flask-api-8389d42b0684

    return f"<h1>{type},{id}</h1>"
    




if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)