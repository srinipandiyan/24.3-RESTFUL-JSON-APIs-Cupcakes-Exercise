"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
db.create_all()

@app.route("/")
def root():
    """Render homepage at root directory."""

    return render_template("index.html")

@app.route("/api/cupcakes", methods=["GET"])
def get_all_cupcakes():
    """Get values for each cupcake instance in JSON format:
    {cupcakes: [{id, flavor, size, rating, image}, ...]}."""

    #list comprehension to serialize all instances of cupcake in table 'cupcakes'
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["GET"])
def get_cupcake(cupcake_id):
    """Get existing cupcake within index by id in JSON format: 
    {cupcake: [{id, flavor, size, rating, image}, ...]},
    or return 404."""

    get_cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake = get_cupcake.serialize()
    return jsonify(cupcake=cupcake)

@app.route("/api/cupcakes", methods=["POST"])
def create_new_cupcake():
    """Create new cupcake, add to index, and return data in JSON format:
    {cupcake: [{id, flavor, size, rating, image}, ...]}."""

    #create new cupcake instance from create cupcake form response
    res = request.json
    new_cupcake = Cupcake(
        flavor = res['flavor'],
        size = res['size'],
        rating = res['rating'],
        image = res['image'] or None
    )

    #add new cupcake to database
    db.session.add(new_cupcake)
    db.session.commit()

    #return new cupcake data in JSON format with HTTP Status of 201, per RESTful API conventions
    cupcake = new_cupcake.serialize()
    return (jsonify(cupcake=cupcake), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update existing cupcake within index by id and return data in JSON format:
    {cupcake: [{id, flavor, size, rating, image}, ...]},
    or raise 404."""

    #access cupcake by id and update form responses
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    res = request.json

    #update Cupcake attributes with form responses
    cupcake.flavor = res['flavor']
    cupcake.size = res['size']
    cupcake.rating = res['rating']
    cupcake.image = res.get('image', None)

    #commit to updates to database
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete existing cupcake within index by id and return confirmation message in JSON format:
     {message: "Deleted"},
     or raise 404."""
    
    #access cupcake by id
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    #delete cupcake and update database
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")