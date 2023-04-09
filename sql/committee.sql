-- create committee table
create table COMMITTEE (
  comit_id varchar(36) primary key,
  name varchar(100) not null,
);

-- add new committee
insert into COMMITTEE
values ('comit_id', 'name', 'icon');

-- delete committee
delete from COMMITTEE
where comit_id="comit_id";

-- get all committees
select * from COMMITTEE;

-- update committee name
update COMMITTEE
set name="name"
where comit_id="comit_id";
