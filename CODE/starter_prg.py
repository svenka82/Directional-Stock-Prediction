from pip._internal import main as pipmain

from CODE.stock_direction_prediction import one_day_window_model
from CODE.stock_prediction_4hr_window import four_hour_window_model

for package in ['glob', 'sklearn', 'vaderSentiment', 'pandas', 'numpy']:
    pipmain(["install", package])

one_day_window_model()
four_hour_window_model()
