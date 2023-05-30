import sys,os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder,LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from src.utils import save_object
from src.logging import logging
from src.exception import CustomException
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    logging.info('preparing a preprocessor pikel file')
    preprocessor_obj_path=os.path.join('artifacts','preprocessor.pkl')

class data_transformation:
    def __init__(self):
        self.data_transformation_obj=DataTransformationConfig()
    
    def get_transformation_obj(self):
        try:
            logging.info('ínitializing and creatng pipeline and preprocessor')
            num_col=['tempo', 'beats', 'chroma_stft', 'rmse', 'spectral_centroid', 
                     'spectral_bandwidth', 'rolloff', 'zero_crossing_rate', 'mfcc1', 
                     'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8', 
                     'mfcc9', 'mfcc10', 'mfcc11', 'mfcc12', 'mfcc13', 'mfcc14', 
                     'mfcc15', 'mfcc16', 'mfcc17', 'mfcc18', 'mfcc19', 'mfcc20']
            cat_col=['label']      

            num_pipeline=Pipeline(steps=[('scaling',MinMaxScaler()),
                            ('PCA',PCA(n_components=10, random_state=32))])
            cat_pipeline=Pipeline(steps=[('encoder',OneHotEncoder())])

            preprocessor=ColumnTransformer([('numerical_pipeline',num_pipeline,num_col),
                                ('categorical_pipeline',cat_pipeline,cat_col)])
            
            clusterer=Pipeline(steps=[("kmeans",KMeans(n_clusters=10,init="k-means++", n_init=50,max_iter=500,
                                           random_state=32))])
            
            pipe=Pipeline(steps=[("preprocessor",preprocessor),
                                 ("clusterer",clusterer)])
            return pipe
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_trasformation(self,raw_path):
        try:
            logging.info('initializing data transformation')
            df_raw=pd.read_csv(raw_path)
            le=LabelEncoder()
            le_class=le.fit_transform(df_raw['label'])
            n_clusters = len(le.classes_)
            print(f'No of clusters used:{n_clusters}')
        
            logging.info('initializing preprocessor object')
            pipe_obj=self.get_transformation_obj()

            input_feature_df=df_raw.drop(columns=['filename'])
            
            logging.info('Appliying preprocessor object on train and test file')

            input_feature_train_arr=pipe_obj.fit(input_feature_df)
            preprocessed_data=pipe_obj['preprocessor'].transform(input_feature_df)

            predicted_labels=pipe_obj['clusterer']['kmeans'].labels_

            score=silhouette_score(preprocessed_data, predicted_labels)
            ari=adjusted_rand_score(le_class,predicted_labels)
            print(f'Sildouette score for un-supervised learning using K-means={score}')

            save_object(
                file_path=self.data_transformation_obj.preprocessor_obj_path,
                obj=pipe_obj
            )
            logging.info('Applied preprocessor obj formed and saved')
            return (score, ari)

        except Exception as e:
            raise CustomException(e,sys)



