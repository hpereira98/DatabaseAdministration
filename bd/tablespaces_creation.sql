create tablespace aebd_tables_trabalho
datafile '\u01\app\oracle\oradata\orcl12\orcl\aebd_tables_trabalho_01.dbf'
size 500M;

create temporary tablespace aebd_temp_trabalho
tempfile '\u01\app\oracle\oradata\orcl12\orcl\aebd_temp_trabalho_02.dbf'
size 250M;

--select * from dba_tablespaces;
