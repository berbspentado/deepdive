from flask import Flask,render_template,request,redirect,jsonify
from datetime import datetime
import flask_excel as excel
from .app import app
from .database import db
from .models.models import User,ManualAnalysis
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
from passlib.hash import sha256_crypt

login_manager = LoginManager() #used to manage session login
login_manager.init_app(app)
excel.init_excel(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/homepage")
@login_required
def homepage():
    diags = ManualAnalysis.query.all()
    return render_template("content.html",diags=diags)        

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        vusername = request.form["username"]
        vpassword = request.form["password"]
        user = User.query.filter_by(username=vusername).first()
        validate = sha256_crypt.verify(vpassword,user.password)
        if user is not None and user.username==vusername and validate==True:
            login_user(user)
        else:
            return redirect("/")
    return redirect("/homepage")

@app.route("/logout/<int:id>")
def logout(id):
    logout_user()

    return redirect("/")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        vusername = request.form["username"]
        vpassword = request.form["password"]
        vproject=request.form["project"]
        user = User(username=vusername,password=sha256_crypt.encrypt(vpassword),project=vproject)
        db.session.add(user)
        db.session.commit()

        return redirect("/")
    return render_template("register.html")

@app.route("/manual-analysis")
def manual_analysis():
    return render_template("manual_analysis.html")

@app.route("/manual-file",methods=["GET","POST"])
def add_analysis():
    if request.method == "POST":
        vdiagFile= request.form["diags"]
        vrseState=request.form["rse"]
        vbuild = request.form["build"]
        vadk=request.form["adk"]
        vproblemDate=request.form["time"]
        #vproblemDate=datetime.strptime(request.form["time"],'%Y-%m-%d %Z %H:%M')
        vanalysis = request.form["analysis"]
        vjira=request.form["jira"]
        vcategory=request.form["category"]
        vdeviceerror=request.form["deviceerror"]
        vgsa = request.form["gsa"]
        vhardware = request.form["hardware"]
        vmotherboard=request.form["motherboard"]
        vdbmanager = request.form["dbmgr"]
        manual_file_analysis=ManualAnalysis(diagfile=vdiagFile,rse_state=vrseState,build_package=vbuild,adk=vadk,date_time=vproblemDate,analysis=vanalysis,jira=vjira,category=vcategory,device_error=vdeviceerror,gsa=vgsa,hwtype=vhardware,motherboard=vmotherboard,dbmanager=vdbmanager,user_id=current_user.id)

        db.session.add(manual_file_analysis)
        db.session.commit()

        return redirect("/manual-analysis")
    return redirect("/homepage")

@app.route("/edit-analysis/<int:id>",methods=["GET","POST"])
def edit_analyze(id):
    diag = ManualAnalysis.query.get(id)    
    if request.method == "POST":
        diag.diagfile= request.form["diags"]
        diag.rse_state=request.form["rse"]
        diag.build_package = request.form["build"]
        diag.adk=request.form["adk"]
        diag.analysis = request.form["analysis"]
        diag.jira=request.form["jira"]
        diag.category=request.form["category"]
        diag.device_error=request.form["deviceerror"]
        diag.gsa = request.form["gsa"]
        diag.hwtype = request.form["hardware"]
        diag.motherboard=request.form["motherboard"]
        diag.dbmanager = request.form["dbmgr"]
       
        db.session.commit()

        return redirect("/homepage")


    return render_template("edit_manual_analysis.html",diag=diag)


@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    diag = ManualAnalysis.query.get(id)
    db.session.delete(diag)
    db.session.commit()

    return redirect("/homepage")


@app.route("/search_results",methods=["GET","POST"])
def search():
    search_result = request.form["search"]
    filter_result = request.form["filterby"]
    
    if filter_result == "Analysis":
        result = ManualAnalysis.query.filter(ManualAnalysis.analysis.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)
    
    elif filter_result == "Diag":
        result = ManualAnalysis.query.filter(ManualAnalysis.diagfile.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Store":
        result = ManualAnalysis.query.filter(ManualAnalysis.diagfile.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "RSE State":
        result = ManualAnalysis.query.filter(ManualAnalysis.rse_state.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Build Package":
        result = ManualAnalysis.query.filter(ManualAnalysis.build_package.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "ADK":
        result = ManualAnalysis.query.filter(ManualAnalysis.adk.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Date":
        result = ManualAnalysis.query.filter(ManualAnalysis.date_time.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Jira":
        result = ManualAnalysis.query.filter(ManualAnalysis.jira.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Category":
        result = ManualAnalysis.query.filter(ManualAnalysis.category.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Device Error":
        result = ManualAnalysis.query.filter(ManualAnalysis.device_error.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "GSA":
        result = ManualAnalysis.query.filter(ManualAnalysis.gsa.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "HW Type":
        result = ManualAnalysis.query.filter(ManualAnalysis.hwtype.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Motherboard":
        result = ManualAnalysis.query.filter(ManualAnalysis.motherboard.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)                                    
       



       








@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        return jsonify({"result": request.get_array(field_name='file')})

    return redirect("/homepage")   





@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))