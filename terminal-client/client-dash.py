import requests
import json


base_url = "http://127.0.0.1:5000"

## requests makers 
def get_envs():
    url = base_url + "/environments"
    req = requests.get(url).json()
    envs = req.values()
    for i in envs:
        del i['status_summary']
    return envs


def get_status_summary(env_name):
    url = base_url+"/getStatusSummary?environment=" + env_name
    req = requests.get(url).json()
    for i in req :
        del i["categories"]
    return req 


def get_machine_status(env_name, nid):
    url = base_url+"/getDetailedStatus?environment=" + env_name + "&nid=" + nid
    req = requests.get(url).json()
    services_status = []
    for i in req : 
        service = { i['name'] : i['status']}
        services_status.append(service)
    return services_status


def get_service_details(env_name, nid, service_name):
    url = base_url+"/getDetailedStatus?environment=" + env_name + "&nid=" + nid
    services = requests.get(url).json()  
    service_details = []
    for i in services : 
        if i['name'] == service_name :
            service_details = i['data']
            break
    return service_details




count = 0
# for fancy colors 
OKGREEN = '\033[92m'
OKBLUE = '\033[94m'
ENDC = '\033[0m'
RED = '\033[91m'
YELLOW = '\033[93m'
def out(value):
    print RED + "["+str(count)+"] :" + ENDC,
    print str(value)

def pretty_print(json_obj):
    print json.dumps(json_obj, sort_keys=True, indent=2, separators=(',', ': '))

def print_all_data(data):
    out("")
    if type(data) == list : 
        for i in data:
            pretty_print(i)
    else :
        print data 


    
    
user_in = ""

help = YELLOW+ """
welcome to the dashboard clinet terminal app 
envs: lists available environments
ENVNAME: status of env ENVNAME
ENVNAME/MACHINEID: status of MACHINE on ENVNAME
ENVNAMNE/MACHINE_ID/SERVICE_NAME: get service status at 'env_name/machine_nid/service_name'
help: usage 
for exit write 'exit'
""" + ENDC


envs = get_envs()
envs_list = map((lambda env : env['name']), envs)

print help
while(user_in != "exit") :
    user_in = raw_input(OKGREEN + "["+str(count)+"] : " + ENDC)
    user_in = user_in.split("/")
    user_in_len = len(user_in)
    if (user_in_len < 1):
        continue
    elif (user_in[0] == 'help'):
       print_all_data(help)
    elif(user_in[0] == 'envs'):
        print_all_data( envs)
    elif(user_in[0] in envs_list ):
        if(user_in_len < 2):
            res = get_status_summary(user_in[0])
            print_all_data(res)
        else : 
            if (user_in_len == 2) : 
               try:
                    res = get_machine_status(user_in[0], user_in[1])
                    print_all_data(res)
               except :
                   out("wrong machine name !")
               
                
            elif(user_in_len == 3) : 
                try:
                    res = get_service_details(user_in[0], user_in[1], user_in[2])
                    print_all_data(res)
                except :
                    out("wrong machine id or service name")
                
    elif(user_in[0] == 'exit'):
        out("Goodbye :D")
        break
    else : 
        out("wrong input :( ")
        continue
    count += 1
    print 

