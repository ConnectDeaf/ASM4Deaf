from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from my_config import FILEPATH_ROOT
import aux_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://test_user:test_pass@localhost/asm4deaf"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
class HeadModel(db.Model):
    __tablename__ = 'heads'
 
    HeadID = db.Column(db.Integer, primary_key = True)
    Keywords = db.Column(db.String(200))
    VideoURL = db.Column(db.String(1000))
 
    def __init__(self, Keywords, VideoURL):
        self.Keywords = Keywords
        self.VideoURL = VideoURL
 
    def __repr__(self):
        return f"HeadID: {self.HeadID}, Keywords :{self.Keywords}, VideoURL: {self.VideoURL}"

@app.route('/login', methods=["POST", "GET"])
@app.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template("login.html")

@app.route('/new', methods=["POST", "GET"])
@app.route('/new/', methods=["POST", "GET"])
def add_new():
    if request.method == "POST":
        try:
            
            # form fields and files presence-check (return the necessary status codes if not correct)
            ## PENDING (type, keywords, gif file)

            # get GIF type (according to which the rest of the steps into this function 
            #                           will be performed or skipped)
            ## PENDING: must adapt the input form (add 3 radio buttons)

            # create the target save-location path
            ## PENDING
            filepath_root = FILEPATH_ROOT + "heads\\" 

            # store the received GIF on the file system
            aux_.save_gif_on_the_file_system(request, filepath_root)

            #get keywords 
            keywords = request.form["keywords"]

            #save keywords and URL in the database
            # PENDING

            #return status message
            return "Successfully added GIF to the database!"
        except:
            # return status message
            # this is just for the UI
            # PENDING: append the actual error message to this sentence
            return "Failed to add GIF to the database!" 


        # FOR search-gif.html PAGE! (to be moved)
        #create GIF data URI for preview page
        #gif_uri = DataURI.from_file(filepath)
        #return preview page
        #return render_template("search-gif.html", keywords=keywords, gif_uri=gif_uri)
    else:
        return render_template("new-gif.html")
 
 
@app.route('/search', methods=['GET'])
@app.route('/search/', methods=['GET'])
def search():
    pass






if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)