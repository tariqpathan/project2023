# from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from typing import List, Tuple, Dict, Any
# from database.models import Question
# from test_generator.question_service import QuestionService
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

A4_WIDTH, A4_HEIGHT = A4
LEFT_MARGIN = 1 * inch
TOP_MARGIN = 0.5 * inch
RECT_X_OFFSET = 0.4 * inch
RECT_Y_OFFSET = 0.5 * inch
RECT_WIDTH = 0.5 * inch
RECT_HEIGHT = 0.3 * inch

ANSWER_TEXT_Y_OFFSET = 0.4 * inch
TEXT_FONT = "Helvetica"
TEXT_FONT_SIZE = 12
TEXT_HEIGHT = 0.1 * inch
QUESTION_NUMBER_RIGHT_PADDING = 0.15 * inch  # Adjust as needed
QUESTION_ID_RIGHT_PADDING = 0.15 * inch  # Adjust as needed
QUESTION_NUMBER_TOP_MARGIN = 0.37 * inch  # Adjust as needed
QUESTION_ID_TOP_MARGIN = 0.6 * inch  # Adjust as needed

def draw_image(c, image_path, y_position, new_image_width, new_image_height):
    """Draws the image on the canvas."""
    c.drawImage(image_path, 0, y_position - new_image_height, width=new_image_width, height=new_image_height)

def draw_rectangle_and_number(c: canvas.Canvas, y_position: float, question_number: int, question_id: int):
    """Draws the white rectangle and the question number on it."""
    c.setFillColorRGB(1, 1, 1)
    c.rect(RECT_X_OFFSET, y_position - RECT_Y_OFFSET, RECT_WIDTH, RECT_HEIGHT, fill=1, stroke=0)

    # For question_number
    text1 = f"{question_number + 1}"
    text1_width = stringWidth(text1, TEXT_FONT, TEXT_FONT_SIZE)
    x1_position = RECT_X_OFFSET + RECT_WIDTH - text1_width - QUESTION_NUMBER_RIGHT_PADDING
    y1_position = y_position - QUESTION_NUMBER_TOP_MARGIN

    c.setFont(TEXT_FONT, TEXT_FONT_SIZE)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(x1_position, y1_position, text1)

    # For question_id
    text2 = f"r.id.{question_id}"
    text2_width = stringWidth(text2, TEXT_FONT, TEXT_FONT_SIZE - 4)
    x2_position = RECT_X_OFFSET + RECT_WIDTH - text2_width - QUESTION_ID_RIGHT_PADDING
    y2_position = y_position - QUESTION_ID_TOP_MARGIN

    c.setFont(TEXT_FONT, TEXT_FONT_SIZE - 4)
    c.drawString(x2_position, y2_position, text2)

def draw_code(c: canvas.Canvas, code: str) -> None:
    """Draws the code on the PDF."""
    c.setFont(TEXT_FONT, TEXT_FONT_SIZE - 2)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(LEFT_MARGIN, A4_HEIGHT - TOP_MARGIN + TEXT_HEIGHT, f"{code}")

def draw_single_question(c: canvas.Canvas, ques_img_path: str, question_id: int,
                   y_position: float, question_number: int) -> float:
    """
    Draws a single question image on the PDF along with a question number.
    
    :param c: Canvas object for PDF drawing
    :param question: Question object containing data
    :param y_position: The Y-coordinate for the drawing
    :param question_number: The index number of the question
    :return: Updated y_position
    """
    new_image_width, new_image_height = scale_image(ques_img_path, A4_WIDTH)

    if y_position - new_image_height < TOP_MARGIN:
        c.showPage()
        y_position = A4_HEIGHT - TOP_MARGIN

    draw_image(c, ques_img_path, y_position, new_image_width, new_image_height)
    draw_rectangle_and_number(c, y_position, question_number, question_id)
    
    y_position -= (new_image_height + TOP_MARGIN)
    return y_position

def scale_image(image_path: str, max_width: float) -> Tuple[float, float]:
    """Scales the image to fit within the specified max_width."""
    try:
        image = utils.ImageReader(image_path)
        image_width, image_height = image.getSize()
        scaling_factor = max_width / float(image_width)
        new_image_width = (image_width * scaling_factor)
        new_image_height = (image_height * scaling_factor)
        return new_image_width, new_image_height
    except Exception as e:
        raise ValueError(f"Unable to scale image: {e}")


def draw_answers(c: canvas.Canvas, questions: List[Dict[str, str|int]]) -> None:
    """
    Draws the answers to questions on the PDF.
    
    :param c: Canvas object for PDF drawing
    :param questions: List of Question objects
    """
    y_position = A4_HEIGHT - (TOP_MARGIN + ANSWER_TEXT_Y_OFFSET) # Resetting y-position
    c.setFont(TEXT_FONT, TEXT_FONT_SIZE)

    for i, question in enumerate(questions):
        c.drawString(LEFT_MARGIN, y_position, f"[R.ID: {question['id']}] Question {i + 1}: {question['answer']}")
        y_position -= ANSWER_TEXT_Y_OFFSET  # Move down for the next answer

        # Check remaining space for text; if not enough, start a new page
        if y_position < TOP_MARGIN:
            c.showPage()
            y_position = A4_HEIGHT - TOP_MARGIN

def draw_questions(c: canvas.Canvas, questions: List[Dict[str, Any]]) -> None:
    
    y_position = A4_HEIGHT - TOP_MARGIN  # Initialize y_position

    for i, question in enumerate(questions):
    
        img_path = question["question"]
        id = question["id"]
        y_position = draw_single_question(
            c, ques_img_path=img_path, question_id=id, y_position=y_position, question_number= i)

def generate_pdf(data: Dict[str, Any], file_name: str) -> None:
    """
    Generates a PDF file containing questions and their answers.
    
    :param questions: List of Question objects
    :param file_name: Name of the output PDF file
    """
    code = data["code"]
    questions = data["result"]
    c = canvas.Canvas(file_name, pagesize=A4)
    draw_code(c, code)
    draw_questions(c, questions)
    # Move to a new page for answers
    c.showPage()
    draw_code(c, code)
    draw_answers(c, questions)
    c.save()

def draw_debug_line(c: canvas.Canvas):
    c.setStrokeColorRGB(1, 0, 0)
    c.line(LEFT_MARGIN, A4_HEIGHT - TOP_MARGIN, A4_WIDTH - LEFT_MARGIN, A4_HEIGHT - TOP_MARGIN)

if __name__ == "__main__":

    data = {
    "code": "cqob11",
    "result": [
        {
            "id": 2,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-d3948494-7f7b-4f9b-bc8e-ea9243f967dc.jpg",
            "answer": "A"
        },
        {
            "id": 7,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-fa9efa44-3d5a-4de6-a6bb-654dddae4c4c.jpg",
            "answer": "C"
        },
        {
            "id": 14,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-3afa349f-a760-4c55-be39-551ea6917c72.jpg",
            "answer": "A"
        },
        {
            "id": 15,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-6a50a78c-466c-4bc0-bcbd-2143e573153c.jpg",
            "answer": "B"
        },
        {
            "id": 16,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-0eb4b70b-e188-4226-9fe1-66a3c30dbec4.jpg",
            "answer": "B"
        },
        {
            "id": 23,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-315e4780-bbf4-4377-bbf6-91ac20644284.jpg",
            "answer": "D"
        },
        {
            "id": 24,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-b3a5cdcc-5ec7-48db-9b1a-05ace9f60d2c.jpg",
            "answer": "A"
        },
        {
            "id": 27,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-ead2c80f-4343-4d74-889e-3058dcfd9761.jpg",
            "answer": "D"
        },
        {
            "id": 30,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-33b93a85-c23a-4999-9cf8-7be1f0df2517.jpg",
            "answer": "B"
        },
        {
            "id": 40,
            "question": "C:/Users/Tariq/Documents/birkbeck-project/static/question_images/2010-061011-d9189b1d-d9da-47d4-b0d9-f4239d9033f2.jpg",
            "answer": "B"
        }
    ]
}
    
    generate_pdf(data, "deleteThis-test2.pdf")