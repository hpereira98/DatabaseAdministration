import time

import cx_Oracle
import schedule as schedule

USERNAME = 'grupoth'
PASSWORD = "grupoth"

USERNAMESYSTEM = 'system'
PASSWORDSYSTEM = 'oracle'

global connectionPDB  # SYSTEM -> PDB
global connectionTH  # GRUPOTH -> PDB
global connectionCDB  # SYS -> CDB


def establishing_connection():
    global connectionTH
    connectionTH = cx_Oracle.connect(USERNAME, PASSWORD, "127.0.0.1/orcl", encoding="UTF-8")
    # PDB
    global connectionPDB
    connectionPDB = cx_Oracle.connect(USERNAMESYSTEM, PASSWORDSYSTEM, "127.0.0.1/orcl", encoding="UTF-8")
    # CDB
    global connectionCDB
    connectionCDB = cx_Oracle.connect(USERNAMESYSTEM, PASSWORDSYSTEM, "localhost/orcl12c")


# DATABASE_DB -------------------------------------------------------------------

def db_insert(database_name, version, platform_name, host_name, up_time):
    cursorTH = connectionTH.cursor()
    new_id = cursorTH.var(cx_Oracle.NUMBER)
    insertQ = "insert into database_db(database_name,version,platform_name,host_name,up_time,time_stamp) " \
              "values (:2, :3, :4, :5, :6, CURRENT_TIMESTAMP)" \
              "returning id_database into :7"
    cursorTH.execute(insertQ, (database_name, version, platform_name, host_name, up_time, new_id))
    connectionTH.commit()
    cursorTH.close()

    return new_id.getvalue()[0]


def db_update(database_name, version, platform_name, host_name, up_time):
    cursorTH = connectionTH.cursor()
    new_id = cursorTH.var(cx_Oracle.NUMBER)
    updateQ = "update database_db set database_name = :1, version = :2, platform_name = :3, host_name = :4, " \
              "up_time = :5, time_stamp = CURRENT_TIMESTAMP WHERE database_name = :7" \
              "returning id_database into :8"
    cursorTH.execute(updateQ, (database_name, version, platform_name, host_name, up_time, database_name, new_id))

    if cursorTH.rowcount == 0:
        insertQ = "insert into database_db(database_name,version,platform_name,host_name,up_time,time_stamp) " \
                  "values (:2, :3, :4, :5, :6, CURRENT_TIMESTAMP)" \
                  "returning id_database into :7"
        cursorTH.execute(insertQ, (database_name, version, platform_name, host_name, up_time, new_id))

    connectionTH.commit()
    cursorTH.close()

    return new_id.getvalue()[0]


def update_db():
    cursorPDB = connectionPDB.cursor()
    selectQ = 'select instance_name, REGEXP_SUBSTR((CURRENT_TIMESTAMP - startup_time)*24*60,\'[^ ]+\' ) UP_TIME, ' \
              '( select platform_name from v$database),(select name from v$database) , host_name, version  from ' \
              'v$instance '
    cursorPDB.execute(selectQ)
    results = cursorPDB.fetchone()
    cursorPDB.close()

    instance_name = results[0]
    up_time = results[1]
    host_name = results[4]
    version = results[5]
    platform_name = results[2]
    database_name = results[3]

    return db_update(database_name, version, platform_name, host_name, up_time)


# SESSION_DB ------------------------------------------------------------------------
def session_insert(sid, username, status, session_type, logon_time, schemaname, database_id):
    cursorTH = connectionTH.cursor()
    insertQ = "insert into session_db(sid_session,username,status,session_type,logon_time,schemaname,database_id, time_stamp) " \
              "values (:1,:2, :3, :4, :5, :6, :7, CURRENT_TIMESTAMP) "

    cursorTH.execute(insertQ, (sid, username, status, session_type, logon_time, schemaname, database_id))
    connectionTH.commit()
    cursorTH.close()


def session_update(sid, username, status, session_type, logon_time, schemaname, database_id):
    cursorTH = connectionTH.cursor()
    updateQ = "update session_db set sid_session = :1, username = :2, status = :3, session_type = :4, logon_time = :5," \
              "schemaname = :6, database_id = :7, time_stamp = CURRENT_TIMESTAMP WHERE sid_session = :8"
    cursorTH.execute(updateQ, (sid, username, status, session_type, logon_time, schemaname, database_id, sid))

    if cursorTH.rowcount == 0:
        insertQ = "insert into session_db(sid_session,username,status,session_type,logon_time,schemaname,database_id, " \
                  "time_stamp) values (:1,:2, :3, :4, :5, :6, :7, CURRENT_TIMESTAMP) "

        cursorTH.execute(insertQ, (sid, username, status, session_type, logon_time, schemaname, database_id))

    connectionTH.commit()
    cursorTH.close()


def update_session(id_database):
    cursorPDB = connectionPDB.cursor()
    selectQ = 'select v.sid, v.username, v.status, v.type, v.logon_time, v.schemaname from v$session v'
    cursorPDB.execute(selectQ)
    results = cursorPDB.fetchall()
    cursorPDB.close

    for result in results:
        sid = result[0]
        username = result[1]
        if username is None:
            username = None
        status = result[2]
        type = result[3]
        logon_time = result[4]
        schemaname = result[5]

        session_update(sid, username, status, type, logon_time, schemaname, id_database)


# MEMORY_DB -----------------------------------------------------------------------------------

def memory_insert(total_ram, memory_used, used_ram, free_ram, cpu_count, cpu_socket_count, cpu_core_count, id_database):
    cursor = connectionTH.cursor()
    insertStatment = "insert into memory_db(total_ram,memory_used,ram_used,free_ram,cpu_count,cpu_socket_count, cpu_core_count," \
                     "database_id,time_stamp)" \
                     "values (:2, :3, :4, :5, :6, :7, :8,:9, CURRENT_TIMESTAMP)"
    cursor.execute(insertStatment, (
    total_ram, memory_used, used_ram, free_ram, cpu_count, cpu_socket_count, cpu_core_count, id_database))
    connectionTH.commit()
    cursor.close()


def memory(id_database):
    cursorCDB = connectionCDB.cursor()
    selectQ = "select cpu_count, cpu_core_count, cpu_socket_count, ( select round(sum(bytes)/1024/1024,2) from v$sgastat where name = " \
              "\'free memory\' ) FREE_MEMORY,(select round(sum(bytes)/1024/1024,2) from dba_data_files) MEMORY_USED ," \
              "(select round(sum(value)/1024/1024,2) from v$sga) TOTAL_RAM from dba_cpu_usage_statistics where dbid = " \
              "776972821 "
    cursorCDB.execute(selectQ)
    results = cursorCDB.fetchone()
    cursorCDB.close()

    cpu_count = results[0]
    cpu_core_count = results[1]
    cpu_socket_count = results[2]
    free_ram = results[3]
    total_ram = results[5]
    used_ram = total_ram - free_ram
    memory_used = results[4]

    memory_insert(total_ram, memory_used, used_ram, free_ram, cpu_count, cpu_socket_count, cpu_core_count, id_database)


# TABLESPACE_DB ------------------------------------------------------------------------------------------------------------------------------------

def tablespace_insert(cursorTH, tablespace_name, status, max_size, used_size, space_allocated, free_space,
                      tablespace_type, id_database):
    insertQ = "insert into tablespace_db (tablespace_name, status, max_size, used_space, space_allocated, " \
              "free_space, tablespace_type,database_id, time_stamp)" \
              "values (:2, :3, :4, :5, :6, :7, :8, :9, CURRENT_TIMESTAMP)"
    cursorTH.execute(insertQ,
                     (tablespace_name, status, max_size, used_size, space_allocated, free_space, tablespace_type,
                      id_database))
    connectionTH.commit()


def tablespace_update(cursorTH, tablespace_name, status, max_size, used_size, space_allocated, free_space,
                      tablespace_type, id_database):
    updateQ = "update tablespace_db set tablespace_name = :0, status = :1, max_size = :2, used_space = :3, " \
              "space_allocated = :4, free_space = :5, tablespace_type = :6, database_id = :7, time_stamp = " \
              "CURRENT_TIMESTAMP WHERE tablespace_name = :8 "
    cursorTH.execute(updateQ, (
        tablespace_name, status, max_size, used_size, space_allocated, free_space, tablespace_type, id_database,
        tablespace_name))


def update_tablespace(id_database):
    cursorPDB = connectionPDB.cursor()
    selectQ1 = "select tablespace_name, status, contents, round(max_size/1024/1024,2)  from dba_tablespaces"
    cursorPDB.execute(selectQ1)
    rows = cursorPDB.fetchall()

    cursorTH = connectionTH.cursor()

    for row in rows:
        tablespace_name = row[0]
        status = row[1]
        tablespace_type = row[2]
        max_size = row[3]

        if tablespace_type == "TEMPORARY":
            selectQ2 = "select round(bytes_free/1024/1024,2), round(bytes_used/1024/1024,2) from V$temp_space_header " \
                       "where tablespace_name = :1 "
            cursorPDB.execute(selectQ2, (tablespace_name,))
            result = cursorPDB.fetchall()
            free_space = result[0][0]
            used_size = result[0][0]
            space_allocated = round(float(free_space) + float(used_size), 2)

        else:
            selectQ2 = 'select round(sum(bytes)/1024/1024 ,2) FREE_SPACE, (select round(sum(bytes)/1024/1024,' \
                       '2) from dba_data_files where tablespace_name = :1 group by tablespace_name) SPACE_ALLOCATED ' \
                       'from dba_free_space where tablespace_name = :2 group by tablespace_name '
            cursorPDB.execute(selectQ2, (tablespace_name, tablespace_name))
            result = cursorPDB.fetchall()
            free_space = result[0][0]
            space_allocated = result[0][1]  # aka total_space
            used_size = round(float(space_allocated) - float(free_space), 2)

        tablespace_update(cursorTH, tablespace_name, status, max_size, used_size, space_allocated, free_space,
                          tablespace_type, id_database)
        if cursorTH.rowcount == 0:
            tablespace_insert(cursorTH, tablespace_name, status, max_size, used_size, space_allocated, free_space,
                              tablespace_type, id_database)
    connectionTH.commit()
    cursorTH.close()
    cursorPDB.close()


# USERS_DB ------------------------------------------------------------------------------------------------------------------------


def users_insert(cursorTH, username, account_status, last_login, creation_date, defTablespace, tempTablespace,
                 database_id):
    insertQ = "insert into user_db(username, account_status, last_login, creation_date, defaulttablespace, " \
              "temporarytablespace, database_id, time_stamp )" \
              "values (:2, :3, :4, :5, :6, :7,:8, CURRENT_TIMESTAMP)"
    cursorTH.execute(insertQ,
                     (username, account_status, last_login, creation_date, defTablespace, tempTablespace, database_id))


def users_update(cursorTH, username, account_status, last_login, creation_date, defTablespace, tempTablespace,
                 database_id):
    updateQ = "update user_db set username = :1, account_status = :2, last_login = :3, " \
              "creation_date = :4, defaulttablespace = :5, temporarytablespace = :6, time_stamp = " \
              "CURRENT_TIMESTAMP, database_id = :6  where username = :7 "
    cursorTH.execute(updateQ, (
        username, account_status, last_login, creation_date, defTablespace, tempTablespace, database_id, username))


def update_users(database_id):
    cursorPDB = connectionPDB.cursor()
    cursorTH = connectionTH.cursor()
    selectQ1 = "select username, account_status, created, default_tablespace, temporary_tablespace, last_login from " \
               "dba_users "
    cursorPDB.execute(selectQ1)
    rows = cursorPDB.fetchall()
    cursorPDB.close()

    for row in rows:
        username = row[0]
        account_status = row[1]
        creation_date = row[2]
        defTablespace = row[3]
        temTablespace = row[4]
        last_login = row[5]

        if last_login is None:
            last_login = None

        users_update(cursorTH, username, account_status, last_login, creation_date, defTablespace, temTablespace,
                     database_id)

        if cursorTH.rowcount == 0:
            users_insert(cursorTH, username, account_status, last_login, creation_date, defTablespace,
                         temTablespace, database_id)
    connectionTH.commit()
    cursorTH.close()


# DATAFILE_DB ---------------------------------------------------------------------------------------------------------------


def datafile_insert(cursorTH, datafile_name, auto_extensible, max_size, used_space, status, tablespace_id):
    insertQ = "insert into datafile_db (datafile_name, autoextensible, max_size, used_space, status, " \
              "tablespace_id, time_stamp)" \
              "values (:2, :3, :4, :5, :6, :7, CURRENT_TIMESTAMP)"
    cursorTH.execute(insertQ, (datafile_name, auto_extensible, max_size, used_space, status, tablespace_id))


def datafiles_update(cursorTH, datafile_name, auto_extensible, max_size, used_space, status, tablespace_id):
    updateQ = "update datafile_db set datafile_name = :1, autoextensible = :2, max_size = :3, used_space = :4, " \
              "status = :5, tablespace_id = :6, time_stamp = CURRENT_TIMESTAMP where datafile_name = :7"
    cursorTH.execute(updateQ,
                     (datafile_name, auto_extensible, max_size, used_space, status, tablespace_id, datafile_name))


def update_datafiles():
    cursorPDB = connectionPDB.cursor()
    selectQ1 = "select file_name, tablespace_name, round(bytes/1024/1024,2), status, autoextensible, " \
               "round(maxbytes/1024/1024,2)" \
               "from dba_data_files"
    cursorPDB.execute(selectQ1)
    rows = cursorPDB.fetchall()
    cursorPDB.close()

    cursorTH = connectionTH.cursor()
    for row in rows:
        datafile_name = row[0]
        tablespace_name = row[1]
        statment2 = "select id_tablespace from tablespace_db where tablespace_name = :1"
        cursorTH.execute(statment2, (tablespace_name,))
        tablespace_id = cursorTH.fetchall()[0][0]
        used_space = row[2]
        status = row[3]
        auto_extensible = row[4]
        max_size = row[5]

        datafiles_update(cursorTH, datafile_name, auto_extensible, max_size, used_space, status, tablespace_id)

        if cursorTH.rowcount == 0:
            datafile_insert(cursorTH, datafile_name, auto_extensible, max_size, used_space, status, tablespace_id)

    connectionTH.commit()
    cursorTH.close()


# UPDATE_DB
def update():
    print("UPDATING")
    database_id = update_db()
    memory(database_id)
    update_tablespace(database_id)
    update_users(database_id)
    update_session(database_id)
    update_datafiles()


if __name__ == '__main__':
    establishing_connection()
    update()

    schedule.every(10).seconds.do(update)
    while True:
        schedule.run_pending()
        time.sleep(1)
