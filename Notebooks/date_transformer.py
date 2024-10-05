# Custom transformer to handle date transformation
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class DateCyclicalTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, date_column):
        self.date_column = date_column

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        X[self.date_column] = pd.to_datetime(X[self.date_column], format='%Y-%m-%d')
        X['Day'] = X[self.date_column].dt.day
        X['Month'] = X[self.date_column].dt.month
        X['Year'] = X[self.date_column].dt.year

        X['Month_sin'] = np.sin(2 * np.pi * X['Month'] / 12)
        X['Month_cos'] = np.cos(2 * np.pi * X['Month'] / 12)
        X['Day_sin'] = np.sin(2 * np.pi * X['Day'] / 31)
        X['Day_cos'] = np.cos(2 * np.pi * X['Day'] / 31)

        X.drop([self.date_column, 'Day', 'Month'], axis=1, inplace=True)

        return X