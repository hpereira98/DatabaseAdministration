delete from data_base where id_database = 2;
delete from status where id_status = 1;


drop table status;
drop table data_file;
drop table user_db;
drop table tablespace_bd;
drop table data_base;

drop sequence status_id;
drop sequence database_id;
drop sequence datafile_id;
drop sequence user_id;
drop sequence tablespace_id;