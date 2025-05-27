from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(200), nullable = False)
    Description = db.Column(db.String(500), nullable = False)
    Date_Created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'{self.SNo}-{self.Title}'

@app.route('/', methods = ['POST', 'GET'])
def myApp():
    if request.method == 'POST':
        Title = request.form['todoTitle']
        Description = request.form['todoDescription']
        todo = Todo(Title = Title, Description = Description)
        db.session.add(todo)
        db.session.commit()
    
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:SNo>', methods = ['GET', 'POST'])
def update(SNo):
    todo = Todo.query.get_or_404(SNo)
    if request.method == 'POST':
        todo.Title = request.form['todoTitle']
        todo.Description = request.form['todoDescription']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)
    # print(alltodo)
    # return'This is products page'

@app.route('/delete/<int:SNo>', methods =['GET', 'POST'])
def delete(SNo):
    todo = Todo.query.filter_by(SNo=SNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == ('__main__'):
    with app.app_context():
        db.create_all() 
        print('Database created successfully')
app.run(debug=True)