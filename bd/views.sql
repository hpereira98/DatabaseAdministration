-- DATABASE_BD
CREATE OR REPLACE VIEW database_info AS
SELECT INITCAP(database_name) DATABASE_NAME, INITCAP(version) VERSION,INITCAP(platform_name) PLATFORM_NAME, INITCAP(host_name) HOST_NAME, up_time FROM grupoth.database_db;


-- DB_MEMORY
CREATE OR REPLACE VIEW cpu_count AS
SELECT cpu_count, cpu_core_count,cpu_socket_count, to_char(time_stamp, 'HH24:MI:SS') TIME
FROM memory_db;


CREATE OR REPLACE VIEW ram_usage AS
SELECT total_ram, free_ram, ram_used,  to_char(time_stamp, 'HH24:MI:SS') TIME
FROM memory_db;


-- TABLESPACE_DB
CREATE OR REPLACE VIEW tablespace_info AS
SELECT INITCAP(tablespace_name) tablespace_name, INITCAP(status) status, INITCAP(tablespace_type) tablespace_type, max_size,space_allocated, used_space, free_space
FROM tablespace_db;

CREATE OR REPLACE VIEW count_tablespaces AS
SELECT COUNT(ID_TABLESPACE) TOTAL
FROM tablespace_db;

CREATE OR REPLACE VIEW total_space_used AS
SELECT ROUND(SUM(used_space),2) TOTAL_SPACE_USED
FROM tablespace_db;

CREATE OR REPLACE VIEW permTables AS
SELECT COUNT(id_tablespace) TOTAL
FROM tablespace_db
WHERE tablespace_type = 'PERMANENT';

CREATE OR REPLACE VIEW tempTables AS
SELECT COUNT(id_tablespace) TOTAL
FROM tablespace_db
WHERE tablespace_type = 'TEMPORARY';

CREATE OR REPLACE VIEW undoTables AS
SELECT COUNT(id_tablespace) TOTAL
FROM tablespace_db
WHERE tablespace_type = 'UNDO';

-- DATAFILES_DB
CREATE OR REPLACE VIEW datafiles_info AS
SELECT INITCAP(d.datafile_name) datafile_name, INITCAP(t.tablespace_name) tablespace_name, INITCAP(d.status) status, INITCAP(d.autoextensible) autoextensible, d.max_size, d.used_space
FROM tablespace_db t,  datafile_db d
WHERE t.id_tablespace = d.tablespace_id;

CREATE OR REPLACE VIEW count_datafiles AS
SELECT COUNT(id_datafile) TOTAL
FROM datafile_db;

CREATE OR REPLACE VIEW totalspace_used AS
SELECT ROUND(SUM(used_space),2) TOTAL_SPACE_USED
FROM datafile_db;

-- USERS_DB
CREATE OR REPLACE VIEW username_info AS
SELECT INITCAP(u.username) username, INITCAP(u.account_status) account_status, to_char(u.last_login, 'DD Month YYYY HH24:MI:SS') LAST_LOGIN, to_char(u.creation_date, 'DD MONTH YYYY HH24:MI:SS') CREATION_DATE,
INITCAP(u.temporarytablespace) temporarytablespace, INITCAP(u.defaulttablespace) defaulttablespace
FROM user_db u;

CREATE OR REPLACE VIEW user_count AS
SELECT COUNT(id_user) TOTAL
FROM user_db;

CREATE OR REPLACE VIEW status_locked AS
SELECT  COUNT(account_status) TOTAL
FROM user_db
WHERE account_status = 'LOCKED';

CREATE OR REPLACE VIEW status_open AS
SELECT  COUNT(account_status) TOTAL
FROM user_db
WHERE account_status = 'OPEN';

CREATE OR REPLACE VIEW status_expired AS
SELECT  COUNT(account_status) TOTAL
FROM user_db
WHERE account_status = 'EXPIRED';

CREATE OR REPLACE VIEW status_EL AS
SELECT  COUNT(account_status) TOTAL
FROM user_db
WHERE account_status != 'LOCKED' and  account_status != 'OPEN' and account_status != 'EXPIRED';


--SESSION_DB
CREATE OR REPLACE VIEW session_info AS
SELECT sid_session, INITCAP(username) username, INITCAP(status) status, INITCAP(session_type) session_type, to_char(logon_time,'DD MONTH YYYY HH24:MI:SS') LOGON_TIME, INITCAP(schemaname) schemaname
FROM session_db ;

CREATE OR REPLACE VIEW sessions_status AS
SELECT session_type 
FROM session_db
WHERE session_type = 'BACKGROUND';

CREATE OR REPLACE VIEW session_count AS
SELECT COUNT(id_session) TOTAL
FROM session_db;

CREATE OR REPLACE VIEW inactive_count AS
SELECT COUNT(id_session) TOTAL
FROM session_db
WHERE status = 'INACTIVE';

CREATE OR REPLACE VIEW active_count AS
SELECT COUNT(id_session) TOTAL
FROM session_db
WHERE status = 'ACTIVE';

CREATE OR REPLACE VIEW background_count AS
SELECT COUNT(id_session) TOTAL
FROM session_db
WHERE session_type = 'BACKGROUND';

CREATE OR REPLACE VIEW user_session_count AS
SELECT COUNT(id_session) TOTAL
FROM session_db
WHERE session_type = 'USER';
