from db.handlers.users import *
from db.connect_db import sql_query, sql_mutation

def get_user_favorite_problems():
    pass

def add_user_favorite_problem(problemid, useremail): #problemid: Int, useremail: String, apikey: String
    pars = (useremail, problemid,)
    sql_prepared = """insert into favorites (user_email, problem_id) values (%s, %s);"""
    sql_mutation(sql_prepared, pars)

def remove_user_favorite_problem(problemid, useremail):
    pars = (useremail, problemid,)
    sql_prepared = """delete from favorites where user_email = %s and problem_id = %s;"""
    sql_mutation(sql_prepared, pars)

def get_user_history():
    pass

def add_user_history():
    pass

def is_favorite(problemid, useremail):
    pars = (useremail, problemid,)
    sql_prepared = """select exists(select distinct user_email from favorites where user_email like %s and favorites.problem_id = %s) as favorite;"""
    res = sql_query(sql_prepared, pars)
    return res[0][0] == 1