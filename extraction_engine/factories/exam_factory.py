import logging

from database.models import Exam, Subject

logger = logging.getLogger(__name__)


class ExamFactory:

    def _normalise_exam_data(self, session, exam_data: dict):
        # Validate required fields
        if "subject" in exam_data:
            subject = session.query(Subject).filter(
                Subject.name.ilike(exam_data["subject"])).first()
            exam_data["subject_id"] = subject.id
        lowercased = {k: v.lower() if isinstance(v, str) else v for k, v in exam_data.items()}
        return lowercased

    def get_or_create_exam(self, session, input_data: dict) -> Exam:
        exam_data = self._normalise_exam_data(session, input_data)
        exam = session.query(Exam).filter(
            Exam.month.ilike(exam_data['month']),
            Exam.year == exam_data['year'],
            Exam.unit_code.ilike(exam_data['unit_code']),
            Exam.component_code.ilike(exam_data['component_code'])
        ).first()

        if not exam:
            exam = Exam(
                subject_id=exam_data['subject_id'],
                exam_board=exam_data['exam_board'].lower(),
                month=exam_data['month'].lower(),
                year=exam_data['year'],
                unit_code=exam_data['unit_code'],
                component_code=exam_data['component_code'],
            )
            session.add(exam)
        return exam
