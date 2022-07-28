from server.similarity import read_file, search_similarity
from server.db.connect_db import MySQLDatabase

import latex2mathml.converter

def resolve_api_status(obj, info):
    return f'API is running'

def resolve_get_all_equations(obj, info):
    # get all equations from database
    sql = "SELECT * FROM mathu_similarity_index_database.problems;"

    db = MySQLDatabase()
    results = db.execute_query(sql)

    payload = []

    for id, problem in results:
        payload.append({
            "id": id,
            "mathml": problem,
            "latex": "undefined",
            "type": "unknown",
            "category": "unknown"
        })

    # payload = [
    #     {
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
    #     }
    # ]
    return payload

def resolve_search(obj, info, input, islogedin, useremail, apikey):
    # print("input:", input)

    # sql = r"SELECT problem, levenshtein(problem, 'y^22+23 y-frac{256}{y(y+23)}=226') AS distance FROM problems ORDER BY distance ASC"
    # db = MySQLDatabase()
    # results = db.execute_query(sql)

    # for 
    # problems = read_file()

    # min_sim = 0
    # max_sim = indexed_problems[indexed_problems_len-1]['similarity']

    # if(max_sim == 0):
    #     max_sim = 1

    # equations = []

    # for i in range(indexed_problems_len):
    #     sim = indexed_problems[i]['similarity']
    #     inverse_sim = max_sim - sim
    #     normalized_sim = inverse_sim / (max_sim) * 100

    #     indexed_problems[i]['similarity'] = normalized_sim

    #     equations.append({
    #         "equation": {
    #             "id": indexed_problems[i]['id'],
    #             "mathml": indexed_problems[i]['problem'],
    #             "latex": "undefined",
    #             "type": "unknown",
    #             "category": "unknown"
    #         },
    #         "similarity": indexed_problems[i]['similarity']
    #     })
    
    # payload = {
    #     "numberofresults": indexed_problems_len,
    #     "equations": equations
    # }

    payload = {
        "numberofresults": 2,
        "equations": [
            {
                "equation": {
                    "id": 1,
                    "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>",
                    "latex": "1+2",
                    "type": "Equation",
                    "category": "Addition"
                },
                "similarity": 0
            },
            {
                "equation": {
                    "id": 2,
                    "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>",
                    "latex": "3-2",
                    "type": "Equation",
                    "category": "Subtraction"
                },
                "similarity": 0
            }
        ]
    }
    return payload

def get_user_history(obj, info, useremail, apikey):
    pass

def GetAllComments(obj, info, ):
    pass
def GetComments(obj, info, problemid):
    pass
def GetFavoriteProblems(obj, info, useremail):
    pass

def AuthenticateLogin(obj, info, useremail, passwordsalt):
    pass