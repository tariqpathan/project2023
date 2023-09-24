from database.models import Exam
from database.database_utils import get_subject_id


class ExamFactory:
    
    def _validate_exam_data(self, session, exam_data: dict):
        # Validate required fields
        if "subject_name" in exam_data:
            exam_data["subject_id"] = get_subject_id(session, exam_data["subject_name"])
        # required_fields = ['exam_board', 'month', 'year', 'unit_code', 'component_code', 'subject_id']
        # integer_fields = set(['year', 'subject_id', 'component_code', 'unit_code'])
        
        # for field in required_fields:
        #     if field not in exam_data:
        #         raise ValueError(f"{field} is required for Exam creation.")
        #     if field in integer_fields and not isinstance(exam_data[field], int):
        #         raise ValueError(f"{field} must be an integer.")

    def get_or_create_exam(self, session, exam_data: dict) -> Exam:
        self._validate_exam_data(session, exam_data)
        exam = session.query(Exam).filter(
            Exam.month.ilike(exam_data['month']),
            Exam.year == exam_data['year'],
            Exam.unit_code.ilike(exam_data['unit_code']),
            Exam.component_code.ilike(exam_data['component_code'])
        ).first()
        
        if not exam:
            exam = Exam(
                month=exam_data['month'].lower(),
                year=exam_data['year'],
                unit_code=exam_data['unit_code'],
                component_code=exam_data['component_code'],
            )
            session.add(exam)
        return exam
    