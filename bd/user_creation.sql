create user grupoth identified by grupoth
default tablespace aebd_tables_trabalho
temporary tablespace aebd_temp_trabalho
quota unlimited on aebd_tables_trabalho
account unlock;

grant resource to grupoth;
grant connect to grupoth;