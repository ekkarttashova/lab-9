from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_book.db'
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        new_contact = Contact(name=name, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('index'))
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)