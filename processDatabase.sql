use sys;
drop database if exists DatabaseProcess;
create database DatabaseProcess;
use DatabaseProcess;

create table ManageTime
(
	ID int,
    StartTime time,
    EndTime time,

    constraint PK_ManageTime primary key (ID)
);

insert ManageTime
values(1, '6:00', '16:00');
select ID, Time_format(StartTime, '%H:%i') , Time_format(EndTime, '%H:%i') from ManageTime
