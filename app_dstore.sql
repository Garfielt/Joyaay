-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- 生成日期: 2015 年 09 月 30 日 10:46
-- 服务器版本: 5.5.23
-- PHP 版本: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `app_dstore`
--

-- --------------------------------------------------------

--
-- 表的结构 `xjy_feedback`
--

CREATE TABLE IF NOT EXISTS `xjy_feedback` (
  `fid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(10) unsigned NOT NULL,
  `grade` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `suggest` varchar(255) DEFAULT NULL,
  `addtime` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`fid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='评分反馈' AUTO_INCREMENT=12 ;

--
-- 转存表中的数据 `xjy_feedback`
--

INSERT INTO `xjy_feedback` (`fid`, `uid`, `grade`, `suggest`, `addtime`) VALUES
(1, 1, 3, 'suggest', 1410947554),
(2, 1, 3, 'OKLLL', 1410947599),
(3, 34, 1, '不咋地', 1411005890),
(4, 34, 3, '哈哈', 1411006344),
(5, 34, 3, '', 1411006349),
(6, 34, 3, '', 1411006367),
(7, 34, 5, '垃圾', 1411020594),
(8, 34, 4, 'hao', 1411032485),
(9, 34, 5, '默默', 1411032628),
(10, 52, 5, '好', 1411099264),
(11, 1, 4, '不错哦', 1411468609);

-- --------------------------------------------------------

--
-- 表的结构 `xjy_logs`
--

CREATE TABLE IF NOT EXISTS `xjy_logs` (
  `lid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `event` varchar(10) NOT NULL DEFAULT '',
  `mesg` text NOT NULL,
  `addtime` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`lid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='日志记录' AUTO_INCREMENT=179 ;

--
-- 表的结构 `xjy_member`
--

CREATE TABLE IF NOT EXISTS `xjy_member` (
  `mid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(10) unsigned NOT NULL,
  `nickname` varchar(30) NOT NULL DEFAULT '',
  `birthday` char(10) NOT NULL DEFAULT '2014-01-01',
  `sex` char(1) NOT NULL DEFAULT 'M',
  `gravatar` varchar(100) DEFAULT NULL,
  `addtime` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`mid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='成员数据' AUTO_INCREMENT=60 ;

--
-- 表的结构 `xjy_pointdata`
--

CREATE TABLE IF NOT EXISTS `xjy_pointdata` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(10) unsigned NOT NULL,
  `height` float NOT NULL DEFAULT '0',
  `weight` float NOT NULL DEFAULT '0',
  `note` char(255) NOT NULL DEFAULT '',
  `addday` char(8) NOT NULL DEFAULT '00000000',
  `addtime` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='成员测量数据' AUTO_INCREMENT=49 ;

--
-- 表的结构 `xjy_share`
--

CREATE TABLE IF NOT EXISTS `xjy_share` (
  `sid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(10) unsigned NOT NULL,
  `hash` char(10) NOT NULL DEFAULT '0',
  `type` char(6) NOT NULL,
  `params` varchar(255) DEFAULT NULL,
  `addtime` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='用户分享' AUTO_INCREMENT=1 ;

--
-- 转存表中的数据 `xjy_share`
--


-- --------------------------------------------------------

--
-- 表的结构 `xjy_timeline`
--

CREATE TABLE IF NOT EXISTS `xjy_timeline` (
  `tid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(10) unsigned NOT NULL,
  `mid` int(10) unsigned NOT NULL,
  `photo` varchar(100) NOT NULL DEFAULT '',
  `note` varchar(255) DEFAULT '',
  `addday` char(8) NOT NULL DEFAULT '00000000',
  `addtime` int(10) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='时光轴数据' AUTO_INCREMENT=66 ;

--
-- 表的结构 `xjy_user`
--

CREATE TABLE IF NOT EXISTS `xjy_user` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `phone` char(11) NOT NULL DEFAULT '',
  `password` char(32) NOT NULL DEFAULT '',
  `device` varchar(30) DEFAULT '',
  `regtime` int(10) unsigned NOT NULL DEFAULT '0',
  `acttime` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `Phone` (`phone`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='用户数据' AUTO_INCREMENT=61 ;