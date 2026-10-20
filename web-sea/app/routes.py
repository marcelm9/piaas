from flask import Blueprint, render_template, request, redirect, url_for
from .extensions import db
from .models import Observation

main = Blueprint("main", __name__)


@main.route("/")
def index():
    observations = Observation.query.order_by(Observation.timestamp.desc()).all()
    return render_template("index.html", observations=observations)


@main.route("/add", methods=["POST"])
def add_observation():
    animal = request.form.get("animal_name")
    stream = request.form.get("stream_name")

    if animal and stream:
        new_obs = Observation(animal_name=animal, stream_name=stream)
        db.session.add(new_obs)
        db.session.commit()

    return redirect(url_for("main.index"))
