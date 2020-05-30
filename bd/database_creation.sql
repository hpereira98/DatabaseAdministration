-- TABLE DATABASE
CREATE TABLE database_db(
id_database number not null,
database_name varchar2(50 byte) not null,
version varchar2(100 byte) not null,
platform_name varchar2(100 byte) not null,
host_name varchar2(100 byte) not null,
up_time number not null,
time_stamp timestamp not null,
constraint database_pk primary key(id_database)
);

-- TABLE MEMORY
CREATE TABLE memory_db(
id_memory number not null,
total_ram number not null,
memory_used number not null,
ram_used number not null,
free_ram number not null,
cpu_count number not null,
cpu_socket_count number not null,
cpu_core_count number not null,
database_id number not null,
time_stamp timestamp not null,
constraint memory_pk primary key(id_memory),
constraint memory_fk foreign key(database_id) references database_db(id_database)on delete cascade
);

-- TABLE USER_DB
CREATE TABLE user_db(
id_user number not null,
username varchar2(200 byte) not null ,
account_status varchar2(30 byte) not null,
last_login timestamp,
creation_date timestamp not null,
defaultTablespace varchar2(200 byte) not null,
temporaryTablespace varchar2(200 byte) not null,
time_stamp timestamp not null,
database_id number not null,
constraint user_pk primary key(id_user),
constraint user_fk foreign key(database_id) references database_db(id_database)on delete cascade
);


-- TABLE SESSIONS
CREATE TABLE session_db(
id_session number not null,
sid_session number not null,
username varchar2(50 byte),
status varchar2(50 byte) not null,
session_type varchar2(50 byte) not null,
logon_time timestamp not null,
schemaname varchar2(50 byte) not null,
database_id number not null,
time_stamp timestamp not null,
constraint session_pk primary key(id_session),
constraint session_fk foreign key(database_id) references database_db(id_database)on delete cascade
);


-- TABLE TABLESPACE_BD
CREATE TABLE tablespace_db(
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
constraint tablespace_pk primary key(id_tablespace),
constraint tablespace_fk1 foreign key(database_id) references database_db(id_database) on delete cascade
);


-- TABLE DATA_FILE
CREATE TABLE datafile_db(
id_datafile number not null,
datafile_name varchar2(200 byte) not null,
autoextensible varchar2(3 byte) not null,
used_space number not null,
max_size number not null,
status varchar2(10 byte) not null,
tablespace_id number not null,
time_stamp timestamp not null,
constraint data_file_pk primary key(id_datafile),
constraint data_file_fk foreign key(tablespace_id) references tablespace_db(id_tablespace) on delete cascade
);



