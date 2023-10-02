import pytest
from unittest.mock import Mock, patch
from test_generator.question_pdf_creator import draw_rectangle_and_number, scale_image, draw_single_question


def test_draw_rectangle_and_number():
    c = Mock()
    draw_rectangle_and_number(c, 100, 1, 5)

    # Check if methods on the canvas c are called. Adjust as needed.
    c.setFillColorRGB.assert_called()
    c.rect.assert_called()
    c.setFont.assert_called()
    c.setFillColorRGB.assert_called()
    c.drawString.assert_called()


def test_scale_image():
    with patch("reportlab.lib.utils.ImageReader") as MockImageReader:
        MockImageReader.return_value.getSize.return_value = (400, 400)

        new_width, new_height = scale_image("some_path", 800)

        assert new_width == 800
        assert new_height == 800


def test_draw_single_question():
    c = Mock()
    with patch("test_generator.question_pdf_creator.draw_image") as mock_draw_image, \
            patch("test_generator.question_pdf_creator.scale_image") as mock_scale_image, \
            patch(
                "test_generator.question_pdf_creator.draw_rectangle_and_number") as mock_draw_rectangle_and_number:

        mock_scale_image.return_value = (400, 400)

        new_y_position = draw_single_question(c, "some_path", 1, 500, 0)

        mock_draw_image.assert_called()
        mock_draw_rectangle_and_number.assert_called()
        assert new_y_position == 64
