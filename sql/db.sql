create database if not exists blog;
use blog;
create table article
(
	id int not null auto_increment,
	comment int not null default 0,
	title varchar(255) not null,
	date datetime,
	content text not null,
	usrid int not null default 1,
	author varchar(255) default '',
	tag varchar(32) default '',
	primary key(id)
)engine=innodb,charset=utf8;

create table comment
(
	id int not null auto_increment,
	content text not null,
	author varchar(255) not null,
	email  varchar(512) not null,
	homepage varchar(512) not null default '',
	usrid int not null default 0,
	articleid int not null,
	upnum int(11) default 0,
	downnum int(11) default 0,
	date datetime not null,
	ipv4 int,
	ipv6 binary(16),
	useragent varchar(100),
	primary key(id)
)engine=innodb,charset=utf8;

CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `author` varchar(255) NOT NULL,
  `email` varchar(512) NOT NULL,
  `homepage` varchar(512) NOT NULL DEFAULT '',
  `usrid` int(11) NOT NULL DEFAULT '0',
  `articleid` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `upnum` int(11) DEFAULT '0',
  `downnum` int(11) DEFAULT '0',
  `ipv4` int(11) DEFAULT NULL,
  `ipv6` binary(16) DEFAULT NULL,
  `useragent` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8

create table user
(
	id int not null auto_increment,
	password char(32) not null,
	user varchar(255) not null unique,
	primary key(id)
)engine=innodb,charset=utf8;

create table msg
(
  id int not null auto_increment,
	content varchar(255) not null,
	author varchar(255) not null,
	email  varchar(512) not null,
	homepage varchar(512) not null default '',
	usrid int not null default 0,
	date datetime not null,
	primary key(id)
)engine=innodb,charset=utf8;

delimiter ||
drop trigger if exists t_afterinsert_on_comment ;
create trigger t_afterinsert_on_comment  
after insert 
on comment 
for each row 
	begin update article set article.comment=article.comment+1 where article.id=new.articleid; 
end ||
delimiter ;

