from marshmallow import Schema, fields, validates, ValidationError

class HazardSchema(Schema):
    id = fields.Int(dump_only=True)
    step_id = fields.Int()
    description = fields.Str(required=True)
    controls = fields.Str(required=True)


class StepSchema(Schema):
    id = fields.Int(dump_only=True)
    step_number = fields.Int(dump_only=True)
    step_description = fields.Str(required=True)
    jha_id = fields.Int()
    hazards = fields.List(fields.Nested(HazardSchema), dump_only=True)


class JHASchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    job_description = fields.Str(required=True)
    job_location = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    steps = fields.List(fields.Nested(StepSchema), dump_only=True)
