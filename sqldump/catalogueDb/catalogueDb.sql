DROP DATABASE IF EXISTS `catalogue`;
CREATE DATABASE `catalogue`;
USE `catalogue`;

CREATE TABLE `product` (
     `product_id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(100) DEFAULT NULL,
     `category` varchar(100) DEFAULT NULL,
     `price` float DEFAULT NULL,
     `location` varchar(100) DEFAULT NULL,
     PRIMARY KEY (`product_id`)
);


INSERT INTO `product`(`name`, `category`, `price`, `location`) VALUES('nike', 'shoe', 11, '/static/shoe.jpg');

INSERT INTO `product`(`name`, `category`, `price`, `location`) VALUES('iphone', 'mobile', 100, '/static/mobile.jpg');
