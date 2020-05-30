create sequence memory_id start with 1;
create sequence database_id start with 1;
create sequence tablespace_id start with 1;
create sequence datafile_id start with 1;
create sequence user_id start with 1;
create sequence session_id start with 1;


-- MEMORY_ID
create or replace trigger memoryId_trigger
before insert on memory_db
for each row
begin
    select memory_id.nextval
    into :new.id_memory
    from dual;
end memoryId_trigger;

-- DATABASE_ID
create or replace trigger databaseId_trigger
before insert on database_db
for each row
begin
    select database_id.nextval
    into :new.id_database
    from dual;
end databaseId_trigger;

-- DATAFILE_ID
create or replace trigger datafileId_trigger
before insert on datafile_db
for each row
begin
    select datafile_id.nextval
    into :new.id_datafile
    from dual;
end datafileId_trigger;

-- USER ID
create or replace trigger userId_trigger
before insert on user_db
for each row
begin
    select user_id.nextval
    into :new.id_user
    from dual;
end userId_trigger;

-- SESSION_ID
create or replace trigger session_trigger
before insert on session_db
for each row
begin
    select session_id.nextval
    into :new.id_session
    from dual;
end session_trigger;

-- TABLESPACE_ID
create or replace trigger tablespaceId_trigger
before insert on tablespace_db
for each row
begin
    select tablespace_id.nextval
    into :new.id_tablespace
    from dual;
end tablespaceId_trigger;
