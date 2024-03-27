from flask import Blueprint
from ..utils import login_required, update_current_task
from uuid import UUID

change_annotation = Blueprint('change_annotation', __name__)


@change_annotation.get('/<task_uuid>')
@login_required
def redirect_to_change_annotation(task_uuid: str, username: str):
    task_uuid = UUID(task_uuid)