-- create committee table
create table COMMITTEE (
  comit_id varchar(36) primary key,
  name varchar(100),
  icon varchar(200)
);

-- add new committee
insert into COMMITTEE
values ('comit_id', 'name', 'icon')
