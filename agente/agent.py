import time

import cx_Oracle
import schedule as schedule

USERNAME = 'grupoth'
PASSWORD = "grupoth"

USERNAMESYSTEM = 'system'
PASSWORDSYSTEM = 'oracle'

global connectionPDB        # SYSTEM -> PDB
global connectionTH         # GRUPOTH -> PDB
global connectionCDB        # SYS -> CDB


# TODO : SYSTEM -> BD
# TODO : SCHEDULING TIME TO DO IT
def establishing_connection():
    global connectionTH
    connectionTH = cx_Oracle.connect(USERNAME, PASSWORD, "127.0.0.1/orcl", encoding="UTF-8")
    # PDB
    global connectionPDB
    connectionPDB = cx_Oracle.connect(USERNAMESYSTEM, PASSWORDSYSTEM, "127.0.0.1/orcl", encoding="UTF-8")
    # CDB
    global connectionCDB
    connectionCDB = cx_Oracle.connect(USERNAMESYSTEM, PASSWORDSYSTEM, "localhost/orcl12c")


# TODO: UP_TIME
def db():
    cursor = connectionPDB.cursor()
    statment = 'select instance_name, startup_time, host_name, version  from v$instance'
    cursor.execute(statment)
    results1 = cursor.fetchone()

    statment2 = 'select platform_name, name from v$database'
    cursor.execute(statment2)
    results2 = cursor.fetchone()
    cursor.close()

    instance_name = results1[0]
    up_time = results1[1]
    host_name = results1[2]
    version = results1[3]
    plataform_name = results2[0]
    database_name = results2[1]

    cursor = connectionTH.cursor()
    new_id = cursor.var(cx_Oracle.NUMBER)
    insert = "insert into data_base(database_name,version,plataform,host_name,up_time,time_stamp) " \
             "values (:2, :3, :4, :5, :6, CURRENT_TIMESTAMP)" \
             "returning id_database into :7"
    cursor.execute(insert, (database_name, version, plataform_name, host_name, 10, new_id))

    new_id2 = new_id.getvalue()
    database_id = int(new_id2[0])

    connectionTH.commit()
    cursor.close()

    return database_id


def status(id_database):
    cursor = connectionCDB.cursor()
    statment1 = "select cpu_count, cpu_core_count from dba_cpu_usage_statistics"
    cursor.execute(statment1)
    rows = cursor.fetchall()

    for row in rows:
        cpu_count = row[0]
        cpu_core_count = row[1]

    statment2 = "select round(sum(bytes)/1024/1024,2) from v$sgastat where name = \'free memory\' "
    cursor.execute(statment2)
    row = cursor.fetchall()
    free_ram = row[0][0]

    statment3 = "select sum(value) from v$sga"
    cursor.execute(statment3)
    result = cursor.fetchall()
    total_ram = result[0][0]

    used_ram = total_ram - free_ram

    statment4 = "select sum(bytes) from dba_data_files"
    cursor.execute(statment4)
    result = cursor.fetchall()
    memory_used = result[0][0]

    cursor.close()


    cursor = connectionTH.cursor()
    insertStatment = "insert into status(total_ram,memory_used,ram_used,free_ram,cpu_count,cpu_core_count,database_id,time_stamp)" \
                     "values (:2, :3, :4, :5, :6, :7, :8, CURRENT_TIMESTAMP)"
    cursor.execute(insertStatment, (total_ram, memory_used, used_ram, free_ram, cpu_count,cpu_core_count,id_database))
    connectionTH.commit()
    cursor.close()


def tablespace(id_database):
    cursor = connectionPDB.cursor()
    statment = "select tablespace_name, status, contents, round(max_size/1024/1024,2)  from dba_tablespaces"
    cursor.execute(statment)
    rows = cursor.fetchall()

    cursorDB = connectionTH.cursor()

    for row in rows:
        tablespace_name = row[0]
        status = row[1]
        type = row[2]
        max_size = row[3]

        if type == "TEMPORARY":
            statment2 = "select round(bytes_free/1024/1024,2), round(bytes_used/1024/1024,2) from V$temp_space_header where tablespace_name = :1"
            cursor.execute(statment2, (tablespace_name,))
            result = cursor.fetchall()

            free_space = result[0][0]
            used_size = result[0][1]
            space_allocated = round(float(free_space) + float(used_size),2)

            max_ts_size_pc = (used_size / float(max_size)) * 100

        else:
            statment2 = "select round(sum(bytes)/1024/1024 ,2) from dba_free_space where tablespace_name = :1" \
                        "group by tablespace_name"
            cursor.execute(statment2, (tablespace_name, ))
            result = cursor.fetchall()

            free_space = result[0][0]

            statment2 = "select round(sum(bytes)/1024/1024,2) from dba_data_files where tablespace_name = :1" \
                        "group by tablespace_name"
            cursor.execute(statment2, (tablespace_name,))
            result = cursor.fetchall()

            space_allocated = result[0][0]       #aka total_space
            used_size = round(float(space_allocated) - float(free_space),2)

            # percentagem de uso sobre o tamanho total
            max_ts_size_pc = (used_size / float(max_size)) * 100

        insertStatment = "insert into tablespace_db (tablespace_name, status, max_size, used_space, space_allocated, free_space, tablespace_type,database_id, time_stamp)" \
                         "values (:2, :3, :4, :5, :6, :7, :8, :9, CURRENT_TIMESTAMP)"
        cursorDB.execute(insertStatment, (tablespace_name, status, max_size, used_size, space_allocated, free_space, type,id_database))
        connectionTH.commit()

    cursor.close()
    cursorDB.close()


def users():
    cursor = connectionPDB.cursor()
    cursorBD = connectionTH.cursor()
    statment = "select username, account_status, created, default_tablespace, temporary_tablespace, last_login from dba_users"
    cursor.execute(statment)
    rows = cursor.fetchall()

    for row in rows:
        username = row[0]
        account_status = row[1]
        creation_date = row[2]
        defTablespace_name = row[3]

        statment = "select id_tablespace from tablespace_db where tablespace_name = :1"
        cursorBD.execute(statment, (defTablespace_name, ))
        result = cursorBD.fetchall()
        defTablespace_id = result[0][0]

        temTablespace_name = row[4]
        statment = "select id_tablespace from tablespace_db  where tablespace_name = :1"
        cursorBD.execute(statment, (temTablespace_name,))
        result = cursorBD.fetchall()
        tempTablespace_id = result[0][0]
        last_login = row[5]

        if last_login is None:
            last_login = None

        insertStatment = "insert into user_db(username, account_status, last_login, creation_date, defaulttablespace_id, temporarytablespace_id, time_stamp )" \
                         "values (:2, :3, :4, :5, :6, :7, CURRENT_TIMESTAMP)"
        cursorBD.execute(insertStatment,(username, account_status, last_login, creation_date, defTablespace_id, tempTablespace_id))
        connectionTH.commit()

    cursor.close()
    cursorBD.close()


def datafiles():

    cursor = connectionPDB.cursor()
    statment = "select file_name, tablespace_name, round(bytes/1024/1024,2), status, autoextensible, round(maxbytes/1024/1024,2)" \
               "from dba_data_files"
    cursor.execute(statment)
    rows = cursor.fetchall()
    cursor.close()

    cursorDB = connectionTH.cursor()
    for row in rows:
        datafile_name = row[0]
        tablespace_name = row[1]
        statment2 = "select id_tablespace from tablespace_db where tablespace_name = :1"
        cursorDB.execute(statment2, (tablespace_name, ))
        tablespace_id = cursorDB.fetchall()[0][0]
        print(f"TABLESPACE_ID = {tablespace_id}")
        total_size = row[2]
        status = row[3]
        auto_extensible = row[4]
        max_size = row[5]

        insertStatment = "insert into data_file (datafile_name, autoextensible, max_size, total_size, status, tablespace_id, time_stamp)" \
                         "values (:2, :3, :4, :5, :6, :7, CURRENT_TIMESTAMP)"
        cursorDB.execute(insertStatment,(datafile_name, auto_extensible, max_size, total_size, status, tablespace_id))
        connectionTH.commit()

    cursorDB.close()


def initial_load():
    database_id = db()
    status(database_id)
    tablespace(database_id)
    users()
    datafiles()


def test():
    print("I'm a test!")


if __name__ == '__main__':
    #establishing_connection()
    #initial_load()
    schedule.every(10).seconds.do(test)
    while True:
        schedule.run_pending()
        time.sleep(1)