import sys
import json

def return_json():
    # a python dictionary
    a = {'name':'Sarah', 'age': 24, 'isEmployed': True }

    python2json = json.dumps(a)
    print (python2json)


def start_car():
    print("RoboCar started !!!")

def get_info():
    # print("Here is the requested info")
    return_json()


if sys.argv[1] == "START_CAR":
    start_car()

if sys.argv[1] == "GET_INFO":
    get_info()
    

