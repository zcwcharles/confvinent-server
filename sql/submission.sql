-- create submission table
create table SUBMISSION (
  sub_id varchar(36) primary key,
  sub_time bigint not null,
  title varchar(200) not null,
  status varchar(10) not null,
  con_id varchar(36),
  foreign key(con_id) references CONFERENCE(con_id) on delete cascade
);

-- add submission
insert into SUBMISSION
values ("sub_id", UNIX_TIMESTAMP() * 1000, "title", "status", "con_id");

-- get submission
select * from SUBMISSION left join CONFERENCE on SUBMISSION.con_id=CONFERENCE.con_id
where sub_id="sub_id";

-- update submission status
update SUBMISSION
set status="status"
where sub_id="sub_id";

-- get submission list by user id
select SUBMISSION.sub_id, CONFERENCE.submit_deadline, SUBMISSION.name, CONFERENCE.name as con_name, status from AUTHOR
left join SUBMISSION on AUTHOR.sub_id=SUBMISSION.sub_id
left join CONFERENCE on CONFERENCE.con_id=SUBMISSION.con_id
where AUTHOR.user_id="user_id";
