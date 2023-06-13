import csv
import os




CODE_DIRECTORY = os.path.join(os.path.abspath(os.pardir), "assets")
CODE_FILE = os.path.join(CODE_DIRECTORY, 'codes.csv')

# Row format = [Partial code, digit, Full code, desc, desc, disease]

# Gets an ICD-10 CM code description row 
# Returns the disease
def get_disease_from_row(row):
    try:
        return row[5]
    except Exception as e:
        print("Error occured while retrieving the disease: " + str(e))
        return None
    
# Gets an ICD-10 CM code description row 
# Returns the full code
def get_full_code_from_row(row):
    try:
        return row[2]
    except Exception as e:
        print("Error occured while retrieving the full code: " + str(e))
        return None
    
def get_medical_condition_from_row(row):
    try:
        return row[-2:]
    except Exception as e:
        print("Error occured while retrieving the medical condition: " + str(e))
        return None


# Returns list of all the codes related to a disease (IF available)
def get_all_codes(disease="", file=CODE_FILE):
    try:
        all_codes = []
        disease = disease.lower()
        with open(file=file, mode='r') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',')  
            for idx, row in enumerate(all_rows):
                row_code = get_full_code_from_row(row=row)
                if row_code == None:
                    print(f"Invalid row {idx + 1} in {file}")
                    return None
                if disease != "":
                    row_disease = get_disease_from_row(row=row)
                    if row_disease == None:
                        print(f"Invalid row {idx + 1} in {file}")
                        return None
                    row_disease = row_disease.lower()
                    if row_disease == disease: all_codes.append(row_code)
                else:
                    all_codes.append(row_code)
        return all_codes
    except Exception as e:
        print("Error occured while accessing codes: " + str(e))
        return None
    

# Returns a dictionary mapping full codes to disease and description
def get_dict_of_codes(disease="", file=CODE_FILE):
    try:
        dict_of_codes = dict()
        disease = disease.lower() 
        with open(file=file, mode='r') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',')  
            for idx, row in enumerate(all_rows):
                row_code = get_full_code_from_row(row=row)
                if row_code == None:
                    print(f"Invalid row {idx + 1} in {file}")
                    return None
                if disease != "":
                    row_disease = get_disease_from_row(row=row)
                    if row_disease == None:
                        print(f"Invalid row {idx + 1} in {file}")
                        return None
                    row_disease = row_disease.lower()
                    if row_disease == disease: 
                        dict_of_codes[row_code] = get_medical_condition_from_row(row)
                else:
                    dict_of_codes[row_code] = get_medical_condition_from_row(row)
        return dict_of_codes
    except Exception as e:
        print("Error occured while accessing codes: " + str(e))
        return None
    
# Gets a full ICD-10 code
# Returns the whole row in codes.csv file containing the code
def get_row_from_code(code="", file=CODE_FILE):
    try:
        code = code.upper()
        with open(file=file, mode='r') as csvfile:
            all_rows = csv.reader(csvfile, delimiter=',')  
            for idx, row in enumerate(all_rows):
                row_code = get_full_code_from_row(row=row)
                if row_code == None:
                    print(f"Invalid row {idx + 1} in {file}")
                    return None
                row_code = row_code.upper()
                if row_code == code:
                    return row
    except Exception as e:
        print("Error occured while accessing codes: " + str(e))
        return None
    
# Gets a list of full codes
# Returns a dictionary tha maps code to medical condition and disease
def get_rows_from_codes(codes=[], full_row=False, file=CODE_FILE):
    try:
        code_map = dict()
        for code in codes:
            if not full_row:
                code_map[code] = get_medical_condition_from_code(code, file)
            else:
                code_map[code] = get_row_from_code(code)
        return code_map
    except Exception as e:
        print("Error occured while accessing rows: " + str(e))
        return None
    
# Gets a full ICD-10 code. 
# Returns the medical codition and disease as a list
def get_medical_condition_from_code(code="", file=CODE_FILE):
    try:
        row =  get_row_from_code(code=code, file=file)
        return get_medical_condition_from_row(row)
    except Exception as e:
        print("Error occured while accessing codes: " + str(e))
        return None
def main():
    print(len(get_all_codes()))
    print(get_dict_of_codes(disease="Cholera"))
    print(get_medical_condition_from_code(code="A043"))
    print(get_row_from_code(code="A043"))
    print(len(get_dict_of_codes()))
    row = get_row_from_code(code="A043")
    print(get_medical_condition_from_code(code="A043"))
    print(get_medical_condition_from_row(row))
    print(get_disease_from_row(row))
    print(get_full_code_from_row(row))
    print(get_rows_from_codes(["A043", "A051"]))

if __name__ == "__main__":
    main()
