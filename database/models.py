from sqlalchemy import Boolean, Integer, String, ForeignKey, Table, Column, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class Subject(Base):
    __tablename__ = 'subjects'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True, nullable=False)

    exams = relationship('Exam', back_populates='subject')
    subtopics = relationship('Subtopic', back_populates='subject')


class Exam(Base):
    __tablename__ = 'exams'

    id = mapped_column(Integer, primary_key=True)
    exam_board = mapped_column(String, nullable=False)
    month = mapped_column(String, nullable=False)
    year = mapped_column(Integer, nullable=False)
    unit_code = mapped_column(String, nullable=False)
    component_code = mapped_column(String, nullable=False)
    subject_id = mapped_column(Integer, ForeignKey('subjects.id'))

    subject = relationship('Subject', back_populates='exams')
    questions = relationship('Question', back_populates='exam')

    __table_args__ = (UniqueConstraint('exam_board', 'month', 'year', 'unit_code',
                                       'component_code', 'subject_id', name='uc_exam'),)  # comma is required for tuple


class Difficulty(Base):
    __tablename__ = 'difficulties'

    id = mapped_column(Integer, primary_key=True)
    level = mapped_column(String, unique=True, nullable=False)

    questions = relationship('Question', back_populates='difficulty')


class Question(Base):
    __tablename__ = 'questions'

    id = mapped_column(Integer, primary_key=True)
    image_filename = mapped_column(String, unique=True, nullable=False)
    question_number = mapped_column(Integer, nullable=True)
    difficulty_id = mapped_column(Integer, ForeignKey('difficulties.id'), nullable=True)
    exam_id = mapped_column(Integer, ForeignKey('exams.id'), nullable=False)

    # uselist = False means it's a one-to-one relationship
    answer = relationship('Answer', back_populates='question', uselist=False)
    difficulty = relationship('Difficulty', back_populates='questions')
    exam = relationship('Exam', back_populates='questions')
    subtopics = relationship('Subtopic', secondary='question_subtopic', back_populates='questions')
    codes = relationship('Code', secondary='question_code', back_populates='questions')
    # question_text = relationship('QuestionText', uselist=False, back_populates='question')


class Subtopic(Base):
    __tablename__ = 'subtopics'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    subject_id = mapped_column(Integer, ForeignKey('subjects.id'))

    subject = relationship('Subject', back_populates='subtopics')
    questions = relationship('Question', secondary='question_subtopic', back_populates='subtopics')


class Answer(Base):
    __tablename__ = 'answers'

    id = mapped_column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answer_text = mapped_column(String, nullable=False)

    question = relationship('Question', back_populates='answer')


class Code(Base):
    __tablename__ = 'codes'

    id = mapped_column(Integer, primary_key=True)
    code_str = mapped_column(String, unique=True, nullable=False)

    questions = relationship('Question', secondary='question_code', back_populates='codes')


# class QuestionText(Base):
#     __tablename__ = 'question_texts'
#
#     id = mapped_column(Integer, primary_key=True)
#     question_id = mapped_column(Integer, ForeignKey('questions.id'), nullable=False)
#     raw_text = mapped_column(String, nullable=False)
#     processed_text = mapped_column(String, nullable=False)
#     is_training_data = mapped_column(Boolean, default=False)
#
#     question = relationship('Question', back_populates='question_texts')


# Association table for many-to-many relationship between questions and subtopics
question_subtopic_table = Table('question_subtopic', Base.metadata,
                                Column('question_id', Integer, ForeignKey('questions.id'), primary_key=True),
                                Column('subtopic_id', Integer, ForeignKey('subtopics.id'), primary_key=True)
                                )

question_code_table = Table('question_code', Base.metadata,
                            Column('question_id', Integer, ForeignKey('questions.id'), primary_key=True),
                            Column('code_id', Integer, ForeignKey('codes.id'), primary_key=True)
                            )