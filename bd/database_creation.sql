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
constraint status_fk foreign key(database_id) references data_base(id_database)on delete cascade
);

-- TABLE TABLESPACE_BD
create table tablespace_db(
id_tablespace number not null,
tablespace_name varchar2(200 byte) not null,
status varchar2(10 byte) not null,
max_size number not null,
used_space number not null,
space_allocated number not null,
free_space number not null,
tablespace_type varchar2(10 byte) not null,
database_id number not null,
time_stamp timestamp,
constraint table_space_pk primary key(id_tablespace),
constraint table_space_fk1 foreign key(database_id) references data_base(id_database) on delete cascade
);


-- TABLE DATA_FILE
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
constraint data_file_fk foreign key(tablespace_id) references tablespace_db(id_tablespace) on delete cascade
);

-- TABLE USER_DB
create table user_db(
id_user number not null,
username varchar2(200 byte) not null ,
account_status varchar2(30 byte) not null,
last_login timestamp,
creation_date timestamp not null,
defaultTablespace_id number not null,
temporaryTablespace_id number not null,
time_stamp timestamp not null,
constraint user_db_pk primary key(id_user),
constraint user_db_fk1 foreign key(defaultTablespace_id) references tablespace_db(id_tablespace) on delete cascade,
constraint user_db_fk2 foreign key(temporaryTablespace_id) references tablespace_db(id_tablespace) on delete cascade
);


