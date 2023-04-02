-- create admin table
create table ADMINS (
  user_id varchar(36),
  comit_id varchar(36),
  foreign key (user_id) references USER(user_id) on delete cascade,
  foreign key (comit_id) references COMMITTEE(comit_id) on delete cascade,
  primary key (user_id, comit_id)
);

-- add new admin
insert into ADMINS
values ("user_id", "comit_id");

-- remove admin
delete from ADMINS
where user_id="user_id" and comit_id="comit_id";
