DROP TABLE IF EXISTS `仓库`;
CREATE TABLE `仓库` (
  `货物代码` char(20) NOT NULL,
  `货物名称` char(20) default null,
  `货物类型` char(20) DEFAULT NULL,
  `存放库位` char(26) default null,
  `库存总量` char(26) default null,
  `计量单位` char(26) default null,
  `供应商` char(26) default null,
  KEY (`货物代码`,`供应商`,`计量单位`,`存放库位`,`货物类型`,`货物名称`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `链接表`;
CREATE TABLE `链接表` (
  `货物代码` char(20) NOT NULL,
  `货物名称` char(20) default null,
  `货物类型` char(20) DEFAULT NULL,
  `计量单位` char(26) default null,
  `供应商` char(16) default null,
  KEY (`货物代码`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `链接表` VALUES ('1-1-1',  'mate50pro','手机','台','华为');
INSERT INTO `链接表` VALUES ('1-1-2',  'iphone14pro','手机','台','Apple');
INSERT INTO `链接表` VALUES ('1-1-3',  '小新14s','笔记本电脑','台','联想');
INSERT INTO `链接表` VALUES ('1-1-4',  'U盘64G','电子产品','个','SanDisk');
INSERT INTO `链接表` VALUES ('1-1-5',  '鼠标','电子产品','个','Apple');
INSERT INTO `链接表` VALUES ('1-1-6',  '键盘','电子产品','个','联想');
INSERT INTO `链接表` VALUES ('1-1-7',  '耳机','电子产品','对','华为');
INSERT INTO `链接表` VALUES ('1-1-8',  '智能手表','电子产品','支','Apple');
INSERT INTO `链接表` VALUES ('1-1-9',  '平板电脑','电子产品','台','联想');
INSERT INTO `链接表` VALUES ('1-2-1',  '冲锋衣','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-2',  '衬衫','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-3',  '西装','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-4',  '短袖','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-5',  '牛仔外套','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-6',  '防晒衣','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-7', '卫衣','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-8',  '民族服','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-2-9',  '羽绒服','衣服','件','淘宝');
INSERT INTO `链接表` VALUES ('1-3-1',  '苹果','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-2',  '梨子','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-3',  '香蕉','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-4',  '红龙果','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-5', '橘子','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-6',  '荔枝','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-7',  '榴莲','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-8',  '哈密瓜','水果','斤','天猫');
INSERT INTO `链接表` VALUES ('1-3-9',  '桃子','水果','斤','天猫');

DROP TABLE IF EXISTS `入库单`;
CREATE TABLE `入库单` (
  `入库单编号` char(20) NOT NULL,
  `货物代码` char(20) NOT NULL,
  `货物名称` char(20) default null,
  `货物类型` char(20) DEFAULT NULL,
  `存放库位` char(26) default null,
  `入库总量` char(26) default null,
  `计量单位` char(26) default null,
  `入库单价` char(26) default null,
  `入库时间` char(32) default null,
  `供应商` char(26) default null,
  `经办人` char(26) default null,
  KEY (`入库单编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TRIGGER IF EXISTS `ru_c`;
DELIMITER ;;
CREATE TRIGGER `ru_c` AFTER INSERT ON `入库单` FOR EACH ROW begin
set @q=new.入库单编号;
set @a=new.货物代码;
set @b=new.货物名称;
set @c=new.货物类型;
set @d=new.存放库位;
set @e=new.入库总量;
set @f=new.计量单位;
set @g=new.入库单价;
set @h=new.入库时间;
set @i=new.供应商;
set @j=new.经办人;



if(select 仓库.货物代码 from 仓库 where 仓库.货物名称=@b and 仓库.货物类型=@c and 仓库.存放库位=@d and 仓库.计量单位=@f and 仓库.供应商=@i ) is null

then

insert into 仓库 values(@a,@b,@c,@d,@e,@f,@i);

else

update 仓库

set 仓库.库存总量=仓库.库存总量+@e

where 仓库.货物代码=@a and 仓库.货物名称=@b and 仓库.货物类型=@c and 仓库.存放库位=@d and 仓库.计量单位=@f and 仓库.供应商=@i;
end if;

end
;;
DELIMITER ;


DROP TABLE IF EXISTS `出库单`;
CREATE TABLE `出库单` (
  `出库单编号` char(20) NOT NULL,
  `货物代码` char(20) NOT NULL,
  `货物名称` char(20) default null,
  `货物类型` char(20) DEFAULT NULL,
  `存放库位` char(26) default null,
  `出库总量` char(26) default null,
  `计量单位` char(26) default null,
  `出库单价` char(26) default null,
  `出库时间` char(32) default null,
  `供应商` char(26) default null,
  `经办人` char(26) default null,
  KEY (`出库单编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TRIGGER IF EXISTS `chu_k`;
DELIMITER ;;
CREATE TRIGGER `chu_k` AFTER INSERT ON `出库单` FOR EACH ROW begin
set @q=new.出库单编号;
set @a=new.货物代码;
set @b=new.货物名称;
set @c=new.货物类型;
set @d=new.存放库位;
set @e=new.出库总量;
set @f=new.计量单位;
set @g=new.出库单价;
set @h=new.出库时间;
set @i=new.供应商;
set @j=new.经办人;
 
if(select 仓库.货物代码 from 仓库 where 仓库.货物代码=@a and 仓库.货物名称=@b and 仓库.货物类型=@c and 仓库.存放库位=@d and 仓库.计量单位=@f and 仓库.供应商=@i ) is not null

then

update 仓库
 
set 仓库.库存总量=仓库.库存总量-@e
 
where 仓库.货物代码=@a and 仓库.货物名称=@b and 仓库.货物类型=@c and 仓库.存放库位=@d and 仓库.计量单位=@f and 仓库.供应商=@i;

end if;

 
end
;;
DELIMITER ;
