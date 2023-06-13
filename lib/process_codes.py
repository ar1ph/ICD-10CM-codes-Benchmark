import csv
import os

# Function for getting all the codes
# Function for returning a dictionary where keys are codes and values are rest of the info in list
# Function for getting the rows containing a code
# Function for getting medical condition given a code
# Function for getting codes based on the provided diseas

CODE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
CODE_FILE = os.path.join(CODE_DIRECTORY, 'codes.csv')

# Returns list of all the codes
def get_all_codes():
    try:
        with open(file=CODE_FILE, mode='r') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',')
            for row in all_rows[:2]:
                print(row)

    except Exception as e:
        print("Error occured while accessing codes: " + str(e))
        return None
    

def main():
    
