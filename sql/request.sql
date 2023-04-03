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

-- get request list
select req_id, create_time, email, status, make_by from REQUEST
left join USER on REQUEST.make_by = USER.user_id
where comit_id="comit_id";

-- get request by id
select * from REQUEST
left join USER on REQUEST.make_by = USER.user_id
where req_id="req_id";

-- get request list for non-admin
select req_id, create_time, email, status, from REQUEST
left join USER on REQUEST.make_by = USER.user_id
where make_by="user_id";
