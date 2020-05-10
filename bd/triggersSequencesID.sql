create sequence status_id start with 1;
create sequence database_id start with 1;
create sequence datafile_id start with 1;
create sequence user_id start with 1;
create sequence tablespace_id start with 1;

-- STATUS_ID
create or replace trigger status_id_trigger
before insert on status
for each row
begin
    select status_id.nextval
    into :new.id_status
    from dual;
end status_id_trigger;

-- DATABASE_ID
create or replace trigger data_base_id_trigger
before insert on data_base
for each row
begin
    select database_id.nextval
    into :new.id_database
    from dual;
end data_base_id_trigger;

-- DATAFILE_ID
create or replace trigger data_file_id_trigger
before insert on data_file
for each row
begin
    select datafile_id.nextval
    into :new.id_datafile
    from dual;
end data_file_id_trigger;

-- USER ID
create or replace trigger user_id_trigger
before insert on user_db
for each row
begin
    select user_id.nextval
    into :new.id_useruser_id_trigger
    from dual;
end user_id_trigger;

-- TABLESPACE
create or replace trigger tablespace_id_trigger
before insert on tablespace_bd
for each row
begin
    select tablespace_id.nextval
    into :new.id_tablespace
    from dual;
end tablespace_id_trigger;
