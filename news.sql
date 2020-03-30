/*
 Navicat Premium Data Transfer

 Source Server         : Adminstrastor
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : ccnews

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 14/07/2019 16:13:14
*/

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `ccnews`;
USE `ccnews`;
-- ----------------------------
-- Table structure for login
-- ----------------------------
DROP TABLE IF EXISTS `news_item`;
-- 
CREATE TABLE `news_item` (
  `title` varchar(200) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `url` varchar(100),
  `date` varchar(64),
  `source` varchar(100),
  `website` varchar(100),
  `theme` varchar(20)
);