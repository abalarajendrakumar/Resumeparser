import os
#import magic
from app import app
from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx','doc'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/',methods=['POST','GET'])
def home_form():
	return render_template('home.html')

@app.route('/how_it_works')
def how_it_works():
	return render_template('howitwork.html')

@app.route('/upload',methods=['POST','GET'])
def upload_form():
    if request.method=='POST':
        n=request.form.get('username')
        #print("username=",n)
        return render_template('upload.html',variable=n)

@app.route('/candidatelogin')
def candidatelogin():
    return render_template("candidatelogin.html")

@app.route('/clogin',methods=['POST','GET'])
def clogin():
    if request.method=='POST':
        n=request.form.get('uname')
        e=request.form.get('email')
        p1=request.form.get('pass')
        p2=request.form.get('repass')
        if p1!=p2:
            #flash("Password Mismatched")
            return render_template("candidateregister.html")
        elif p1=="" or e=="" or n=="" or p2=="":
            #flash("Please fill all details ")
            return render_template("candidateregister.html")
        else:
            import sqlite3
            conn = sqlite3.connect('project.db')
            cursor = conn.execute("SELECT USER_NAME,EMAIL,PASSWORD from Candidate")
            for row in cursor:
                if row[0]==n:
                    #flash("Candidate already exists!")
                    return render_template("candidate_login.html")
                    break
            else:
                conn = sqlite3.connect('project.db')
                conn.execute("INSERT INTO Candidate (USER_NAME,EMAIL,PASSWORD) VALUES (?, ?, ?)",(n, e,p1))
                conn.commit()
                conn.close()
                #flash("Registration successful")
                return render_template("candidatelogin.html")
    return render_template("candidateregister.html")

@app.route('/candidateregister',methods = ['POST', 'GET'])
def candidate_register():
    return render_template('candidateregister.html')

@app.route('/login',methods=['POST','GET'])
def login_form():
    if request.method == 'POST':
        result = request.form
        n=request.form.get("cname")
        e=request.form.get("email")
        p1=request.form.get("pass")
        p2=request.form.get("pass1")
        if p1!=p2:
            #flash("Password Mismatched")
            return render_template("register.html")
        elif p1=="" or e=="" or n=="" or p2=="":
            #flash("Please fill all details ")
            return render_template("register.html")
        else:
            import sqlite3
            conn = sqlite3.connect('project.db')
            cursor = conn.execute("SELECT COMPANY_NAME,EMAIL,PASSWORD from Recruiter")
            for row in cursor:
                if row[0]==n:
                    #flash("Recruiter already exists")
                    return render_template("login.html")
            else:
                conn.execute("INSERT INTO Recruiter (COMPANY_NAME,EMAIL,PASSWORD) VALUES (?, ?, ?)",(n, e,p1))
                conn.commit()
                conn.close()
                return render_template("login.html",result=result)
    else:
        return render_template("login.html")

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/jobdescription',methods=['POST','GET'])
def describe():
    if request.method=='POST':
        rec_email=request.form.get("email")
        rec_pass=request.form.get("pass")
        if rec_email=="" and rec_pass=="":
            #flash("Please fill your email and password ")
            return render_template("login.html")
        elif rec_email=="":
            #flash("Please fill your email ")
            return render_template("login.html")
        elif rec_pass=="":
            #flash("Please fill your password ")
            return render_template("login.html")
        else:
            import sqlite3
            conn = sqlite3.connect('project.db')
            cursor = conn.execute("select * from RECRUITER where EMAIL=? AND PASSWORD=?",(rec_email,rec_pass))
            if cursor!=None:
                x=cursor.fetchone()[0]
                return render_template('jobdescription.html',variable=x)
            else:
                #flash("Invalid Login Credentials")
                return render_template("login.html")

@app.route('/dispCandidate',methods=['POST','GET'])
def dispCandidates():
    if request.method == 'POST':
        #result = request.form
        n=request.form.get("name")
        d=request.form.get("desig")
        l=request.form.get("sel1")
        e=request.form.get("sel2")
        s=request.form.get("skills")
        ed=request.form.get("sel3")
        import sqlite3
        conn = sqlite3.connect('project.db')
        ##c.execute("CREATE TABLE JobPostings (COMPANY TEXT NOT NULL,LOCATION TEXT NOT NULL,SKILL json NOT NULL,DESIGNATION TEXT NOT NULL,EXPERIENCE TEXT NOT NULL,EDUCATION TEXT NOT NULL)")
        conn.execute("INSERT INTO JobPostings (COMPANY,LOCATION,SKILL,DESIGNATION,EXPERIENCE,EDUCATION) VALUES (?, ?, ?, ?, ?, ?)",(n,l,s,d,e,ed))
        conn.commit()
        conn.close()
        #flash("Job posted successfully ")
        mydict={}
        i=1
        import sqlite3
        conn = sqlite3.connect('project.db')
        #c.execute("CREATE TABLE CandidateDetails (username varchar(30) PRIMARY KEY, data json NOT NULL)")
        cursor = conn.execute("select * from CandidateDetails")
        for cur in cursor:
            import json
            res=json.loads(cur[1])
            '''print("myres=",res)
            print("list of skills in db=",res['SKILLS'])
            print("dict value=",res['exp'],"db=",e)
            print("dict value=",res['EDUCATION'],"db=",ed)'''
            if res['exp']==int(e):
                if ed in res['EDUCATION']:
                    jdskills=s.split(" ")
                   
                    for sk in jdskills:
                        if sk in res['SKILLS']:
                            mydict[i]={}
                            mydict[i]['un']=cur[0]
                            mydict[i]['ex']=res['exp']
                            mydict[i]['sk']=res['SKILLS']
                            mydict[i]['ed']=res['EDUCATION']
                            mydict[i]['ph']=res['PHONE']
                            mydict[i]['em']=res['EMAIL']
                            i=i+1
                            break
                        
        for i in range(1,len(mydict)+1):
            for j in range(1,len(mydict)+1):
                if mydict[i]['ex']<mydict[j]['ex']:
                    temp=mydict[i]
                    mydict[i]=mydict[j]
                    mydict[j]=temp
                    
        for i in range(1,len(mydict)+1):
            for j in range(1,len(mydict)+1):
                if mydict[i]['ex']==mydict[j]['ex'] and len(mydict[i]['sk'])>len(mydict[j]['sk']):
                    temp=mydict[i]
                    mydict[i]=mydict[j]
                    mydict[j]=temp
                    
        #print("mydict contents=",mydict)
    return render_template("dispCandidate.html",result=mydict)
        
def filereading(username,filename):
    import PyPDF2 
    import os
    import docx2txt 
    from nltk.corpus import stopwords 
    from nltk.tokenize import word_tokenize 
    from nltk.tokenize import sent_tokenize
    #entry=os.listdir('F:/SEMESTER4/MINI_PROJECT/pdf_to_text/Uploads')
    content=""
    filename='F:/SEMESTER 4/MINI PROJECT/uploads/'+filename
    #filename='F:/SEMESTER4/MINI_PROJECT/pdf_to_text/Uploads/'+filename
    name, ext = os.path.splitext(filename)
    if(ext==".pdf"):
        pdfFileObj = open(filename, 'rb') 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        x=pdfReader.numPages 
        for i in range(0,x):
            pageObj = pdfReader.getPage(i) 
            ans=pageObj.extractText()
            content=content+ans
    if(ext==".txt"):
        tfobj=open(filename,'r')
        content=tfobj.read()
    if(ext==".docx"):
        content = docx2txt.process(filename)
        
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt') 
    stop_words = set(stopwords.words('english')) 
    stop_words.add(".")
    stop_words.add(",")
    stop_words.add(":")
    stop_words.add("&")
    
    import re
    econtent=re.sub(' +',' ',content)
    
    #print("Stop words=",stop_words)
    #print("\n\n")
    word_tokens =word_tokenize(content) 
    #print("Tokenized words=",word_tokens)
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words and w not in filtered_sentence: 
            filtered_sentence.append(w) 
    #print("\n After removing stop words",filtered_sentence)
    
    
    words=""
    for i in range(0,len(filtered_sentence)):
        words+=' '+filtered_sentence[i]
    
       
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    import re
    education=[]
    EDUCATION = ['B.Sc','Bachelor of Science','Master of Computer Applications','Bachelor of Engineering','B.E.','B.E','ME ', 'M.E', 'M.E.',
             'M.S','MCA','Master of Science','BTECH','B.TECH','Bachelor of Technology','M.TECH','MTECH']
    for i in range(0,len(EDUCATION)):
        if (content.find(EDUCATION[i])!=-1):
            if EDUCATION[i]=="Bachelor of Science":
                education.append('B.Sc')
            elif EDUCATION[i]=="Master of Computer Applications":
                education.append('MCA')
            else:
                education.append(EDUCATION[i])

    education=list(set(education))      
            
    #print("\n   Words=",words) 
    
    
    #extracting skills
    skills=[]
    SKILLS = ['C','C++','OOP','JAVA','RProgramming','BASIC','SAP','ORACLE','LISP','PYTHON','PASCAL','PERL','JAVASCRIPT','RUPY','C#','COBOL','MATLAB','HTML','XML','PHP','ANDROID'
              'CSS','UI','UX','UI/UX','SQL','MySQL','UNIX']
    for i in range(0,len(SKILLS)):
        if (words.find(SKILLS[i])!=-1):
            skills.append(SKILLS[i])

    #extracting phone number
    #phone=re.findall(r"[6-9][0-9]{9}",words)
    phone = re.findall(r"[6-9][0-9]{9}",econtent)
    if phone:
        print(phone)
    else:
        phone=re.findall(r"\d{3}-\d{3}-\d{4}",econtent)
        if phone:
            print("phone=",phone)
        else:
            phone=re.findall(r"\d{5}[\s]\d{5}",econtent)
            if phone:
                print("phone=",phone)
            else:
                phone=re.findall(r"[\s][6-9][0-9]{9}",econtent)
                if phone:
                    print("phone=",phone)
    
    #print("COntents=",econtent)

    #extracting email    
    
    email = re.findall("[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Za-z]{2,}",econtent)
    if email:
        print("email1=",email)
    else:
        email = re.findall("[A-Za-z0-9._%+-]+[\s]+@[A-Za-z]+\.[A-Za-z]{2,}",econtent)
        print("email2=",email)
    
    email="".join(email)
    email=email.strip()   
    email=email.replace("\n","")
    #print("final email=",email)

    dicti={}
    dicti['1']=1
    dicti['2']=2
    dicti['3']=3
    dicti['4']=4
    dicti['5']=5
    dicti['6']=6
    dicti['7']=7
    dicti['8']=8
    dicti['9']=9
    dicti['10']=10
    dicti['one']=1
    dicti['two']=2
    dicti['three']=3
    dicti['four']=4
    dicti['five']=5
    dicti['six']=6
    dicti['seven']=7
    dicti['eight']=8
    dicti['nine']=9
    dicti['ten']=10
    
    exp=0
    #extracting experience
    sentences =sent_tokenize(content)
    for sent in sentences:
        if sent.find('experience')!=-1 or sent.find('Experience')!=-1:
            words=word_tokenize(sent)
            for word in words:
                if word in dicti:
                    exp+=dicti.getValue(word)

    #create python dictionary of fetched details
    mydict={}
    mydict["exp"]=exp
    mydict["SKILLS"]=skills
    if len(education)!=0:
        mydict["EDUCATION"]=education
    if len(phone)!=0:
        mydict["PHONE"]=phone[0]
    if len(email)!=0:
        mydict["EMAIL"]=email
        
        
    #import json
    import json
    jsonObj=json.dumps(mydict)
    print('JSON OUTPUT:\n\n')
    print(jsonObj)
    
    
    import sqlite3
    conn = sqlite3.connect('project.db')
    cursor = conn.execute("SELECT username from CandidateDetails")
    for row in cursor:
        if row[0]==username:
            conn.execute("UPDATE CandidateDetails set data=? where username=?",(jsonObj,username))
            conn.commit()
            conn.close()
            break
    else:
        conn = sqlite3.connect('project.db')
        conn.execute("INSERT INTO CandidateDetails (username,data) VALUES (?, ?)",(username,jsonObj))
        conn.commit()
        conn.close()
        
    print("finished")

    return (username,jsonObj)
    
    
def myjobs(jsonObj):    
    #print('coming in')
    import json
    data=json.loads(jsonObj)
    experience=data['exp']
    mydict={}
    i=1
    import sqlite3
    conn = sqlite3.connect('project.db')
    length=len(data['EDUCATION'])
    for ind in range(0,length):
        education=data['EDUCATION'][ind]
        cursor = conn.execute("select * from JobPostings where experience=? and education=?",(experience,education,))
        for cur in cursor:
            mydict[i]={}
            mydict[i]['company']=cur[0]
            mydict[i]['location']=cur[1]
            mydict[i]['skillset']=cur[2]
            mydict[i]['designation']=cur[3]
            mydict[i]['experience']=cur[4]
            mydict[i]['education']=cur[5]
            i=i+1
        
    return mydict


@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        username=request.form.get("username")
        if 'files[]' not in request.files:
            #flash('Please select file')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename= secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data1,data2=filereading(username,filename)
                #print("Data1=",data1,data2)
                data2=myjobs(data2)
                #flash('File successfully uploaded')
        return render_template('display.html',result=data2)
    
    
@app.route('/filter',methods=['POST'])
def filter_candidate():
    return render_template("filter.html")

@app.route('/canOptions',methods=['POST','GET'])
def opt():
    if request.method=='POST':
        result=request.form
        #print(result)
        can_email=request.form.get("username")
        can_pass=request.form.get("password")
        #print("email=",can_email)
        #print("password=",can_pass)
        if can_email=="" and can_pass=="":
            #flash("Please Fill username and password!")
            return render_template('canddidate_login.html')
        elif can_email=="":
            #flash("Please Fill Your Email!")
            return render_template('canddidate_login.html')
        elif can_pass=="":
            #flash("Please Fill Your Password!")
            return render_template('canddidate_login.html')
        else:
            import sqlite3
            conn = sqlite3.connect('project.db')
            cursor = conn.execute("select * from Candidate where EMAIL=? AND PASSWORD=?",(can_email,can_pass))
            if cursor.fetchone()[0]:
                #print("Authentication Success")
                return render_template('canOptions.html',variable=can_email)
            else:
                #flash("Invalid Login Credentials")
                return render_template('canddidate_login.html')
    else:
        return render_template("canOptions.html")

@app.route('/canOpt',methods=['POST','GET'])
def canopt():
    return render_template('canOptions.html')

@app.route('/browseall',methods=['POST','GET'])
def browse_all():
    mydict={}
    i=1
    import sqlite3
    conn = sqlite3.connect('project.db')
    cursor = conn.execute("select * from JobPostings")
    for cur in cursor:
        mydict[i]={}
        mydict[i]['companyname']=cur[0]
        mydict[i]['location']=cur[1]
        mydict[i]['skillset']=cur[2]
        mydict[i]['designation']=cur[3]
        mydict[i]['experience']=cur[4]
        mydict[i]['education']=cur[5]
        i=i+1
    return render_template("browseall.html",result=mydict)
    
@app.route('/jobbyloc',methods=['POST','GET'])
def jobby_loc():
    return render_template("jobbyloc.html")

@app.route('/browsebyloc',methods=['POST','GET'])
def browse_loc():
    l=request.form.get('sel1')
    l=l.upper()
    mydict={}
    i=1
    import sqlite3
    conn = sqlite3.connect('project.db')
    cursor = conn.execute("select * from JobPostings where upper(LOCATION)=?",(l,))
    for cur in cursor:
        mydict[i]={}
        mydict[i]['companyname']=cur[0]
        mydict[i]['skillset']=cur[2]
        mydict[i]['designation']=cur[3]
        mydict[i]['experience']=cur[4]
        mydict[i]['education']=cur[5]
        i=i+1
    return render_template("browsebyloc.html",result=mydict)

@app.route('/jobbycom',methods=['POST','GET'])
def jobbycompany():    
    return render_template('jobbycom.html')

@app.route('/browsebycom',methods=['POST','GET'])
def browsebycompany():    
    cn=request.form.get('inp')
    cn=cn.upper()
    mydict={}
    i=1
    import sqlite3
    conn = sqlite3.connect('project.db')
    cursor = conn.execute("select * from JobPostings where upper(COMPANY)=?",(cn,))
    for cur in cursor:
        mydict[i]={}
        mydict[i]['location']=cur[1]
        mydict[i]['skillset']=cur[2]
        mydict[i]['designation']=cur[3]
        mydict[i]['experience']=cur[4]
        mydict[i]['education']=cur[5]
        i=i+1
    return render_template("browsebycom.html",result=mydict)

@app.route('/jobbydes',methods=['POST','GET'])
def jobbydes():    
    return render_template('jobbydes.html')

@app.route('/browsebydes',methods=['POST','GET'])
def browsebydes():    
    cn=request.form.get('inp')
    cn=cn.upper()
    mydict={}
    i=1
    import sqlite3
    conn = sqlite3.connect('project.db')
    cursor = conn.execute("select * from JobPostings where upper(DESIGNATION)=?",(cn,))
    for cur in cursor:
        mydict[i]={}
        mydict[i]['company']=cur[0]
        mydict[i]['location']=cur[1]
        mydict[i]['skillset']=cur[2]
        mydict[i]['experience']=cur[4]
        mydict[i]['education']=cur[5]
        i=i+1
    return render_template("browsebydes.html",result=mydict)

if __name__ == "__main__":
    app.run()
    
if __name__ == "__main__":
    app.run()