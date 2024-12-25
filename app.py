from flask import Flask,render_template,redirect,url_for,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
app=Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True )
    content = db.Column(db.String(100), nullable=False ) 
    complete = db.Column(db.Integer, default=0) 
    create = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:

        return f"Task {self.id}"
with app.app_context():
    db.create_all()    


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
        current_task=request.form['content']
        new_task=todo(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f'ERROR{e}')
            return f'ERROR:{e}'
    else:
        tasks=todo.query.order_by(todo.create).all()    
    return render_template("index.html",tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id:int):
    try:

        delete_task=todo.query.get_or_404(id)
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR{e}")
        return f"ERROR{e}"

@app.route('/update/<int:id>',methods=["POST","GET"])
def update(id:int):
    task=todo.query.get_or_404(id)
    if request.method == "POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR{e}"
    else:
        return render_template("update.html", task=task)  



if __name__ == ("__main_"):
    app.run(debug=True)
