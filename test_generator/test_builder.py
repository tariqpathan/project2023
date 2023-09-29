from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from typing import List, Tuple
from database.models import Question
from database.database_manager import DatabaseManager
from test_generator.question_retriever import QuestionRetriever
from extraction_engine.managers.file_manager import FileManager
from reportlab.lib.units import inch

Y_MARGIN = 0.5 * inch

def draw_question(c, question, y_position, question_number):
    
    image_path = f"./static/question_images/{question.image_filename}"
    new_image_width, new_image_height = scale_image(image_path, c._pagesize[0])  # Full A4 width

    # Check if the image height goes over the remaining page height
    if y_position - new_image_height < 0:
        c.showPage()
        y_position = c._pagesize[1] - 1 * inch

    # Draw the image over the white rectangle
    c.drawImage(image_path, 0, y_position - new_image_height, width=new_image_width, height=new_image_height)

    # Set fill color to white for rectangle
    c.setFillColorRGB(1, 1, 1)  # White

    # Calculate the position for the rectangle. You might need to adjust these.
    rect_x = 0.4 * inch
    rect_y = y_position - 0.5 * inch
    rect_width = 0.5 * inch
    rect_height = 0.3 * inch

    # Draw a white rectangle
    c.rect(rect_x, rect_y, rect_width, rect_height, fill=1, stroke=0)

    # Set font and color for text
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0, 0, 0)  # Black for text

    # Draw the question number on top of the rectangle
    text_x = 0.5 * inch
    text_y = y_position - 0.4 * inch
    c.drawString(text_x, text_y, f"{question_number + 1}")

    """
    alternative
    # Relative position of rectangle to image
    rect_x = image_x + 10  # 10 points from the left edge of the image
    rect_y = image_y + image_height - 30  # 30 points from the top edge of the image
    rect_width = 60  # width of the rectangle
    rect_height = 20  # height of the rectangle

    # Draw rectangle with fill
    c.setFillColorRGB(1, 1, 1)  # White
    c.rect(rect_x, rect_y, rect_width, rect_height, fill=1)

    # Draw text on top of the rectangle
    text_x = rect_x + 5  # 5 points from the left edge of the rectangle
    text_y = rect_y + 5  # 5 points from the bottom edge of the rectangle

    # Set font and text color
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0, 0, 0)  # Black

    # Draw the question number on top of the rectangle
    c.drawString(text_x, text_y, f"Q{question_number + 1}")
    
    """


    # Update y_position
    y_position -= (new_image_height + 1 * inch)
    return y_position

def draw_answers(c, questions):
    y_position = c._pagesize[1] - 1 * inch  # Resetting y-position
    c.setFont("Helvetica", 12)
    for i, question in enumerate(questions):
        c.drawString(1 * inch, y_position, f"Answer to Question {i + 1}: {question.answer.answer_text}")
        y_position -= 0.5 * inch  # Move down for the next answer

        # Check remaining space for text, if not enough, start a new page
        if y_position < 0:
            c.showPage()
            y_position = c._pagesize[1] - 1 * inch

def generate_pdf(questions: List, file_name: str):
    c = canvas.Canvas(file_name, pagesize=A4)
    
    # Initialize y_position
    y_position = c._pagesize[1] - 1 * inch

    # Draw questions and images
    for i, question in enumerate(questions):
        y_position = draw_question(c, question, y_position, i)

    # Move to a new page for answers
    c.showPage()

    # Draw answers
    draw_answers(c, questions)

    c.save()

def old_generate_pdf(questions: List[Question], file_name: str):
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4  # Width and height of A4 paper in points

    # Font settings
    c.setFont("Helvetica", 12)

    # Print questions at the top
    y_position = height - Y_MARGIN # Starting y-position
    max_width = width

    for i, question in enumerate(questions):
        c.drawString(0.5 * inch, y_position, f"{i + 1}:")

        # Scale and draw the image
        image_path = f"./static/question_images/{question.image_filename}"  # Adjust path as needed
        new_image_width, new_image_height = scale_image(image_path, max_width)

        # Check if image fits the remaining space, if not start a new page
        if y_position - new_image_height < 0:
            c.showPage()
            y_position = height - Y_MARGIN

        c.drawImage(image_path, Y_MARGIN, y_position - new_image_height, width=new_image_width, height=new_image_height, mask='auto')

        y_position -= (new_image_height + Y_MARGIN)  # Move down for the next question

        # Check remaining space for text, if not enough, start a new page
        if y_position < 0:
            c.showPage()
            y_position = height - Y_MARGIN

    # Move to the second page for answers
    c.showPage()

    # Print answers at the bottom
    y_position = height - Y_MARGIN  # Resetting y-position
    for i, question in enumerate(questions):
        answer = question.answer.answer_text if question.answer else "No answer available"
        c.drawString(Y_MARGIN, y_position, f"{i + 1}: {answer}")
        y_position -= 0.5 * inch  # Move down for the next answer

        # Check remaining space for text, if not enough, start a new page
        if y_position < 0:
            c.showPage()
            y_position = height - Y_MARGIN

    c.save()

def scale_image(image_path: str, max_width: float) -> Tuple[int, int]:
    # Load the image
    image = utils.ImageReader(image_path)
    image_width, image_height = image.getSize()

    # Calculate the scaling factor
    scaling_factor = max_width / float(image_width)

    # Calculate the new dimensions
    new_image_width = int(image_width * scaling_factor)
    new_image_height = int(image_height * scaling_factor)

    return new_image_width, new_image_height

# Example usage:
if __name__=="__main__":
    qr = QuestionRetriever()
    
    path = FileManager.get_filepaths("db_path")
    db_manager = DatabaseManager(path)
    
    with db_manager.get_session() as session:
        questions = qr.get_random_questions(session, 10)
    
    generate_pdf(questions, "deleteThis-testGen.pdf")
