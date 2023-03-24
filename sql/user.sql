-- create user table
create table USER (
  user_id varchar(36) primary key,
  email varchar(100),
  password varchar(100),
  first_name varchar(100),
  last_name varchar(100),
  address varchar(200),
  organization varchar(100)
);

-- add new committee
insert into USER
values ('user_id', 'email', 'password', 'first_name', 'last_name', 'address', 'organization')
