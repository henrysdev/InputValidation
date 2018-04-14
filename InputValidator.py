"""
ADD <Person> <Telephone #> - Add a new person to the database 
DEL <Person> - Remove someone from the database by name 
DEL <Telephone #> - Remove someone by telephone # 
LIST - Produce a list of the members of the database 
"""
import re
import sys
from Tests import tests

ADD_REGEX = r'(((O’)?[A-Z][a-z]+)(( |(, )|-)((O’)?([A-Z][a-z]+)|([A-Z].))){0,2}) (([1-9]{3}\d{7})|(\+?(1?)(\d{5}|\(\d{3}\))(\d{3})-(\d{4}))|((\d{5})(.(\d{5}))?)|(\d{3}\.\d{3}\.\d{4})|(\d{3}-\d{3}-\d{4})|((\d{3} (\d{1} )?)?\d{3} \d{3} \d{4})|(\d{3}-\d{4})|(\+[1-9]{2} \(\d{2}\) \d{3}-\d{4}|((\+1) \d{3} \d{3} \d{4})))'
DEL_REGEX = r'(((O’)?[A-Z][a-z]+)(( |(, )|-)((O’)?([A-Z][a-z]+)|([A-Z].))){0,2})|(([1-9]{3}\d{7})|(\+?(1?)(\d{5}|\(\d{3}\))(\d{3})-(\d{4}))|((\d{5})(.(\d{5}))?)|(\d{3}\.\d{3}\.\d{4})|(\d{3}-\d{3}-\d{4})|((\d{3} (\d{1} )?)?\d{3} \d{3} \d{4})|(\d{3}-\d{4})|(\+[1-9]{2} \(\d{2}\) \d{3}-\d{4}|((\+1) \d{3} \d{3} \d{4})))'

TEST_CASES = tests()


class InputValidator:
    def __init__(self):
        self.db = {"tel":{},"name":{}}


    def print_list(self):
        for key in self.db["name"]:
            print("{} : {}".format(key,self.db["name"][key]))


    def add_record(self, name, phone_number):
        if phone_number not in self.db["tel"] and name not in self.db["name"]:
            self.db["tel"][phone_number] = name
            self.db["name"][name] = phone_number
        else:
            print("ERROR: Duplicate Record Detected. Unable to Add.")


    def del_by_name(self, name):
        if name in self.db["name"]:
            self.db["name"].pop(name)
        else:
            print("ERROR: Unable to Locate Record for Name={}".format(name))


    def del_by_tel(self, phone_number):
        if phone_number in self.db["tel"]:
            self.db["tel"].pop(phone_number)
        else:
            print("ERROR: Unable to Locate Record for Tel={}".format(phone_number))


    def validate(self, user_input):
        parts = user_input.split(' ',1)
        cmd = parts[0]
        if cmd == "ADD":
            if len(parts) == 2:
                content = parts[1]
                result = re.match(ADD_REGEX, content)
                if result is not None:
                    # check that the regex matches the entire line
                    if result.group() == parts[1]:
                        name = result.group(1) # 
                        phone_number = result.group(11)
                        self.add_record(name, phone_number)
                        return
            print("Failed")
        elif cmd == "DEL":
            if len(parts) == 2:
                content = parts[1]
                result = re.match(DEL_REGEX, content)
                if result is not None:
                    # check that the regex matches the entire line
                    if result.group() == parts[1]:
                        if result.group(1) is not None:
                            self.del_by_name(result.group(1))
                            return
                        elif result.group(11) is not None:
                            self.del_by_tel(result.group(11))
                            return
            print("Failed")
        elif cmd == "LIST":
            self.print_list()
        else:
            print("Invalid command. Exiting...")


if __name__ == "__main__":
    validator = InputValidator()
    # DEBUG CASE TESTING
    if len(sys.argv) == 2:
        for case in TEST_CASES:
            print("\n>>>>>>>>\n",case)
            validator.validate(case)
            validator.print_list()
            print("\n<<<<<<<<")
    while True:
        user_input = input("> ")
        validator.validate(user_input)