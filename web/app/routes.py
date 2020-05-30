from app import app
from flask import render_template
import requests
import json




@app.route('/')
@app.route('/index')
def index():
    # DATABASE_DB
    r = requests.get('http://localhost:8082/ords/grupoth/database_info/')
    data = json.loads(r.text)

    r2 = requests.get('http://localhost:8082/ords/grupoth/ram_usage/')
    ram_usage = json.loads(r2.text)

    r3 = requests.get('http://localhost:8082/ords/grupoth/cpu_count/')
    cpu_usage = json.loads(r3.text)

    r4 = requests.get('http://localhost:8082/ords/grupoth/count_tablespaces/')
    tablespaces = json.loads(r4.text)

    r5 = requests.get('http://localhost:8082/ords/grupoth/user_count/')
    users = json.loads(r5.text)

    r6 = requests.get('http://localhost:8082/ords/grupoth/count_datafiles/')
    datafiles = json.loads(r6.text)

    r7 = requests.get('http://localhost:8082/ords/grupoth/session_count/')
    sessions = json.loads(r7.text)

    r8 = requests.get('http://localhost:8082/ords/grupoth/inactive_count/')
    inactive = json.loads(r8.text)

    r9 = requests.get('http://localhost:8082/ords/grupoth/active_count/')
    active = json.loads(r9.text)

    r10 = requests.get('http://localhost:8082/ords/grupoth/undotables/')
    undoTables = json.loads(r10.text)

    r11 = requests.get('http://localhost:8082/ords/grupoth/temptables/')
    tempTables = json.loads(r11.text)

    r12 = requests.get('http://localhost:8082/ords/grupoth/permtables/')
    permTables = json.loads(r12.text)

    return render_template('index.html', database=data['items'], ram_usage=ram_usage['items'], legend1 = 'Total RAM (MB)',
                           legend2 = 'Free RAM (MB)', legend3 = 'RAM Used (MB)', cpu_usage = cpu_usage['items'], tablespaces = tablespaces['items'], sessions = sessions['items'],
                           datafiles = datafiles['items'], users = users['items'], active = active['items'], inactive = inactive['items'], undoTables = undoTables['items'],
                           permTables = permTables['items'], tempTables = tempTables['items'])


@app.route('/tablespaces')
def tablespaces():
    r = requests.get('http://localhost:8082/ords/grupoth/tablespace_info/?limit=500')
    tablespaces = json.loads(r.text)

    r2 = requests.get('http://localhost:8082/ords/grupoth/count_tablespaces/')
    countTablespaces = json.loads(r2.text)

    r3 = requests.get('http://localhost:8082/ords/grupoth/total_space_used/')
    space_used = json.loads(r3.text)

    return render_template('tablespaces.html', tablespaces=tablespaces['items'],
                           countTablespaces=countTablespaces['items'], space_used=space_used['items'])


@app.route('/users')
def users():
    r = requests.get('http://localhost:8082/ords/grupoth/username_info/?limit=500')
    users = json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/user_count/')
    user_count = json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/status_el/')
    expLocke = json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/status_expired/')
    expired= json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/status_locked/')
    locked = json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/status_open/')
    open = json.loads(r.text)

    return render_template('users.html', users=users['items'], userCount=user_count['items'], expLocke = expLocke['items'],
                           expired = expired['items'], locked = locked['items'], open = open['items'])


@app.route('/datafiles')
def datafiles():
    r = requests.get('http://localhost:8082/ords/grupoth/datafiles_info/?limit=500')
    datafiles = json.loads(r.text)

    r2 = requests.get('http://localhost:8082/ords/grupoth/count_datafiles/')
    countDatafiles = json.loads(r2.text)

    r3 = requests.get('http://localhost:8082/ords/grupoth/totalspace_used/')
    space_used = json.loads(r3.text)

    return render_template('datafiles.html', datafiles=datafiles['items'], countDatafiles=countDatafiles['items'],
                           space_used=space_used['items'])

@app.route('/sessions')
def sessions():
    r = requests.get('http://localhost:8082/ords/grupoth/session_info/?limit=500')
    sessions = json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/session_count/')
    countSessions = json.loads(r.text)

    r = requests.get('http://localhost:8082/ords/grupoth/background_count/')
    backgroundS = json.loads(r.text)

    return render_template('session.html', sessions = sessions['items'], countSessions = countSessions['items'], backgroundS = backgroundS['items'])
