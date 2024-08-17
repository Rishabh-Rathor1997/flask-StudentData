from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Student(db.Model):
    sno = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    class_ = db.Column(db.String(50))
    section = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    address = db.Column(db.String(200))
    dob = db.Column(db.String(50))
    mobile_no = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())

    def __repr__(self):
        return f'<Student {self.name}>'

@app.route("/")
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    search_option = request.args.get("search_option")

    if not query or not search_option:
        # Return an error message if the query or search option is missing
        return "Missing query or search option.", 400

    # Perform the search based on the search option
    if search_option == "Name":
        students = Student.query.filter(Student.name.ilike(f"%{query}%", escape="/")).all()
    elif search_option == "Id":
        try:
            id_value = int(query)
            students = Student.query.filter(Student.id == id_value).all()
        except ValueError:
            # Return an error message if the Id search option is not a valid integer
            return "Invalid Id value.", 400
    elif search_option == "Mobile_No":
        students = Student.query.filter(Student.mobile_no.ilike(f"%{query}%", escape="/")).all()
    elif search_option == "Dob":
        students = Student.query.filter(Student.dob.ilike(f"%{query}%", escape="/")).all()
    elif search_option == "Email":
        students = Student.query.filter(Student.email.ilike(f"%{query}%", escape="/")).all()
    else:
        # Return an error message if the search option is not recognized
        return "Invalid search option.", 400

    # Render the search results using the search.html template
    return render_template("search.html", students=students, query=query, search_option=search_option)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        id = request.form["id"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        class_ = request.form["class"]
        section = request.form["section"]
        gender = request.form["gender"]
        address = request.form["address"]
        dob = request.form["dob"]
        mobile_no = request.form["mobile_no"]

        student = Student(name=f"{firstname} {lastname}",
                          id=id,
                          email=email,
                          class_=class_,
                          section=section,
                          gender=gender,
                          address=address,
                          dob=dob,
                          mobile_no=mobile_no)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    student = Student.query.filter_by(id=id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for('index'))
    
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    student = Student.query.filter_by(id=id).first()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        class_ = request.form["class"]
        section = request.form["section"]
        gender = request.form["gender"]
        address = request.form["address"]
        dob = request.form["dob"]
        mobile_no = request.form["mobile_no"]
        
        student.name = name
        student.email = email
        student.class_ = class_
        student.section = section
        student.gender = gender
        student.address = address
        student.dob = dob
        student.mobile_no = mobile_no
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('update.html', student=student)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)