-- MySQL Script generated by MySQL Workbench
-- Wed May 16 13:56:00 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema plagiarism_detection
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema plagiarism_detection
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `plagiarism_detection` DEFAULT CHARACTER SET utf8 ;
USE `plagiarism_detection` ;

-- -----------------------------------------------------
-- Table `plagiarism_detection`.`text_collection_meta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`text_collection_meta` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creationDate` DATETIME NOT NULL,
  `name` TEXT NOT NULL,
  `sourceUrl` TEXT NULL,
  `description` TEXT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`raw_text`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`raw_text` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `textCollectionMetaId` INT UNSIGNED NOT NULL,
  `text` MEDIUMTEXT NOT NULL,
  `fileName` TEXT NOT NULL,
  `type` ENUM('suspicious', 'source') NULL,
  PRIMARY KEY (`id`),
  INDEX `rawText_into_textCollectionMeta_idx` (`textCollectionMetaId` ASC),
  CONSTRAINT `rawText_into_textCollectionMeta`
    FOREIGN KEY (`textCollectionMetaId`)
    REFERENCES `plagiarism_detection`.`text_collection_meta` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`raw_text_pair`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`raw_text_pair` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `suspiciousRawTextId` INT UNSIGNED NOT NULL,
  `sourceRawTextId` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `rawTextPair_into_rawText_idx` (`suspiciousRawTextId` ASC),
  INDEX `rawTextPair_into_rawTextSource_idx` (`sourceRawTextId` ASC),
  CONSTRAINT `rawTextPair_into_rawTextSuspicious`
    FOREIGN KEY (`suspiciousRawTextId`)
    REFERENCES `plagiarism_detection`.`raw_text` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `rawTextPair_into_rawTextSource`
    FOREIGN KEY (`sourceRawTextId`)
    REFERENCES `plagiarism_detection`.`raw_text` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`classifier_algorithm`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`classifier_algorithm` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `algorithmName` TEXT NOT NULL,
  `algorithmDescription` TEXT NOT NULL,
  `algorithmTag` TINYTEXT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`classifier`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`classifier` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `classifierAlgorithmId` INT UNSIGNED NOT NULL,
  `classifierTarget` ENUM('seeding', 'extension', 'filter', 'all') NOT NULL,
  `pickleRaw` MEDIUMBLOB NOT NULL,
  `details` TEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `classifier_into_classifierAlgorithm_idx` (`classifierAlgorithmId` ASC),
  CONSTRAINT `classifier_into_classifierAlgorithm`
    FOREIGN KEY (`classifierAlgorithmId`)
    REFERENCES `plagiarism_detection`.`classifier_algorithm` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`pre_process_step`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`pre_process_step` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `algorithm` JSON NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`pre_process_step_chain_node`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`pre_process_step_chain_node` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `preProcessedDataId` INT UNSIGNED NOT NULL,
  `preProcessStepId` INT UNSIGNED NOT NULL,
  `stepPosition` INT UNSIGNED NOT NULL,
  `previousPreProcessStepChainNodeId` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `preProcessStepChainNode_into_preProcessedData_idx` (`preProcessedDataId` ASC),
  INDEX `preProcessStepChainNode_into_preProcessStep_idx` (`preProcessStepId` ASC),
  INDEX `preProcessStepChainNode_into_preProcessStepChainNode_idx` (`previousPreProcessStepChainNodeId` ASC),
  CONSTRAINT `preProcessStepChainNode_into_preProcessedData`
    FOREIGN KEY (`preProcessedDataId`)
    REFERENCES `plagiarism_detection`.`pre_processed_data` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `preProcessStepChainNode_into_preProcessStep`
    FOREIGN KEY (`preProcessStepId`)
    REFERENCES `plagiarism_detection`.`pre_process_step` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `preProcessStepChainNode_into_preProcessStepChainNode`
    FOREIGN KEY (`previousPreProcessStepChainNodeId`)
    REFERENCES `plagiarism_detection`.`pre_process_step_chain_node` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`pre_processed_data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`pre_processed_data` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `topPreProcessStepChainNodeId` INT UNSIGNED NULL,
  `textCollectionMetaId` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `preProcessedData_into_preProcessStepChainNode_idx` (`topPreProcessStepChainNodeId` ASC),
  INDEX `preProcessedData_into_textCollectionMetaId_idx` (`textCollectionMetaId` ASC),
  CONSTRAINT `preProcessedData_into_preProcessStepChainNode`
    FOREIGN KEY (`topPreProcessStepChainNodeId`)
    REFERENCES `plagiarism_detection`.`pre_process_step_chain_node` (`id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL,
  CONSTRAINT `preProcessedData_into_textCollectionMetaId`
    FOREIGN KEY (`textCollectionMetaId`)
    REFERENCES `plagiarism_detection`.`text_collection_meta` (`id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`seeding_data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`seeding_data` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `preProcessedDataId` INT UNSIGNED NOT NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `seedingData_into_preProcessedData_idx` (`preProcessedDataId` ASC),
  CONSTRAINT `seedingData_into_preProcessedData`
    FOREIGN KEY (`preProcessedDataId`)
    REFERENCES `plagiarism_detection`.`pre_processed_data` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`seeding_experiment_setup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`seeding_experiment_setup` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creationDate` DATETIME NOT NULL,
  `isCommited` ENUM('Yes') NULL,
  `description` TEXT NOT NULL,
  `seedingDataId` INT UNSIGNED NULL,
  `classifierAlgorithmId` INT UNSIGNED NULL,
  `seedClassifierId` INT UNSIGNED NULL,
  `seedDataBaseTestFraction` DECIMAL NULL,
  PRIMARY KEY (`id`),
  INDEX `seedExperimentSetup_into_classifier_idx` (`seedClassifierId` ASC),
  INDEX `seedExperimentSetup_into_classifierAlgorithm_idx` (`classifierAlgorithmId` ASC),
  INDEX `seedExperimentSetup_into_seedingData_idx` (`seedingDataId` ASC),
  CONSTRAINT `seedExperimentSetup_into_classifier`
    FOREIGN KEY (`seedClassifierId`)
    REFERENCES `plagiarism_detection`.`classifier` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `seedExperimentSetup_into_classifierAlgorithm`
    FOREIGN KEY (`classifierAlgorithmId`)
    REFERENCES `plagiarism_detection`.`classifier_algorithm` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `seedExperimentSetup_into_seedingData`
    FOREIGN KEY (`seedingDataId`)
    REFERENCES `plagiarism_detection`.`seeding_data` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`pre_process_setup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`pre_process_setup` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `creationDate` DATETIME NULL,
  `preProcessedDataId` INT UNSIGNED NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `preProcessSetup_into_preProcessedData_idx` (`preProcessedDataId` ASC),
  CONSTRAINT `preProcessSetup_into_preProcessedData`
    FOREIGN KEY (`preProcessedDataId`)
    REFERENCES `plagiarism_detection`.`pre_processed_data` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`experiment_setup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`experiment_setup` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `isCommited` ENUM('Yes') NULL,
  `textCollectionId` INT UNSIGNED NOT NULL,
  `preProcessSetupId` INT UNSIGNED NOT NULL,
  `seedExperimentId` INT UNSIGNED NOT NULL,
  `creationDate` DATETIME NULL,
  `description` TEXT NULL,
  `dataBaseTestFractionDefault` DECIMAL NULL,
  PRIMARY KEY (`id`),
  INDEX `experimentSetup_into_seedExperimentSetup_idx` (`seedExperimentId` ASC),
  INDEX `experimentSetup_into_textCollectionMeta_idx` (`textCollectionId` ASC),
  INDEX `experimentSetup_into_preProcessSetup_idx` (`preProcessSetupId` ASC),
  CONSTRAINT `experimentSetup_into_seedExperimentSetup`
    FOREIGN KEY (`seedExperimentId`)
    REFERENCES `plagiarism_detection`.`seeding_experiment_setup` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `experimentSetup_into_textCollectionMeta`
    FOREIGN KEY (`textCollectionId`)
    REFERENCES `plagiarism_detection`.`text_collection_meta` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `experimentSetup_into_preProcessSetup`
    FOREIGN KEY (`preProcessSetupId`)
    REFERENCES `plagiarism_detection`.`pre_process_setup` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`raw_text_excerpt_location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`raw_text_excerpt_location` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `rawTextId` INT UNSIGNED NOT NULL,
  `firstCharacterPosition` INT UNSIGNED NOT NULL,
  `lastCharacterPosition` INT UNSIGNED NULL,
  `stringLength` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `rawTextLocation_into_rawText_idx` (`rawTextId` ASC),
  CONSTRAINT `rawTextLocation_into_rawText`
    FOREIGN KEY (`rawTextId`)
    REFERENCES `plagiarism_detection`.`raw_text` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`sentence_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`sentence_list` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `rawTextId` INT UNSIGNED NULL,
  `preProcessStepChainNodeId` INT UNSIGNED NOT NULL,
  `rawTextExcerptLocationId` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `sentenceList_into_preProcessStepChainNode_idx` (`preProcessStepChainNodeId` ASC),
  INDEX `sentenceList_into_rawText_idx` (`rawTextId` ASC),
  CONSTRAINT `sentenceList_into_rawText`
    FOREIGN KEY (`rawTextId`)
    REFERENCES `plagiarism_detection`.`raw_text` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `sentenceList_into_preProcessStepChainNode`
    FOREIGN KEY (`preProcessStepChainNodeId`)
    REFERENCES `plagiarism_detection`.`pre_process_step_chain_node` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`sentence`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`sentence` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `sentenceListId` INT UNSIGNED NULL,
  `text` TEXT NOT NULL,
  `rawTextExcerptLocationId` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `sentence_into_sentenceList_idx` (`sentenceListId` ASC),
  INDEX `sentence_into_rawTextExcerptLocation_idx` (`rawTextExcerptLocationId` ASC),
  CONSTRAINT `sentence_into_sentenceList`
    FOREIGN KEY (`sentenceListId`)
    REFERENCES `plagiarism_detection`.`sentence_list` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `sentence_into_rawTextExcerptLocation`
    FOREIGN KEY (`rawTextExcerptLocationId`)
    REFERENCES `plagiarism_detection`.`raw_text_excerpt_location` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`bag_of_words`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`bag_of_words` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `sentenceId` INT UNSIGNED NOT NULL,
  `wordOccurenceDictionary` JSON NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `bagOfWords_into_sentence_idx` (`sentenceId` ASC),
  CONSTRAINT `bagOfWords_into_sentence`
    FOREIGN KEY (`sentenceId`)
    REFERENCES `plagiarism_detection`.`sentence` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`detection`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`detection` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `textCollectionMetaId` INT UNSIGNED NOT NULL,
  `rawTextSuspiciousLocationId` INT UNSIGNED NOT NULL,
  `rawTextSourceLocationId` INT UNSIGNED NOT NULL,
  `rawTextPairId` INT UNSIGNED NULL,
  `name` TEXT NULL,
  `obfuscation` ENUM('none', 'random') NULL,
  `type` ENUM('artificial') NULL,
  `obfuscationDegree` DOUBLE NULL,
  `isGiven` ENUM('Yes', 'No') NOT NULL,
  `isDetected` ENUM('Yes', 'No') NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `detection_into_rawTextSuspiciousLocation_idx` (`rawTextSuspiciousLocationId` ASC),
  INDEX `detection_into_rawTextSourceLocation_idx` (`rawTextSourceLocationId` ASC),
  INDEX `detection_into_textCollectionMeta_idx` (`textCollectionMetaId` ASC),
  INDEX `detection_into_rawTextPair_idx` (`rawTextPairId` ASC),
  CONSTRAINT `detection_into_rawTextSuspiciousLocation`
    FOREIGN KEY (`rawTextSuspiciousLocationId`)
    REFERENCES `plagiarism_detection`.`raw_text_excerpt_location` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `detection_into_rawTextSourceLocation`
    FOREIGN KEY (`rawTextSourceLocationId`)
    REFERENCES `plagiarism_detection`.`raw_text_excerpt_location` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `detection_into_textCollectionMeta`
    FOREIGN KEY (`textCollectionMetaId`)
    REFERENCES `plagiarism_detection`.`text_collection_meta` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `detection_into_rawTextPair`
    FOREIGN KEY (`rawTextPairId`)
    REFERENCES `plagiarism_detection`.`raw_text_pair` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`seed`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`seed` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `seedingDataId` INT UNSIGNED NOT NULL,
  `suspiciousSentenceId` INT UNSIGNED NOT NULL,
  `sourceSentenceId` INT UNSIGNED NOT NULL,
  `rawTextPairId` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `seed_into_seedingData_idx` (`seedingDataId` ASC),
  INDEX `seed_into_sentenceSource_idx` (`sourceSentenceId` ASC),
  INDEX `seed_into_sentenceSuspicious_idx` (`suspiciousSentenceId` ASC),
  INDEX `seed_into_rawTextPair_idx` (`rawTextPairId` ASC),
  CONSTRAINT `seed_into_seedingData`
    FOREIGN KEY (`seedingDataId`)
    REFERENCES `plagiarism_detection`.`seeding_data` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `seed_into_sentenceSuspicious`
    FOREIGN KEY (`suspiciousSentenceId`)
    REFERENCES `plagiarism_detection`.`sentence` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `seed_into_sentenceSource`
    FOREIGN KEY (`sourceSentenceId`)
    REFERENCES `plagiarism_detection`.`sentence` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `seed_into_rawTextPair`
    FOREIGN KEY (`rawTextPairId`)
    REFERENCES `plagiarism_detection`.`raw_text_pair` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`seed_attributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`seed_attributes` (
  `seedId` INT UNSIGNED NOT NULL,
  `plagiarismType` ENUM('none', 'direct', 'obfuscatedRandom', 'obfuscatedTranslation', 'obfuscatedSummary') NULL,
  `isInsideDetection` ENUM('Yes', 'No') NULL,
  `cosine` DOUBLE NULL,
  `maxCosine` DOUBLE NULL,
  `dice` DOUBLE NULL,
  `maxDice` DOUBLE NULL,
  PRIMARY KEY (`seedId`),
  CONSTRAINT `seedAttributes_into_seed`
    FOREIGN KEY (`seedId`)
    REFERENCES `plagiarism_detection`.`seed` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`evaluation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`evaluation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `classifierId` INT UNSIGNED NOT NULL,
  `experimentSetupId` INT UNSIGNED NOT NULL,
  `creationDate` DATETIME NOT NULL,
  `evaluationTarget` ENUM('seeding', 'extension', 'filter', 'all') NOT NULL,
  `precisionScore` DOUBLE NULL,
  `recallScore` DOUBLE NULL,
  `fScore` DOUBLE NULL,
  `granularityScore` DOUBLE NULL,
  `plagDetScore` DOUBLE NULL,
  PRIMARY KEY (`id`),
  INDEX `evaluation_into_classifier_idx` (`classifierId` ASC),
  INDEX `evaluation_into_experimentSetup_idx` (`experimentSetupId` ASC),
  CONSTRAINT `evaluation_into_classifier`
    FOREIGN KEY (`classifierId`)
    REFERENCES `plagiarism_detection`.`classifier` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `evaluation_into_experimentSetup`
    FOREIGN KEY (`experimentSetupId`)
    REFERENCES `plagiarism_detection`.`experiment_setup` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`classifier_train_data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`classifier_train_data` (
  `classifierId` INT UNSIGNED NOT NULL,
  `seedId` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`classifierId`, `seedId`),
  INDEX `classifierTrainData_into_seed_idx` (`seedId` ASC),
  CONSTRAINT `classifierTrainData_into_seed`
    FOREIGN KEY (`seedId`)
    REFERENCES `plagiarism_detection`.`seed` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `classifierTrainData_into_classifier`
    FOREIGN KEY (`classifierId`)
    REFERENCES `plagiarism_detection`.`classifier` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`cross_validation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`cross_validation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `experimentSetupId` INT UNSIGNED NOT NULL,
  `folds` INT UNSIGNED NOT NULL,
  `creationDate` DATETIME NOT NULL,
  `evaluationTarget` ENUM('seeding', 'extension', 'filter', 'all') NOT NULL,
  `precisionScore` DOUBLE NULL,
  `recallScore` DOUBLE NULL,
  `fScore` DOUBLE NULL,
  `granularityScore` DOUBLE NULL,
  `plagDetScore` DOUBLE NULL,
  PRIMARY KEY (`id`),
  INDEX `crossValidation_into_experimentSetup_idx` (`experimentSetupId` ASC),
  CONSTRAINT `crossValidation_into_experimentSetup`
    FOREIGN KEY (`experimentSetupId`)
    REFERENCES `plagiarism_detection`.`experiment_setup` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`classifier_and_evaluation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`classifier_and_evaluation` (
  `crossValidationId` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `classifierId` INT UNSIGNED NOT NULL,
  `evaluationId` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`crossValidationId`),
  INDEX `classifierAndEvaluation_into_evaluation_idx` (`evaluationId` ASC),
  CONSTRAINT `classifierAndEvaluation_into_classifier`
    FOREIGN KEY (`classifierId`)
    REFERENCES `plagiarism_detection`.`classifier` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `classifierAndEvaluation_into_evaluation`
    FOREIGN KEY (`evaluationId`)
    REFERENCES `plagiarism_detection`.`evaluation` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `classifierAndEvaluation_into_crossValidation`
    FOREIGN KEY (`crossValidationId`)
    REFERENCES `plagiarism_detection`.`cross_validation` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plagiarism_detection`.`n_grams_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plagiarism_detection`.`n_grams_list` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `sentenceId` INT UNSIGNED NOT NULL,
  `nGramsOccurenceDictionary` JSON NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `nGramsList_into_sentence_idx` (`sentenceId` ASC),
  CONSTRAINT `nGramsList_into_sentence`
    FOREIGN KEY (`sentenceId`)
    REFERENCES `plagiarism_detection`.`sentence` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
