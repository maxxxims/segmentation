import plotly.express as px
import numpy as np
from backend import draw_annotations
import plotly.graph_objects as go


def get_zoomed_figure(image: np.ndarray, json_data: dict, newshape: dict, zoom_level: float = 0.95):
    figure = px.imshow(image, binary_string=True, height=800)
    figure.update_layout(dragmode="drawopenpath", newshape=newshape)
    data = json_data['small_image']['relative']
    x0, y0 = data['h0'], data['w0']
    x1, y1 = x0 + data['h'], y0 + data['w']
    
    max_distance = min(x0, y0)
    coeff = (1 - zoom_level)
    x0_new, y0_new = x0 - max_distance * coeff, y0 - max_distance * coeff
    x1_new, y1_new = x1 + max_distance * coeff, y1 + max_distance * coeff
    
    figure.update_layout(
        xaxis={'range': [x0_new, x1_new]},
        yaxis={'range': [y1_new, y0_new]},
        margin={'t': 10, 'b': 50}
    )
    return figure


def zoom_figure(fig: dict, zoom_value: float, json_data: dict) -> dict:
    """
        zoom figure by slider value
    """
    data_relative = json_data['small_image']['relative']
    x0, y0 = data_relative['h0'], data_relative['w0']
    x1, y1 = x0 + data_relative['h'], y0 + data_relative['w']
    
    max_distance = min(x0, y0)
    coeff = (1 - zoom_value)
    x0_new, y0_new = x0 - max_distance * coeff, y0 - max_distance * coeff
    x1_new, y1_new = x1 + max_distance * coeff, y1 + max_distance * coeff
    figure = go.Figure(fig)
    figure.update_layout(
        xaxis={'range': [x0_new, x1_new]},
        yaxis={'range': [y1_new, y0_new]},
    )
    return figure.to_dict()
    

def get_filled_figure(full_image: np.ndarray, json_data: dict, marker_class_1: list, reverse: bool):
    img_add, img = draw_annotations(full_image,marker_class_1, reverse=reverse)
    print(f'INPUT IMAGE SHAPE = {full_image.shape}; IMG ADD SHAPE = {img_add.shape}')
    data = json_data['small_image']['relative']
    h0, w0 = data['h0'], data['w0']
    h, w = h0 + data['h'], w0 + data['w']
    stencil = 255 * np.ones_like(img_add, dtype=np.uint8)
    for i in range(3):
        stencil[:, :, i] = full_image
    stencil[h0:h, w0:w] = img_add[h0:h, w0:w]
    fig = px.imshow(stencil, binary_string=True, height=800)   
    return fig


