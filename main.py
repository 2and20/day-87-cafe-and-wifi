
import random
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)

### CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(250))
    map_url = db.Column(db.String(500))
    img_url = db.Column(db.String(250))
    location = db.Column(db.String(250))
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.Integer)
    coffee_price = db.Column(db.String(20))

    def to_dict(self):
        my_dict = {}
        for column in self.__table__.columns:
            my_dict[column.name] = getattr(self, column.name)
        return my_dict

cafes = Cafe()
my_dict = cafes.to_dict()
all_cafes = db.session.query(Cafe).all()


@app.route("/")
def homepage():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', my_dict=my_dict, all_cafes=all_cafes)

@app.route('/random')
def get_rand_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    print(jsonify(cafe=random_cafe.to_dict()))
    # return jsonify(cafe=random_cafe.to_dict())
    return render_template(random_cafe.html)


@app.route('/add-cafe', methods=["GET","POST"])
def add_a_cafe():
    if request.method == "GET":
        return render_template('add-cafe.html')
    else:
        if request.form.get('plug') == "Yes":
            plug = True
        else:
            plug = False
        if request.form.get('toilet') == True:
            toilet = True
        else:
            toilet = False
        if request.form.get('wifi') == True:
            wifi = True
        else:
            wifi = False
        if request.form.get('calls') == "On":
            calls = True
        else:
            calls = False

        new_cafe = Cafe(
            # id = db.Column(db.String(250), primary_key = True)
            name = request.form.get('name'),
            map_url = request.form.get('map'),
            img_url = request.form.get('image'),
            location = request.form.get('location'),
            has_sockets = plug,
            has_toilet = toilet,
            has_wifi = wifi,
            can_take_calls = calls,
            seats = request.form.get('seats'),
            coffee_price = request.form.get('price')
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('homepage'))


@app.route('/delete_cafe')
def delete():
    cafe_delete_id = request.args.get('cafe_id')
    cafe_to_delete = Cafe.query.get(cafe_delete_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('homepage'))




## must be at end of code, keeps flask running ##
if __name__ == "__main__":
    app.run(debug=True)

