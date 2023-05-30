import sys,os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.logging import logging
from src.exception import CustomException
from src.components.data_transformation import data_transformation
#from src.components.model_trainer import model_trainer
from dataclasses import dataclass

@dataclass
class data_ingestion_config:
    raw_path:str=os.path.join('artifacts','raw.csv')
class data_ingestion:
    def __init__(self):
        self.ingestion_config=data_ingestion_config()

    def initiate_data_ingestion(self):
        try:
            logging.info('data initiation started')
            data=pd.read_csv('C:\\Users\\Lenovo\\Downloads\\ML project\\music_genre\\notebook\\data_gnre.csv')
            
            logging.info('data ingested done')

            logging.info('making directories for storing raw data')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_path),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_path,index=False)

            return(self.ingestion_config.raw_path)
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=data_ingestion()
    raw_data=obj.initiate_data_ingestion()

    transformation_obj=data_transformation()
    print(transformation_obj.initiate_data_trasformation(raw_data))



    

