DROP DATABASE IF EXISTS `user`;
CREATE DATABASE `user`;
USE `user`;

CREATE TABLE `user` (
     `user_id` int(11) NOT NULL AUTO_INCREMENT,
     `username` varchar(100) DEFAULT NULL,
     `password` varchar(100) DEFAULT NULL,
     `email` varchar(100) DEFAULT NULL,
     `type` varchar(20) DEFAULT NULL,
     `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
     PRIMARY KEY (`user_id`)
);
