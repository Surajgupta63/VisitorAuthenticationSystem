from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import base64
import bcrypt

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'  # Default DB
app.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///user.db',
    'db2': 'sqlite:///vms.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.init_app(app)
app.secret_key = 'secret_key6393'


class DefaultModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class User(db.Model):
    __bind_key__ = 'db1'  # Uses user.db
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(100), unique=True)
    password     = db.Column(db.String(8))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))



class VisitorDB(db.Model):
    __bind_key__        = 'db2' # Uses vms.db
    sno                 = db.Column(db.Integer, primary_key = True)
    visitor_name        = db.Column(db.String(25), nullable = False)
    mobile_number       = db.Column(db.Integer, nullable = False)
    email               = db.Column(db.String(100), nullable = False)
    purpose_of_visit    = db.Column(db.String(500), nullable = False)
    host_name           = db.Column(db.String(25), nullable = False)
    host_dept           = db.Column(db.String(25), nullable = False)
    vis_company_name    = db.Column(db.String(25), nullable = False)
    vis_company_address = db.Column(db.String(100), nullable = False)
    image_path          = db.Column(db.String(100), nullable = False)
    check_in_time       = db.Column(db.DateTime, default=datetime.utcnow)
    check_out_time      = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"{self.visitor_name} - {self.mobile_number} - {self.email} - "
            f"{self.purpose_of_visit} - {self.host_name} - {self.host_dept} - " 
            f"{self.vis_company_name} - {self.vis_company_address} - {self.image_path}"
            f"{self.check_in_time} - {self.check_out_time}"
        )



with app.app_context():
    db.create_all()


UPLOAD_FOLDER = "static\\images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return redirect('/login')


@app.route('/photo')
def photo():
    return render_template('photo.html')


@app.route("/upload", methods=["GET", "POST"])
def upload():
    print("Koi Image aaya bhai")
    image_data = request.form["imageData"]
    if image_data:
        # Decode the Base64 image
        image_data = image_data.split(",")[1]  # Remove data:image/png;base64,
        image_binary = base64.b64decode(image_data)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"captured_{timestamp}.png"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(image_binary)

        # Return the correct path to the uploaded image
        image_url = f"{file_path}"

        return render_template('index.html', image_url=image_url)
        

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        visitor_name        = request.form['visitor_name']
        mobile_number       = request.form['mobile_number']
        email               = request.form['email']
        vis_company_name    = request.form['vis_company_name']
        vis_company_address = request.form['vis_company_address']
        purpose_of_visit    = request.form['purpose_of_visit']
        host_name           = request.form['host_name']
        host_dept           = request.form['host_dept']    

        visitor_update = VisitorDB.query.filter_by(sno=sno).first()

        visitor_update.visitor_name        = visitor_name
        visitor_update.mobile_number       = mobile_number
        visitor_update.email               = email
        visitor_update.vis_company_name    = vis_company_name
        visitor_update.vis_company_address = vis_company_address
        visitor_update.purpose_of_visit    = purpose_of_visit
        visitor_update.host_name           = host_name
        visitor_update.host_dept           = host_dept

        db.session.add(visitor_update)
        db.session.commit()
        return redirect('/show_details')

    visitor = VisitorDB.query.filter_by(sno=sno).first()
    return render_template('update.html', visitor=visitor)

@app.route('/delete/<int:sno>')
def delete(sno):
    visitor = VisitorDB.query.filter_by(sno=sno).first()
    db.session.delete(visitor)
    db.session.commit()
    return redirect('/show_details')


### ---------------Authentication Routes----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ## kuch karna hai
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        
        try:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')

        except:
            db.session.rollback()  # Rollback changes to avoid breaking the session
            print("Error: bhai this email is already registered.")
            return render_template('register.html', error='Invalid!!')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ## kuch karna hai
        email    = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email']    = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error = 'Invalid!!')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    if session['email']:
        user = User.query.filter_by(email = session['email']).first()
    
    if request.method == 'POST':
        visitor_name        = request.form['visitor_name']
        mobile_number       = request.form['mobile_number']
        email               = request.form['email']
        vis_company_name    = request.form['vis_company_name']
        vis_company_address = request.form['vis_company_address']
        purpose_of_visit    = request.form['purpose_of_visit']

        host_name           = request.form['host_name']
        host_dept           = request.form['host_dept']

        image_path          = request.form['span_value']
        
        print("Mil gaya path: ", image_path)

        visitor_db = VisitorDB(visitor_name=visitor_name, mobile_number=mobile_number,
                               email=email, vis_company_name=vis_company_name, vis_company_address=vis_company_address,
                               purpose_of_visit=purpose_of_visit, image_path=image_path, host_name=host_name, host_dept=host_dept)
        
        db.session.add(visitor_db)
        db.session.commit()
    
    all_visitors = VisitorDB.query.all()  
    return render_template('index.html', all_visitors=all_visitors, user=user)

@app.route('/show_details', methods=['GET', 'POST'])
def show_details():
    if request.method == 'POST' and request.form['search']:
        visitor_name = request.form['search']

        visitor = VisitorDB.query.filter_by(visitor_name=visitor_name).first()
        
        return render_template('data.html', visitor=visitor)

    all_visitors = VisitorDB.query.all()
    return render_template('data.html', all_visitors=all_visitors)

if __name__ == '__main__':
    app.run(debug=True, port=8000)