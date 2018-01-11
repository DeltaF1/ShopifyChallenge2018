import json
import requests

CHALLENGE_ID = 1

url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=" + CHALLENGE_ID + "&page="

menus = {}

page = 0

while True:
    r = requests.get(url+str(page))
    response = json.loads(r.text)

    for menu in response['menus']:
        menus[menu['id']] = menu

    page += 1
    print("nodes: "+str(len(menus)))

    if len(menus) >= response['pagination']['total']:
        break
    
print(json.dumps(menus, indent=4, sort_keys=True))

parents = [menus[id] for id in menus if "parent_id" not in menus[id]]   

valid = []
invalid = []

def get_children(menu, seen):
    valid = True
    if not menu["child_ids"]:
        return [], True
    ids = []
    for id in menu["child_ids"]:
        if id in seen:
            valid = False
        else:
            seen.append(id)
            if id not in menus:
                #invalid: missing menu
                valid = False
                continue
            ids.append(id)
            child = menus[id]
            ret_ids, ret_valid = get_children(child, seen)
            ids += ret_ids
            valid = valid and ret_valid
    return ids, valid

for parent in parents:
    
    
    child_ids, valid_flag = get_children(parent, [])

    return_value = {"root_id" : parent['id'], "children" : child_ids}


    if valid_flag:
        valid.append(return_value)
    else:
        invalid.append(return_value)
        
