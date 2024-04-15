from .login import get_users, login_required, register_admin, register_users_from_csv, start_sessions, \
    register_local_user
from .session_operation import finish_task, update_current_task
from .registration import register_user, make_tasks_from_folder, add_tasks_to_users
from .show_figure import get_zoomed_figure, get_filled_figure, zoom_figure
from .process_annotations import add_marker_class_for_shapes, update_shape_hash, \
    calculate_pixels_proportions, validate_pixels_propotions