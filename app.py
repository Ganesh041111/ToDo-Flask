from turtle import title
from flask import Flask, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)

@app.route('/')
def index():
    todolist=Todo.query.all()
    print(todolist)
    return render_template('base.html',todolist=todolist)

@app.route("/add", methods=["POST"])
def add():
    title= request.form.get("title")
    new_todo=Todo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todoid>")
def update(todoid):
    todo=Todo.query.filter_by(id=todoid).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todoid>")
def delete(todoid):
    todo=Todo.query.filter_by(id=todoid).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__=='__main__':
    db.create_all()

    # new_todo = Todo(title='test1', complete=False)
    # db.session.add(new_todo)
    # db.session.commit()


    app.run(debug=True)
