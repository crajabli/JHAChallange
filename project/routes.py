from flask import Blueprint, request, jsonify
from .models import db, JHA, Step, Hazard
from .schemas import StepSchema, JHASchema, HazardSchema
from marshmallow import ValidationError

main = Blueprint("main", __name__)


jha_schema = JHASchema()
step_schema = StepSchema()
hazard_schema = HazardSchema()
hazards_schema = HazardSchema(many=True)

# request payload:
# {
#   "title": "Welding Safety",
#   "author": "John Doe",
#   "job_description": "This JHA covers the hazards associated with welding tasks.",
#   "job_location": "Workshop A"
# }
@main.route("/jha", methods=["POST"])
def create_jha():
    data = request.get_json()

    try:
        validated_data = jha_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400


    new_jha = JHA(
        title=validated_data["title"],
        author=validated_data["author"],
        job_description=validated_data["job_description"],
        job_location=validated_data["job_location"],
    )

    db.session.add(new_jha)
    db.session.commit()
    return jsonify(jha_schema.dump(new_jha)), 201


# Get all of the JHAs
@main.route("/jhas", methods=["GET"])
def get_jhas():
    jhas = JHA.query.all()
    response = jha_schema.dump(jhas, many=True)
    return jsonify({"jhas": response}), 200


# Get a single JHA
@main.route("/jha/<int:jha_id>", methods=["GET"])
def get_jha(jha_id):
    jha = JHA.query.get_or_404(jha_id)
    response = jha_schema.dump(jha)

    return jsonify(response), 200


# Update a JHA
# Example request payload:
# {
#   "title": "Updated Welding Safety",
#   "job_location": "Workshop B"
# }
@main.route("/jha/<int:jha_id>", methods=["PUT"])
def update_jha(jha_id):
    data = request.get_json()
    jha = JHA.query.get_or_404(jha_id)

    jha.title = data.get("title", jha.title)
    jha.author = data.get("author", jha.author)
    jha.job_description = data.get("job_description", jha.job_description)
    jha.job_location = data.get("job_location", jha.job_location)

    db.session.commit()
    return jsonify({"message": "JHA updated successfully"}), 200


# Delete a JHA
@main.route("/jha/<int:jha_id>", methods=["DELETE"])
def delete_jha(jha_id):
    jha = JHA.query.get_or_404(jha_id)
    db.session.delete(jha)
    db.session.commit()
    return jsonify({"message": "JHA deleted successfully"}), 200


# Add a step to a JHA
# Example request payload:
# {
#   "step_number": 1,
#   "description": "Prepare the equipment",
#   "hazards": "Electrical hazards",
#   "controls": "Wear insulated gloves"
# }
@main.route("/jha/<int:jha_id>/step", methods=["POST"])
def add_step(jha_id):
    highest_step = Step.query.filter_by(jha_id=jha_id).order_by(Step.step_number.desc()).first()
    next_step_number = 1 if highest_step is None else highest_step.step_number + 1
    data = request.get_json()

    try:
        validated_data = step_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_step = Step(
        jha_id=jha_id,
        step_number=next_step_number,
        step_description=validated_data["step_description"],
    )

    db.session.add(new_step)
    db.session.commit()

    return jsonify({"message": "Step added successfully", "New Step": step_schema.dump(new_step)}), 201


# Update a step
@main.route("/step/<int:step_id>", methods=["PUT"])
def update_step(step_id):
    data = request.get_json()
    step = Step.query.get_or_404(step_id)

    new_step_number = data.get('step_number')

    if new_step_number and new_step_number != step.step_number:
        conflicting_step = Step.query.filter_by(jha_id=step.jha_id, step_number = new_step_number).first()

        if conflicting_step:
            conflicting_step.step_number = step.step_number
            step.step_number = new_step_number
            db.session.commit()
        else:
            step.step_number = new_step_number

    step.step_description = data.get("step_description", step.step_description)

    db.session.commit()
    return jsonify({"message": "Step updated successfully"}), 200


# Get a single step
@main.route("/step/<int:step_id>", methods=["GET"])
def get_step(step_id):
    step = Step.query.get_or_404(step_id)
    response = step_schema.dump(step)

    return jsonify(response), 200


# Delete a step
@main.route("/step/<int:step_id>", methods=["DELETE"])
def delete_step(step_id):
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({"message": "Step deleted successfully"}), 200


# Add a hazard to a step
@main.route("/step/<int:step_id>/hazard", methods=["POST"])
def add_hazard(step_id):
    data = request.get_json()

    try:
        validated_data = hazard_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_hazard = Hazard(
        step_id=step_id,
        description=validated_data["description"],
        controls=validated_data["controls"],
    )

    db.session.add(new_hazard)
    db.session.commit()

    return jsonify({"message": "Hazard added successfully", "New Hazard": hazard_schema.dump(new_hazard)}), 201


# Update a hazard
@main.route("/hazard/<int:hazard_id>", methods=["PUT"])
def update_hazard(hazard_id):
    data = request.get_json()
    hazard = Hazard.query.get_or_404(hazard_id)

    hazard.description = data.get("description", hazard.description)
    hazard.controls = data.get("controls", hazard.controls)

    db.session.commit()
    return jsonify({"message": "Hazard updated successfully"}), 200


# Delete a hazard
@main.route("/hazard/<int:hazard_id>", methods=["DELETE"])
def delete_hazard(hazard_id):
    hazard = Hazard.query.get_or_404(hazard_id)
    db.session.delete(hazard)
    db.session.commit()
    return jsonify({"message": "Hazard deleted successfully"}), 200
