from ..database import figure_table

def get_string_hash(obj: str) -> str:
    return str(obj.__hash__())

SELECTED_CLASS_KEY = 'selected_class'



def add_marker_class_for_shapes(username: str, shapes: list, selected_class: int) -> None:
    cnt = 0
    user_hashes = figure_table.get_shapes_hashes(username)
    # print(f'USER HASHES = {user_hashes}')
    if user_hashes is None:
        user_hashes = {}
    for shape in shapes:
        shape_hash = get_string_hash(shape['path'])
        shape['hash'] = shape_hash
        if shape_hash in user_hashes.keys():
            shape[SELECTED_CLASS_KEY] = user_hashes[shape_hash]
        else:
            user_hashes[shape_hash] = selected_class
            shape[SELECTED_CLASS_KEY] = selected_class
            cnt += 1
            
    figure_table.set_shapes_hashes(username, user_hashes)
    
    if cnt != 1:
        print()
        print()
        print(f'*********************************** EROROR; cnt = {cnt}')


def update_shape_hash(username: str, idx_old: int, new_geometry: str) -> None:
    markers_class_1 = figure_table.get_marker_class_1(username)
    user_hashes = figure_table.get_shapes_hashes(username)
    new_hash = get_string_hash(new_geometry)
    old_hash = markers_class_1[idx_old]['hash']
    markers_class_1[idx_old]['path'] = new_geometry
    markers_class_1[idx_old]['hash'] = new_hash
    user_hashes[new_hash] = markers_class_1[idx_old][SELECTED_CLASS_KEY]
    user_hashes.pop(old_hash)
    figure_table.save_marker_class_1(username, markers_class_1)
    figure_table.set_shapes_hashes(username, user_hashes)
    # figure_table.save_last_figure(username, figure)
    


def calculate_pixels_proportions(username: str, annotated_class_1: int, annotated_class_0: int, to_str: bool = True) -> tuple:
    class_1, class_0 = figure_table.get_pixels_numbers(username)
    
    
    if class_1 == 0 or class_0 == 0:
        return '', ''
    p_1 = round(100 * annotated_class_1 / class_1)
    p_0 = round(100 * annotated_class_0 / class_0)
    if to_str:
        p_1 = str(p_1) + '%'
        p_0 = str(p_0) + '%'
    return p_1, p_0


# def validate_pixels_propotions(username: str, annotated_class_1: int, annotated_class_0: int) -> bool:
#     class_1, class_0 = figure_table.get_pixels_numbers(username)
#     if class_1 == 0 or class_0 == 0:
#         return False
#     p_1 = annotated_class_1 / class_1
#     p_0 = annotated_class_0 / class_0
    
#     if p_1 < 0.3 or p_0 < 0.3:
#         return False
#     return True

def validate_pixels_propotions(p_1: int, p_0: int) -> bool:
    if isinstance(p_1, str) or isinstance(p_0, str):
        return False
    print(f'P_1 = {p_1}; P_0 = {p_0}')
    if p_1 < 30 or p_0 < 30:
        print(f'NOT VALIDATED')
        return False
    print(f'VALIDATED')
    return True