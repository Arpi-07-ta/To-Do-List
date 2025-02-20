from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        status = request.form['status']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()

        new_task = Task(title=title, description=description, category=category, status=status, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('list_view'))
    return render_template('form.html')

@app.route('/tasks', methods=['GET'])
def list_view():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.category = request.form['category']
        task.status = request.form['status']
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('list_view'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('list_view'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
