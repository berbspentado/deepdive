from flask import Flask,render_template,request,redirect,jsonify
from datetime import datetime
import flask_excel as excel
from .app import app
from .database import db
from .models.models import User,ManualAnalysis,UploadAnalysis,RseFile
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
from passlib.hash import sha256_crypt
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

login_manager = LoginManager() #used to manage session login
login_manager.init_app(app)
excel.init_excel(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#-------------------------------- LOGIN / LOGOUT SESSION    

@app.route("/")
def home():
    return render_template("index.html")

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
    
#--------------------------------MANUAL FILE

@app.route("/homepage")
@login_required
def homepage():
    diags = ManualAnalysis.query.all()
    return render_template("content.html",diags=diags)    

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

    elif filter_result == "Analysis":
        result = UploadAnalysis.query.filter(UploadAnalysis.analysis.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)    

    elif filter_result == "Diag":
        result = ManualAnalysis.query.filter(ManualAnalysis.diagfile.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Diag":
        result = UploadAnalysis.query.filter(UploadAnalysis.diagfile_name.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)     

    elif filter_result == "Store":
        result = ManualAnalysis.query.filter(ManualAnalysis.diagfile.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Store":
        result = UploadAnalysis.query.filter(UploadAnalysis.diagfile_name.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)     

    elif filter_result == "RSE State":
        result = ManualAnalysis.query.filter(ManualAnalysis.rse_state.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "RSE State":
        result = UploadAnalysis.query.filter(UploadAnalysis.rse_state.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Build Package":
        result = ManualAnalysis.query.filter(ManualAnalysis.build_package.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Build Package":
        result = UploadAnalysis.query.filter(UploadAnalysis.build.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "ADK":
        result = ManualAnalysis.query.filter(ManualAnalysis.adk.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "ADK":
        result = UploadAnalysis.query.filter(UploadAnalysis.adk.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Date":
        result = ManualAnalysis.query.filter(ManualAnalysis.date_time.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Date":
        result = UploadAnalysis.query.filter(UploadAnalysis.probdate.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)    

    elif filter_result == "Jira":
        result = ManualAnalysis.query.filter(ManualAnalysis.jira.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Jira":
        result = UploadAnalysis.query.filter(UploadAnalysis.associated_jira.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)    

    elif filter_result == "Category":
        result = ManualAnalysis.query.filter(ManualAnalysis.category.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Category":
        result = UploadAnalysis.query.filter(UploadAnalysis.category.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Device Error":
        result = ManualAnalysis.query.filter(ManualAnalysis.device_error.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "Device Error":
        result = UploadAnalysis.query.filter(UploadAnalysis.device_error.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "GSA":
        result = ManualAnalysis.query.filter(ManualAnalysis.gsa.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "GSA":
        result = UploadAnalysis.query.filter(UploadAnalysis.gsa_version.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "HW Type":
        result = ManualAnalysis.query.filter(ManualAnalysis.hwtype.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)

    elif filter_result == "HW Type":
        result = UploadAnalysis.query.filter(UploadAnalysis.hw_type.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)    

    elif filter_result == "Motherboard":
        result = ManualAnalysis.query.filter(ManualAnalysis.motherboard.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result) 

    elif filter_result == "Motherboard":
        result = UploadAnalysis.query.filter(UploadAnalysis.motherboard.like('%' + search_result +'%')).all()
        return render_template('search_results.html',diags=result)     

###---------------------------------------------UPLOAD FILE
@app.route("/upload_analysis")
@login_required
def upload_mainfile():
    diags = UploadAnalysis.query.all()
    return render_template("upload.html",diags=diags)    


@app.route("/upload_edit-analysis/<int:id>",methods=["GET","POST"])
def upload_edit_analyze(id):
    diag = UploadAnalysis.query.get(id)    
    if request.method == "POST":
        diag.diagfile_name= request.form["diags"]
        diag.rse_state=request.form["rse"]
        diag.build = request.form["build"]
        diag.adk=request.form["adk"]
        diag.analysis = request.form["analysis"]
        diag.associated_jira=request.form["jira"]
        diag.category=request.form["category"]
        diag.device_error=request.form["deviceerror"]
        diag.gsa_version = request.form["gsa"]
        diag.hw_type = request.form["hardware"]
        diag.motherboard=request.form["motherboard"]
        diag.dbmger = request.form["dbmgr"]
       
        db.session.commit()

        return redirect("/upload_analysis")

    return render_template("upload_edit_manual_analysis.html",diag=diag)


@app.route("/upload_delete/<int:id>",methods=["GET","POST"])
def upload_delete(id):
    diag = UploadAnalysis.query.get(id)
    db.session.delete(diag)
    db.session.commit()

    return redirect("/upload_analysis")         

@app.route("/upload_search_results",methods=["GET","POST"])
def upload_search():
    search_result = request.form["search"]
    filter_result = request.form["filterby"]
    
    if filter_result == "Analysis":
        result = UploadAnalysis.query.filter(UploadAnalysis.analysis.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)    

    elif filter_result == "Diag":
        result = UploadAnalysis.query.filter(UploadAnalysis.diagfile_name.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)     

    elif filter_result == "Store":
        result = UploadAnalysis.query.filter(UploadAnalysis.diagfile_name.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)     

    elif filter_result == "RSE State":
        result = UploadAnalysis.query.filter(UploadAnalysis.rse_state.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)

    elif filter_result == "Build Package":
        result = UploadAnalysis.query.filter(UploadAnalysis.build.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)

    elif filter_result == "ADK":
        result = UploadAnalysis.query.filter(UploadAnalysis.adk.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)

    elif filter_result == "Date":
        result = UploadAnalysis.query.filter(UploadAnalysis.probdate.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)    

    elif filter_result == "Jira":
        result = UploadAnalysis.query.filter(UploadAnalysis.associated_jira.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)    

    elif filter_result == "Category":
        result = UploadAnalysis.query.filter(UploadAnalysis.category.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)

    elif filter_result == "Device Error":
        result = UploadAnalysis.query.filter(UploadAnalysis.device_error.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)

    elif filter_result == "GSA":
        result = UploadAnalysis.query.filter(UploadAnalysis.gsa_version.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)

    elif filter_result == "HW Type":
        result = UploadAnalysis.query.filter(UploadAnalysis.hw_type.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)    

    elif filter_result == "Motherboard":
        result = UploadAnalysis.query.filter(UploadAnalysis.motherboard.like('%' + search_result +'%')).all()
        return render_template('upload_search_results.html',diags=result)
       

@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        df = pd.read_excel(request.files.get('file'))
        sql_engine = create_engine('mysql+pymysql://root:@localhost:3306/deepdive')
        dbConnection = sql_engine.connect()

        try:
            frame = df.to_sql("upload_analysis",dbConnection,if_exists='append',index=False)

        except ValueError as vx:
            print(vx)

        except Exception as ex:
            print(ex)         

        finally:
            dbConnection.close()

        return redirect('/upload_analysis')    

#----------------------------EOD REPORT

@app.route("/eod_report")
def eod_content():

    return render_template('eod_report.html')
    






#----------------------------RSE REPORT


@app.route("/rse_report",methods=["GET","POST"])
def rse_content():
    rse_diags = RseFile.query.all()
    if request.method == "POST":
        df = pd.read_excel(request.files.get('rse_file'),sheet_name="RSE 3-8")
        sql_engine = create_engine('mysql+pymysql://root:@localhost:3306/deepdive')
        dbConnection = sql_engine.connect()

        try:
            frame = df.to_sql("rse_reports",dbConnection,if_exists='append',index=False)

        except ValueError as vx:
            print(vx)

        except Exception as ex:
            print(ex)         

        finally:
            dbConnection.close()

        return redirect('/rse_report') 
        
       
    return render_template("rse_report.html",rse_diags=rse_diags)
       
'''@app.route("/generate_data",methods=["POST","GET"])
def generate_chart():

    sql_engine = create_engine('mysql+pymysql://root:@localhost:3306/deepdive')

    SQL_Query = pd.read_sql_query(
    select
    diagfile_name,
    build,
    jira,
    Category,
    adk
    from rse_reports, sql_engine)
    height = [3, 12, 5, 18, 45]
    df = pd.DataFrame(SQL_Query, columns=['diagfile_name','build','jira','Category','adk'])
    

    return render_template("display_chart.html")'''


@app.route("/generate_data",methods=["POST","GET"])
def generate_chart():
    data = [['E001', 'M', 34, 123, 'Normal', 350], 
        ['E002', 'F', 40, 114, 'Overweight', 450], 
        ['E003', 'F', 37, 135, 'Obesity', 169], 
        ['E004', 'M', 30, 139, 'Underweight', 189], 
        ['E005', 'F', 44, 117, 'Underweight', 183], 
        ['E006', 'M', 36, 121, 'Normal', 80], 
        ['E007', 'M', 32, 133, 'Obesity', 166], 
        ['E008', 'F', 26, 140, 'Normal', 120], 
        ['E009', 'M', 32, 133, 'Normal', 75], 
        ['E010', 'M', 36, 133, 'Underweight', 40] ] 
 
    df = pd.DataFrame(data, columns = ['EMPID', 'Gender',  
                                    'Age', 'Sales', 
                                    'BMI', 'Income'] ) 

    df.hist()

    plt.show()

    return redirect("/generate_data")










'''@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        #return jsonify({"result": request.get_array(field_name='file')})
        
        #df = pd.read_excel(request.files.get('file'),index_col=None,na_values=['NA'], usecols = "A",header=0)
        df = pd.read_excel(request.files.get('file'))
        return df.to_html()
       

        return render_template('upload.html',shapes = df)
    return render_template('upload.html')  

@app.route("/upload",methods=["GET","POST"])
def upload_file():

    sql_engine = create_engine('mysql+pymysql://root:@localhost:3306/deepdive')
    
    if request.method == "POST":
        df = pd.read_excel(request.files.get('file'))

        return df.to_sql(
            name='upload_analysis',
            con=sql_engine,
            index = True,
            if_exists = 'append'

        )   '''

