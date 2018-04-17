USE plagiarism_detection;

CREATE TABLE IF NOT EXISTS `raw_text` (
	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
	`text` MEDIUMTEXT NOT NULL,
	`fileName` TEXT NOT NULL,
    `type` ENUM(
		'suspicious', 
		'source') NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;