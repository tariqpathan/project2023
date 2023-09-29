from sqlalchemy.orm import Session

from extraction_engine.managers.file_manager import FileManager
from database.database_manager import DatabaseManager
from database.models import Subtopic

# TODO: change db_manager to handle Path objects
db_path = FileManager.get_filepaths("db_path").as_posix()
db_manager = DatabaseManager(db_path)


def get_subtopics(session):
    subtopics = session.query(Subtopic).all()
    return subtopics


def main():
    with db_manager.get_session() as session:
        subtopics = get_subtopics(session)

    subtopic_shortcuts = {}
    for index, subtopic in enumerate(subtopics):
        shortcut = str(index + 1)  # Starting from "1"
        subtopic_shortcuts[shortcut] = subtopic.name

    print("Available Subtopics:")
    for shortcut, name in subtopic_shortcuts.items():
        print(f"{shortcut}. {name}")

    selected_shortcut = input("Enter the shortcut of the subtopic you want to select: ")
    selected_subtopic = subtopic_shortcuts.get(selected_shortcut)

    if selected_subtopic:
        print(f"You have selected: {selected_subtopic}")
    else:
        print("Invalid shortcut.")


if __name__ == "__main__":
    main()
