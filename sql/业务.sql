DROP TABLE IF EXISTS `业务信息`;
CREATE TABLE `业务信息` (
  `业务编码` char(20) NOT NULL,
  `业务情况` char(20) NOT NULL,
  `代码` char(20) default null,
  `名称` char(20) default null,
  `类型` char(20) DEFAULT NULL,
  `位置` char(26) default null,
  `总量` char(26) default null,
  `单位` char(26) default null,
  `单价` char(26) default null,
  `供应商` char(26) default null,
  KEY (`业务编码`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;