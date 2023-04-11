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

-- get user group
select MEMBERS.user_id as is_member, ADMINS.user_id as is_admin, SUPERADMIN.user_id as is_superadmin from USER
left join MEMBERS on USER.user_id=MEMBERS.user_id
left join ADMINS on USER.user_id=ADMINS.user_id
left join SUPERADMIN on USER.user_id=SUPERADMIN.user_id
where USER.user_id="user_id";

-- change password
update USER
set password="password"
where email="email";