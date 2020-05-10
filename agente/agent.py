import cx_Oracle

USERNAME = 'grupoth'
PASSWORD = "grupoth"

USERNAMES = 'system'
PASSWORDS = 'oracle'

USERNAMESYS = 'system'
PASSWORDSYS = 'oracle'
global connectionSystem     #SYSTEM -> PDB
global connectionTH         #GRUPOTH -> PDB
global connectionSys        # SYS -> CDB


# TODO : SYSTEM -> BD
# TODO : SCHEDULING TIME TO DO IT
# TODO : UPDATES X EM X TIME
def establishing_connection():
    global connectionTH
    connectionTH = cx_Oracle.connect(USERNAME, PASSWORD, "127.0.0.1/orcl", encoding="UTF-8")
    global connectionSystem
    connectionSystem = cx_Oracle.connect(USERNAMES, PASSWORDS, "127.0.0.1/orcl", encoding="UTF-8")          # PDB
    global connectionSys
    connectionSys = cx_Oracle.connect(USERNAMESYS, PASSWORDSYS, "localhost/orcl12c")   # CDB


def db():
    statment = 'select instance_name, startup_time, host_name, version  from v$instance'
    statmen2 = 'select platform_name, name from v$database'
    cursor = connectionSystem.cursor()
    cursor.execute(statment)
    row = cursor.fetchone()
    cursor.execute(statmen2)
    row2 = cursor.fetchone()
    cursor.close()

    # Instance_name
    instance_name = row[0]
    print(f"Instance_name = {instance_name}")
    # Up_time
    up_time = row[1]
    print(f"Up_time = {up_time}")
    # Host_name
    host_name = row[2]
    print(f"Host_name = {host_name}")
    # Version
    version = row[3]
    print(f"Version = {version}")
    # Plataform_Name
    plataform_name = row2[0]
    print(f"Plataform_Name{plataform_name}")
    # Database_name
    database_name = row2[1]
    print(f"Database_name = {database_name}")

    # TODO: UP_TIME
    # Insert into data_base
    insert = "insert into data_base(database_name,version,plataform,host_name,up_time,time_stamp) values (:2, :3, :4, :5, :6, CURRENT_TIMESTAMP)"
    cursor = connectionTH.cursor()
    cursor.execute(insert, (database_name, version, plataform_name, host_name, 10))
    connectionTH.commit()
    cursor.close()
    # save id from table database


def status():
    cursor = connectionSys.cursor()
    statment1 = "select cpu_count, cpu_core_count from dba_cpu_usage_statistics"
    cursor.execute(statment1)
    rows = cursor.fetchall()
    # cursor.close()
    for row in rows:
        # cpu_count
        cpu_count = row[0]
        print(f"CPU_COUNT = {cpu_count}")
        # cpu_core_count
        cpu_core_count = row[1]
        print(f"CPU_CORE_COUNT = {cpu_core_count}")
    # used_ram
    statment2 = "select sum(bytes) from v$sgastat where name = \'free memory\' "
    cursor.execute(statment2)
    row = cursor.fetchall()
    free_ram = row[0][0]            # bytes -> Mb?
    print(f"Free_ram = {row[0][0]}")

    # total_ram
    statment3 = "select sum(value) from v$sga"
    cursor.execute(statment3)
    result = cursor.fetchall()
    total_ram = result[0][0]
    print(f'Total_ram = {total_ram}')
    # memory_used
    # ram_used
    # id_database
    # timestamp




if __name__ == '__main__':
    establishing_connection()
    status()
    #db()
