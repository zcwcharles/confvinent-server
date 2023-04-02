-- create request table
create table REQUEST (
  req_id varchar(36) primary key,
  comit_id varchar(36),
  create_time bigint not null,
  status varchar(8) not null,
  processed_time bigint,
  reason varchar(500) not null,
  make_by varchar(36),
  process_by varchar(36),
  foreign key(comit_id) references COMMITTEE(comit_id) on delete cascade,
  foreign key(make_by) references USER(user_id) on delete cascade,
  foreign key(process_by) references USER(user_id) on delete cascade
);

-- add new request
insert into REQUEST
values ("req_id", "comit_id", "create_time", "status", null, "reason", "make_by", null);

-- process request
update REQUEST
set status="status", process_by="process_by"
where req="req_id";

-- get request status
select status from REQUEST
where req_id="req_id";
