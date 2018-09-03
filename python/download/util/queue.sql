DROP TABLE IF EXISTS `hainiu_queue`;
CREATE TABLE `hainiu_queue` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` tinyint(2) NOT NULL COMMENT '����',
  `action` varchar(2000) NOT NULL COMMENT '���ж���',
  `params` text COMMENT '����Ԥ��',
  `fail_ip` varchar(20) NOT NULL DEFAULT '' COMMENT '����ʧ�ܻ�����IP',
  `fail_times` int(5) NOT NULL DEFAULT '0' COMMENT '����ʧ�ܵĴ���',
  `create_times` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  PRIMARY KEY (`id`),
  KEY `id` (`id`),
  KEY `type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `hainiu_web_seed`;
CREATE TABLE `hainiu_web_seed` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(2000) NOT NULL COMMENT '����URL',
  `md5` varchar(40) NOT NULL COMMENT '����URL��MD5',
  `domain` varchar(100) NOT NULL COMMENT '������վ��domain',
  `host` varchar(200) NOT NULL COMMENT '������վHOST',
  `category` varchar(200) NOT NULL COMMENT '����',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '����ʱ��',
  `last_crawl_time` timestamp NULL DEFAULT NULL COMMENT '�������ɹ���ȡʱ��',
  `last_crawl_internally` int(10) DEFAULT NULL COMMENT '�������ɹ���ȡ������',
  `last_crawl_externally` int(10) DEFAULT NULL COMMENT '�������ɹ���ȡ������',
  `fail_times` int(11) DEFAULT '0' COMMENT 'ץȡʧ�ܴ���',
  `fail_ip` varchar(20) DEFAULT NULL COMMENT '���ʧ�ܵĻ���IP',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '״̬ 0 ���� 1 �ر�',
  PRIMARY KEY (`md5`),
  KEY `id` (`id`) USING BTREE,
  KEY `host` (`host`(191)) USING BTREE,
  KEY `domain` (`domain`) USING BTREE,
  KEY `md5` (`md5`) USING BTREE,
  KEY `status` (`status`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;


DROP TABLE IF EXISTS `hainiu_web_seed_internally`;
CREATE TABLE `hainiu_web_seed_internally` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(2000) NOT NULL COMMENT '����URL',
  `md5` varchar(40) NOT NULL COMMENT '����URL��MD5',
  `param` text COMMENT '����Ԥ��',
  `domain` varchar(100) NOT NULL COMMENT '������վ��domain',
  `host` varchar(200) NOT NULL COMMENT '������վHOST',
  `a_url` varchar(2000) NOT NULL COMMENT 'ץȡҳ�е�����',
  `a_md5` varchar(40) NOT NULL COMMENT 'ץȡҳ�е�������MD5',
  `a_host` varchar(200) NOT NULL COMMENT 'ץȡҳ�е�������HOST',
  `a_xpath` text NOT NULL COMMENT 'ץȡҳ�е�������XPATH',
  `a_title` text COMMENT 'ץȡҳ�е�������title',
  `create_time` int(11) NOT NULL COMMENT '��¼����ʱ��',
  `create_day` int(11) NOT NULL COMMENT '��¼������',
  `create_hour` int(11) NOT NULL COMMENT '��¼����Сʱ',
  `update_time` int(11) NOT NULL COMMENT '��¼����ʱ��',
  `fail_times` int(11) DEFAULT '0' COMMENT 'ץȡʧ�ܴ���',
  `fail_ip` varchar(20) DEFAULT NULL COMMENT '���ʧ�ܵĻ���IP',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '����״̬ 0 δ���� 1 �Ѵ���',
  PRIMARY KEY (`md5`,`a_md5`),
  KEY `id` (`id`) USING BTREE,
  KEY `host` (`host`(191)) USING BTREE,
  KEY `domain` (`domain`) USING BTREE,
  KEY `md5` (`md5`) USING BTREE,
  KEY `a_md5` (`a_md5`) USING BTREE,
  KEY `md5_aMd5` (`md5`,`a_md5`) USING BTREE,
  KEY `a_host` (`a_host`(191)) USING BTREE,
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;


DROP TABLE IF EXISTS `hainiu_web_seed_externally`;
CREATE TABLE `hainiu_web_seed_externally` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(2000) NOT NULL COMMENT '����URL',
  `md5` varchar(40) NOT NULL COMMENT '����URL��MD5',
  `param` text COMMENT '����Ԥ��',
  `domain` varchar(100) NOT NULL COMMENT '������վ��domain',
  `host` varchar(200) NOT NULL COMMENT '������վHOST',
  `a_url` varchar(2000) NOT NULL COMMENT 'ץȡҳ�е�����',
  `a_md5` varchar(40) NOT NULL COMMENT 'ץȡҳ�е�������MD5',
  `a_host` varchar(200) NOT NULL COMMENT 'ץȡҳ�е�������HOST',
  `a_xpath` text NOT NULL COMMENT 'ץȡҳ�е�������XPATH',
  `a_title` text COMMENT 'ץȡҳ�е�������title',
  `create_time` int(11) NOT NULL COMMENT '��¼����ʱ��',
  `create_day` int(11) NOT NULL COMMENT '��¼������',
  `create_hour` int(11) NOT NULL COMMENT '��¼����Сʱ',
  `update_time` int(11) NOT NULL COMMENT '��¼����ʱ��',
  `fail_times` int(11) DEFAULT '0' COMMENT 'ץȡʧ�ܴ���',
  `fail_ip` varchar(20) DEFAULT NULL COMMENT '���ʧ�ܵĻ���IP',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '����״̬ 0 δ���� 1 �Ѵ���',
  PRIMARY KEY (`md5`,`a_md5`),
  KEY `id` (`id`) USING BTREE,
  KEY `host` (`host`(191)) USING BTREE,
  KEY `domain` (`domain`) USING BTREE,
  KEY `md5` (`md5`) USING BTREE,
  KEY `a_md5` (`a_md5`) USING BTREE,
  KEY `md5_aMd5` (`md5`,`a_md5`) USING BTREE,
  KEY `a_host` (`a_host`(191)) USING BTREE,
  KEY `status` (`status`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;


DROP TABLE IF EXISTS `hainiu_web_page`;
CREATE TABLE `hainiu_web_page` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(2000) NOT NULL DEFAULT '' COMMENT '��ҳURL',
  `md5` varchar(40) NOT NULL COMMENT 'URL��MD5ֵ',
  `param` text COMMENT '����Ԥ��',
  `domain` varchar(100) NOT NULL COMMENT '��վdomain',
  `host` varchar(200) NOT NULL COMMENT '��վHOST',
  `title` varchar(500) DEFAULT NULL COMMENT '��ҳ��title��ǩ����',
  `create_time` int(11) NOT NULL COMMENT '��¼����ʱ��',
  `create_day` int(11) NOT NULL COMMENT '��¼������',
  `create_hour` int(11) NOT NULL COMMENT '��¼����Сʱ',
  `update_time` int(11) NOT NULL COMMENT '��¼����ʱ��',
  `fail_times` int(11) DEFAULT '0' COMMENT 'ץȡʧ�ܴ���',
  `fail_ip` varchar(20) DEFAULT NULL COMMENT '���ʧ�ܵĻ���IP',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '�Ƿ�ɹ����� 1 �ɹ� 2 δ�ɹ�',
  PRIMARY KEY (`md5`),
  KEY `id` (`id`),
  KEY `host` (`host`(191)),
  KEY `update_time` (`update_time`),
  KEY `md5` (`md5`),
  KEY `domain` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;




#on DUPLICATE KEY ��SQL����
insert_web_page_sql = """
    insert into hainiu_web_page (url,md5,create_time,create_day,create_hour,domain,param,update_time,host,
    title,fail_ip,status) values ("%s","%s",%s,%s,%s,"%s","%s",%s,"%s","%s","%s",%s)
    on DUPLICATE KEY UPDATE fail_times=fail_times+1,fail_ip=values(fail_ip);
"""