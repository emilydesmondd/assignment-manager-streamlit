class AssignmentManager:
    def __init__(self, initial_assignments: list[dict]) -> None:
        self.assignments = initial_assignments  # This will hold all assignments in memory

    def all(self) -> list[dict]:
        return list(self.assignments)

    def add(self, title: str, description: str, due_date: str, points: int, assignment_type: str):
        assignment_id = len(self.assignments) + 1  # Simple ID generation
        new_assignment = {
            'id': assignment_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'points': points,
            'type': assignment_type
        }
        self.assignments.append(new_assignment)
        return new_assignment

    def delete(self, assignment_id: int):
        self.assignments = [a for a in self.assignments if a['id'] != assignment_id]
