from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Update the database URI to connect to your PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://admin:password@localhost/simpleform"
)

db = SQLAlchemy(app)


# Define a model for your data
class Item(db.Model):
    __tablename__ = "simple_data"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)


@app.route("/")
def index():
    items = Item.query.all()  # Retrieve all records from the database
    return render_template("index.html", items=items)


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", item=item)


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/create", methods=["GET", "POST"])
def create_item():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
