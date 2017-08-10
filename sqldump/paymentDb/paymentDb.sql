DROP DATABASE IF EXISTS `payment`;
CREATE DATABASE `payment`;
USE `payment`;

CREATE TABLE `payment` (
     `payment_id` int(11) NOT NULL AUTO_INCREMENT,
     `order_id` int(11) DEFAULT NULL,
     `paid_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
     PRIMARY KEY (`payment_id`)
);
