from src.api import db
from src.models import Project

def create_project(project: dict) -> int:

    project = Project(
        code=project['code'],
        name=project['name'],
        description=project.get('description'),
        start_date=project.get('start_date'),
        end_date=project.get('end_date'),
        is_archived=project.get('is_archived', False)
    )

    db.session.add(project)
    db.session.commit()

    return project.id_project
