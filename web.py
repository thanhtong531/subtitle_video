from flask import Flask,redirect,url_for,render_template,request,send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flaskext.mysql import MySQL
import pymysql
import os

from io import BytesIO
import time
from datetime import datetime

app = Flask(__name__,template_folder="templates",static_folder="templates/admin")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 't/'
app.config['time_start'] = ''
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB']='luanvan'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/",methods=["GET","POST"])

def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from user WHERE username=%s",username)
        userlist = cursor.fetchall()
        print(userlist['username'])
    
    if username == userlist[0]['username'] and password == userlist[0]['password']:
    
            return redirect(url_for("index"))
    return render_template('login.html')




class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    language_list = [("en","Tiếng Anh"),("vi","Tiếng Việt"),("af", 'Afrikaans'), ("ar", 'Arabic'),("az",'Azerbaijani'),("be",'Belarusian'),("bg",'Bulgarian'),("bn",'Bengali'),("bs",'Bosnian'),("ca",'Catalan'),("ceb",'Cebuano'),("cs",'Czech'),("cy",'Welsh'),("da",'Danish'),("de",'German'),("el",'Greek'),("eo",'Esperanto'),("es",'Spanish'),("et",'Estonian'),("eu",'Basque'),("fa",'Persian'),("fi",'Finnish'),("fr",'French'),("ga",'Irish'),("gl",'Galician'),("gu",'Gujarati'),("ha",'Hausa'),("hi",'Hindi'),("hmn",'Hmong'),("hr",'Croatian'),("ht",'Haitian Creole'),("hu",'Hungarian'),("hy",'Armenian'),("id",'Indonesian'),("ig",'Igbo'),("is",'Icelandic'),("it",'Italian'),("iw",'Hebrew'),("ja",'Japanese'),("jw",'Javanese'),("ka",'Georgian'),("kk",'Kazakh'),("km",'Khmer'),("kn",'Kannada'),("ko",'Korean'),("la",'Latin'),("lo",'Lao'),("lt",'Lithuanian'),("lv",'Latvian'),("mg",'Malagasy'),("mi",'Maori'),("mk",'Macedonian'),("ml",'Malayalam'),("mn",'Mongolian'),("mr",'Marathi'),("ms",'Malay'),("mt",'Maltese'),("my",'Myanmar(Burmese)'),("ne",'Nepale'),("nl",'Dutch'),("no",'Norwegian'),("ny",'Chichewa'),("pa",'Punjaabi'),("pl",'Polish'),("pt",'Portuguese'),("ro",'Romanian'),("ru",'Russian'),("si",'Sinhala'),("sk",'Slovak'),("sl",'Slovenian'),("so",'Somali'),("sq",'Albanian'),("th",'Thai'),("tl",'Filipino'),("tr",'Turkish'),("uk",'Ukrainian'),("ur",'Urdu'),("uz",'Uzbek'),("yi",'Yiddish'),("yo",'Yoruba'),("zh-CN",'Tiếng Trung (Giản thể)'),("zh-TW",'Tiếng Trung (Truyền thống)'),("zu",'Zulu')]
    language = SelectField("Ngôn ngữ ", choices=language_list)
    language2 = SelectField("Ngôn ngữ 2",choices=language_list)
    submit = SubmitField("Tải Tập tin")

@app.route("/index",methods=["POST","GET"])

def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        start_time = datetime.now()
        file = form.file.data
        language_in = form.language.data
        language_out = form.language2.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        PATH = app.config['UPLOAD_FOLDER']
        # os.system('python3 wav.py -i {} -s {}'.format(PATH+file.filename,language_in))
        # end_time = datetime.now()
        # app.config['time-start'] = str(end_time-start_time)
        return redirect(url_for("loading",file=file.filename,lang1=language_in,lang2=language_out))
    return render_template('index.html',form=form)

    


@app.route("/loading",methods = ['GET','POST'])

def loading():
    return render_template("loading.html")

def loading(file,lang1,lang2):
    return render_template("loading")    
# @app.route("/success")

# def success():
#     return render_template("success.html")




    


if __name__ == "__main__":
    app.run(debug=True)