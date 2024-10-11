from flask import Blueprint, request, jsonify
from .models import db, JHA, Step

main = Blueprint('main', __name__)

#
@main.route('/jha', methods=['POST'])
def create_jha():
    data = request.get_json()
    new_jha = JHA(
        title=data['title'],
        author=data['author'],
        job_description=data['job_description'],
        job_location=data['job_location']
    )
    db.session.add(new_jha)
    db.session.commit()
    return jsonify({"message": "JHA created successfully", "jha_id": new_jha.id}), 201


@main.route('/jhas', methods=['GET'])
def get_jhas():
    jhas = JHA.query.all()
    output = []
    for jha in jhas:
        output.append({
            "id": jha.id,
            "title": jha.title,
            "author": jha.author,
            "job_description": jha.job_description,
            "job_location": jha.job_location,
            "created_at": jha.created_at,
            "updated_at": jha.updated_at
        })
    return jsonify({"jhas": output}), 200


@main.route('/jha/<int:jha_id>', methods=['GET'])
def get_jha(jha_id):
    jha = JHA.query.get_or_404(jha_id)
    steps = Step.query.filter_by(jha_id=jha_id).all()

    steps_output = []
    for step in steps:
        steps_output.append({
            "id": step.id,
            "step_number": step.step_number,
            "step_description": step.step_description,
            "hazard_description": step.hazard_description,
            "hazard_controls": step.hazard_controls
        })

    jha_data = {
        "id": jha.id,
        "title": jha.title,
        "author": jha.author,
        "job_description": jha.job_description,
        "job_location": jha.job_location,
        "steps": steps_output,
    }

    return jsonify({"jha": jha_data}), 200


@main.route('/jha/<int:jha_id>', methods=['PUT'])
def update_jha(jha_id):
    data = request.get_json()
    jha = JHA.query.get_or_404(jha_id)

    jha.title = data.get('title', jha.title)
    jha.author = data.get('author', jha.author)
    jha.job_description = data.get('job_description', jha.job_description)
    jha.job_location = data.get('job_location', jha.job_location)

    db.session.commit()
    return jsonify({"message": "JHA updated successfully"}), 200


@main.route('/jha/<int:jha_id>', methods=['DELETE'])
def delete_jha(jha_id):
    jha = JHA.query.get_or_404(jha_id)
    db.session.delete(jha)
    db.session.commit()
    return jsonify({"message": "JHA deleted successfully"}), 200


@main.route('/jha/<int:jha_id>/step', methods=['POST'])
def add_step(jha_id):
    jha = JHA.query.get_or_404(jha_id)
    data = request.get_json()

    new_step = Step(
        jha_id=jha.id, 
        step_number=data['step_number'],
        step_description=data['step_description'],
        hazard_description=data['hazard_description'],
        hazard_controls=data['hazard_controls']
    )

    db.session.add(new_step)
    db.session.commit()

    return jsonify({"message": "Step added successfully", "step_id": new_step.id}), 201

@main.route('/step/<int:step_id>', methods=['PUT'])
def update_step(step_id):
    data = request.get_json()
    step = Step.query.get_or_404(step_id)

    step.step_number = data.get('step_number', step.step_number)
    step.step_description = data.get('step_description', step.step_description)
    step.hazard_description = data.get('hazard_description', step.hazard_description)
    step.hazard_controls = data.get('hazard_controls', step.hazard_controls)

    db.session.commit()
    return jsonify({"message": "Step updated successfully"}), 200


@main.route('/step/<int:step_id>', methods=['DELETE'])
def delete_step(step_id):
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({"message": "Step deleted successfully"}), 200