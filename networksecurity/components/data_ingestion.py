from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.logging.logger import logging
import os, sys, pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import pandas as pd
from networksecurity.entity.artiffact_entity import DataIngestionArtifact
import csv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.data_ingestion_config.database_name]
            self.collection = self.database[self.data_ingestion_config.collection_name]
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
            data = pd.DataFrame(list(self.collection.find()))
            data.drop(columns=["_id"], inplace=True)
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_data_into_feature_store(self, df: pd.DataFrame) -> str:
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_dir
            os.makedirs(feature_store_dir, exist_ok=True)
            file_path = os.path.join(feature_store_dir, "phisingData.csv")
            os.makedirs(feature_store_dir, exist_ok=True)  # Ensure the feature store directory exists
            df.to_csv(file_path, index=False, header=True)
            return df 
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data(self, df: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train and test split on the Dataframe")
            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(train_dir_path, exist_ok=True)
            test_dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(test_dir_path, exist_ok=True)
            logging.info("Exporting train and test file path")
            # export train and test list into it's own csv file
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initate_data_ingestion(self):
        try:
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_data(df)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
