from datetime import datetime
import re
from db.connect_db import sql_mutation, sql_query
from services.tools import get_date_time_type

from services.authentication import authenticate, generate_key, APIKey

from app import GLOBAL_SERVER_CONFIG_AUTO_CACHE, GLOBAL_SERVER_DATA, GLOBAL_SERVER_CONFIG_SEQURITY

# from sqlalchemy import true

def resolve_create_comment(obj, info, problemid, useremail, apikey, comment):
    try:
        print("resolve_create_comment")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey)
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        # check if problem exists
        sql_prepared = """SELECT count(*) FROM mathu_similarity_index_database.problems where problem_id = %s;"""
        x = sql_query(sql_prepared, (problemid,))
        if x[0][0] > 0:
            # insert problem
            # check user //todo
            # insert comment
            dt = datetime.now()
            dt_nano = dt.strftime("%f")

            sql_prepared = """insert into mathu_similarity_index_database.comments (problem_id, date_time, nanosecond, user_email, comment) values (%s,%s,%s,%s,%s);"""
            sql_mutation(sql_prepared, (problemid,dt,dt_nano,useremail,comment,))

            payload = {
                "success": True,
                "msg": "Success",
                "comment": {
                    "problemid": problemid,
                    "datetime": get_date_time_type(dt),
                    "useremail": "useremail",
                    "comment": "comment"
                }
            }
            return payload
        else:
            payload = {
                "success": False,
                "msg": "Problem not in database"
            }
            return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_add_user_search_click(obj, info, problemid, useremail, apikey):
    print("resolve_add_user_search_click")

    payload = {
        "success": False,
        "msg": "Access Denied"
    }
    return payload

def resolve_user_sign_up(obj, info, apikey, useremail, password):
    try:
        print("resolve_user_sign_up")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate("default", apikey, [1,3])
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload
        
        # print("signup: ", useremail, password)
        # valid email
        valid_email = re.match(r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$", useremail)
        # print("signup v email")
        if valid_email:
            sql_prepared = """SELECT count(*) FROM mathu_similarity_index_database.users where email like %s;"""
            x = sql_query(sql_prepared, (useremail,))
            # print("x: ",x) # prints: [(1,)]
            # print("x: ",x[0][0]) # < use that for 1 value returns
            if x[0][0] == 0:
                # insert user:
                sql_prepared = """insert into mathu_similarity_index_database.users (email,user_name,password,password_salt,is_admin) values (%s,%s,%s,%s,%s);"""
                sql_mutation(sql_prepared, (useremail,"None",password,password,False,))
                sql_prepared = """insert into mathu_similarity_index_database.user_settings (user_email, dark_theme) values (%s,%s);"""
                sql_mutation(sql_prepared, (useremail,False,))

                # Select user
                # sql_prepared = """SELECT count(*) FROM mathu_similarity_index_database.users where email like %s;"""
                # results = sql_query(sql_prepared, (useremail,))

                # Global server data
                apikey = generate_key("web")
                GLOBAL_SERVER_DATA["users"][useremail] = dict()
                GLOBAL_SERVER_DATA["users"][useremail]["web_key"] = apikey
                GLOBAL_SERVER_DATA["users"][useremail]["apikeys"] = dict()
                reset_interval = 60*60 # 1 hour
                GLOBAL_SERVER_DATA["users"][useremail]["apikeys"][apikey] = APIKey(apikey, 2, useremail, 5000, datetime(9999, 12, 31, 23, 59, 59), 1, True, reset_interval)


                payload = {
                    "success": True,
                    "msg": "Signup Success",
                    "user": {
                        "useremail": useremail,
                        "username": "None",
                        "apikey": apikey,
                        "isadmin": False,
                        "darktheme": False
                    }
                }
                return payload
            else:
                payload = {
                    "success": False,
                    "msg": "Signup Failed, email already exists"
                }
                return payload
        else:
            payload = {
                "success": False,
                "msg": "Signup Failed, not a valid email"
            }
            return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_add_equation(obj, info, useremail, apikey, equation):
    print("resolve_add_equation")
    # Authenticate as admin
    # Insert
    sql_prepared = """//"""

    payload = {
        "success": False,
        "msg": "Access Denied",
        # "equation": {
        #     "id": 0,
        #     "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>",
        #     "latex": "1+2",
        #     "type": "Equation",
        #     "category": "Addition"
        # }
    }
    return payload

def resolve_set_server_settings(obj, info, useremail, apikey, password, autocaching):
    try:
        print("resolve_set_server_settings")

        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey, [1,3])
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        GLOBAL_SERVER_CONFIG_AUTO_CACHE = autocaching

        payload = {
            "success": True,
            "msg": ""
        }
        return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_set_theme(obj, info, useremail, apikey, darktheme):
    print("resolve_set_theme")

    payload = {
        "success": False,
        "msg": "Access Denied"
    }
    return payload

# todo remove equation