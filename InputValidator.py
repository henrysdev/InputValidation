"""
ADD <Person> <Telephone #> - Add a new person to the database 
DEL <Person> - Remove someone from the database by name 
DEL <Telephone #> - Remove someone by telephone # 
LIST - Produce a list of the members of the database
"""
import re
import sys
from Tests import tests
from random import randint

ADD_REGEX = r'(((O(’|\'))?[A-Z][a-z]+)(( |(, )|-)((O(’|\'))?([A-Z][a-z]+)|([A-Z].))){0,2}) (([1-9]{3}\d{7})|(\+?(1?)(\d{5}|\(\d{3}\))(\d{3})-(\d{4}))|((\d{5})(.(\d{5}))?)|(\d{3}\.\d{3}\.\d{4})|(\d{3}-\d{3}-\d{4})|((\d{3} (\d{1} )?)?\d{3} \d{3} \d{4})|(\d{3}-\d{4})|(\+[1-9]{2} \(\d{2}\) \d{3}-\d{4}|((\+1) \d{3} \d{3} \d{4})))'
DEL_REGEX = r'(((O(’|\'))?[A-Z][a-z]+)(( |(, )|-)((O(’|\'))?([A-Z][a-z]+)|([A-Z].))){0,2})|(([1-9]{3}\d{7})|(\+?(1?)(\d{5}|\(\d{3}\))(\d{3})-(\d{4}))|((\d{5})(.(\d{5}))?)|(\d{3}\.\d{3}\.\d{4})|(\d{3}-\d{3}-\d{4})|((\d{3} (\d{1} )?)?\d{3} \d{3} \d{4})|(\d{3}-\d{4})|(\+[1-9]{2} \(\d{2}\) \d{3}-\d{4}|((\+1) \d{3} \d{3} \d{4})))'


"""
Database record. Stores name and phone number and 
has method to nicely print them out.
"""
class UserRecord:
    def __init__(self, name, phone_number, rec_id):
        self.name = name
        self.phone_number = phone_number
        self.rec_id = rec_id

    def __str__(self):
        return "{} : {}".format(self.name, self.phone_number)


"""
Validation engine and gatekeeper to database.
"""
class InputValidator:
    def __init__(self):
        self.db = []
        self.id_increment = randint(1,999)


    def print_list(self):
        print("********** Database **********")
        for record in self.db:
            print(str(record))
        print("******************************")


    def add_record(self, name, phone_number):
        record = UserRecord(name, phone_number, self.id_increment)
        self.db.append(record)
        self.id_increment += 1
        print("Success")


    def del_by_id(self, rec_id):
        for i, rec in enumerate(self.db):
            if rec.rec_id == rec_id:
                self.db.pop(i)
                print("Success")
                return


    def find_by_name(self, name, context=None):
        if not context:
            context = self.db
        found_entries = []
        for i, record in enumerate(context):
            if record.name == name:
                found_entries.append(record)
        # desired case (1 entry for key)
        if len(found_entries) == 1:
            self.del_by_id(found_entries[0].rec_id)
        # expection case (>1 entry for key)
        elif len(found_entries) > 1:
            print("Multiple Records Found... Enter the Telephone # for the Account as well: ")
            phone_number = input("> ")
            self.find_by_tel(phone_number, context=found_entries)
        # default case (no entry for key)
        else:
            if context == self.db:
                print("ERROR: Unable to Locate Record for Name={}".format(name))
            else:
                print("ERROR: Unable to Locate Record")


    def find_by_tel(self, phone_number, context=None):
        if not context:
            context = self.db
        found_entries = []
        for i, record in enumerate(context):
            if record.phone_number == phone_number:
                found_entries.append(record)
        # desired case (1 entry for key)
        if len(found_entries) == 1:
            self.del_by_id(found_entries[0].rec_id)
        # expection case (>1 entry for key)
        elif len(found_entries) > 1:
            print("Multiple Records Found... Enter the Name for the Account as well: ")
            name = input("> ")
            self.find_by_name(name, context=found_entries)
        # default case (no entry for key)
        else:
            if context == self.db:
                print("ERROR: Unable to Locate Record for Tel={}".format(phone_number))
            else:
                print("ERROR: Unable to Locate Record")


    def validate(self, user_input):
        parts = user_input.split(' ',1)
        cmd = parts[0]
        if cmd.upper() == "ADD":
            if len(parts) == 2:
                content = parts[1]
                result = re.match(ADD_REGEX, content)
                if result is not None:
                    # check that the regex matches the entire line
                    if result.group() == parts[1]:
                        name = result.group(1)
                        phone_number = result.group(13)
                        self.add_record(name, phone_number)
                        return
        elif cmd.upper() == "DEL":
            if len(parts) == 2:
                content = parts[1]
                result = re.match(DEL_REGEX, content)
                if result is not None:
                    # check that the regex matches the entire line
                    if result.group() == parts[1]:
                        if result.group(1) is not None:
                            self.find_by_name(result.group(1))
                            return
                        elif result.group(13) is not None:
                            self.find_by_tel(result.group(13))
                            return
        elif cmd.upper() == "LIST":
            self.print_list()
            return


if __name__ == "__main__":
    validator = InputValidator()
    # DEBUG CASE TESTING
    if len(sys.argv) == 2:
        for i, case in enumerate(tests()):
            print("\n>>>>[{}]>>>>\n{}\n--------".format(i,case))
            validator.validate(case)
            validator.print_list()
            print("\n<<<<<<<<")
    while True:
        user_input = input("> ")
        validator.validate(user_input)