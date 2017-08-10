DROP DATABASE IF EXISTS `cart`;
CREATE DATABASE `cart`;
USE `cart`;

CREATE TABLE `cart` (
     `cart_id` int(11) NOT NULL AUTO_INCREMENT,
     `user_id` int(11) DEFAULT NULL,
     `total_price` int(11) DEFAULT NULL,
     `state` varchar(50) DEFAULT NULL,
     PRIMARY KEY (`cart_id`)
);

CREATE TABLE `cart_items` (
     `cart_items_id` int(11) NOT NULL AUTO_INCREMENT,
     `cart_id` int(11) DEFAULT NULL,
     `product_id` int(11) DEFAULT NULL,
     `quantity` int(11) DEFAULT NULL,
     PRIMARY KEY (`cart_items_id`)
);
