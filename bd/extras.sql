-- SESSION
-- PDB
select * from v$session;

-- PDB
select * from v$database;
-- PDB
select * from v$instance;

select instance_name from v$instance;

-- CDB
select * from dba_cpu_usage_statistics;

-- TABLESPACES
select * from dba_tablespaces
order by tablespace_name ASC;

select bytes_used

select * from V$temp_space_header;

select round(bytes_free/1024/1024,2) as FREE_BYTES from V$temp_space_header;

select * from dba_free_space;

select * from dba_data_files;

select * from dba_segments;

select tablespace_name, round(max_size/1024/1024,2) from dba_tablespaces;

-- 
select b.tablespace_name, tbs_size , a.free_space 

from  (select tablespace_name, round(sum(bytes)/1024/1024 ,2) as free_space

       from dba_free_space

       group by tablespace_name) a,

      (select tablespace_name, sum(bytes)/1024/1024 as tbs_size

       from dba_data_files

       group by tablespace_name) b
       
where a.tablespace_name(+)=b.tablespace_name
order by tablespace_name ASC;

-- FreeSize size
select tablespace_name, sum(bytes) as BYTES from dba_free_space
group by tablespace_name;


select startup_time from v$instance;

select instance_name, REGEXP_SUBSTR((CURRENT_TIMESTAMP - startup_time)*24*60,'[^ ]+' ), host_name, version  from v$instance;
-- 
select * from dba_data_files;


-- USER

select * from v$sga;
select sum(value) from v$sga;

select * from v$session;

select * from v$sgastat
where name = 't';