from flask import Blueprint, request, jsonify
from .models import db, JHA, Step
from .schemas import StepSchema, JHASchema

main = Blueprint("main", __name__)


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
    new_jha = JHA(
        title=data["title"],
        author=data["author"],
        job_description=data["job_description"],
        job_location=data["job_location"],
    )
    db.session.add(new_jha)
    db.session.commit()
    return jsonify({"message": "JHA created successfully", "jha_id": new_jha.id}), 201


# Get all of the JHAs
@main.route("/jhas", methods=["GET"])
def get_jhas():
    jhas = JHA.query.all()
    response = [
        JHASchema(
            jha.id,
            jha.title,
            jha.author,
            jha.job_description,
            jha.job_location,
            jha.created_at,
            jha.updated_at,
            [],
        ).to_dict()
        for jha in jhas
    ]
    return jsonify({"jhas": response}), 200


# Get a single JHA
@main.route("/jha/<int:jha_id>", methods=["GET"])
def get_jha(jha_id):
    jha = JHA.query.get_or_404(jha_id)
    steps = Step.query.filter_by(jha_id=jha_id).all()

    steps_output = [
        StepSchema(
            step.id,
            step.step_number,
            step.step_description,
            step.hazard_description,
            step.hazard_controls,
        )
        for step in steps
    ]

    jha_response = JHASchema(
        jha.id,
        jha.title,
        jha.author,
        jha.job_description,
        jha.job_location,
        jha.created_at,
        jha.updated_at,
        steps_output,
    )

    return jsonify(jha_response.to_dict()), 200


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
    jha = JHA.query.get_or_404(jha_id)
    highest_step = Step.query.filter_by(jha_id=jha_id).order_by(Step.step_number.desc()).first()
    next_step_number = 1 if highest_step is None else highest_step.step_number + 1
    data = request.get_json()

    new_step = Step(
        jha_id=jha.id,
        step_number=next_step_number,
        step_description=data["step_description"],
        hazard_description=data["hazard_description"],
        hazard_controls=data["hazard_controls"],
    )

    db.session.add(new_step)
    db.session.commit()

    return jsonify({"message": "Step added successfully", "step_number": next_step_number}), 201


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
    step.hazard_description = data.get("hazard_description", step.hazard_description)
    step.hazard_controls = data.get("hazard_controls", step.hazard_controls)

    db.session.commit()
    return jsonify({"message": "Step updated successfully"}), 200


# Delete a step
@main.route("/step/<int:step_id>", methods=["DELETE"])
def delete_step(step_id):
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({"message": "Step deleted successfully"}), 200
