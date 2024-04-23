import pandas as pd
from pathlib import Path
import os
import numpy as np
from backend import Evaluator, Accuracy, F1_binary, EPorosity, MarkerContainer,\
    IoU_pores, BaseMetric, Image, MarkerByPoints2D, MarkerBorder2D, Segmentation, \
    EvaluatorBorder
import backend.filters.filters_2dim as filters_2d
import json
from sklearn.ensemble import RandomForestClassifier


PATH_TO_BORDERS = Path('C:/Users/maxxx/VSprojects/back/0/0/border')
RELATIVE_PATH_TO_GT = r'02. Segmented\00. Original'
IMGTAG2BORDER = {
    'img0_300': PATH_TO_BORDERS / '0.png',
    'img1_300': PATH_TO_BORDERS / '0.png',
    'img2_300': PATH_TO_BORDERS / '0.png',
    'img3_300': PATH_TO_BORDERS / '0.png',
}


class EvaluateMetrics:
    def __init__(self, metrics: list[BaseMetric], border_metrics: list[BaseMetric], n_diameter: int):
        self.n_diameter = n_diameter
        self.border_metrics = {f'{m.name}_{n_diameter}': m for m in border_metrics}
        self.metrics = {m.name: m for m in metrics}
        self.names_dict = self.metrics.keys() + self.border_metrics.keys()
        
        
class MeasurementsData:
    def __init__(self, path_to_folder: Path, path_to_csv: Path,
                       path_to_image_folder: Path, metrics: EvaluateMetrics):
        for path in [path_to_folder, path_to_csv, path_to_image_folder]:
            if isinstance(path, str):
                path = Path(path)
            
        if path_to_csv.exists():
            self.df = pd.read_csv(path_to_csv)
        else:
            self.df = self.__make_df(metrics)

        self.n_diameter = metrics.n_diameter
        self.metrics = metrics
        self.path_to_folder = path_to_folder
        self.path_to_csv = path_to_csv
        self.path_to_image_folder = path_to_image_folder
        self.__parse_operator_folders()
        self.__validate_input_data()
        
        
    def __make_df(self, metrics: EvaluateMetrics) -> pd.DataFrame:
        df = pd.DataFrame(columns=['Operator', 'Parts'] + [name for name in metrics.names_dict])
        return df
    def __parse_operator_folders(self):
        self.operator2part = {}
        self.parts = []
        for operator_folder in self.path_to_folder.iterdir():
            if operator_folder.is_dir():
                self.operator2part[operator_folder.name] = [f_name.name for f_name in operator_folder.iterdir() if f_name.is_dir()]
                self.parts.append(el for el in self.operator2part[operator_folder.name])
        self.operators = list(self.operator2part.keys())
        self.parts = list(set(self.parts))
    def __validate_input_data(self):
        for operator in self.operators:
            assert np.equal(self.parts == self.operator2part[operator])
    
    def save_df(self):
        self.df.to_csv(self.path_to_csv, index=False)
        
    def update_df(self, operator: str, part: str, metrics: dict[str, float]):
        data = metrics.copy()
        data['Operator'] = operator
        data['Parts'] = part
        self.df = pd.concat([self.df, pd.DataFrame(data)], ignore_index=True)
        self.save_df()
    
    def process_one_part(self, operator: str, part: str, show: bool = False):
        folder = self.path_to_folder / operator / part
        with open(folder / 'result.json', 'r') as f:
            result = json.load(f)
        img_folder = Path(result['folder_path'])
        img_name = result['image_name']
        abs_img_folder = self.path_to_image_folder / img_folder
        original_img_path = abs_img_folder / result['relative_image_path'] / img_name
        gt_img_path = abs_img_folder / RELATIVE_PATH_TO_GT / img_name
        border_img_path = IMGTAG2BORDER[result['image_tag']]
        
        orig_img = Image(path_to_image=original_img_path)
        gt_image = Image(path_to_image=gt_img_path)
        
        border_marker = MarkerBorder2D(Image(path_to_image=border_img_path))
        marker_class1 = MarkerByPoints2D(x_indexes=np.array(result['x_1_class'])+ result['width0'], 
                                        y_indexes=np.array(result['y_1_class'])+ result['height0'], value=1)
        marker_class0 = MarkerByPoints2D(x_indexes=np.array(result['x_0_class'])+ result['width0'], 
                                        y_indexes=np.array(result['y_0_class'])+ result['height0'], value=0)

        markers = MarkerContainer([marker_class1, marker_class0])
        
        if show:
            for m in markers:
                orig_img.draw_marker(m, color=255 * m.value)
            orig_img.draw_marker(border_marker, color=0)
            orig_img.show()
            return
        
        
        filters = [
                filters_2d.MedianFilter(size=5),   filters_2d.GaussianFilter(15),
                filters_2d.VarianceFilter(size=6), filters_2d.HighPassFilter(k=9), filters_2d.BaseFilter2D(), 
                filters_2d.Erosion(size=3), filters_2d.Dilation(size=3),
                filters_2d.Closing(size=3), filters_2d.Opening(size=3)
              ]
    
        for ii in [2, 4]:
            scalled_filters =[
                        filters_2d.MedianFilter(size=5, scale=ii),   filters_2d.GaussianFilter(15, scale=ii),
                        filters_2d.BaseFilter2D(scale=ii), 
                        filters_2d.Erosion(size=3, scale=ii), filters_2d.Dilation(size=3, scale=ii),
                        filters_2d.Closing(size=3, scale=ii), filters_2d.Opening(size=3, scale=ii)
                    ]
            filters += scalled_filters
        sgm = Segmentation(model=RandomForestClassifier(n_jobs=-1, random_state=42), filters=filters)
        segmented = sgm.fit_and_predict(orig_img, markers)
        
        metrics, metrics_names = self.metrics.metrics.values(), self.metrics.metrics.keys()
        border_metrics, border_metrics_names = self.metrics.border_metrics.values(), self.metrics.border_metrics.keys()
    
        res = Evaluator.evaluate(segmented, gt_image, markers, border_marker, *metrics)
        res2 = EvaluatorBorder.evaluate(self.n_diameter, segmented, gt_image, markers, border_marker, *border_metrics)
        for key, value in res2.items():
            res[f'{key}_{self.n_diameter}'] = value
            
        self.update_df(operator, part, res)