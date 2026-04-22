import json
from pathlib import Path

class AssignmentStore:
    def __init__(self) -> None:
        self.file_path = Path('assignments.json')
        self.assignments = self.load_assignments()

    def load_assignments(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def save_assignments(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.assignments, f, indent=4)

    def add_assignment(self, manager_id: str, employee_id: str):
        if manager_id not in self.assignments:
            self.assignments[manager_id] = []
        if employee_id not in self.assignments[manager_id]:
            self.assignments[manager_id].append(employee_id)
            self.save_assignments()

    def get_assignments(self, manager_id: str):
        return self.assignments.get(manager_id, [])