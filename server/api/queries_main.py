from db.connect_db import MySQLDatabase, sql_query, sql_q_test, sql_query_custom
from datetime import datetime
from db.handlers.problems import get_all_problems_favorite_autocache
from db.handlers.users_shared import get_user_favorite_problems
from db.handlers.users import get_user_data
# from config import *
from config import *
from services.tools import get_date_time_type
# from services.confidence_calc import get_all as get_all_conf
from services.authentication import authenticate, generate_key, APIKey

import re

from app import GLOBAL_SERVER_DATA
from app import GLOBAL_SERVER_CONFIG_AUTO_CACHE, GLOBAL_SERVER_CONFIG_SEQURITY

# import latex2mathml.converter

#tests:
# def set_test_global_nolock(obj, info, index, data):
#     # print(GLOBAL_SERVER_DATA)
#     GLOBAL_SERVER_DATA[index] = data
#     return GLOBAL_SERVER_DATA[index]

# def get_test_global_nolock(obj, info, index):
#     # print(GLOBAL_SERVER_DATA)
#     return GLOBAL_SERVER_DATA[index]

# def get_test_global_nolock_full(obj, info):
#     return str(GLOBAL_SERVER_DATA)

# def test_sessions_var(obj, info):
#     # if 'int_val' in session:
#     #     temp = "session value: " + session["users"]["default"]
#     #     counter = session["int_val"]
#     #     session["int_val"] = counter+1
#     #     var_value = "def-test-value_"+str(session["int_val"])
#     #     session["users"]["default"] = var_value
#     #     return temp
#     # else:
#     #     session['users'] = dict()
#     #     session['int_val'] = 0
#     #     var_value = "def-test-value_"+str(session["int_val"])
#     #     session['users']["default"] = var_value
#     #     temp = "session value: " + session["users"]["default"]
#     #     return temp
    
#     global index_add_counter
#     temp = index_add_counter
#     index_add_counter = temp+1
#     return temp

#main:
def resolve_api_status(obj, info):
    print("resolve_api_status")
    return f'API is running'

def resolve_get_all_equations(obj, info, useremail, apikey):
    try:
        print("resolve_get_all_equations")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey)
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        # get all equations from database
        sql = "SELECT problem_id, problem FROM mathu_similarity_index_database.problems;"

        db = MySQLDatabase()
        db.set_default()
        db.connect_to_db()
        results = db.execute_query(sql)

        payload = []

        for id, problem in results:
            # print(str(id) + problem)
            payload.append({
                "id": str(id),
                "mathml": problem,
                "latex": problem
            })

        #stubbed - todo
        final_payload = {
            "success": True,
            "msg": "",
            "equations": payload
        }
        return final_payload
        #return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

# def resolve_search(obj, info, input, isloggedin, useremail, apikey):
#     print("resolve_search")
#     print("input:", input, "\tislogedin", isloggedin, "\tuseremail", useremail, "\tapikey",apikey)

#     # sql = "SELECT problem_id, problem, levenshtein2(problem, '" + input + "') AS distance FROM problems ORDER BY distance ASC;"
#     # sql = "SELECT problem_id, problem, 0 AS distance FROM problems;"
#     sql = "SELECT problem_id, problem, user_search, has_memo FROM mathu_similarity_index_database.problems;"
#     db = MySQLDatabase()
#     db.set_default()
#     # db.print_config_db()
#     db.connect_to_db()
#     results = db.execute_query(sql)

#     # results = get_all_conf(input, results, 1, 4)

#     ids = []
#     problems = []
#     similarities = []
#     indexed_problems = []
#     for id, problem, user_search, has_memo, similarity in results:
#         ids.append(id)
#         problems.append(problem)
#         similarities.append(similarity)

#         # print(id)

#         # indexed_prob = {
#         #     "id" : id,
#         #     "problem" : problem,
#         #     "similarity" : similarity
#         # }

#         # indexed_problems.append(indexed_prob)

#     db.commit()

#     # mark problem for insert problem if not in db
#     insert_problem = False
#     if similarities[0] > 0:
#         insert_problem = True

#     # sql = "INSERT INTO problems(problem) VALUES('" + input + "');"
#     db_insert = MySQLDatabase()
#     db_insert.set_default()
#     # db_insert.print_config_db()
#     db_insert.connect_to_db()
#     try:
#         sql = "INSERT INTO mathu_similarity_index_database.history (user_email, search_input, date_time) VALUES ('" + useremail + "', '" + input + "', '" + str(datetime.now()) + "');"
#         print("insert sql: ",sql)
#         db_insert.execute_query(sql)
#     except:
#         print("sql error")
#     finally:
#         db_insert.commit()

#     indexed_problems_len = len(ids)

#     min_sim = 0
#     max_sim = similarities[indexed_problems_len-1]

#     if(max_sim == 0):
#         max_sim = 1

#     equations = []

#     for i in range(indexed_problems_len):
#         sim = similarities[i]
#         inverse_sim = max_sim - sim
#         normalized_sim = inverse_sim / (max_sim) * 100

#         similarities[i] = normalized_sim

#         equations.append({
#             "equation": {
#                 "id": ids[i],
#                 "mathml": problems[i],
#                 "latex": problems[i]
#             },
#             "similarity": similarities[i]
#         })

#     payload = {
#         "numberofresults": indexed_problems_len,
#         "equations": equations
#     }

#     # payload = {
#     #     "numberofresults": 2,
#     #     "equations": [
#     #         {
#     #             "equation": {
#     #                 "id": 1,
#     #                 "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>",
#     #                 "latex": "1+2",
#     #                 "type": "Equation",
#     #                 "category": "Addition"
#     #             },
#     #             "similarity": 0
#     #         },
#     #         {
#     #             "equation": {
#     #                 "id": 2,
#     #                 "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>",
#     #                 "latex": "3-2",
#     #                 "type": "Equation",
#     #                 "category": "Subtraction"
#     #             },
#     #             "similarity": 0
#     #         }
#     #     ]
#     # }
#     return payload

def resolve_get_user_history(obj, info, useremail, apikey):
    try:
        print("resolve_get_user_history")

        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey)
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        valid_email = re.match(r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$", useremail)
        if (not valid_email):
            return {
                "success": False,
                "msg": "Invalid email address"
            }

        # payload = [{
        #         "id": 3,
        #         "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>',
        #         "latex": "1+2",
        #         "type": "Equation",
        #         "category": "Addition"
        #     },
        #     {
        #         "id": 2,
        #         "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>',
        #         "latex": "3-2",
        #         "type": "Equation",
        #         "category": "Subtraction"
        #     }]
        payload = []

        # print(useremail)

        sql = "SELECT user_email, search_input, date_time FROM mathu_similarity_index_database.history where user_email LIKE '" + useremail + "' ORDER BY date_time desc;"
        db = MySQLDatabase()
        db.set_default()
        db.connect_to_db()
        results = db.execute_query(sql)

        emails = []
        problems = []
        dates = []
        for email, problem, date in results:
            emails.append(email)
            problems.append(problem)
            dates.append(date)

            eq = {
                "id": 0,
                "mathml": "",
                "latex": problem,
                "issearch": True
            }

            payload.append(eq)

        final_payload = {
            "success": False,
            "msg": "",
            "equations": payload
        }
        return final_payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_get_all_comments(obj, info, useremail, apikey):
    print("resolve_get_all_comments")
    payload = [
        {
            "problemid": 0,
            "datetime": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 0,
                "nano": 0,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment"
        },
        {
            "problemid": 0,
            "datetime": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 1,
                "nano": 0,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment 2"
        },
        {
            "problemid": 1,
            "datetime": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 1,
                "nano": 0,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment 3"
        }
    ]
    payload = []
    #stubbing - todo
    final_payload = {
        "success": False,
        "msg": "Access Denied",
        # "comments": payload
    }
    return final_payload

def resolve_get_comments(obj, info, useremail, apikey, problemid):
    try:
        print("resolve_get_comments")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey)
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        # get comments
        payload = []
        sql_prepared = """SELECT problem_id, date_time, nanosecond, user_email, comment FROM mathu_similarity_index_database.comments where problem_id = %s order by date_time;"""
        result = sql_query(sql_prepared, (problemid,))

        for problem_id, date_time, nanosecond, user_email, comment in result:
            # str = date_time+"."+nanosecond
            # print(date_time)
            # print(date_time.__class__.__name__)
            # dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
            dt = datetime.now()
            comment = {
                "problemid": problem_id,
                "datetime": get_date_time_type(date_time),
                "useremail": user_email,
                "comment": comment
            }

            payload.append(comment)

        final_payload = {
            "success": True,
            "msg": "",
            "comments": payload
        }
        return final_payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_get_favorite_problems(obj, info, useremail, apikey):
    try:
        print("resolve_get_favorite_problems")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey)
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        res = get_user_favorite_problems(useremail)
        print("payload\n\n")
        tempArr = []
        for problem_id, problem, user_search, has_memo, favorite, tags, links in res:
            tagsArr = []
            for tag_id, tag_name, tag_description in tags:
                tag = {
                    "id": tag_id,
                    "name": tag_name,
                    "description": tag_description
                }
                tagsArr.append(tag)

            temp = {
                "id": problem_id,
                "latex": problem,
                "tags": tagsArr,

                "mathml": "",

                "memolinks": links,

                "favorite": favorite,
                "issearch": user_search,
            }
            tempArr.append(temp)

        payload = {
            "success" : True,
            "msg" : "Successfully retrieved favorite problems",
            "equations" : tempArr
        }
        print(payload)
        return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_authenticate_login(obj, info, apikey, useremail, password):
    try:
        print("resolve_authenticate_login")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate("default", apikey, [1,3])
        # if apikey != "Qx0m5eK38EHYNNwxcytbkpWR92KNTnrOQbBETydtHr2B57LrEyjnaksbeQXJ":
        if not auth:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        valid_email = re.match(r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$", useremail)
        invalid_format = True
        if valid_email:
            invalid_format = False
            print("valid email")
        print("invalid_format: " + str(invalid_format))
        if (invalid_format) or (useremail == "") or (useremail == None):
            if (useremail == "default") or (useremail == "admin"):
                print("default or admin")
            else:
                payload = {
                    "success": False,
                    "msg": "Invalid email format"
                }
                return payload

        if useremail == "default":
            payload = {
                "success": True,
                "msg": "Successfully logged in",
                "useremail": useremail,
                "apikey": apikey
            }
            return payload
        elif useremail == "admin":
            payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return payload
        else:
            results = get_user_data(useremail) # returns: email, user_name, password, password_salt, is_admin
            try:
                user_email, user_name, user_password, password_salt, is_admin = results[0]
                if user_password == password:
                    # local user data
                    #

                    # generate apikey
                    apikey = "key1"

                    # global server data
                    # if not exists, create
                    if user_email in GLOBAL_SERVER_DATA["users"]:
                        print("user exists")
                        apikey = GLOBAL_SERVER_DATA["users"][user_email]["web_key"]
                    else:
                        print("user does not exist")
                        apikey = generate_key("web")
                        print("apikey: " + apikey)
                        GLOBAL_SERVER_DATA["users"][user_email] = dict()
                        print("created user dict")
                        GLOBAL_SERVER_DATA["users"][user_email]["web_key"] = apikey
                        print("set web_key")
                        GLOBAL_SERVER_DATA["users"][user_email]["apikeys"] = dict()
                        print("created apikeys dict")
                        reset_interval = 60*60 # 1 hour
                        print("reset_interval: " + str(reset_interval))
                        apikey_obj = APIKey(str(apikey), 2, useremail, 5000, datetime(9999, 12, 31, 23, 59, 59), 1, True, reset_interval)
                        print("created apikey_obj")
                        GLOBAL_SERVER_DATA["users"][user_email]["apikeys"][apikey] = apikey_obj
                        print("created data")


                    payload = {
                        "success": True,
                        "msg": "Login Success",
                        "user": {
                            "useremail": user_email,
                            "username": "none",
                            "apikey": apikey,
                            "isadmin": is_admin,
                            "darktheme": False
                        }
                    }
                    return payload
            except:
                payload = {
                    "success": False,
                    "msg": "Invalid email or password"
                }
                return payload

        # payload = {
        #     "success": True,
        #     "msg": "Login Success",
        #     "user": {
        #         "useremail": "test@email.com",
        #         "username": "none",
        #         "apikey": "testkey",
        #         "isadmin": False,
        #         "darktheme": False
        #     }
        # }
        # return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_get_server_settings(obj, info, useremail, apikey):
    try:
        print("resolve_get_server_settings")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey, [3])
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        payload = {
            "success": True,
            "msg": "Success",
            "autocaching": GLOBAL_SERVER_CONFIG_AUTO_CACHE
        }
        return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_get_all_tags(obj, info, useremail, apikey):
    try:
        print("resolve_get_all_tags")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey)
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        # print("arr",testarr)
        # print("api key: ",apikey)

        # results = sql_query("SELECT tag_id, tag_name, description FROM mathu_similarity_index_database.tags;")
        sql = "SELECT tag_id, tag_name, description FROM mathu_similarity_index_database.tags;"
        # for i in range(0,1):
        #     db = MySQLDatabase()
        #     db.set_default()
        #     results2 = sql_q_test(sql, db)
        #     print(results2.__class__.__name__)
        #     results = results2.fetchall()
        #     print(results.__class__.__name__)
        #     results2.close()
        #     db.commit()
        #     db.close()
        # db.connect_to_db()
        # results = db.execute_query(sql)

        results = sql_query_custom(sql, MySQLDatabase())

        # print("slq done")
        # print(results[0][0])
        # print(results)

        payload = []

        for id, name, description in results:
            tag = {
                "id": id,
                "name": name,
                "description": description
            }

            payload.append(tag)

        final_payload = {
            "success": True,
            "msg": "",
            "tags": payload
        }
        return final_payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload

def resolve_get_problem(obj, info, useremail, apikey, problemid):
    final_payload = {
        "success": False,
        "msg": "Not Available"
    }
    return final_payload

def resolve_get_permanent_apiKey(obj, info, useremail, apikey):
    try:
        print("resolve_get_permanent_apiKey")
        # Auth
        print("apikey: " + apikey)
        auth = authenticate(useremail, apikey, [1,2,3])
        if (not auth) and GLOBAL_SERVER_CONFIG_SEQURITY:
            final_payload = {
                "success": False,
                "msg": "Access Denied"
            }
            return final_payload

        apikey = "temp"

        if useremail in GLOBAL_SERVER_DATA["users"]:
            print("user exists")
            if "perm_key" in GLOBAL_SERVER_DATA["users"][useremail]:
                apikey = GLOBAL_SERVER_DATA["users"][useremail]["perm_key"]
            else:
                print("no perm_key")
                apikey = generate_key("per")
                GLOBAL_SERVER_DATA["users"][useremail]["perm_key"] = apikey
                reset_interval = 60*60 # 1 hour
                GLOBAL_SERVER_DATA["users"][useremail]["apikeys"][apikey] = APIKey(apikey, 0, useremail, 5000, datetime(9999, 12, 31, 23, 59, 59), 1, True, reset_interval)

        else:
            print("user not found")
            apikey = generate_key("per")
            GLOBAL_SERVER_DATA["users"][useremail] = dict()
            GLOBAL_SERVER_DATA["users"][useremail]["perm_key"] = apikey
            GLOBAL_SERVER_DATA["users"][useremail]["apikeys"] = dict()
            reset_interval = 60*60 # 1 hour
            GLOBAL_SERVER_DATA["users"][useremail]["apikeys"][apikey] = APIKey(apikey, 0, useremail, 5000, datetime(9999, 12, 31, 23, 59, 59), 1, True, reset_interval)

        print(GLOBAL_SERVER_DATA["users"][useremail]["apikeys"])

        payload = {
            "success": True,
            "msg": "Success",
            "data": apikey
        }
        return payload
    except:
        payload = {
            "success": False,
            "msg": "TC-Error"
        }
        return payload