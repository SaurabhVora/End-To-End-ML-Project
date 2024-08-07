'''
This file is for Training the Model.
training code written here for all the model training.
'''

import os
import sys
from dataclasses import dataclass
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import r2_score
from src.utils import save_object,evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifact","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Spliting Training and Testing input data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            models = {
                 "Linear Regression": LinearRegression(),
                 "K-Neighbors Regressor": KNeighborsRegressor(),
                 "Decision Tree": DecisionTreeRegressor(),
                 "Gradient Boosting": GradientBoostingRegressor(),
                 "Random Forest Regressor": RandomForestRegressor(),
                 "XGBRegressor": XGBRegressor(), 
                 "AdaBoost Regressor": AdaBoostRegressor()
            }
            model_report:dict = evaluate_model(X_train = X_train,y_train = y_train,X_test = X_test,y_test=y_test,
                                               models=models)
            
            ##To get best model score from dict
            best_model_score = max(sorted(model_report.values()))
            ## To get best model name from dictionary
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found!!!!")
            logging.info(f"Best Found Model on both training and testing Dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test,predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e,sys)