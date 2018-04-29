*******************************************************
*                                                     *
*              Pacific Bell Telephone CLI             *
*                  (Henry Warren 2018)                *
*                                                     *
*******************************************************

DEPENDENCIES
- Python 3

RUN INSTRUCTIONS
- Navigate to directory containing .py source files
    $ cd InputValidation/src/

- Execute the program in one of two modes
    1. Manual Mode (manually enter commands one at a time)
       $ python3 InputValidator.py

    2. Auto Mode (pass the program a text file containing line-delimited commands
                  to be run sequentially by the program. Example cmdlist.txt file included)
       $ python3 InputValidator.py <cmdlist-file>