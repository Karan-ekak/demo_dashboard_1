# print('Start')
import logging
from flask import Flask, render_template, request, send_file, session, redirect, g, url_for, jsonify
import requests
from datetime import timedelta
from functools import wraps
from flask_caching import Cache
from loguru import logger



import random
import hashlib
from flask_mail import Mail, Message
from database_connection import ArgusDB
import logging



from datetime import datetime, timedelta
import pytz
import pandas as pd
from io import BytesIO

# import logging
# from logging.handlers import RotatingFileHandler
import os
import re
# from sys import getsizeof
import time
import json
from convert_video_format import compare_video_id , check_video_in_static,compare_video_id2 , check_video_in_static2
# from flask_cors import CORS

""" Local Modules """
import authorization
import authentication
from database_connection import ArgusDB
import incident_id_gen
from activity import upload_actitivity
import ist_time_zone as ist
from report_generation import report_generate
import api_request
from download_rendered_video import download_video
import department_sub_department_logic as dept_logic


""" Constant Dict """
from constants import DICT_INCIDENT_DATA,DICT_CAMERA_LIST

from collections import defaultdict
from flask_cors import CORS


""" Google auth modules"""

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_requests
from urllib.parse import urljoin


app = Flask(__name__)
CORS(app)  # Allow CORS for cross-origin access

cache = Cache(app, config={'CACHE_TYPE': 'simple'})






#setting OAUTHLIB insecure transport to 1
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


logger.add("logs/system.log", level="INFO",
           retention="10 days", rotation="100 MB")

app.secret_key = "iU9VOlj2itEAAAAAAAAAAb2U6J8tjz96S7f-6GAaAt6B7SXBgruIHEHkz1jdQFnn"
# app.config['SESSION_COOKIE_SECURE'] = True

# app.config['SESSION_COOKIE_DOMAIN'] = "49.50.87.70"
app.config['SESSION_COOKIE_SECURE'] = False  # Change to True if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'








""" Mail configurations """


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'astha@ekak.in'
app.config['MAIL_PASSWORD'] = 'gsex qmlc scfv zbml'  # App password
app.config['MAIL_DEFAULT_SENDER'] = 'astha@ekak.in'

mail = Mail(app)

""" Decorator Start"""


def login_required(f):
    """Decorator : Checking Email Login Or Not

    Returns:
        If Not Logged in : Redirect to Login Page
        If Logged in : Redirect to that Request Page

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("session.get('email'))", session.get('email'))
        if session.get('email') is None:
            print("User is Not Logged in")
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(func):
    """Decorator : Checking Current User is Admin Or Not 

        Return :
            If User GROUP is 1 : Return to Admin's View Page
            If User Not Logged : Redirect to Admin Page
            If User Logged In But Not Admin : Redirect to Their Dashboard Page

    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session.get('email'), "session.get('email')")
        print(session.get('group'), "session.get('group')")
        if session.get('email') is not None:
            if session.get('group') == 1:
                # print("User Not Login")
                return func(*args, **kwargs)
            return redirect(url_for('login'))
        # print("User is admin login")
        return redirect(url_for('dropsession'))

    # print("Return Decorator Function")
    return decorated_function


def incident_manager_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session.get('email'), "session.get('email')")
        print(session.get('group'), "session.get('group')")
        if session.get('email') is not None:
            if session.get('group') == 3:
                # print("User Not Login")
                return func(*args, **kwargs)

            return redirect(url_for('login'))
        # print("User is admin login")
        return redirect(url_for('dropsession'))

    # print("Return Decorator Function")
    return decorated_function


def department_supervisor_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session.get('email'), "session.get('email')")
        print(session.get('group'), "session.get('group')")
        if session.get('email') is not None:
            if session.get('group') == 2:
                # print("User Not Login")
                return func(*args, **kwargs)

            return redirect(url_for('login'))
        # print("User is admin login")
        return redirect(url_for('dropsession'))

    # print("Return Decorator Function")
    return decorated_function





dict_group_id = {
    1: 'admin',
    2: 'deparment_supervisior',
    3: 'incident_manager'
}

status_true = {
    "status": True
}

status_false = {
    "status": False
}

##############################################################

def time_decoration(time_val):
    time_val=str(time_val)

    if len(time_val)==1:
        return '00 : 00 : 0' + time_val
    elif len(time_val)==2:
        return '00 : 00 :' + time_val
    elif len(time_val)==3:
        return '00: 0'+time_val[:-2] + ' : ' + time_val[-2:]
    elif len(time_val)==4:
        return '00 : '+time_val[-4:-2] + ' : ' + time_val[-2:]
    elif len(time_val)==5:
        return '0' + time_val[-5] + '  : '+time_val[-4:-2] + ' : ' + time_val[-2:] 
    elif len(time_val)==6:
        return time_val[:-4] + '  : '+time_val[-4:-2] + ' : ' + time_val[-2:]
    else:
        return '00 : 00 : 00'
    
def date_decoation(date_val):
    date_val = str(date_val)
    return date_val[:4]+'/'+date_val[4:6]+'/'+date_val[6:]



##############################################################

# Cache
"""Cache Variable/Function Starts from ca """


@cache.cached(timeout=60)
@app.route('/get_notification')
@login_required
def latest_10_notification():
    try:
        all_incident = ArgusDB().get_10_incident('1007')
        name_id = get_alluserName_userId()
        
        if name_id:
            # print(name_id)
            
            return {"name_id": name_id, "all_incident": all_incident}
        else:
            return {"Not Found": "False"}
    except Exception as e:
        logging.error(f"Error in latest_10_notification: {e}")

        return {"Error": str(e)}



@cache.cached(timeout=60)
def ca_customer_user_data():
    """Cache Function Return Customer's All user Data
    """
    # return ArgusDB().get_customer_name_email_status_admin_group(session['customer_id'])
    return ArgusDB().get_customer_name_email_status_admin_group(session['customer_id'])


def get_alluserName_userId() -> dict:
    """ Getting All Users - User Id and UserName
        Step 1 : Getting User Data From ca_customer_user_data()
        Step 2 : Checking Its Empty Or False , So Return Empty
        Step 3 : Extracting User_id and User_name And Return Data

        Error Occurs : Return Empty Dict that , Not Break the Flow

    Returns:
        dict: { user_id : user_name }
    """
    name_id = {1: 'System'}
    try:
        logger.info("Start Getting All User_id & User_name ")
        # Calling Function Of User_Data
        logger.info(
            "_Calling Cache Function that Return Customer's All Users Data")
        user_data = ca_customer_user_data()
        # Checking User_data is have Data Or Not
        logger.info(
            "_Get Data and Extracting From List Of Tuples & Append Into Dict ( User_id : user_name )")
        if user_data:
            name_id = {user[5]: user[0] for user in user_data}
            name_id[1] = 'System'
            return name_id
        
        logger.debug(
            "_Data is Not Found in Customer's Users , So Return Empty Dict")
        # if This Return Which Means Data is Not Found
        return name_id
    except Exception as E:
        logger.exception(f"Error in fn get_allUserName_userId {E} \n")
        logger.debug(f"Error Found : {E}")
        return {}


def table_prefix(table_name: str) -> str:
    """Table Prefix | Adding Text | argus_ID_+table_name

    Args:
        table_name (str): 

    Returns:
        str: argus._Customer + table_name
    """
    return f'"argus"."{session["customer_id"]}_{table_name}"'


def generate_session_id():
    import uuid
    return str(uuid.uuid4())


def secure_session():
    session_id = generate_session_id()
    session['session_id'] = session_id


def is_session_secure(session_id):
    if session_id not in session:
        return False
    return True








@app.before_request
def before_request():
    g.email = None
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=150)
    if 'email' in session:
        g.email = session.get('email')


@app.route("/dropsession")
def dropsession():
    try:
        upload_actitivity(session['user_id'],
                          "User Logout", "User Logout from Dashboard")
        session_keys = list(session.keys()) 
        
        session.pop('user_id', None)
        logger.info("Users POP ")
        session.clear()
        return redirect(url_for('index'))
    except KeyError as e:
        session.pop('user_id', None)
        logger.info("KeyError ")
        session.clear()
        
        print(f"Error In Logout KeyError: {e}")
        logger.info(f"Error In Logout KeyError: {e}")
        return redirect(url_for('index'))
    except Exception as e:
        session.pop('user_id', None)
        print(f"Error In Logout E: {e}")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    return redirect('dropsession')


@app.route('/updateProfile', methods=['POST'])
@login_required
def updateProfile():
    # print(request)
    try:
        logger.info(f"Uploading Profile Start: {session['user_id']}")
        request_param = request.get_json()

        if len(request_param) == 0:
            print("No Data found From Form ")
            """No data Found from Profile form / Client side  """
            logger.info(
                f"__No values Found From Request Form : {session['user_id']}")
            return status_false
        # Extract Columns and Values then Pass into Variable
        column = tuple(request_param.keys())[0]
        value = tuple(request_param.values())[0]
        # print(column,value)
        logger.info(f"__Values Found From Function {request_param}")

        # Dynamic Creating a table Name
        # table_name=str(session['customer_id'])+'_users'
        table_name = table_prefix('users')
        # Typecasting the userId Into int
        user_id = int(session['user_id'])

        # Writing Query for Inserting values In DB
        # query=F'UPDATE \"argus\".\"{table_name}\" set {column} = \'{value}\' where user_id={user_id} '
        # update_query_where
        logger.info(f"__Query for Updating_Profile : {user_id}")
        # Insertion Query
        where = f'user_id = {user_id}'
        updating_status = ArgusDB().update_query_where(table_name=table_name, columns={column: value},
                                                       where_condition=where)

        logger.info(
            f"__Updating Status for Updating_Profile {updating_status} : {session['user_id']}")
        print(updating_status)
        if updating_status:
            """True Means Data is to Insert In to DB """
            session[column] = value
            # print(column)
            upload_actitivity(
                session['user_id'], "Updating Profile ", f"{column} and Value are {value}")
            logger.info(
                f"__Uploading Updating Profile User Activity into DB   : {session['user_id']}")
            # print(value)
            return status_true
        logger.info(
            f"__Unable to Update User Profile Return False : {session['user_id']}")
        return status_false
        # print(updating_status)

    except Exception as E:
        print(f"Error as E {E}")
        logger.exception("Error in Updating Profile {E} \n")
        logger.info(
            f"__Unable to Update User Profile Return False : {session['user_id']}")
        return status_false


@app.route('/team')
@admin_required
def team():
    # table_name = f'"argus".\"{session["customer_id"]}_users\"'
    table_name = table_prefix('users')

    columns = ['user_id', 'email', 'user_name', 'role',
               'groups', 'mid', 'up_node', 'down_node']
    all_team = ArgusDB().get_columns(table_name=table_name,
                                     columns=columns, where='status=true')
    user_id_name = get_alluserName_userId()
    # print(user_id_name)
    # print(all_team)
    return render_template('admin_team.html', page="Team", users_data=all_team, user_email=session.get('email'),
                           user_id_name=user_id_name, dict_group_id=dict_group_id)


@app.route('/team/profile/<team_member_id>', methods=['GET'])
@admin_required
def team_member_profile(team_member_id):
    try:
        print(team_member_id)
        user_id_name = get_alluserName_userId()
        print(user_id_name)

        table_name = table_prefix('users')
        columns = ['user_id', 'email', 'user_name', 'role',
                   'groups', 'mid', 'up_node', 'down_node', 'mobile']
        team_member = ArgusDB().get_columns(table_name=table_name, columns=columns,
                                            where=f'user_id={team_member_id} and status=true', getOne=True)

        department_supervisor = ArgusDB().get_all_department_supervisor(
            session["customer_id"])
        print("Your Department Supervisor", department_supervisor)
        # team_member=ArgusDB().get_query(query)
        print(team_member)
        if team_member in [None, False]:
            return render_template('error_page.html')
        return render_template('admin_team_member_profile.html', page='Profile', email=session.get('email'),
                               dict_group_id=dict_group_id, group=dict_group_id.get(
                                   session['group']),
                               team_member=team_member, user_id_name=user_id_name,
                               department_supervisor=department_supervisor)
    except Exception as E:
        print(f"Error Occurs As E: {E}")
        return render_template('error_page.html')


@app.route('/team/profile/<team_member_id>', methods=['POST'])
def edit_team_member_profile(team_member_id):
    try:
        logger.info(
            f"Uploading Profile Start: {session['user_id']} , User_id : {team_member_id}")
        request_param = request.get_json()

        if len(request_param) == 0:
            print("No Data found From Form ")
            """No data Found from Profile form / Client side  """
            logger.info(
                f"__No values Found From Request Form : {team_member_id}")
            return status_false
        # Extract Columns and Values then Pass into Variable
        print(request_param)
        column = tuple(request_param.keys())[0]
        value = tuple(request_param.values())[0]
        # print(column,value)
        logger.info(f"__Values Found From Function {request_param}")

        # Dynamic Creating a table Name
        table_name = str(session['customer_id']) + '_users'

        # Typecasting the userId Into int
        user_id = int(session['user_id'])
        updating_status = False
        if column == 'up_node':
            logger.info(f"__Updating UpNodes : {team_member_id}")
            # If we Update Up_NODE
            up_node_new = value

            # STEP 1  Updating The In Incident Manager Up Node
            # query=F'UPDATE \"argus\".\"{table_name}\" set {column} = \'{up_node_new}\' where user_id= {team_member_id} '
            # logger.info(f"__Query 1 Updation : {query}")
            # updating_status=ArgusDB().insert_query(query)

            up_node_current = request_param.get('up_node_current')
            print(up_node_current)
            up_node_current = int(up_node_current)

            # STEP 2 Updating the Department Supervisor Down Node
            # query=F'UPDATE \"argus\".\"{table_name}\" set down_node = array_append(down_node,{team_member_id})  where user_id = {up_node_new}'
            # logger.info(f"__Query 2 Updation : {query}")
            # print(query)
            # updating_status=ArgusDB().insert_query(query)
            # print("Query ",updating_status)

            # STEP 1  Updating The In Incident Manager Up Node
            # STEP 2 Updating the Department Supervisor Down Node
            all_query = [
                F'UPDATE \"argus\".\"{table_name}\" set {column} = \'{up_node_new}\' where user_id= {team_member_id} ',
                F'UPDATE \"argus\".\"{table_name}\" set down_node = array_append(down_node,{team_member_id})  where user_id = {up_node_new}',
            ]

            if up_node_current != 0:
                # Step 3 : Removing From Down Node Old Incident Manager
                query = F'UPDATE \"argus\".\"{table_name}\" set down_node = array_remove(down_node,{team_member_id})  where user_id = {up_node_current}'
                # logger.info(f"__Query 3 Update : {query}")
                # print(query)
                # updating_status=ArgusDB().insert_query(query)
                # print("Query ",updating_status)

                all_query.append(query)

            # print("Up Node :",value)
            # print("Down Node :",team_member_id)

            print(all_query)
            updating_status = ArgusDB().multiple_query(all_query)
            print("Updating Status Of Multiple Query")
            # Writing Query for Inserting values In DB
        else:
            table_name = table_prefix('users')
            where = f'user_id = {team_member_id}'
            updating_status = ArgusDB().update_query_where(table_name=table_name, columns={column: value},
                                                           where_condition=where)
            logger.info(f"__Query for Updating_Profile  :  {team_member_id}")
            # Insertion Query
            # updating_status=ArgusDB().insert_query(query)
            logger.info(
                f"__Updating Status for Updating_Profile {updating_status} :  {team_member_id}")
        print(updating_status)
        if updating_status:
            print()
            """True Means Data is to Insert In to DB """
            session[column] = value
            # print(column)
            upload_actitivity(
                session['user_id'], "Updating Profile ", f"{column} and Value are {value}")
            logger.info(
                f"__Uploading Updating Profile User Activity into DB   :  {team_member_id}")
            # print(value)
            return status_true
        logger.info(
            f"__Unable to Update User Profile Return False :  {team_member_id}")
        return status_false

    except Exception as E:
        print(f"Error as E here {E}")
        logger.exception("Error in Updating Profile {E} \n")
        logger.info(
            f"__Unable to Update User Profile Return False :  {team_member_id}")
        return status_false


@app.route('/del/<team_member_id>')
@admin_required
def del_team_memeber(team_member_id):
    print(session['customer_id'])
    del_status = ArgusDB().del_team_member(
        session["customer_id"], team_member_id)
    if del_status:
        upload_actitivity(session['user_id'], "Delete User",
                          f"Delete User Profile ID : {team_member_id} & Deleted By : {session['user_id']}")

        return status_true
    else:
        return status_false


@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/signUp')
def signUp():
    return render_template("signUp.html")



@app.route('/reset')
def reset():
    return render_template("email_form.html")



@app.route('/')
def login():
    """Check If Users Logged in , If Loggin Check Group_name and then Check Group_id

    Returns:
        redirect :  dashboard if login detail is True
    otherWISE redirect : Same page

    """
    if g.email:
        if session.get('group') == 1:
            # Check Current is belongs to Admin
            return redirect('/dashboard_run')

        elif session.get('group') == 2:
            # Check Current is belongs to Department Supervisor
            return redirect('/d/dashboard_run')

        elif session.get('group') == 3:
            # Check Current is belongs to Incident Manager
            return redirect('/r/dashboard_run')
        else:
            # Here Its Means Users Role is not found
            return redirect('/dropsession')
    # User is not Login
    # return render_template('index.html')
    return render_template('index2.html')


@app.route("/form_login", methods=['GET', 'POST'])
def dashboard():
    if request.method == "GET":
        return redirect(url_for('login'))
    if request.method == "POST":
        session.pop('email', None)
        session.pop('folder_id', None)
        session.pop('sites', None)
        try:
            # Removing Old Stored Session Data
            session.clear()
        except Exception as E:
            print(f"Error in Clearing Session : {E}")
            logger.info(f"Error in Clearing Session : {E}")

        logger.info("Moving to Dashboard ")

        session['allArgus'] = []

        email = request.form['email']
        pwd = request.form['password']

        authenticate, customer_id, user_id = authentication.main_function(
            email, pwd)
        # print("authentication is Here")
        print(authenticate, customer_id)

        if authenticate == False or authenticate == None:
            return render_template("index2.html", info="No Account Found ! Contact Admin")
        else:
            """
            Session Alocating
            1-Email_id  : login_email
            2-folder_id : alocate by data dict(database)
            3-Sites     : geting from DB
            4-group      : getting from DB
            5-Session   : Session_id Random
            """
            print("Authorization starts here")

            auth = authorization.main_function(
                authenticate, customer_id, email)
            print("AUTH", auth)

            if auth == False:
                return render_template("index2.html", info="No Account Found ! Contact Admin")
            elif auth in ['No group', 'No Group']:
                # Its May Be No Group or Account Deleted
                return render_template("index2.html", info="No Account Found ! Contact Admin")

            else:

                # auth['']
                # customer_id, site, group,mid = auth

                # print(auth)
                # print(email, customer_id, site, group)

                # User Data Keys Means Required data from Keys
                session['email'] = email
                session['customer_id'] = customer_id
                user_data_keys = ["user_id", "user_name",
                                  "mobile", "customer_id", "group", "mid"]

                for each_key in user_data_keys:
                    try:
                        session[each_key] = auth[each_key]
                    except KeyError:
                        print("KeyError in Auth ")
                        pass

                # Check if the `mid` key is present in the auth dictionary. If it is not, set it to 0.
                session["mid"] = 0 if "mid" not in session else auth["mid"]
                print('Session', session)

                if len(str(customer_id)) == 3:
                    session['folder_id'] = 'Argus_' + str(customer_id)
                else:
                    session['folder_id'] = str(customer_id)

                secure_session()

                logger.info("account Logging " + session['email'])

                """
                Folder Creation """
                basedir = os.path.abspath(os.path.dirname(__file__))

                try:
                    KnownPersonalDatabase = basedir + "/static/" + session[
                        'folder_id'] + "/images/KnownPersonalDatabase"
                    UnknownPerson = basedir + "/static/" + \
                        session['folder_id'] + "/images/UnknownPerson"
                    Upload_Image = basedir + "/static/" + \
                        session['folder_id'] + "/images/Upload_Image"
                    Report_CSV = basedir + "/static/" + \
                        session['folder_id'] + "/CSV_Files/Report_CSV"
                    diagnostics = basedir + "/static/" + \
                        session['folder_id'] + "/diagnostics"
                    all_unknown = basedir + "/static/" + \
                        session['folder_id'] + "/images/All_Unknown"

                    logger.info("Folder Not Found " + session['email'])
                    os.makedirs(KnownPersonalDatabase)
                    logger.info("Folder Creations " +
                                KnownPersonalDatabase + " " + session['email'])
                    os.makedirs(UnknownPerson)
                    logger.info("Folder Creations " +
                                UnknownPerson + " " + session['email'])
                    os.makedirs(Upload_Image)
                    logger.info("Folder Creations " +
                                Upload_Image + " " + session['email'])
                    os.makedirs(Report_CSV)
                    logger.info("Folder Creations " +
                                Report_CSV + " " + session['email'])
                    os.makedirs(diagnostics)
                    logger.info("Folder Creations " +
                                diagnostics + " " + session['email'])

                    os.makedirs(all_unknown)
                    logger.info("Folder Creations " +
                                all_unknown + " " + session['email'])

                except FileExistsError:
                    # print("File already exists")
                    logger.debug(
                        "Folder already exists  images & Report_CSV " + session['email'])

                # upload_actitivity(session['user_id'],
                #                   "Login Page", "Authencation Done")
                if session['group'] == 1:
                    # upload_actitivity(
                    #     session['user_id'], "Dashboard Page", "Authorization Done")
                    print("Admin Dashboard Page")
                    return redirect('/dashboard_run')
                elif session['group'] == 2:
                    upload_actitivity(
                        session['user_id'], "Dashboard Page", "Authorization Done")
                    print("Department Supervisor Dashboard Page")
                    return redirect('/d/dashboard_run')
                else:
                    upload_actitivity(
                        session['user_id'], "Dashboard Page", "Authorization Done")
                    print("incident_manager Dashboard Page")
                    return redirect('/r/dashboard_run')


@app.route("/google_login")
def google_login():
    """
    Initiates the Google OAuth2 login flow.

    - Retrieves client ID and secret from environment variables.
    - Configures the OAuth2 flow with required scopes.
    - Sets the redirect URI and generates an authorization URL.
    - Stores OAuth state and final redirect URL in session.
    - Redirects the user to the Google OAuth consent screen.
    """
    logger.info("Initiating Google login process")

    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

    logger.debug(f"client_id: {client_id}")
    logger.debug(f"client_secret: {client_secret}")

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
    )

    # flow.redirect_uri = "http://localhost:3005/google_login/oauth2callback"
    base_url = request.host_url.rstrip('/')  # e.g., http://localhost:3005 or http://49.50.87.70.nip.io:3005
    redirect_uri = urljoin(base_url, "/google_login/oauth2callback")
    flow.redirect_uri = redirect_uri
    logger.debug(f"Redirect URI set: {flow.redirect_uri}")

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="select_account",
        include_granted_scopes="true"
    )

    session.permanent = True
    session["state"] = state
    # session['final_redirect'] = "http://localhost:3005/logged_in"
    session['final_redirect'] = urljoin(base_url, "/logged_in")

    logger.info(f"OAuth state stored in session: {state}")
    logger.debug(f"Session keys: {list(session.keys())}")

    return redirect(authorization_url)


@app.route("/google_login/oauth2callback")
def auth_login_google_oauth2callback():
    """
    Handles the OAuth2 callback after the user authenticates via Google.

    - Validates session state.
    - Fetches token using the authorization response.
    - Verifies the ID token and retrieves user info.
    - Stores user ID info in the session.
    - Redirects the user to the final destination stored in session.
    """
    logger.info("Handling OAuth2 callback from Google")
    logger.debug(f"Session keys at callback start: {list(session.keys())}")

    session_state = session.get('state')
    if not session_state:
        logger.warning("Session state missing or expired")
        return "Session expired or invalid state", 400

    redirect_uri = request.base_url
    authorization_response = request.url
    logger.debug(f"Authorization response received: {authorization_response}")

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ],
        state=session_state
    )

    flow.redirect_uri = redirect_uri
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    time.sleep(2)
    logger.debug(f"Credentials obtained: {credentials}")
    

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=google_auth_requests.Request(),
        audience=os.environ.get("GOOGLE_CLIENT_ID")
    )

    session["id_info"] = id_info
    logger.info("User ID info stored in session")

    return redirect(session['final_redirect'])


@app.route("/logged_in")
def logged_in():
    """
    Processes post-login logic after a successful Google sign-in.

    - Retrieves user email from session and checks if account exists.
    - Authorizes the user based on their group or role.
    - Sets relevant session variables based on user information.
    - Redirects user to the appropriate dashboard based on their group.
    """
    id_info = session.get("id_info")

    if not id_info:
        logger.warning("No ID info found in session, redirecting to login")
        return redirect(url_for("login"))

    email = id_info["email"]
    logger.info(f"User logged in with email: {email}")

    authenticate, customer_id, user_id = authentication.check_email_exist(email)
    logger.debug(f"Authentication result: {authenticate}, Customer ID: {customer_id}, User ID: {user_id}")

    if not authenticate:
        logger.warning("Authentication failed: No account found")
        return render_template("index2.html", info="No Account Found! Contact Admin")

    auth = authorization.main_function(authenticate, customer_id, email)
    logger.debug(f"Authorization result: {auth}")

    if not auth or auth in ['No group', 'No Group']:
        logger.warning("Authorization failed: Invalid group")
        return render_template("index2.html", info="Authorization failed!")

    session['email'] = email
    session['customer_id'] = customer_id
    user_data_keys = ["user_id", "user_name", "mobile", "customer_id", "group", "mid"]

    for key in user_data_keys:
        session[key] = auth.get(key, None)

    session["mid"] = 0 if "mid" not in auth else auth["mid"]
    logger.info("Session variables set with user data")

    group = session.get("group")
    logger.info(f"Redirecting user based on group: {group}")

    if group == 1:
        return redirect("/dashboard_run")
    elif group == 2:
        return redirect("/d/dashboard_run")
    elif group == 3:
        return redirect("/r/dashboard_run")
    else:
        logger.warning("Invalid group found. Redirecting to dropsession.")
        return redirect("/dropsession")



def parse_idle_time_to_minutes(idle_time):

    #Converting H:M format into Minutes only
    total_minutes = 0
    parts = idle_time.lower().split()

    for i in range(len(parts)):
        if parts[i].startswith('hour'):
            total_minutes += int(parts[i - 1]) * 60
        elif parts[i].startswith('min'):
            total_minutes += int(parts[i - 1])

    return total_minutes



@app.route('/dashboard_run')
@admin_required
def dashboard_run():
    # upload_actitivity(session['user_id'], "Admin Dashboard Page", "Home Redirect")

    return render_template('dashboard.html', page='Dashboard', user_email=session.get('email'))



@app.route('/all_rendered_video')
@admin_required
def all_rendered_video():
    table_name = table_prefix('rendered_videos')
    list_rendered_video = ArgusDB().get_columns(
        table_name, ['render_id', 'url', 'rendered'])
    return render_template('admin_all_rendered_video.html', page='Analytics', list_rendered_video=list_rendered_video)


@app.route('/analytics', methods=['GET', 'POST'])
@admin_required
def analytics():
    if request.method == 'GET':
   
        table_name = table_prefix('rendered_videos')
        list_rendered_video = ArgusDB().get_columns(table_name, [
            'search_date', 'search_time', 'render_id', 'url', 'rendered', 'camera_id'], extra=' ORDER BY date DESC ')

        return render_template('admin_analytics.html', page='Analytics', user_email=session.get('email'), list_rendered_video=list_rendered_video)
    elif request.method == 'POST':
        '''
        1. Check "Request Video Input Time" Video is in analysed(its means Json is created ) or Not If Exist in DB Video . Go Step 2
            If Not Found . Show Video Not Found 
        2. Check Video is Exist into Rendered Video 
            2.1. If Exist : Then (Video Already Request For Generated)
                2.1.a Check If false Which means video not GENERATED
                2.1.a Check If false Which means video not GENERATED
            2.2. If Video is not exist Then Add New Video in Rendered Table
        '''
        try:
            # Taking Input From Forms
            camera_id = request.form.get('camId', False)
            # print(camera_id)

            int_camera_id = camera_id[3:] #Extracting a Single Camera Name

            table_name = table_prefix(F'camera{int_camera_id}_analysis')
            # if camera_id == 'Cam2':
            #     table_name = table_prefix('camera2_analysis')
            # else:
            #     table_name = table_prefix('camera3_analysis')
            startFormDate = request.form.get('startDate', False)
            startFormTime = request.form.get('startTime', False)
            # endFormDate=request.form.get('endDate',False)
            # endFormTime=request.form.get('endTime',False)

            print("\n\n\n\n", camera_id, startFormDate, startFormTime)

            # Check Input data From FORMs
            if len(startFormDate) != 10 and len(startFormTime) != 5:
                return render_template('admin_analytics.html', page='Analytics', user_email=session.get('email'), invalid_date=True)

            # Variable That Will Be USed for this ROutes
            insertion_rendered_status = False
            list_video_id = []
            rendered_data = []
            list_rendered_video = []

            # Improve Data
            startDate = int(startFormDate.replace('-', ''))
            search_time = startFormTime.replace(':', '')
            startTime = startFormTime.replace(':', '')+'00'

            # Taking Date and Time IMPROVING 1 minuets__ Using Time Delta Method
            input_time = datetime.strptime(
                str(startDate)+str(startTime), '%Y%m%d%H%M%S')
            """Calculating Input_time Next 1 Min"""
            increment_time = input_time+timedelta(minutes=1)
            # print('increment_time',increment_time)
            end_date_time = increment_time.strftime("%Y%m%d,%H%M%S")
            endDate, endTime = end_date_time.split(',')
            endDate, endTime = int(endDate), int(endTime)
            # print('Start Date',startDate)
            # print('Start Time',startTime)
            # print('endData',endDate)
            # print('endTime',endTime)

            # print(end_date_time)

            # table_name=table_prefix('camera3_analysis')
            analysis = ArgusDB().get_columns(table_name=table_name, columns=['DISTINCT(video_id)'],
                                             where=f'date BETWEEN {startDate} AND {endDate} AND time BETWEEN {startTime} AND {endTime} LIMIT 10')

            # print('analysis',analysis)
            if not analysis:
                # return 'No Video Found'
                return render_template('admin_analytics.html', page='Analytics', user_email=session.get('email'), no_video_found=True)

            if analysis:

                table_name = table_prefix('rendered_videos')
                rows_values = ''
                today_ist = ist.ist_time()
                today_date = int(today_ist.strftime('%Y%m%d'))
                today_time = int(today_ist.strftime('%H%M'))

                # Inserting Only One Video
                rendered_data = ArgusDB().get_columns(table_name, [
                    'search_date', 'search_time', 'render_id', 'url', 'rendered','camera_id'], where=f'video_id= {analysis[0][0]}')

                if len(rendered_data) > 0:
                    """Video is Already Request For processing"""
                    return render_template('admin_analytics.html', page='Analytics', user_email=session.get('email'), list_rendered_video=rendered_data)
                else:
                    """Video Processing is Added for Rendering"""
                    # 2.b. If videos Exist that Day but Un Processed
                    # Inserted Into DB
                    # Run argus-Backend Service
                    print("Not FOund", rendered_data)

                    query = f''' INSERT INTO {table_name} (video_id,date,time,search_date,search_time,camera_id) VALUES  {analysis[0][0] , today_date,today_time,startDate,search_time,camera_id}'''
                    insertion_rendered_status = ArgusDB().insert_query(query=query)
                    print('insertion_status', insertion_rendered_status)
                # print(list_video_id)
                # print(rows_values)
                list_rendered_video = ArgusDB().get_columns(table_name, [
                    'search_date', 'search_time', 'render_id', 'url', 'rendered','camera_id'], extra=' ORDER BY date DESC ')
                # print(list_rendered_video)

            context = {'page': 'Analytics', 'user_email': session.get(
                'email'), 'list_rendered_video': list_rendered_video, 'under_processing': True}
            # **context take dictionary , split into variable
            return render_template('admin_analytics.html', **context)

        except Exception as Err:
            print(F"Issue Error {Err}")
            logger.debug(F"Issue Error {Err}")
            context = {'page': 'Analytics', 'user_email': session.get(
                'email'), 'list_rendered_video': [], 'error_500': True}
            # **context take dictionary , split into variable
            return render_template('admin_analytics.html', **context)

    else:
        # return 'Something Went Wrong'
        context = {'page': 'Analytics', 'user_email': session.get(
            'email'), 'list_rendered_video': [], 'error_500': True}
        # **context take dictionary , split into variable
        return render_template('admin_analytics.html', **context)


@app.route('/analyticsSearch')
@admin_required
def analyticSearch():
    # upload_actitivity(session['user_id'], "Admin Analytics Page", "View Analytics Data")
    return render_template('admin_analytics_search.html', page='Analytics', user_email=session.get('email'))

@app.route('/video_play')
def video_play():
    return render_template('video_play.html')

@app.route('/analyticsVideo/<int:video_id>')
@admin_required
def analyticsVideo(video_id):
    try:
        table_name = table_prefix('rendered_videos')
        print(video_id, type(video_id))
        list_rendered_video = ArgusDB().get_columns(
            table_name, ['render_id', 'url', 'rendered'], where=f'render_id = {video_id}')
        print(list_rendered_video)
        staic_video_path = f'static/{session.get("customer_id")}/videos/{video_id}.mp4'
        status_video = False
        if len(list_rendered_video) >= 1:
            url = list_rendered_video[0][1]
            basedir = os.path.abspath(os.path.dirname(__file__))
            output_file_path = f'{basedir}/static/{session.get("customer_id")}/videos/'
            video_path = output_file_path+f'{video_id}.mp4'
            try:
                print("Folder Creation")
                os.makedirs(output_file_path, exist_ok=True)
            except Exception as Err:
                print("Issue in Folder Creation", Err)
            status_video = download_video(url, video_path)
        return send_file(video_path, as_attachment=True)
        # upload_actitivity(session['user_id'], "Admin Analytics Page", "View Analytics Data")
        # return render_template('admin_analytics_video.html', page='Analytics', user_email=session.get('email'),status_video=status_video,staic_video_path=staic_video_path)
    except Exception as E:
        print('analyticsVideo :', E)
        return redirect('/error_page')


# @app.route('/admin_users')
# @admin_required
# def admin_users():
#     # upload_actitivity(session['user_id'],
#     #                   "Admin Users List Page", "View Users Page")
#     users_data = ca_customer_user_data()
#     # print(users_data)
#     return render_template('admin_users.html', page='Setting', page_option='Admin Users', users_data=users_data,
#                            user_email=session.get('email'), group=dict_group_id)








@app.route('/settings')
def settings_page(): 

    return render_template("setting1.html")

@app.route('/profile')
@login_required
def profile():
    return render_template('admin_profile.html', page='Profile', email=session.get('email'),
                           group=dict_group_id.get(session['group']), mid=session['mid'], mobile=session.get('mobile'),
                           user_name=session.get('user_name'))




@app.route('/alert')
@admin_required
def alert():
    return render_template('alert.html')
    


@app.route('/production_log')
@admin_required
def production_log():
    return render_template('production_log.html')



@app.route('/event_test')
@admin_required
def event_test():
    return render_template('event_test.html')

@app.route('/event_test2')
@admin_required
def event_test2():
    return render_template('event_test2.html')




@app.route('/alert2')
@admin_required
def alert2():
    return render_template('alert2.html')
    


@app.route('/transit_log')
@admin_required
def transit_log():
    return render_template('transit_log.html')



@app.route('/transit_event')
@admin_required
def transit_event():
    return render_template('transit_event.html')




@app.route('/alert3')
@admin_required
def alert3():
    return render_template('alert3.html')
    


@app.route('/safety_log')
@admin_required
def safety_log():
    return render_template('safety_log.html')



@app.route('/safety_event')
@admin_required
def safety_event():
    return render_template('safety_event.html')


@app.route('/safety_w_comp')
@admin_required
def safety_w_comp():
    return render_template('safety_w_comp.html')


# THis is Inventory Section
@app.route('/alert4')
@admin_required
def alert4():
    return render_template('alert4.html')


@app.route('/inventory_log')
@admin_required
def inventory_log():
    return render_template('inventory_log.html')

@app.route('/stock_inventory')
@admin_required
def stock_inventory():
    return render_template('stock_inventory.html')
    

@app.route('/log_click', methods=['POST'])
def log_click():
    ''' To update the value of render_video column in table '''
    try:
        data = request.json  
        incident_id = data.get('incidentId')

        print(f"Received AJAX Request for VideoID: {incident_id}")  
        
        if not incident_id:
            return jsonify({"error": "Invalid Video ID"}), 400

        update_status = ArgusDB().update_query_where(
        table_name='argus."1007_cam3_material_count"',  
        columns={"render_video": False},  
        where_condition=f"video_id = {incident_id}"
        
        
        )


        if update_status:
            print(f"Updated render_video=True for Incident ID: {incident_id}")  
            return jsonify({"message": "Status updated", "status": True})
        else:
            print(f"Database update failed for Incident ID: {incident_id}")  
            return jsonify({"error": "Database update failed"}), 500

    except Exception as e:
        print("Error in log_click:", str(e))  
        return jsonify({"error": str(e)}), 500









@app.route('/incident/<int:incidentId>')
@login_required
def incident(incidentId):
    """Render the incident page first without video."""
    try:
        incident = [] 
        print("incident_id", incidentId, type(incidentId))
        video_time = ArgusDB().fetch_time(incidentId)
        table1 = 'argus."1007_cam3_material_count"'
        where = F'video_id={incidentId}'
        column = ('total_material_count',)
       
        total_material_pieces = ArgusDB().get_columns(table1, column, where, getOne=True)
        total_material_pieces = total_material_pieces[0] if total_material_pieces else 0

        print("total_material_count ::::",total_material_pieces)


        
        return render_template('incident1_alert.html', page='Alert', total_material_pieces=total_material_pieces,incidentId=incidentId, incident=incident, video_time=video_time)
    except KeyError:
        return redirect(url_for('login'))
    except:
        return redirect(url_for('error_page'))

@app.route('/incident/<int:incidentId>/get-data')
def get_data(incidentId):
    """Fetch video URL asynchronously after page load."""
    video_name = check_video_in_static(incidentId)
    if not video_name:
        video_name = compare_video_id(incidentId)
        print(f'compare video_id : {video_name}')
        if not video_name:
            try:
                log_click()
                time.sleep(35)  # Wait and retry
                video_name = compare_video_id(incidentId)
            except Exception as err:
                print(f"Issue in {err}")
    
    if video_name:
        return jsonify({"video_url": f'/static/render_videos/{video_name}'})
    else:
        return jsonify({"error": "No video available"}), 404


@app.route('/incident/<int:incidentId>/get-material-json')
def get_material_json(incidentId):
    try:
        # Fetch the material_json from the database
        print("printing material json")
        material_json = ArgusDB().fetch_one(incidentId)
        
        print("Material JSON : ", material_json)

        if material_json:
            material_data = material_json[0].get("Material_Count_data", [])
            
            # Extract only Material_count and timeStamp
            filtered_data = [{"Material_count": item["Material_count"], "timeStamp": item["timeStamp"]} for item in material_data]
            print("Filtered json",filtered_data)
            return jsonify(filtered_data)  # Return the filtered JSON data
        else:
            return jsonify({"error": "No material data found for this incident."}), 404
    except Exception as e:
        print(f"Error fetching material JSON for incident {incidentId}: {e}")
        return jsonify({"error": "Error fetching material data."}), 500



@app.route('/incident_search', methods=['GET', 'POST'])
@login_required
def incident_search():
    try:
        if request.method == "GET":
            return render_template('search_incident.html', page='Alert')
        elif request.method == 'POST':
            print("Request Data ", request.form['incident'])
            where = {'incident_id': request.form['incident']}
            name_id = get_alluserName_userId()
            all_incient = []
            offset = 1

            all_incident = ArgusDB().get_all_incident(
                '1005', offset=offset*100, where=where)

            print(all_incident)
            return render_template('searched_incident_list.html', page='Alert', all_incident=all_incident, incident_data=DICT_INCIDENT_DATA,
                                   name_id=name_id, user_email=session.get('email'))
            return render_template('search_incident.html', page='Alert')
        return '404'
    except Exception as E:
        print(E)
        print(f"Exception as E: {E}")
        return render_template('error_page.html')








@app.route('/log_click2', methods=['POST'])
def log_click2():
    ''' To update the value of render_video column in table '''
    try:
        data = request.json  
        incident_id = data.get('incidentId')

        print(f"Defects Received AJAX Request for VideoID: {incident_id}")  
        
        if not incident_id:
            return jsonify({"error": "Invalid Video ID"}), 400

        update_status = ArgusDB().update_query_where(
        table_name='argus."1007_cam3_defect_count"',  
        columns={"render_video": False},  
        where_condition=f"video_id = {incident_id}"
        
        
        )
        print("Update status",update_status)


        if update_status:
            print(f"Updated render_video=True for Incident ID of defetcs table: {incident_id}")  
            return jsonify({"message": "Status updated", "status": True})
        else:
            print(f"Database update failed for Incident ID: {incident_id}")  
            return jsonify({"error": "Database update failed"}), 500

    except Exception as e:
        print("Error in log_click:", str(e))  
        return jsonify({"error": str(e)}), 500

@app.route('/incident2/<int:incidentId>')
def incident2(incidentId):
    """Render the incident page first without video."""
    try:
        incident = [] 
        print("incident_id", incidentId, type(incidentId))
        video_time = ArgusDB().fetch_time2(incidentId)
        
        
        print("video_time : ",video_time)

        return render_template('incident21_alert.html', page='Alert', incidentId=incidentId, incident=incident, video_time=video_time)
    except KeyError:
        return redirect(url_for('login'))
    except:
        return redirect(url_for('error_page'))

@app.route('/incident2/<int:incidentId>/get-data2')
def get_data2(incidentId):
    """Fetch video URL asynchronously after page load."""
    video_name = check_video_in_static2(incidentId)
    if not video_name:
        video_name = compare_video_id2(incidentId)
        print(f'compare video_id : {video_name}')
        if not video_name:
            try:
                log_click2()
                time.sleep(40)  # Wait and retry
                video_name = compare_video_id2(incidentId)
            except Exception as err:
                print(f"Issue in {err}")
    
    if video_name:
        return jsonify({"video_url": f'/static/render_videos/{video_name}'})
    else:
        return jsonify({"error": "No video available"}), 404


@app.route('/incident2/<int:incidentId>/get-material-json2')
def get_material_json2(incidentId):
    try:
        material_json = ArgusDB().fetch_one2(incidentId)
        
        # print("Material JSON of defects: ", material_json)

        if material_json:
            material_data = material_json[0].get("defect_count_data", [])
            
            filtered_data = []
            for item in material_data:
                try:
                    # Convert timestamp format to a valid format
                    raw_timestamp = item["timeStamp"]
                    formatted_timestamp = fix_timestamp_format(raw_timestamp)
                    
                    filtered_data.append({"Material_count": item["defect_count"], "timeStamp": formatted_timestamp})
                except Exception as e:
                    print(f"Skipping invalid timestamp {item['timeStamp']}: {e}")
            
            # print("Filtered data for defects:", filtered_data)
            return jsonify(filtered_data) 
        else:
            return jsonify({"error": "No material data found for this incident."}), 404
    except Exception as e:
        print(f"Error fetching material JSON for incident {incidentId}: {e}")
        return jsonify({"error": "Error fetching material data."}), 500


def fix_timestamp_format(timestamp):
    """Fix incorrect timestamp format (e.g., 2025_03_18 84:10:4 -> 2025-03-18 12:10:04)"""
    try:
        date_part, time_part = timestamp.split(" ")
        date_part = date_part.replace("_", "-")  # Change 2025_03_18 to 2025-03-18
        
        hours, minutes, seconds = map(int, time_part.split(":"))
        hours = hours % 24  # Ensure hours are within 0-23

        return f"{date_part} {hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception:
        return "1970-01-01 00:00:00"  # Return a default valid timestamp if parsing fails



@app.route('/incident_report/<dateRange>')
@admin_required
def incident_report(dateRange):
    try:
        # Set the authorization header
        headers = {"Authorization":  "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6Im51bWFuIn0.heaQilFsyWuk4rrljvtkc7wYR8PzvQKMfCjZJFZXRP0"}

        # Make the request
        # response = requests.post("http://127.0.0.1:5000/protected", headers=headers, data=data)
        response = requests.get(
            f"https://argus-backend-reports-4ddd5d1b1135.herokuapp.com/report_generate/{session['customer_id']}/{dateRange}", headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # The request was successful.

            print(response.content)
            return json.loads(response.content)
            # print(json.loads(response.content))
        else:
            # The request failed.
            print("Status Code Failed")
            print(f"Status _Code {response.status_code}")
            return status_false
    except Exception as E:
        print(f'Error in incident_report : {E}')
        return status_false

    # return report_generate(customer_id=session['customer_id'], dateRange=dateRange)




@app.route('/create_incident')
@admin_required
def create_incident():
    if g.email:
        # upload_actitivity(
        #     session['user_id'], "Alert/Request Incident Page", "Request A New Incident")
        user_data = ca_customer_user_data()
        name_id = get_alluserName_userId()
        return render_template('create_incident.html', page='Alert', name_id=name_id, user_id=session['user_id'])


@app.route('/create_new_incident', methods=['POST', 'GET'])
@admin_required
def create_new_incident():
    try:
        # upload_actitivity(
        #     session['user_id'], "Alert/Request/Creating Incident Page", "Request A New Incident")
        if request.method == "GET":
            return redirect('create_incident')
        elif request.method == 'POST':
            # upload_actitivity(
            #     session['user_id'], "Alert/Request/Creating Incident Page", "Filling Pop form")
            priority = request.form['priority']
            category = request.form['category']
            location = request.form['location']
            status = request.form['status']
            user_id = session['user_id']
            assigned_officer = request.form['assigned_officer']

            # Generating Incident ID
            incident_id = int(incident_id_gen.generate_incidentID('1005'))
            print(incident_id)
            print(type(incident_id))

            today_date = int(datetime.now().strftime("%Y%m%d%H%M"))
            # incident_id=random.randint(0,999999)

            print(priority, "Insertion Start ", incident_id, priority, category, today_date, location, status, user_id,
                  assigned_officer)
            query_status = ArgusDB().insert_new_incident('1005', incident_id, priority, category, today_date, location,
                                                         status, user_id, assigned_officer)
            print("Query Status", query_status)
            if query_status:
                update_Latest_incidentID = ArgusDB().update_ca_latest_incidentID(
                    session['customer_id'], incident_id)
                print('Update_Latest_incidentID', update_Latest_incidentID)
                if update_Latest_incidentID:
                    # upload_actitivity(session['user_id'], F"Alert/Request/ Incident Created Page",
                    #                   "SuccessFully Incident Created {update_Latest_incidentID}")
                    return render_template('alert_success_page.html', page='Alert', backUrl='create_incident',
                                           heading="New Incident Created", subHeading='New ')
            # upload_actitivity(
            #     session['user_id'], "Alert/Request/ Incident Created Page", "Unable to Create New ")
            return render_template('alert_failed_page.html', page='Alert', backUrl='create_incident',
                                   heading="Create New Incident", subHeading='Wrong Data Input Data')

    except Exception as E:
        logger.exception("Error In ")
        print(E)
        return render_template('alert_failed_page.html', page='Alert', backUrl='create_incident',
                               heading="Unable to Create New Incident", subHeading='Wrong Data Input Data')




@app.route('/incident_history_update', methods=['POST'])
@login_required
def incident_history_update():
    print("We Are Here")
    try:
        if request.method == 'POST':
            status = int(request.form['updateStatus'])
            today_date = str(datetime.now().strftime("%Y%m%d%H%M%S"))
            incident_id = int(request.form['incident_id'])
            assignee = int(request.form['assignee'])
            assigned_by = int(request.form['assigned_by'])
            comment = request.form['comment']
            print(1005, today_date, status, assignee,
                assigned_by, comment, incident_id)
            print(type(today_date), type(status), type(assignee),
                type(assigned_by), type(comment), type(incident_id))
            query_status = ArgusDB().update_incident_history('1005', today_date, status, assignee, assigned_by, comment,
                                                            incident_id)
            print("\n\n\nExecuting ", {query_status})
            # if query_status:
            #     # update_status=
            #     # *** Do Not C
            #     table_name = table_prefix('incident')
            #     where = f'incident_id = {incident_id}'
            #     updating_status = ArgusDB().update_query_where(table_name=table_name, columns={'status': status},
            #                                                 where_condition=where)
            #     print(updating_status)

            return redirect('incident/' + str(incident_id))
        else:
            print("True")
            return redirect('incident/' + str(incident_id))
    except :
        print("Error")
        return redirect('incident/'+str(incident_id))







""" Reset password related functions"""





@app.route('/send_otp', methods=['POST'])
def send_otp():
    """
    Handle the OTP sending process for a given email.
    
    Steps:
    - Validates if the email exists.
    - Checks if the user is currently blocked.
    - Deletes any expired OTP.
    - Sends a new OTP via email.
    - Inserts or updates OTP details in the database.
    
    Returns:
        Rendered template with status message or OTP input page.
    """
    input_email = request.form['email']
    db_ps, customer_id, user_id = authentication.check_email_exist(input_email)

    if not db_ps:
        logger.warning(f"Email not found: {input_email}")
        return render_template('email_form.html', info="Email not found!")

    block_check_query = f'''
        SELECT blocked_until FROM argus."1007_OTP_log" WHERE user_id = {user_id}
    '''
    result = ArgusDB().fetch_query(block_check_query)

    if result and result[0][0]:
        blocked_until = result[0][0].replace(tzinfo=pytz.UTC)
        if datetime.utcnow().replace(tzinfo=pytz.UTC) < blocked_until:
            logger.warning(f"User {user_id} is blocked until {blocked_until}")
            return render_template('email_form.html', info="No further attempts allowed. Please try again after 2 hours.")

    delete_query = f"""
        DELETE FROM argus."1007_OTP_log"
        WHERE user_id = {user_id} AND otp_created_at < (NOW() - INTERVAL '5 minutes')
    """
    ArgusDB().execute_query(delete_query)
    logger.info(f"Expired OTPs deleted for user_id={user_id}")

    otp = str(random.randint(100000, 999999))
    msg = Message('Your OTP Code', recipients=[input_email])
    msg.body = f'Your OTP code is {otp}. It will expire in 5 minutes.'

    try:
        mail.send(msg)
        logger.info(f"OTP sent to {input_email}: {otp}")

        check_query = f'''SELECT COUNT(*) FROM argus."1007_OTP_log" WHERE user_id = {user_id}'''
        result = ArgusDB().fetch_query(check_query)

        if result and result[0][0] > 0:
            ArgusDB().update_query_where(
                table_name='argus."1007_OTP_log"',
                columns={"otp": otp, "otp_created_at": "now()", "attempt_count": 0},
                where_condition=f"user_id = {user_id}"
            )
            logger.info(f"OTP log updated for user_id={user_id}")
        else:
            ArgusDB().insert_db(
                table_name='1007_OTP_log',
                Key_values={'user_id': user_id, 'otp': otp, 'attempt_count': 0}
            )
            logger.info(f"OTP log created for user_id={user_id}")

        return render_template('otp_enter.html', email=input_email)

    except Exception as e:
        logger.exception("Failed to send OTP email")
        return f'Failed to send email: {e}', 500


@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    """
    Validate the entered OTP for a given email.

    Steps:
    - Retrieve the OTP, attempt count, and block status from the database.
    - Check if the OTP is valid and not expired.
    - Increment attempt count or block the user after multiple failed attempts.
    
    Returns:
        Rendered template based on the validation result.
    """
    entered_otp = ''.join([
        request.form.get(f'otp{i}', '').strip() for i in range(1, 7)
    ])
    email = request.form['email'].strip()

    db_ps, customer_id, user_id = authentication.check_email_exist(email)

    fetch_query = f'''
        SELECT otp, otp_created_at, attempt_count, blocked_until
        FROM argus."1007_OTP_log"
        WHERE user_id = {user_id}
    '''
    result = ArgusDB().fetch_query(fetch_query)

    if result:
        db_otp, created_at, attempt_count, blocked_until = result[0]
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        if blocked_until:
            blocked_until = blocked_until.replace(tzinfo=pytz.UTC)
            if now < blocked_until:
                logger.warning(f"Blocked user {user_id} tried to validate OTP before {blocked_until}")
                return render_template('email_form.html', info="No further attempts allowed. Try again after 2 hours.", email=email)
            else:
                ArgusDB().execute_query(f'''DELETE FROM argus."1007_OTP_log" WHERE user_id = {user_id}''')
                logger.info(f"OTP log deleted after block expired for user_id={user_id}")
                return render_template('email_form.html', info="Time limit passed. Please re-enter your email to receive a new OTP.")

        if (now - created_at.replace(tzinfo=pytz.UTC)).total_seconds() <= 300:
            if str(db_otp).strip() == entered_otp:
                logger.info(f"OTP validated successfully for user_id={user_id}")
                return render_template('set_password.html', email=email)
            else:
                attempt_count += 1
                update_fields = f"attempt_count = {attempt_count}"
                logger.warning(f"Invalid OTP attempt {attempt_count} for user_id={user_id}")

                if attempt_count >= 5:
                    blocked_time = now + timedelta(minutes=1)
                    update_fields += f", blocked_until = '{blocked_time}'"
                    logger.warning(f"User {user_id} blocked until {blocked_time} due to repeated invalid attempts")

                ArgusDB().execute_query(
                    f'''UPDATE argus."1007_OTP_log" SET {update_fields} WHERE user_id = {user_id}'''
                )

                if attempt_count >= 5:
                    return render_template('otp_enter.html', info="No further attempts allowed. Try again after 2 hours.", email=email)

                return render_template('otp_enter.html', info="Invalid OTP", email=email)
        else:
            ArgusDB().execute_query(f'''DELETE FROM argus."1007_OTP_log" WHERE user_id = {user_id}''')
            logger.info(f"Expired OTP deleted for user_id={user_id}")
            return render_template('email_form.html', info="OTP expired. Please request a new one.")

    logger.warning(f"OTP not found in DB for user_id={user_id}")
    return render_template('otp_enter.html', info="OTP not found. Please request again.", email=email)


@app.route('/set_password', methods=['POST'])
def set_password():
    """
    Update the password for the given user after successful OTP verification.

    Steps:
    - Retrieve email and new password.
    - Hash the password and update the database.
    
    Returns:
        Rendered template with success or failure message.
    """
    email = request.form['email']
    new_password = request.form['password']

    _, _, user_id = authentication.check_email_exist(email)
    hashed_password = authentication.create_password_hash(new_password)

    update_status = ArgusDB().update_query_where(
        table_name='argus."user"',
        columns={'user_ps': hashed_password},
        where_condition=f"user_id = {user_id}"
    )
    
    if update_status:
        logger.info(f"Password updated successfully for user_id={user_id}")
        return render_template(
            'index2.html',
            info='<span style="background-color:green; color:white;">Password successfully updated!</span>'
        )
    else:
        logger.error(f"Password update failed for user_id={user_id}")
        return render_template(
            'index2.html',
            info='<span style=color:#a31717;background-color: rgba(235, 125, 125, 0.5);>Failed to update password</span>'
        )









# READ JSON File
"""
import yaml
ddd=''
with open('1005_incident_values.yaml') as f:
    ddd=yaml.load(f,Loader=yaml.FullLoader)
print(ddd)
"""


# Error Handling Page




@app.route('/index2')
def index2():
    return render_template('index2.html')



@app.route('/settings_test')
def settings_test():
    return render_template('settings_test.html')

@app.errorhandler(404)
def invalid_route(e):
    return render_template('error_page.html')


@app.route('/error')
def error_page():
    return render_template('error_page.html')


@app.errorhandler(500)
def error500(error=0):
    logger.warning(f"Server Error 500 Occurs")
    return render_template('error_500.html')


@app.route('/error500')
def error_500page():
    return render_template('error_500.html')



if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run(
        debug=False,
        host="0.0.0.0",
        port=3005,
       
        
        
    )

