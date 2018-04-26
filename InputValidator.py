# Henry Warren 2018

import re
import sys
from Tests import tests
from random import randint

ADD_REGEX = (r'(((O(’|\'))?[A-Z][a-z]+)(( |(, )|-)((O(’|\'))?([A-Z][a-z]+)'
             r'|([A-Z].))){0,2}) (([1-9]{3}\d{7})|(\+?(1?)(\d{5}|\(\d{3}\))'
             r'(\d{3})-(\d{4}))|((\d{5})(.(\d{5}))?)|(\d{3}\.\d{3}\.\d{4})|'
             r'(\d{3}-\d{3}-\d{4})|((\d{3} (\d{1} )?)?\d{3} \d{3} \d{4})|'
             r'(\d{3}-\d{4})|(\+[1-9]{2} \(\d{2}\) \d{3}-\d{4}|((\+1) \d{3}'
             r' \d{3} \d{4})))')
DEL_REGEX = (r'(((O(’|\'))?[A-Z][a-z]+)(( |(, )|-)((O(’|\'))?([A-Z][a-z]+)'
             r'|([A-Z].))){0,2})|(([1-9]{3}\d{7})|(\+?(1?)(\d{5}|\(\d{3}\))'
             r'(\d{3})-(\d{4}))|((\d{5})(.(\d{5}))?)|(\d{3}\.\d{3}\.\d{4})|'
             r'(\d{3}-\d{3}-\d{4})|((\d{3} (\d{1} )?)?\d{3} \d{3} \d{4})|'
             r'(\d{3}-\d{4})|(\+[1-9]{2} \(\d{2}\) \d{3}-\d{4}|((\+1) \d{3}'
             r' \d{3} \d{4})))')
NAME_GROUP = 1
PHONENUM_GROUP = 13



class UserRecord:
    """ Database record. Stores name and phone number and 
        has method to nicely print them out. """
    def __init__(self, name, phone_number, rec_id):
        self.name = name
        self.phone_number = phone_number
        self.rec_id = rec_id


    def __str__(self):
        return "{} : {}".format(self.name, self.phone_number)



class InputValidator:
    """ Validation engine and gatekeeper to database """
    def __init__(self):
        self.db = []
        self.id_increment = randint(1,999)
        self.add_regex = re.compile(ADD_REGEX)
        self.del_regex = re.compile(DEL_REGEX)


    def print_list(self):
        """ attempt to prettyprint database contents """
        try:
            print(">>>>>>>> Database >>>>>>>>")
            if len(self.db) == 0:
                print("(empty)")
            for record in self.db:
                print(str(record))
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
            return True
        except:
            return False


    def sanitize(self, phone_number):
        """ reduces phone number to digit string, stripping the formatting """
        return ''.join(filter(lambda x: x.isdigit(), phone_number))


    def add_record(self, name, phone_number):
        """ add database record from given input """
        try:
            phone_number = self.sanitize(phone_number)
            for i, record in enumerate(self.db):
                if record.name == name and record.phone_number == phone_number:
                    print("ERROR: Duplicate Record Detected")
                    return False
            record = UserRecord(name, phone_number, self.id_increment)
            self.db.append(record)
            self.id_increment += 1
            return True
        except:
            return False


    def del_by_id(self, rec_id):
        """ delete a record by its id """
        for i, rec in enumerate(self.db):
            if rec.rec_id == rec_id:
                self.db.pop(i)
                return True
        return False


    def find_by_name(self, name, context=None):
        """ attempt to find record by name """
        if not context:
            context = self.db
        found_entries = []
        for i, record in enumerate(context):
            if record.name == name:
                found_entries.append(record)
        # desired case (1 entry for key)
        if len(found_entries) == 1:
            return self.del_by_id(found_entries[0].rec_id)
        # expected case (>1 entry for key)
        elif len(found_entries) > 1:
            print("Multiple Records Found... "
                "Please Specify the Telephone # for the Account as well")
            phone_number = input("> ")
            phone_number = self.sanitize(phone_number)
            return self.find_by_tel(phone_number, context=found_entries)
        # default case (no entry for key)
        else:
            if context == self.db:
                print("ERROR: Unable to Locate Record for Name={}".format(name))
                return False
            else:
                print("ERROR: Unable to Locate Record")
                return False


    def find_by_tel(self, phone_number, context=None):
        """ attempt to find record by phone number """
        if not context:
            context = self.db
        found_entries = []
        for i, record in enumerate(context):
            if record.phone_number == phone_number:
                found_entries.append(record)
        # desired case (1 entry for key)
        if len(found_entries) == 1:
            return self.del_by_id(found_entries[0].rec_id)
        # expected case (>1 entry for key)
        elif len(found_entries) > 1:
            print("Multiple Records Found... "
                "Please Specify the Name for the Account as well")
            name = input("> ")
            return self.find_by_name(name, context=found_entries)
        # default case (no entry for key)
        else:
            if context == self.db:
                print("ERROR: Unable to Locate Record for Tel={}".format(phone_number))
                return False
            else:
                print("ERROR: Unable to Locate Record")
                return False


    def validate(self, user_input):
        """ attempt to validate user input and return a success or failure """
        parts = user_input.split(' ',1)
        cmd = parts[0]
        if cmd.upper() == "ADD":
            if len(parts) == 2:
                content = parts[1]
                result = self.add_regex.match(content)
                if result is not None:
                    # check that the regex matches the entire line
                    if result.group() == parts[1]:
                        name = result.group(NAME_GROUP)
                        phone_number = result.group(PHONENUM_GROUP)
                        return self.add_record(name, phone_number)
        elif cmd.upper() == "DEL":
            if len(parts) == 2:
                content = parts[1]
                result = self.del_regex.match(content)
                if result is not None:
                    # check that the regex matches the entire line
                    if result.group() == parts[1]:
                        if result.group(NAME_GROUP) is not None:
                            name = result.group(NAME_GROUP)
                            return self.find_by_name(name)
                        elif result.group(PHONENUM_GROUP) is not None:
                            phone_number = self.sanitize(result.group(
                                                        PHONENUM_GROUP))
                            return self.find_by_tel(phone_number)
        elif cmd.upper() == "LIST":
            return self.print_list()
        elif cmd.upper() == "HELP":
            print(" ADD <Name> <Phone Number>")
            print(" DEL <Name> or <Phone Number>")
            print(" LIST")
            print(" HELP\n")
            return True
        print("Invalid Input")
        return False


if __name__ == "__main__":
    validator = InputValidator()
    # DEBUG CASE TESTING
    if len(sys.argv) == 2:
        for i, case in enumerate(tests()):
            validator.validate(case)
    print(" ***********************")
    print(" *                     *")
    print(" *  GLOBAL PHONE BOOK  *")
    print(" *                     *")
    print(" ***********************")
    print("Enter HELP for commands list")
    while True:
        user_input = input("> ")
        res = validator.validate(user_input)
        if res:
            print("[ACTION COMPLETE]")
        if not res:
            print("[ACTION FAILED]")
