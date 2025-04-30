from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation
import sys

if __name__ == '__main__':
    try:
        TrainingPipelineConfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initate Data Ingestion    ")
        data_ingestion_artifact = data_ingestion.initate_data_ingestion()
        logging.info("Data Ingestion completed")
        data_validation_config = DataValidationConfig(TrainingPipelineConfig)
        data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
        logging.info("Initate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation)
    except Exception as e:
        NetworkSecurityException(e, sys)


