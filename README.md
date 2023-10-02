
# Automated Test Making Tool

The Automated Test Making Tool is a dynamic platform designed to streamline the creation and distribution of customizable tests and quizzes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites

    Python 3.8 or later
    
    Other dependencies and tools as needed (e.g., database, frontend frameworks, etc.)

Clone the repository:

```bash
  git clone https://github.com/Birkbeck/msc-project-source-code-files-22-23-tariqpathan
  cd your-repo
  pip install virtualenv
  python -m venv venv
```


#### Install the required Python dependencies:
```
pip install -r requirements.txt
```
### Add the following directories:
```
uploads/
static/question_images/
These are the default directories that will be used to store images and retrieve pdf files for uploading to the system.
```

## Usage

### How to run the project, e.g.:
```
Once in a terminal and pointint to the root of the application, run:
uvicorn api.app:app --reload
Use an API platform like postman to send requests

And navigate to http://localhost:8000 in your web browser.
```

Built With

    FastAPI - The web framework used
    SQLAlchemy - SQL Toolkit and ORM
    ReportLab - PDF generation library



