from flask import *
from flask_sqlalchemy import SQLAlchemy
import os, smtplib, ssl, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


        
database_uri = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=	'ziuyibeh',
    dbpass='Scs4CjliASZ5jO6Nj8f0d9-EEKG9X8W7',
    dbhost=	'babar.db.elephantsql.com',
    dbname='ziuyibeh'
)
db = SQLAlchemy()
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.secret_key = b'8e44f8820a35403504a7\n\xec]/'
db.init_app(app)

class Tabela(db.Model):
    __tablename__ = "hsprevent"
    cpf = db.Column(db.String(),primary_key = True)
    nome = db.Column(db.String())
    login = db.Column(db.String())
    senha = db.Column(db.String())
    
    def __init__(self,cpf,nome,login,senha):
        self.cpf = cpf
        self.nome = nome
        self.login = login
        self.senha = senha

arquivos = os.path.join(os.path.dirname(__file__), "arquivos")


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        if request.form.get("send") == "Enviar":
            nome = request.form["nome"]
            cpf = request.form["cpf"]
            row = db.session.query(Tabela.nome).filter_by(cpf=cpf).first()
            if(nome == row[0]):
                session['cpf'] = cpf
                return redirect(url_for("login"))
            else:
                return render_template("index.html")
        elif request.form.get("cadastro") == "Cadastro":
            return redirect(url_for("cadastro"))
    else:
        return render_template("index.html")
@app.route('/cadastro',methods= ["GET", "POST"])
def cadastro():
    if request.method == 'POST':
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        login = request.form["login"]
        senha = request.form["senha"]
        usr = Tabela(cpf,nome,login,senha)
        if(not (db.session.query(Tabela.cpf).exists)):
            db.session.add(usr)
            db.session.commit()
        return redirect(url_for("index"))
    else:    
        return render_template("cadastro.html")
@app.route("/login", methods= ["GET", "POST"])
def login():
    cpf = session.get("cpf",None)
    if request.method == "POST":
        login = request.form["login"]
        senha = request.form["senha"]
        row = db.session.query(Tabela.senha).filter_by(login=login,cpf=cpf).first()
        if(senha == row[0]):
            code = ""
            k = 0
            while k < 6:
                code += str(random.randint(0,9))
                k+=1
            port = 465  
            context = ssl.create_default_context()
            row2 = db.session.query(Tabela.senha).filter_by(login="gzymberg@gmail.com").first()
            snh = row2[0]
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("gzymberg@gmail.com", snh)
                message = MIMEMultipart("alternative")
                message["Subject"] = "Código de autenticação de dois fatores"
                message["From"] = login
                message["To"] = login
                texto = """\
                Segue código de autenticação de dois fatores:
                """+code+"""\
                """
                mime = MIMEText(texto,"plain")
                message.attach(mime)
                try:   
                    server.sendmail(login,login, message.as_string())
                except:
                    return redirect(url_for("index"))
                session['code'] = code
            return redirect(url_for("fa"))
        else:
            return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route('/fa', methods= ["GET", "POST"])
def fa():
    if request.method == "POST":
        code = session.get("code",None)
        codigo = request.form["codigo"]
        if(codigo == code):
            return redirect(url_for("success"))
        else:
            return redirect(url_for("index"))
    else:
        return render_template("fa.html")
@app.route('/success', methods= ["GET", "POST"])
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run()