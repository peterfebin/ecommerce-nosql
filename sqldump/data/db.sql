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

DROP DATABASE IF EXISTS `cart`;
CREATE DATABASE `cart`;
USE `cart`;

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cart_id`)
);

CREATE TABLE `cart_items` (
  `cart_items_id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`cart_items_id`)
);

DROP DATABASE IF EXISTS `orders`;
CREATE DATABASE `orders`;
USE `orders`;

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` int(11) DEFAULT NULL,
  `order_status` varchar(50) DEFAULT NULL,
  `orderDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_price` float DEFAULT NULL,
  PRIMARY KEY (`order_id`)
);

DROP DATABASE IF EXISTS `payment`;
CREATE DATABASE `payment`;
USE `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) DEFAULT NULL,
  `paid_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`)
);
