import json
import requests


#Return the ids of all children of a given node
def get_children(menus, menu, seen):
	#Assume all children are valid
	valid = True
	
	#If we're at an end node, stop recursing
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
			
			#Add child to current list of ids before recursing
			#Without this line, non-end nodes won't be added to the list
			ids.append(id)
			
			ret_ids, ret_valid = get_children(menus, menus[id], seen)
			
			#Add child ids to current tally
			ids += ret_ids
			
			#This node is only valid if all subnodes are also valid
			valid = valid and ret_valid
			
	return ids, valid

def main(url):
	menus = {}
	page = 0

	while True:
		page += 1
		r = requests.get(url+str(page))
		response = json.loads(r.text)

		#Add menu objects to a dictionary keyed by id
		for menu in response["menus"]:
			menus[menu["id"]] = menu

		if len(menus) >= response["pagination"]["total"]:
			break
		
	#print(json.dumps(menus, indent=4, sort_keys=True))

	#Isolate root menus
	parents = [menus[id] for id in menus if "parent_id" not in menus[id]]   

	valid = []
	invalid = []

	for parent in parents:
		
		child_ids, valid_flag = get_children(menus, parent, [])

		return_value = {"root_id" : parent['id'], "children" : child_ids}

		if valid_flag:
			valid.append(return_value)
		else:
			invalid.append(return_value)
			
	print(json.dumps({"valid_menus" : valid, "invalid_meus" : invalid}, indent=4))

if __name__ == '__main__':
	CHALLENGE_ID = input("Which challenge? (1|2) ")

	url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=" + CHALLENGE_ID + "&page="

	main(url)