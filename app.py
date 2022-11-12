from flask import Flask,redirect,url_for,render_template,request,send_file,flash,session,send_from_directory,abort
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flaskext.mysql import MySQL
import pymysql
import os
import shutil
import hashlib

from io import BytesIO
import time
from datetime import datetime

app = Flask(__name__,template_folder="templates",static_folder="static")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SOURCE'] = "static/video/"
app.config['UPLOAD_FOLDER'] = 't/'
app.config['time_start'] = ''
app.config['VIDEO'] = 'video/'
app.config['ALLOWED_VIDEO_EXTENSION'] = ["MP4","WAV"]
mysql = MySQL()


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB']='luanvan'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route("/",methods=["GET","POST"])




def login():
    if "user" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode())
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from user WHERE username=%s",username)
        userlist = cursor.fetchall()
        name = userlist[0]['username']
        pass_word = userlist[0]['password']
        password = password.hexdigest()
        
        if username == name and password == pass_word:
                session['user'] = username
                flash("Đăng nhập thành công")
                return redirect(url_for("index"))

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()       
    
        
    return render_template('login.html')
        
    

def login(err):
    return render_template("login.html",err)

class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    language_list = [("null","Chọn ngôn ngữ"),("en","Tiếng Anh"),("vi","Tiếng Việt"),("af", 'Afrikaans'), ("ar", 'Arabic'),("az",'Azerbaijani'),("be",'Belarusian'),("bg",'Bulgarian'),("bn",'Bengali'),("bs",'Bosnian'),("ca",'Catalan'),("ceb",'Cebuano'),("cs",'Czech'),("cy",'Welsh'),("da",'Danish'),("de",'German'),("el",'Greek'),("eo",'Esperanto'),("es",'Spanish'),("et",'Estonian'),("eu",'Basque'),("fa",'Persian'),("fi",'Finnish'),("fr",'French'),("ga",'Irish'),("gl",'Galician'),("gu",'Gujarati'),("ha",'Hausa'),("hi",'Hindi'),("hmn",'Hmong'),("hr",'Croatian'),("ht",'Haitian Creole'),("hu",'Hungarian'),("hy",'Armenian'),("id",'Indonesian'),("ig",'Igbo'),("is",'Icelandic'),("it",'Italian'),("iw",'Hebrew'),("ja",'Japanese'),("jw",'Javanese'),("ka",'Georgian'),("kk",'Kazakh'),("km",'Khmer'),("kn",'Kannada'),("ko",'Korean'),("la",'Latin'),("lo",'Lao'),("lt",'Lithuanian'),("lv",'Latvian'),("mg",'Malagasy'),("mi",'Maori'),("mk",'Macedonian'),("ml",'Malayalam'),("mn",'Mongolian'),("mr",'Marathi'),("ms",'Malay'),("mt",'Maltese'),("my",'Myanmar(Burmese)'),("ne",'Nepale'),("nl",'Dutch'),("no",'Norwegian'),("ny",'Chichewa'),("pa",'Punjaabi'),("pl",'Polish'),("pt",'Portuguese'),("ro",'Romanian'),("ru",'Russian'),("si",'Sinhala'),("sk",'Slovak'),("sl",'Slovenian'),("so",'Somali'),("sq",'Albanian'),("th",'Thai'),("tl",'Filipino'),("tr",'Turkish'),("uk",'Ukrainian'),("ur",'Urdu'),("uz",'Uzbek'),("yi",'Yiddish'),("yo",'Yoruba'),("zh-CN",'Tiếng Trung (Giản thể)'),("zh-TW",'Tiếng Trung (Truyền thống)'),("zu",'Zulu')]
    language = SelectField("Ngôn ngữ ", choices=language_list)
    language2 = SelectField("Ngôn ngữ 2",choices=language_list)
    submit = SubmitField("Tạo phụ đề")

class DownloadFile(FlaskForm):
    submit2 = SubmitField("Tải file")

@app.route("/index",methods=["POST","GET"])

def index():
    
        
    if "user" not in session:
        return redirect(url_for("login"))
    
    form = UploadFileForm()
    if "user" in session:
        user = session["user"]
    
    

    if form.validate_on_submit():
        source = app.config['SOURCE']
        PATH = app.config['UPLOAD_FOLDER']

        conn = mysql.connect()

        start_time = datetime.now()
        file = form.file.data
        language_in = form.language.data
        language_out = form.language2.data
        os.makedirs(PATH, exist_ok=True)

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        
        # end_time = datetime.now()
        # app.config['time-start'] = str(end_time-start_time)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE username=%s",user)
        usernames = cursor.fetchall()


        
        
        # flash("Tải tập tin {} thành công".format(file.filename))
        
            
        file_output = file.filename[:file.filename.index('.mp4')] + '_output.mp4'
        shutil.move(PATH+file_output, source)
        os.rename(source+file_output,source+file.filename)

        cursor1 = conn.cursor(pymysql.cursors.DictCursor)
        cursor1.execute("INSERT INTO lichsu(id_username,ten_video,lang_in,lang_out) VALUES(%s,%s,%s,%s)",(usernames[0]['id'],file.filename,language_in,language_out))
        userlist = cursor1.fetchall()
        conn.commit()
        # if os.path.exists(PATH):
        #     shutil.rmtree(PATH)
       
        return redirect(url_for("loading",filename=file.filename))
    return render_template('index.html',form=form)




@app.route("/loading/<filename>",methods = ["POST","GET"])

def loading(filename):
    if "user" not in session:
        return redirect(url_for("login"))
    down = DownloadFile()
    

    PATH = app.config['UPLOAD_FOLDER']
    SOURCE =app.config['VIDEO']
    flash(filename)
    redirect(url_for("loading",filename=PATH+filename),code=301)
    if down.validate_on_submit():
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=True)

    return render_template("loading.html",down=down,filename=SOURCE+filename)

   
@app.route("/dangxuat")

def dangxuat():
    if "user" not in session:
        redirect(url_for("login"))
    if "user" in session:
        session.pop("user",None)
        flash("Đăng xuất thành công!")
    return redirect(url_for("login"))
# def success():
#     return render_template("success.html")

@app.route("/lichsu")

def lichsu():
    try:
        if "user" in session:
            user = session["user"]

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE username=%s",user)
        userlist = cursor.fetchall()

        cursor1 = conn.cursor(pymysql.cursors.DictCursor)
        cursor1.execute("SELECT * FROM lichsu WHERE id_username=%s",userlist[0]['id'])
        userlist1 = cursor1.fetchall()

        return render_template("lichsu.html",data=userlist1)
        

        
        # return redirect(url_for("index"))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()  
    return render_template("lichsu.html")
    
#
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True,host='127.0.0.1',port=5000)