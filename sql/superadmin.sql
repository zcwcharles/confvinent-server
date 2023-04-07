create table SUPERADMIN (
  user_id varchar(36),
  foreign key(user_id) references USER(user_id)
);

insert into SUPERADMIN
values ('user_id');
