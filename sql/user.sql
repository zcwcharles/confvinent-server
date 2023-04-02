-- create user table
create table USER (
  user_id varchar(36) primary key,
  email varchar(100) not null,
  password varchar(100) not null,
  first_name varchar(100) not null,
  last_name varchar(100) not null,
  address varchar(200),
  organization varchar(100)
);

-- add new committee
insert into USER
values ('user_id', 'email', 'password', 'first_name', 'last_name', 'address', 'organization');

-- authenticate user
select user_id from USER
where email="email" and password="password";

-- get user by email
select user_id from USER
where email="email";
