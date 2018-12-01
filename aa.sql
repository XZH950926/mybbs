/*
SQLyog Ultimate v12.3.1 (64 bit)
MySQL - 5.5.20 : Database - bbs
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`bbs` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `bbs`;

/*Table structure for table `alembic_version` */

DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `alembic_version` */

insert  into `alembic_version`(`version_num`) values 
('e6377a1c5061');

/*Table structure for table `banner` */

DROP TABLE IF EXISTS `banner`;

CREATE TABLE `banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bannerName` varchar(20) NOT NULL,
  `imglink` varchar(200) NOT NULL,
  `link` varchar(200) NOT NULL,
  `priority` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `imglink` (`imglink`),
  UNIQUE KEY `link` (`link`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

/*Data for the table `banner` */

insert  into `banner`(`id`,`bannerName`,`imglink`,`link`,`priority`) values 
(10,'b1','https://aecpm.alicdn.com/simba/img/TB1XotJXQfb_uJkSnhJSuvdDVXa.jpg','https://aecpm.alicdn.com/simba/img/TB1XotJXQfb_uJkSnhJSuvdDVXa.jpg',1),
(12,'b2','https://img.alicdn.com/tfs/TB1ZN4yswHqK1RjSZFkXXX.WFXa-520-280.png_q90_.webp','https://img.alicdn.com/tfs/TB1ZN4yswHqK1RjSZFkXXX.WFXa-520-280.png_q90_.webp',2),
(13,'b3','https://aecpm.alicdn.com/simba/img/TB183NQapLM8KJjSZFBSutJHVXa.jpg','https://aecpm.alicdn.com/simba/img/TB183NQapLM8KJjSZFBSutJHVXa.jpg',3),
(14,'b4','https://aecpm.alicdn.com/simba/img/TB1JNHwKFXXXXafXVXXSutbFXXX.jpg','https://aecpm.alicdn.com/simba/img/TB1JNHwKFXXXXafXVXXSutbFXXX.jpg',4);

/*Table structure for table `border` */

DROP TABLE IF EXISTS `border`;

CREATE TABLE `border` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `borderName` varchar(20) NOT NULL,
  `postNum` int(11) NOT NULL,
  `create_time` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Data for the table `border` */

insert  into `border`(`id`,`borderName`,`postNum`,`create_time`) values 
(4,'java',0,'2018-09-29 19:47:41.123'),
(5,'python',0,'2018-10-06 19:34:13.260701'),
(6,'c++',0,'2018-10-06 19:34:25.335392'),
(7,'R',0,'2018-10-09 19:02:47.267795');

/*Table structure for table `common` */

DROP TABLE IF EXISTS `common`;

CREATE TABLE `common` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `post_id` int(11) DEFAULT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `common_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `common_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `front_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `common` */

insert  into `common`(`id`,`content`,`post_id`,`user_id`,`create_time`) values 
(1,'<p>sdfsafdsad</p>',1,'r9M7ce42GmBzsG8QJDpEDo','2018-10-06 21:39:00'),
(2,'<p>这是个啥？<img src=\"http://img.baidu.com/hi/jx2/j_0009.gif\"/></p>',1,'r9M7ce42GmBzsG8QJDpEDo','2018-10-07 09:05:13');

/*Table structure for table `front_user` */

DROP TABLE IF EXISTS `front_user`;

CREATE TABLE `front_user` (
  `id` varchar(100) NOT NULL,
  `telephone` varchar(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `_password` varchar(100) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `realname` varchar(50) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `signature` varchar(100) DEFAULT NULL,
  `gender` enum('MALE','FEMALE','SECRET','UNKNOW') DEFAULT NULL,
  `join_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telephone` (`telephone`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `front_user` */

insert  into `front_user`(`id`,`telephone`,`username`,`_password`,`email`,`realname`,`avatar`,`signature`,`gender`,`join_time`) values 
('r9M7ce42GmBzsG8QJDpEDo','15037244351','zhangsan','pbkdf2:sha256:50000$73YdOAeZ$534675e35293e66f93d468ea126f3f2b6c50242a24ea4356fbafbdf712c3ae2e',NULL,NULL,NULL,NULL,'UNKNOW','2018-09-27 16:10:56'),
('WXeJHYoeVJ3GSM8C67ZJEa','13525144142','mafenglei','pbkdf2:sha256:50000$KKlhoc5v$dc0585c292ff51f2976f03c1568c26192516ddc7a362468ff0d0fb84fee93d8a',NULL,NULL,NULL,NULL,'UNKNOW','2018-10-08 08:44:24');

/*Table structure for table `post` */

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(40) NOT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `border_id` int(11) DEFAULT NULL,
  `content` text,
  `create_time` datetime DEFAULT NULL,
  `views` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `border_id` (`border_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`border_id`) REFERENCES `border` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `front_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

/*Data for the table `post` */

insert  into `post`(`id`,`title`,`user_id`,`border_id`,`content`,`create_time`,`views`) values 
(1,'大数据','r9M7ce42GmBzsG8QJDpEDo',4,'<p><img src=\"http://pg438m4az.bkt.clouddn.com/0c0da4044b80faf1d55c21c02c82383f.jpg\" title=\"0c0da4044b80faf1d55c21c02c82383f.jpg\" alt=\"http://pg438m4az.bkt.clouddn.com/0c0da4044b80faf1d55c21c02c82383f.jpg\"/></p>','2018-10-06 09:14:28',NULL),
(2,'数据分析','r9M7ce42GmBzsG8QJDpEDo',4,'<p><img src=\"http://pg438m4az.bkt.clouddn.com/206ec649212c9ce937a98d6223a027ae.jpg\" title=\"206ec649212c9ce937a98d6223a027ae.jpg\" alt=\"http://pg438m4az.bkt.clouddn.com/206ec649212c9ce937a98d6223a027ae.jpg\"/></p>','2018-10-06 09:20:08',NULL),
(3,'大数据','r9M7ce42GmBzsG8QJDpEDo',4,'<p><strong>safdsgf</strong></p>','2018-10-06 14:23:07',NULL),
(4,'casfsdfs','r9M7ce42GmBzsG8QJDpEDo',4,'<p><span style=\"text-decoration: underline;\">xzfdsfsd</span></p>','2018-10-06 14:23:23',NULL),
(5,'asfdsfsfddsf','r9M7ce42GmBzsG8QJDpEDo',4,'<p><span style=\"border: 1px solid rgb(0, 0, 0);\">asfdsf</span>s</p>','2018-10-06 14:23:38',NULL),
(6,'dsfsdgsfgdasgsdg','r9M7ce42GmBzsG8QJDpEDo',4,'<p>dsafdsfsdds</p>','2018-10-06 14:24:00',NULL),
(7,'dsfsdffgda','r9M7ce42GmBzsG8QJDpEDo',4,'<p>agfdsagdfagda</p>','2018-10-06 14:24:14',NULL),
(8,'zsfsagadgf','r9M7ce42GmBzsG8QJDpEDo',4,'<p>sagdfgdfgdagfdag</p>','2018-10-06 14:26:57',NULL),
(9,'asfsad','r9M7ce42GmBzsG8QJDpEDo',4,'<p><strong>sagdfgdsg</strong></p>','2018-10-06 19:27:56',NULL),
(10,'sdgfdsgd','r9M7ce42GmBzsG8QJDpEDo',4,'<p><span style=\"text-decoration: underline;\">sdgdsfgd</span></p>','2018-10-06 19:28:10',NULL),
(13,'adasfdsa','r9M7ce42GmBzsG8QJDpEDo',5,'<p>dsafsdagfs</p>','2018-10-06 20:11:49',NULL),
(14,'sadfsdagfsdffg','r9M7ce42GmBzsG8QJDpEDo',5,'<p>sagsadgfdgdsg</p>','2018-10-06 20:12:03',NULL),
(15,'afsdafdsafdsa','r9M7ce42GmBzsG8QJDpEDo',5,'<p>safdsafdsaf</p>','2018-10-06 20:12:22',2),
(16,'safdsdafdsafdsa','r9M7ce42GmBzsG8QJDpEDo',5,'<p>safsdafdsafdsa</p>','2018-10-06 20:12:47',1);

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(20) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `permis` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `role` */

insert  into `role`(`id`,`role_name`,`desc`,`permis`) values 
(1,'普通用户','只能看自己的信息',2),
(2,'板块管理','可以修改板块',16),
(3,'个人中心','查看自己的信息',1),
(4,'帖子管理','管理帖子',4);

/*Table structure for table `role_user` */

DROP TABLE IF EXISTS `role_user`;

CREATE TABLE `role_user` (
  `rid` int(11) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  KEY `rid` (`rid`),
  KEY `uid` (`uid`),
  CONSTRAINT `role_user_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `role` (`id`),
  CONSTRAINT `role_user_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `role_user` */

insert  into `role_user`(`rid`,`uid`) values 
(1,1),
(2,1),
(3,1),
(4,1);

/*Table structure for table `tag` */

DROP TABLE IF EXISTS `tag`;

CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) DEFAULT NULL,
  `isTag` tinyint(1) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `tag_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `tag` */

insert  into `tag`(`id`,`post_id`,`isTag`,`create_time`) values 
(1,NULL,0,'2018-10-07 19:22:56'),
(2,1,1,'2018-10-07 19:24:33');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `_password` varchar(200) NOT NULL,
  `email` varchar(20) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`_password`,`email`,`create_time`) values 
(1,'xuezenghui','pbkdf2:sha256:50000$Gxyoq91O$366705213f195182f175ec86385b3dcc7825f8120cd5ae0b4b1189dedfde70e0','1759455090@qq.com','2018-09-28 14:46:48');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
