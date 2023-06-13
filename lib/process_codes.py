import csv
import os
 
# Function for returning a dictionary where keys are whole codes and values are rest of the info in list
# Function for getting the rows containing a code
# Function for getting medical condition given a code
# Function for getting codes based on the provided diseas

CODE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
CODE_FILE = os.path.join(CODE_DIRECTORY, 'codes.csv')

# Row format = [Partial code, digit, Full code, desc, desc, disease]

# Returns list of all the codes related to a disease()
def get_all_codes(disease=""):
    try:
        all_codes = []
        disease = disease.lower()
        with open(file=CODE_FILE, mode='r') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',') 
            count = 0
            for row in all_rows:
                if disease != "":
                    if row[-1].lower() == disease: all_codes.append(row[0])
                else:
                    all_codes.append(row[2])
        return all_codes
    except Exception as e:
        print("Error occured while accessing codes: " + str(e))
        return None
    

def main():
    print(len(get_all_codes()))


if __name__ == "__main__":
    main()
