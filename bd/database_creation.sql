-- TABLE DATABASE
create table data_base(
id_database number not null,
database_name varchar2(50 byte) not null,
version varchar2(100 byte) not null,
plataform varchar2(100 byte) not null,
host_name varchar2(100 byte) not null,
up_time number not null,
time_stamp timestamp not null,
constraint data_base_pk primary key(id_database)
);

-- TABLE STATUS
create table status(
id_status number not null,
total_ram number not null,
memory_used number not null,
ram_used number not null,
free_ram number not null,
cpu_count number not null,
cpu_core_count number not null,
database_id number not null,
time_stamp timestamp not null,
constraint status_pk primary key(id_status),
constraint status_fk foreign key(database_id) references data_base(id_database)
);

create table tablespace_bd(
id_tablespace number not null,
tablespace_name varchar2(200 byte) not null,
status varchar2(10 byte) not null,
table_space_size number not null,
max_size number not null,
free_space number not null,
type varchar2(50 byte) not null,
database_id number not null,
time_stamp timestamp,
constraint table_space_pk primary key(id_tablespace),
constraint table_space_fk1 foreign key(database_id) references data_base(id_database)
);

create table data_file(
id_datafile number not null,
datafile_name varchar2(200 byte) not null,
autoextensible varchar2(3 byte) not null,
max_size number not null,
total_size number not null,
status varchar2(10 byte) not null,
tablespace_id number not null,
time_stamp timestamp not null,
constraint data_file_pk primary key(id_datafile),
constraint data_file_fk foreign key(tablespace_id) references tablespace_bd(id_tablespace)
);

create table user_db(
id_user number not null,
username varchar2(200 byte) not null,
account_status varchar2(3 byte) not null,
creation_date date not null,
tablespace_id number,
time_stamp timestamp not null,
constraint user_db_pk primary key(id_user),
constraint user_db_fk foreign key(tablespace_id) references tablespace_bd(id_tablespace)
);


