-- create conference table
create table CONFERENCE (
  con_id varchar(36) primary key,
  name varchar(100) not null,
  submit_deadline bigint not null,
  review_deadline bigint not null,
  review_number_for_each_paper int not null,
  comit_id varchar(36),
  create_time bigint not null,
  end_time bigint not null,
  foreign key (comit_id) references COMMITTEE(comit_id) on delete cascade
);

-- add new conference
insert into CONFERENCE
values(
  "con_id","name", "submit_deadline", "review_deadline",
  "review_number_for_each_paper", "comit_id", "create_time", "end_time"
);

-- delete conference
delete from CONFERENCE
where con_id="con_id";

-- get ongoing conference
select * from CONFERENCE
where end_time > UNIX_TIMESTAMP(NOW()) and comit_id="comit_id";

-- get all conferences can be submitted to
select con_id, name from CONFERENCE
where submit_deadline > UNIX_TIMESTAMP(NOW());
