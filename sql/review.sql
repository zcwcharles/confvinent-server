-- create review table
create table REVIEW (
  user_id varchar(36),
  sub_id varchar(36),
  decision varchar(8),
  foreign key(user_id) references USER(user_id) on delete cascade,
  foreign key(sub_id) references SUBMISSION(sub_id) on delete cascade,
  primary key(user_id, sub_id)
);

-- add reviewer
insert into REVIEW
values ("user_id", "sub_id", null);

-- add reviewers
insert into REVIEW
values ("user_id", "sub_id", null), ("user_id", "sub_id", null);

-- change decision
update REVIEW
set decision="decision"
where user_id="user_id" and sub_id="sub_id";

-- get review list
select REVIEW.sub_id, review_deadline, title, status from REVIEW
left join SUBMISSION on SUBMISSION.sub_id = REVIEW.sub_id
left join CONFERENCE on CONFERENCE.con_id = SUBMISSION.con_id
where user_id="user_id";

-- get review
select * from REVIEW
left join SUBMISSION on REVIEW.sub_id=SUBMISSION.sub_id
where user_id="user_id" and sub_id = "sub_id";

-- get reviews by sub_id
select decision from REVIEW
where sub_id="sub_id";
