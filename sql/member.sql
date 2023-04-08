-- create members table
create table MEMBERS(
  user_id varchar(36),
  comit_id varchar(36),
  comit_status varchar(8) not null,
  foreign key (user_id) references USER(user_id) on delete cascade,
  foreign key (comit_id) references COMMITTEE(comit_id) on delete cascade,
  primary key (user_id, comit_id)
);

-- add member
insert into MEMBERS
values ("user_id", "comit_id", "ACTIVE");

-- inactivate member
update MEMBERS
set comit_status="INACTIVE"
where user_id="user_id" and comit_id="comit_id";

-- activate member
update MEMBERS
set comit_status="ACTIVE"
where user_id="user_id" and comit_id="comit_id";

-- delete member
delete from MEMBERS
where user_id="user_id" and comit_id="comit_id";

-- get all member
select * from MEMBERS
left join USER on MEMBERS.user_id=USER.user_id
where comit_id="comit_id";

-- get comit id by user id
select comit_id from MEMBERS
where user_id="user_id";

-- get all active member and order by review count
select MEMBERS.user_id, cnt from MEMBERS left join (
  select distinct user_id, count(user_id) as cnt from REVIEW where decision is null group by user_id
) as DECISION_CNT on MEMBERS.user_id = DECISION_CNT.user_id
where MEMBERS.comit_id="comit_id" and MEMBERS.comit_status="ACTIVE"
order by cnt asc, cnt is null;

-- get comit id and mamage comit id by user id
select MEMBERS.comit_id, ADMINS.comit_id as manage_comit_id from MEMBERS
left join ADMINS on MEMBERS.user_id=ADMINS_ID.user_id
where MEMBERS.user_id="user_id";
