from database.models import Exam


class ExamFactory:
    
    def __init__(self, db_session):
        self.db_session = db_session

    def create_exam(self, exam_board: str, month: str, year: int, unit_code: str, 
                    component_code: str, subject_id: int) -> Exam:
        
        exam = Exam(
            exam_board=exam_board,
            month=month,
            year=year,
            unit_code=unit_code,
            component_code=component_code,
            subject_id=subject_id
        )

        try:
            self.db_session.add(exam)
        except Exception as e:
            raise Exception(f"Error creating Exam: {exam_board, month, year}. Error: {e}")
        
        return exam
    
    