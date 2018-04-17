USE plagiarism_detection;

CREATE TABLE IF NOT EXISTS `token` (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `occurence` int UNSIGNED NOT NULL,
  `text` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;