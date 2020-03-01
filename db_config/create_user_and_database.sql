-- 创建数据库

create database `movie_heaven_bar` default character set utf8mb4 collate utf8mb4_unicode_ci;
 
use movie_heaven_bar;
 
-- 建表

DROP TABLE IF EXISTS `newest_movie`;
CREATE TABLE `newest_movie`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `movie_link` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_director` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_actors` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_publish_date` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_score` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_download_link` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `movie_hash` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

-- 创建用户并授权

use mysql;
select host, user from user;

-- ----------------mysql:5.7
-- create user movie identified by 'yourpasswd';
-- 将movie_heaven_bar数据库的权限授权给创建的movie用户，密码为yourpasswd：
-- grant all on movie_heaven_bar.* to movie@'%' identified by 'yourpasswd' with grant option;
-- ----------------mysql:5.7

-- ----------------mysql:8
create user 'movie'@'%' identified by 'yourpasswd'; 
grant all privileges on movie_heaven_bar.* to 'movie'@'%' with grant option;
-- 如果没有使用mysql_native_password将无法远程连接MySQL
ALTER USER 'movie'@'%' IDENTIFIED WITH mysql_native_password BY 'yourpasswd'; 
-- ----------------mysql:8

-- 授权
flush privileges;
