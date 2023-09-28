from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

@app.route('/')
def index():
    memos = Memo.query.all()
    return render_template('index.html', memos=memos)

@app.route('/add_memo', methods=['POST'])
def add_memo():
    content = request.form['content']
    if content:
        memo = Memo(content=content)
        db.session.add(memo)
        db.session.commit()
        flash('success メモが追加されました')
    else:
        flash('danger メモが空白です')
    return redirect(url_for('index'))

@app.route('/delete_memo/<int:id>')
def delete_memo(id):
    memo = Memo.query.get_or_404(id)
    db.session.delete(memo)
    db.session.commit()
    flash('success メモが削除されました')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
