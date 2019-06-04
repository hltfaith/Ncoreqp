/*

  设计数据库表结构

 */

-- 创建数据库
CREATE DATABASE ticketdb DEFAULT CHARSET=utf8;

use ticketdb;

--------- 后端 -----------

-- 创建 key 帐号
CREATE TABLE keyinfo(
  `ticket_id` INT unsigned not null auto_increment primary key,
  `ticket_keyid` VARCHAR(100) NOT NULL,
  `ticket_uuid` VARCHAR(100)
);

--------- 前端 -----------

-- 创建用户表
CREATE TABLE userinfo(
  `ticket_id` INT unsigned not null auto_increment primary key,
  `ticket_user` VARCHAR(100) NOT NULL,
  `ticket_passwd` VARCHAR(100) NOT NULL
);

-- 创建用户关注列表
CREATE TABLE followticket(
  `ticket_xh` INT unsigned not null auto_increment primary key,
  `ticket_user` VARCHAR(100) NOT NULL,
  `ticket_lch` VARCHAR(100) NOT NULL,
  `ticket_rq` VARCHAR(100) NOT NULL,
  `ticket_sj` VARCHAR(100) NOT NULL,
  `ticket_station` VARCHAR(100) NOT NULL,
  `ticket_type` VARCHAR(100) NOT NULL,
  `ticket_cjsj` DATE NOT NULL,
  `ticket_bz` VARCHAR(100),
  `ticket_cfcs` VARCHAR(100),
  `ticket_ddcs` VARCHAR(100),
  `ticket_cfsj` VARCHAR(100)
)ENGINE=INNODB  DEFAULT CHARSET=utf8;

-- 发送邮件设置
CREATE TABLE mailinfo(
  `ticket_id` INT unsigned not null auto_increment primary key,
  `ticket_mail` VARCHAR(100) NOT NULL,
  `ticket_message` VARCHAR(1000) NOT NULL,
  `ticket_user` VARCHAR(100) NOT NULL
)ENGINE=INNODB  DEFAULT CHARSET=utf8;

