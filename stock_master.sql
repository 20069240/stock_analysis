mysql -u root -p
CREATE DATABASE stock_master;
USE stock_master;
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON stock_master.* TO 'username'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE `stock_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` int NOT NULL,
  `date` datetime NOT NULL,
  `open` decimal(19,4) NULL,
  `high` decimal(19,4) NULL,
  `low` decimal(19,4) NULL,
  `close` decimal(19,4) NULL,
  `adj_close` decimal(19,4) NULL,
  `volume` bigint NULL,
  PRIMARY KEY (`id`),
  KEY `index_symbol` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `symbol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exchange` int NULL,
  `ticker` varchar(32) NOT NULL,
  `instrument` varchar(64) NOT NULL,
  `name` varchar(255) NULL,
  `sector` varchar(255) NULL,
  `currency` varchar(32) NULL,
  `created_date` datetime NOT NULL,
  `updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_exchange` (`exchange`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
