/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80021
Source Host           : localhost:3306
Source Database       : 仓库管理系统2

Target Server Type    : MYSQL
Target Server Version : 80021
File Encoding         : 65001

Date: 2020-12-24 19:13:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `仓库`
-- ----------------------------
DROP TABLE IF EXISTS `仓库`;
CREATE TABLE `仓库` (
  `货物名称` char(10) DEFAULT NULL,
  `货物编号` char(10) NOT NULL,
  `货物数量` char(10) DEFAULT NULL,
  `供应商编号` char(10) DEFAULT NULL,
  PRIMARY KEY (`货物编号`),
  KEY `供应商编号` (`供应商编号`),
  CONSTRAINT `仓库_ibfk_1` FOREIGN KEY (`供应商编号`) REFERENCES `供应商` (`编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of 仓库
-- ----------------------------
INSERT INTO `仓库` VALUES ('aAAA', '001', '0', '002');
INSERT INTO `仓库` VALUES ('柚子', '002', '100', '003');
INSERT INTO `仓库` VALUES ('哈哈', '111', '88', '001');
INSERT INTO `仓库` VALUES ('苹果', 'P1', '10', '001');

-- ----------------------------
-- Table structure for `供应商`
-- ----------------------------
DROP TABLE IF EXISTS `供应商`;
CREATE TABLE `供应商` (
  `编号` char(10) NOT NULL,
  `姓名` char(10) DEFAULT NULL,
  `电话` char(10) DEFAULT NULL,
  PRIMARY KEY (`编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of 供应商
-- ----------------------------
INSERT INTO `供应商` VALUES ('001', 'www', '123456');
INSERT INTO `供应商` VALUES ('002', 'aaa', '11222');
INSERT INTO `供应商` VALUES ('003', 'bwb', '123456');

-- ----------------------------
-- Table structure for `入库`
-- ----------------------------
DROP TABLE IF EXISTS `入库`;
CREATE TABLE `入库` (
  `入库单号` char(10) NOT NULL,
  `货物编号` char(10) DEFAULT NULL,
  `入库量` char(10) DEFAULT NULL,
  `货物名称` char(10) DEFAULT NULL,
  `供应商编号` char(10) DEFAULT NULL,
  PRIMARY KEY (`入库单号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of 入库
-- ----------------------------
INSERT INTO `入库` VALUES ('1120', '001', '10', 'aAAA', '002');
INSERT INTO `入库` VALUES ('1130', '002', '100', '柚子', '003');
INSERT INTO `入库` VALUES ('456', '111', '100', '哈哈', '001');
INSERT INTO `入库` VALUES ('R111', 'p1', '100', '苹果', '001');
INSERT INTO `入库` VALUES ('R123', 'P1', '700', '苹果', '001');
INSERT INTO `入库` VALUES ('R124', 'P1', '10', '苹果', '001');

-- ----------------------------
-- Table structure for `出库`
-- ----------------------------
DROP TABLE IF EXISTS `出库`;
CREATE TABLE `出库` (
  `出库单号` char(10) NOT NULL,
  `货物编号` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `出库量` char(10) DEFAULT NULL,
  `出库货物` char(10) DEFAULT NULL,
  PRIMARY KEY (`出库单号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of 出库
-- ----------------------------
INSERT INTO `出库` VALUES ('001', '001', '10', 'aAAA');
INSERT INTO `出库` VALUES ('002', 'P1', '600', '苹果');
INSERT INTO `出库` VALUES ('555', '111', '12', '哈哈');
DROP TRIGGER IF EXISTS `ru_c`;
DELIMITER ;;
CREATE TRIGGER `ru_c` AFTER INSERT ON `入库` FOR EACH ROW begin
 
set @a=new.货物名称;
 
set @b=new.货物编号;
 
set @c=new.入库量;
 
set @d=new.供应商编号;
 
if(select 仓库.货物编号 from 仓库 where 仓库.货物编号=@b and 仓库.货物名称=@a and 仓库.供应商编号=@d) is null
 
then
 
insert into 仓库 values(@a,@b,@c,@d);
 
else
 
update 仓库
 
set 仓库.货物数量=仓库.货物数量+@c
 
where 仓库.货物名称=@a and 仓库.货物编号=@b and 仓库.供应商编号=@d;
 
end if;
 
end
;;
DELIMITER ;
DROP TRIGGER IF EXISTS `chu_k`;
DELIMITER ;;
CREATE TRIGGER `chu_k` AFTER INSERT ON `出库` FOR EACH ROW begin
 
set @n=new.出库货物;
 
set @m=new.货物编号;
 
set @s=new.出库量;
 
if(select 仓库.货物编号 from 仓库 where 仓库.货物编号=@m and 仓库.货物名称=@n) is not null
 
then
 
update 仓库
 
set 仓库.货物数量=仓库.货物数量-@s
 
where 仓库.货物编号=@m and 仓库.货物名称=@n;
 
end if;
 
end
;;
DELIMITER ;
