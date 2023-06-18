import string


class Variables(object):

    class _Instance(object):

        def __init__(self, 
                    variables : list[str],
                    instance : dict) -> None: 
            """
            Takes a list of variable names and their values
            Initializes after checking the values
            """
            self.variables = variables
            self.instance = dict()
            self._check_instance(instance)
            self.instance = instance

        def _check_instance(self, 
                            instance: dict) -> None:
            """
            Checks whether the instance is valid
            An instance is valid if the instance contains
            the values of all and only all the variables
            """
            if len(instance) > len(self.variables):
                raise Exception("Instances of all variables are not provided")
            if len(instance) < len(self.variables):
                raise Exception("Unnecessary instances are provided")
            for variable in self.variables:
                if variable not in instance:
                    raise Exception("Values of all variables aren't provided")
            

        def is_initialized(self) -> bool:
            """
            Return True iff all the values of the variables ar non None
            """
            for variable in self.instance:
                if self.instance[variable] == None:
                    return False
            return True

        def get_instance(self) -> dict:
            """
            Returns a map of the variable names and their values
            """
            return self.instance
        
        def __eq__(self, 
                   __value: object) -> bool:
            """
            Checks if two instances are equal
            """
            if not isinstance(self.__class__, __value):
                return False
            if len(__value) != len(self.variables):
                return False
            for variable in __value:
                value = __value[variable]
                if variable not in self.instance:
                    return False
                elif self.instance[variable] != value:
                    return False
            return True
        
        def __ne__(self, 
                   __value: object) -> bool:
            """
            Checks if two instances are not equal
            """
            return not self.__eq__(__value)
        
        def get_value(self,
                      variable: str) -> any:
            """
            Returns the value of a variable in the instance
            """
            if variable not in self.variables:
                raise Exception("No such variable exist")
            return self.variables.get(variable)
        

    

    def __init__(self,
                 variables : list[str]) -> None:
        self.check_variables(variables)
        self.variables : list[str] = variables
        self.instances : list[self._Instance] = []
        pass
        
    def check_variables(self, 
                        variables : list[str]) -> None:
        
        if type(variables) is not list:
            raise Exception("Should be called as a list of string")

        for variable in variables:
            if type(variable) is not str:
                raise Exception("Invalid variable")
            
        unique_variables : set = set(variables)
        if len(unique_variables) != len(variables):
            raise Exception("Variables must be unique")

    def add_instance(self, 
                     instance : dict) -> None:
        self.instances.append(self._Instance(variables=self.variables,
                                             instance=instance))
            
    def get_instances(self) -> dict:
        all_instances : dict = dict()
        for instance in self.instances:
            all_instances.ap
        return self.instances
    
    def get_variables(self) -> list[str]:
        return list(self.instances.keys())
    
    def __str__(self) -> str:
        return str(self.instances)
    
        
    def from_dictionary(self, 
                        var_dict : dict):
        all_variables = list(var_dict.keys())
        variable_obj = Variables(all_variables)
        if len(all_variables) == 0:
            return variable_obj
        instance = dict()
        all_instances = list(var_dict.values())
        num_of_instances = len(all_instances[0])
        try:
            for idx in range(num_of_instances):
                for variable in all_variables:
                    instance[variable] = var_dict[variable][idx]
            variable_obj.add_instance(instance=instance)
        except:
            raise Exception("Invalid dictionary")
        return variable_obj



class QueryTemplate(object):

    def __init__(self,
                 query : str) -> None:
        self.query : str = query
        self._initialize_variables(query)
        self.answers : list[str] = []

    def _initialize_variables(self, 
                              query : str) -> None:
        format_obj = string.Formatter().parse(query)
        all_variables = []
        for tup in format_obj:
            if tup[1] != None: all_variables.append(tup[1])
        self.variables = Variables(all_variables)

    def get_variables(self) -> list[str]:
        return self.variables.get_variables()

    def get_answers(self) -> list[str]:
        return self.answers
    
    def add_instance(self, 
                     var_instance: dict, 
                     answer: str) -> None:
        self.variables.add_instance(var_instance)

        pass

    # def add_

class FileTemplate(object):

    def __init__(self, 
                 file_name : str) -> None:
        self.__file_name : str = file_name
        self.__query_collection : list[str] = []

    def add_query(self, 
                  query : str) -> None:
        self.__queries.append(query)

    def display_queries(self) -> None:
        print(self.__queries)

    def get_file_name(self) -> list[str]:
        return self.__file_name
    
    def generate_json(self):
        pass
    
    def create_file(self) -> None:
        try:
            with open(file=self.__file_name, 
                      mode='w') as file_writer:
                pass
        except Exception as e:
            print("Error occured while creating the file: " + str(e))
        

    
def main():
    # Testing Variable class
    var_obj1 = Variables(["hel", "12"])
    print(var_obj1.get_instances())
    var_obj1.add_instance({"hel": 12, "12": "h1l"})
    print(str(var_obj1))
    # var_obj1.add_instance({"hel": 12, "12": "h1l", 12:"fas"})
    # var_obj1.add_instance({"hel": 12})
    pass

if __name__ == "__main__":
    main()