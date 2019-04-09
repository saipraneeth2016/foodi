from flask import Flask,render_template,request,redirect,session
import sqlite3,random,smtplib

app = Flask(__name__)
app.secret_key = "shit"

def sendmail(otp,remail):
    print(otp)
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("praneethakhil123@gmail.com", "legendakhil")
    message = "The otp for the sign-up is {}".format(otp)
    s.sendmail("sender_email_id", remail, message)
    s.quit()

@app.route('/')
def hello_world():
    return(render_template("index.html",data="Welcome guest"))
    # return 'Hello World!'

@app.route("/confirm",methods=["GET","POST"])
def confirm():
    conn = sqlite3.connect("database")
    email=request.form["email"]
    password=request.form["password"]
    submit=request.form["submit"]
    if submit=="login":
        c=conn.cursor()
        c.execute("select username from details where email='{}' and password='{}'".format(email,password))
        dataa=c.fetchall()
        data="Welcome "+str(dataa[0][0]) if dataa!=[] else "login details are not correct"
        session["login"]=1 if dataa!=[] else 0
        print(session["login"])
        return(render_template("index.html",data=data))
    else:
        conn = sqlite3.connect("database")
        c = conn.cursor()
        data = "user already exists"
        c.execute("select * from details where email='{}';".format(email))
        if c.fetchall() != []:
            return (render_template("index.html", data=data))
        otp=str(random.randint(100000,999999))
        session["otp"]=str(otp)
        session["email"]=email
        session["password"]=password
        sendmail(otp,email)
        return("""<form method="post" action="otpvalid">
                                        <div class="form-group">
                                            <input type="text" id="contact_name" name="username" class="form-control" placeholder="username"  required/>
                                            <input type="password" id="contact_name" name="otp" class="form-control" placeholder="Otp"  required/>
                                            <button type="submit" name="submit" class="pull-xs-right tm-submit-btn" value="login">Login</button>
                                            </div>
                                    </form>""")
@app.route("/otpvalid",methods=["GET","POST"])
def otpvalid():
    conn = sqlite3.connect("database")
    c = conn.cursor()
    otpentered=request.form["otp"]
    if otpentered==session["otp"]:
        email=session["email"]
        password=session["password"]
        username=request.form["username"]
        data = "Welcome {}".format(request.form["username"])
        c.execute('insert into details values("{}", "{}", "{}")'.format(email,password,username));
        conn.commit()
        session["login"]=1
        return (render_template("index.html",data=data))
    return (render_template("index.html",data="otp did not match"))

@app.route("/buy/<id>")
def buy(id):
    conn = sqlite3.connect("database")
    c = conn.cursor()
    c.execute("select text,cost from products where id={};".format(id))
    d=c.fetchall()
    return(render_template("buy.html",data=[id,d[0][0],d[0][1]]))#<div><h1>sai</h1>saipraneeth<br>praneeth<br>chebrolu</div>

@app.route("/confirmbuy",methods=["POST","GET"])
def confirmbuy():
    try:
        if session["login"]==1:
            return (render_template("index.html", data="You cant buy, right now as the site is under construction."))
            #return("gatewayerror")
        if session["login"]==0:
            return (render_template("index.html", data="You must login for a purchace"))
    except:
        return (render_template("index.html", data="You must login for a purchace"))

if __name__ == '__main__':
    app.run(debug=True)