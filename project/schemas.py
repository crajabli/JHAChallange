from typing import List, Dict
from datetime import datetime


class StepSchema:
    def __init__(self, id: int, step_number: int, 
                step_description: str, hazard_description: str, hazard_controls: str):
        self.id = id
        self.step_number = step_number
        self.step_description = step_description
        self.hazard_description = hazard_description
        self.hazard_controls = hazard_controls
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "step_number": self.step_number,
            "step_description": self.step_description,
            "hazard_description": self.hazard_description,
            "hazard_controls": self.hazard_controls
        }
    

class JHASchema:
    def __init__(self, id: int, title: str, author: str, job_description: str, job_location: str, 
                created_at: datetime, updated_at: datetime, steps: List[StepSchema]):
        self.id = id
        self.title = title
        self.author = author
        self.job_description = job_description
        self.job_location = job_location
        self.created_at = created_at
        self.updated_at = updated_at
        self.steps = steps
    
    def to_dict(self) -> Dict:
       
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "job_description": self.job_description,
            "job_location": self.job_location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "steps": [step.to_dict() for step in self.steps]
        }
    