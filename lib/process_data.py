import os
import process_codes



# Function for retrieving the old subset of codes.csv
# Function for getting the codes
# Function for getting associated medical condition
# Function for getting just the disease


DATA_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'data')
ASSETS_DIRECTORY = os.path.join(os.path.abspath(os.pardir), 'assets')


def get_codes_subset():
    pass

# Returns a list of all the file names 
# Assumes that files are txt files
def get_all_file_names(with_format=False):
    file_names = []
    try:
        for _, _, files in os.walk(DATA_DIRECTORY):
            for fl in files:
                if with_format:
                    file_names.append(fl)
                else:
                    file_names.append(fl[:-4])
        return file_names
    except Exception as e:
        print("Error occured while accessing file names: " + str(e))
        return None
    
# Returns all codes using the file names from DATA_DIRECTORY
def get_all_codes():
    all_codes = []
    all_file_names = get_all_file_names()
    if all_file_names == None:
        print("Error occured while getting all codes: " + str(e))
        return None
    for name in all_file_names:
        code = "".join(name.split("."))
        all_codes.append(code)
    return all_codes

# Helper function to convert file name to code
def file_name_to_code(file_name, with_format=False):
    if with_format:
        return "".join(file_name.strip().split(".")[:-1])
    else:
        return "".join(file_name.strip().split("."))

# Gets a subset of codes.csv with codes from DATA_DIRECTORY
def get_new_subset_of_codes(store=False, full_row=False):
    all_codes = get_all_codes() # List of full codes in codes.csv
    if all_codes == None:
        print("Error occured while getting new subset: " + str(e))
        return None
    code_map = process_codes.get_rows_from_codes(all_codes, full_row)
    if code_map == None:
        print("Error occured while getting new subset: " + str(e))
        return None
    if store:
        # TODO: Create a function to store code map in store.csv in assets
        pass
    return code_map
    
    


def main():

    file_names_with_format = get_all_file_names(with_format=True)
    file_names_without_format = get_all_file_names()
    print(file_names_with_format)
    print(file_names_without_format)


if __name__ == "__main__":
    main()