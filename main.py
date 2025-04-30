from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == '__main__':
    try:
        TrainingPipelineConfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initate Data Ingestion")
        data_ingestion_artifact = data_ingestion.initate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        NetworkSecurityException(e, sys)


