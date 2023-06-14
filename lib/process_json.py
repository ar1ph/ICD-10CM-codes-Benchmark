import json
# Gets the path of the src_file (.json) 
# Return the contents in dictionary format
def get_dict_from_json(src_file):
    return get_contents_from_json(src_file)

def get_contents_from_json(src_file):
    try:  
        with open(file=src_file, mode='r') as contents: 
            return json.load(contents)
    except Exception as e:
        print('Error occured while reading config file: ' + str(e))
        return None
    
# Gets the path of the dest_file (.json) and dictionary
# Writes the contents of the dictionary in that file
def store_dict_in_json(dest_file, contents):
    try:
        with open(file=dest_file, mode='w') as json_file:
            json.dump(contents, json_file)
            return True
    except Exception as e:
        print('Error occured while reading config file: ' + str(e))
        return False
    


def main():
    d = {"Hello": "World",
         "Phone": 123}
    
    store_dict_in_json(dest_file='test.json', contents=d)
    d2 = get_dict_from_json("test.json")
    for k in d:
        assert(k in d2 and d[k] == d2[k])
    
    print("Test passed")


if __name__ == "__main__":
    main()