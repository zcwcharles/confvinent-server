-- create author table
create table AUTHOR (
  user_id varchar(36),
  sub_id varchar(36),
  foreign key(user_id) references USER(user_id) on delete cascade,
  foreign key(sub_id) references SUBMISSION(sub_id) on delete cascade,
  primary key(user_id, sub_id)
);

-- add to author list
insert into AUTHOR
values ("user_id", "sub_id");

-- add multiple authors
insert into AUTHOR
values ("user_id", "sub_id"), ("user_id", "sub_id");

-- remove from author list
delete from AUTHOR
where user_id="user_id"

-- get authors by sub id
select first_name, last_name, email
from AUTHOR left join USER on AUTHOR.user_id=USER.user_id
where sub_id="sub_id";
