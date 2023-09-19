from database.models import Exam


class ExamFactory:
    
    def _validate_exam_data(self, exam_data: dict):
        # Validate required fields
        required_fields = ['exam_board', 'month', 'year', 'unit_code', 'component_code', 'subject_id']
        integer_fields = set(['year', 'subject_id', 'component_code', 'unit_code'])
        
        for field in required_fields:
            if field not in exam_data:
                raise ValueError(f"{field} is required for Exam creation.")
            if field in integer_fields and not isinstance(exam_data[field], int):
                raise ValueError(f"{field} must be an integer.")

    def create_exam(self, exam_data: dict) -> Exam:
        self._validate_exam_data(exam_data)

        # If all validations pass, create the Exam object
        exam = Exam(**exam_data)
        return exam

    
    