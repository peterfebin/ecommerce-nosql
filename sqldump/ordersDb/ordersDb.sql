DROP DATABASE IF EXISTS `orders`;
CREATE DATABASE `orders`;
USE `orders`;

CREATE TABLE `orders` (
     `order_id` int(11) NOT NULL AUTO_INCREMENT,
     `cart_id` int(11) DEFAULT NULL,
     `order_status` varchar(50) DEFAULT NULL,
     `orderDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
     PRIMARY KEY (`order_id`)
);
