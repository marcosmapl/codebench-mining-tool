# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp

import keyword
import logging
import model
import os
import pandas as pd
import re
import statistics
import token
import tokenize

from collections import Counter, defaultdict
from datetime import datetime

from radon.metrics import h_visit
from radon.raw import analyze
from radon.visitors import ComplexityVisitor
from typing import Any


# Directory for the output '.csv' files (datasets)
CSV_FILE_OUTPUT_DIR = os.path.join(os.getcwd(), 'csv')

# Regular expression pattern for identifying errors
ERROR_PATTERN = re.compile('[a-zA-Z]*Error')

# Regular expression pattern for identifying CodeMirror events
CODEMIRROR_PATTERN = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}')

# Default file encoding for data files
DEFAULT_FILE_ENCODING = 'utf-8'

CODE_SEMESTER = 0
CODE_COURSE = 1
CODE_ASSIGNMENT = 2
CODE_USER = 3
CODE_EXECUTION = 4
CODE_SOLUTION = 5
CODE_LOGIN = 6
CODE_GRADE = 7
CODE_CODEMIRROR = 8

# Output filenames for different datasets
CSV_FILENAMES = {
    CODE_SEMESTER: 'semesters.csv',
    CODE_COURSE: 'courses.csv',
    CODE_ASSIGNMENT: 'assignments.csv',
    CODE_USER: 'users.csv',
    CODE_EXECUTION: 'executions.csv',
    CODE_SOLUTION: 'solutions.csv',
    CODE_LOGIN: 'logins.csv',
    CODE_GRADE: 'grades.csv',
    CODE_CODEMIRROR: 'mirrors.csv'
}

# Output filenames for different datasets
CSV_HEADERS = {
    CODE_SEMESTER: model.Semester.get_attr_names,
    CODE_COURSE: model.Course.get_attr_names,
    CODE_ASSIGNMENT: model.Assignment.get_attr_names,
    CODE_USER: model.User.get_attr_names,
    CODE_EXECUTION: model.Execution.get_attr_names,
    CODE_SOLUTION: model.SolutionMetrics.get_attr_names,
    CODE_LOGIN: model.Login.get_attr_names,
    CODE_GRADE: model.Grade.get_attr_names,
    CODE_CODEMIRROR: model.CodeMirror.get_attr_names
}

# File extension for data files
DATA_FILE_EXTENSION = '.data'

# Filename for user data
USER_DATA_FILENAME = 'user.data'

# Patterns for splitting user data
USER_LINE_SPLIT_PATTERN = '--'
USER_KEYVALUE_SPLIT_PATTERN = ':'
USER_ATTR_CONNECTOR_PATTERN = '_'

# Key names for user data attributes
USER_FILE_KEY_NAMES = [
    'course_id',
    'course_name',
    'institution_id',
    'institution_name',
    'high_school_name',
    'school_type',
    'shift',
    'graduation_year',
    'has_a_pc',
    'share_this_pc',
    'this_pc_has',
    'previous_experience_of',
    'worked_or_interned',
    'company_name',
    'year_started_working',
    'year_stopped_working',
    'started_other_degree',
    'degree_course',
    'institution_name',
    'year_started_this',
    'year_stopped_this',
    'sex',
    'year_of_birth',
    'civil_status',
    'have_kids'
]

CODE_FILE_EXTENSION = '.py'

# List of built-in types in Python
CODE_BUILTIN_TYPES_LIST = [
    'bool', 'bytes', 'bytearray', 'complex', 'dict', 'float', 'set', 'int', 'list', 'range', 'object', 'str',
    'memoryview', 'None', 'frozenset'
]

# List of built-in functions in Python
CODE_BUILTIN_FUNCS_LIST = [
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile',
    'delattr', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'format', 'getattr', 'globals', 'hasattr',
    'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'len', 'locals', 'map', 'max', 'min', 'next',
    'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
    'slice',
    'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
]

# Token codes for Python language tokens
ENDMARKER = 0
NAME = 1
NUMBER = 2
STRING = 3
NEWLINE = 4
INDENT = 5
DEDENT = 6
LPAR = 7
RPAR = 8
LSQB = 9
RSQB = 10
COLON = 11
COMMA = 12
SEMI = 13
PLUS = 14
MINUS = 15
STAR = 16
SLASH = 17
VBAR = 18
AMPER = 19
LESS = 20
GREATER = 21
EQUAL = 22
DOT = 23
PERCENT = 24
LBRACE = 25
RBRACE = 26
EQ_EQUAL = 27
NOT_EQ = 28
LESS_EQ = 29
GREATER_EQ = 30
TILDE = 31
CIRCUMFLEX = 32
LSHIFT = 33
RSHIFT = 34
DBL_STAR = 35
PLUS_EQ = 36
MINUS_EQ = 37
STAR_EQ = 38
SLASH_EQ = 39
PERCENT_EQ = 40
AMPER_EQ = 41
VBAR_EQ = 42
CIRCUMFLEX_EQ = 43
LSHIFT_EQ = 44
RSHIFT_EQ = 45
DBL_STAR_EQ = 46
DBL_SLASH = 47
DBL_SLASH_EQ = 48
AT = 49
AT_EQ = 50
RARROW = 51
ELLIPSIS = 52
COLON_EQ = 53
OP = 54
ERROR_TOKEN = 59
COMMENT = 60
NL = 61
ENCODING = 62
NUMBER_INT = 63
NUMBER_FLOAT = 64
KWD_AND = 65
KWD_OR = 66
KWD_NOT = 67
KWD_NONE = 68
KWD_FALSE = 69
KWD_TRUE = 70
KWD_AS = 71
KWD_ASSERT = 72
KWD_ASYNC = 73
KWD_AWAIT = 74
KWD_BREAK = 75
KWD_CLASS = 76
KWD_CONTINUE = 77
KWD_DEF = 78
KWD_DEL = 79
KWD_IF = 80
KWD_ELIF = 81
KWD_ELSE = 82
KWD_EXCEPT = 83
KWD_FINALLY = 84
KWD_FOR = 85
KWD_WHILE = 86
KWD_IMPORT = 87
KWD_FROM = 88
KWD_GLOBAL = 89
KWD_IN = 90
KWD_IS = 91
KWD_LAMBDA = 92
KWD_NONLOCAL = 93
KWD_PASS = 94
KWD_RAISE = 95
KWD_RETURN = 96
KWD_TRY = 97
KWD_WITH = 98
KWD_YIELD = 99
KEYWORD = 100
IDENTIFIER = 101
BUILTIN_TYPE = 102
BUILTIN_FUNC = 103
KWD_PRINT = 104
KWD_INPUT = 105

# Dictionary to map token names to their corresponding codes
TOKEN_NAMES = {value: name.lower() for name, value in globals().items() if isinstance(value, int)}

# Dictionary to map token codes to their corresponding names
TOKEN_CODES = {value: key for key, value in TOKEN_NAMES.items()}

class Logger:
    """
    A simple logger class for logging information, warnings, and errors to files and console.
    """

    LOGS_DIR = os.path.join(os.getcwd(), 'logs') # Directory path for storing logs
    __cblogger = None # Private class variable for holding the logger instance

    @staticmethod
    def configure():
        """
        Configures the logger by setting up log file handlers and console handlers.
        """
        logging.basicConfig(level=logging.INFO) # Set the logging level to INFO

        if not os.path.exists(Logger.LOGS_DIR): # Create logs directory if it doesn't exist
            os.mkdir(Logger.LOGS_DIR)

        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s') # Define log message format
        data_hoje = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Get current date and time

        if not Logger.__cblogger: # If logger instance doesn't exist, create one
            Logger.__cblogger = logging.getLogger('cblogger') # Create logger instance with name 'cblogger'
 
            # Create file handlers for different log levels: INFO, WARNING, and ERROR
            ifh = logging.FileHandler(os.path.join(Logger.LOGS_DIR, f'{data_hoje}_info.log'))
            ifh.setLevel(level=logging.INFO)
            ifh.setFormatter(formatter)
            Logger.__cblogger.addHandler(ifh)

            wfh = logging.FileHandler(os.path.join(Logger.LOGS_DIR, f'{data_hoje}_warn.log'))
            wfh.setLevel(level=logging.WARNING)
            wfh.setFormatter(formatter)
            Logger.__cblogger.addHandler(wfh)

            efh = logging.FileHandler(os.path.join(Logger.LOGS_DIR, f'{data_hoje}_error.log'))
            efh.setLevel(level=logging.ERROR)
            efh.setFormatter(formatter)
            Logger.__cblogger.addHandler(efh)

            # Create console handler to output logs to console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level=logging.INFO)
            console_handler.setFormatter(formatter)
            Logger.__cblogger.addHandler(console_handler)

    @staticmethod
    def info(msg: str):
        """
        Logs an information message.
        
        Parameters:
            msg (str): The message to be logged.
        """
        Logger.__cblogger.info(msg)

    @staticmethod
    def warn(msg: str):
        """
        Logs a warning message.
        
        Parameters:
            msg (str): The message to be logged.
        """
        Logger.__cblogger.warning(msg)

    @staticmethod
    def error(msg: str):
        """
        Logs an error message.
        
        Parameters:
            msg (str): The message to be logged.
        """
        Logger.__cblogger.error(msg, exc_info=True)


def extract_semester(path: str):
    """
    Extracts the semester from the given path.
    
    Parameters:
        path (str): The path containing the semester information.
    
    Returns:
        Semester: The Semester object extracted from the path.
    """
    return model.Semester(path.split(os.path.sep)[-1])


def extract_course(semester: str, code: str, path: str):
    """
    Extracts course information from the given path.
    
    Parameters:
        period (str): The period or semester of the course.
        code (str): The code or identifier of the course.
        path (str): The path containing course-related files.
    
    Returns:
        Course: The Course object extracted from the provided path.
    """
    desc = ''
    for entry in os.scandir(os.path.join(path, 'assessments')):
        # If the 'entry' is a file with the '.data' extension, it corresponds to an activity
        if entry.is_file() and entry.path.endswith(DATA_FILE_EXTENSION):
            with open(entry.path, 'rb') as f:
                line = f.readline().decode(DEFAULT_FILE_ENCODING)
                while line:
                    # Title example: ---- class name: Introduction to Computer Programming
                    if line.startswith('---- class name:'):
                        desc = line.strip()[17:]
                        break
                    line = f.readline().decode(DEFAULT_FILE_ENCODING)
    return model.Course(semester, code, desc)

def extract_assignment(semester: str, course: str, path: str):
    """
    Extracts assignment information from a file and creates an Assignment object.

    Parameters:
        semester (str): The semester of the assignment.
        course (str): The course of the assignment.
        path (str): The path to the assignment file.

    Returns:
        Assignment: An Assignment object containing the extracted information.
    """
    new_assignment = model.Assignment(semester, course, os.path.splitext(os.path.basename(path))[0])
    
    with open(path, mode='r', encoding=DEFAULT_FILE_ENCODING) as f:
        lines = f.readlines()
        # Extract assignment details from specific lines in the file
        new_assignment.title = lines[1][23:].strip()
        new_assignment.open_date = lines[4][12:].strip()
        new_assignment.close_date = lines[5][10:].strip()
        new_assignment.programming_lang = lines[6][15:].strip()
        new_assignment.assignment_type = lines[8][11:].strip()
        new_assignment.weight = float(lines[9][13:].strip())
        new_assignment.n_blocks = int(lines[10][22:].strip())

        new_assignment.blocks = []
        # Extract block information
        for line in lines[12:]:
            line = line.strip()[18:]
            if line:
                new_assignment.blocks.append([int(x) for x in line.split(' or ')])

    return new_assignment

def extract_user(semester: str, course: str, path: str):
    """
    Extracts user information from a file and creates a User object.

    Parameters:
        semester (str): The semester of the user.
        course (str): The course of the user.
        path (str): The path to the user data directory.

    Returns:
        User: A User object containing the extracted information.
    """
    new_user = model.User(semester, course, os.path.basename(path))
    
    dict_obj = {}
    with open(os.path.join(path, USER_DATA_FILENAME), mode='r', encoding=DEFAULT_FILE_ENCODING) as f:
        # Parse user data into a dictionary
        for line in f.readlines():
            if line.startswith('----'):
                line = line[5:].strip().lower()
                key, value = line.split(':', 1)
                key = '_'.join(key.split(' ')[:3])
                if key in dict_obj:
                    key = f'{key}_2'
                dict_obj[key] = value

    for attribute in model.User.get_attr_names()[3:]:
        setattr(new_user, attribute, dict_obj.get(attribute, None))

    return new_user

def extract_executions(semester: str, course: str, assignment: str, user: str, problem: str, path: str):
    """
    Extracts execution details from a given file and returns a list of Execution objects.

    Parameters:
        semester (str): The current semester.
        course (str): The name of the course.
        assignment (str): The specific assignment.
        user (str): The user's identifier.
        problem (str): The specific problem.
        path (str): Path to the file containing execution data.

    Returns:
        list: A list of Execution objects with extracted information.
    """
    seq_attempt = 0  # Initialize the sequence attempt counter
    executions = []  # Initialize the list to hold Execution objects

    # Open the file with the specified encoding and read its content
    with open(path, mode='r', encoding=DEFAULT_FILE_ENCODING) as arquivo:
        content = arquivo.read()

    # Split the content into sections by the delimiter that separates each execution
    sections = content.split('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')

    for section in sections:
        section = section.strip()  # Remove leading/trailing whitespace
        if not section:
            continue  # Skip empty sections

        # Split the section into header and sub-sections, with the header containing execution type and date
        header, *sub_sections = section.split('\n-- ')
        exec_type, exec_dt = header[3:].split(' (')
        exec_dt = exec_dt.rstrip(')')  # Remove the closing parenthesis from the execution date

        # The first sub-section contains the student's code, extracted and stripped of leading characters and whitespace
        student_code_str = sub_sections[0][5:].strip()

        # Create an Execution object with the extracted information
        execution = model.Execution(semester, course, assignment, user, problem, seq_attempt, exec_type.strip(), exec_dt)
        # Initialize execution properties
        execution.tcases_results = []
        execution.n_tcases = 0
        execution.has_err = False

        # Process additional sub-sections that contain execution time, test cases, grade, and error information
        for sub_section in sub_sections[1:]:  # Skip the code section already processed
            if sub_section.startswith('EXE'):
                # Extract execution time
                execution.exec_time = sub_section.split(':\n')[1]
            elif sub_section.startswith('TES'):
                # Extract test case results
                test_seq = sub_section.split('\n---- ')
                corr_output = test_seq[2].split(':\n')[-1]
                usr_output = test_seq[3].split(':\n')[-1]
                # Compare outputs to determine test case result
                execution.tcases_results.append(corr_output == usr_output)
                execution.n_tcases += 1
            elif sub_section.startswith('GRA'):
                # Extract grade
                execution.grade = sub_section.split(':')[1].strip()
            elif sub_section.startswith('ERROR:'):
                # Extract error message and type
                execution.has_err = True
                execution.err_msg = sub_section[7:]
                err_types = ERROR_PATTERN.findall(execution.err_msg)
                execution.err_type = err_types[0] if err_types else 'Exception'

        # If there was no error, call a function to extract metrics from the student's code
        if not execution.has_err:
            extract_code_metrics(execution, student_code_str)

        # Add the Execution object to the list of executions
        executions.append(execution)
        # Increment the attempt sequence number for the next execution
        seq_attempt += 1

    return executions  # Return the list of Execution objects


def extract_solution(semester: str, course: str, assignment: str, user: str, problem: str, path: str):
    """
    Extracts solution metrics for a given problem based on the code stored in a file.

    This function reads the entire code from the given file path and extracts metrics
    using the extrair_metricas_codigo function. It initializes a SolutionMetrics object
    with basic information and updates it with the extracted metrics.

    Parameters:
        semester (str): The semester during which the solution was submitted.
        course (str): The course for which the solution was submitted.
        assignment (str): The assignment to which the solution belongs.
        user (str): The user who submitted the solution.
        problem (str): The specific problem the solution is for.
        path (str): The file path where the solution code is stored.

    Returns:
        A SolutionMetrics object populated with the extracted metrics.
    """
    # Initialize the SolutionMetrics object with basic information
    solution = model.SolutionMetrics(semester, course, assignment, user, problem)

    # Open the file containing the solution code and extract metrics
    with open(path, mode='r', encoding=DEFAULT_FILE_ENCODING) as f:
        # Directly pass the file content to extract_code_metrics
        extract_code_metrics(solution, f.read())

    # Return the populated SolutionMetrics object
    return solution

def extract_code_metrics(obj, code: str):
    """
    Extracts various metrics from the provided source code and sets them as attributes of the given object.

    The metrics include complexity metrics, size metrics, Halstead metrics, and token counts. Each metric is extracted
    in a separate try-except block to handle potential errors independently.

    Args:
        obj: The object to which the extracted metrics will be set as attributes.
        code: The source code from which metrics are extracted.
    """
    extract_complexity_metrics(obj, code)
    extract_size_metrics(obj, code)
    extract_halstead_metrics(obj, code)
    extract_token_metrics(obj, code)

def extract_complexity_metrics(obj: Any, code: str) -> None:
    """Extracts and sets complexity-related metrics as attributes of the object."""
    try:
        v = ComplexityVisitor.from_code(code)
        for attr in ['complexity', 'classes', 'functions', 'functions_complexity', 'classes_complexity', 'total_complexity', 'blocks']:
            setattr(obj, attr, getattr(v, attr))
    except BaseException as err:
        Logger.error(f'\t\tError while extracting code complexity metrics: {err}')

def extract_size_metrics(obj: Any, code: str) -> None:
    """Extracts and sets size-related metrics as attributes of the object."""
    try:
        a = analyze(code)
        for attr in ['loc', 'lloc', 'sloc', 'blank', 'comments', 'single_comments', 'multi']:
            setattr(obj, attr, getattr(a, attr))
    except BaseException as err:
        Logger.error(f'\t\tError while extracting code size based metrics: {err}')

def extract_halstead_metrics(obj: Any, code: str) -> None:
    """Extracts and sets Halstead complexity metrics as attributes of the object."""
    try:
        h = h_visit(code)
        for attr in ['h1', 'h2', 'N1', 'N2', 'vocabulary', 'length', 'calculated_length', 'volume', 'difficulty', 'effort', 'bugs', 'time']:
            setattr(obj, attr, getattr(h.total, attr))
    except BaseException as err:
        Logger.error(f'\t\tError while extracting halsted code metrics: {err}')

def __analyze_tokens(tokens, token_count, unique_identifiers, unique_strings, unique_btype, unique_bfunc):
    for tk in tokens:
        if tk.exact_type == token.NUMBER:
            if '.' in tk.string:
                token_count[NUMBER_FLOAT] += 1
            else:
                token_count[NUMBER_INT] += 1
        elif tk.type == token.NAME:
            if keyword.iskeyword(tk.string):
                token_count[TOKEN_CODES.get(tk.string.lower(), KEYWORD)] += 1
            elif tk.string in CODE_BUILTIN_TYPES_LIST:
                token_count[BUILTIN_TYPE] += 1
                unique_btype.add(tk.string)
            elif tk.string in CODE_BUILTIN_FUNCS_LIST:
                if tk.string == 'print':
                    token_count[KWD_PRINT] += 1
                elif tk.string == 'input':
                    token_count[KWD_INPUT] += 1
                else:
                    token_count[BUILTIN_FUNC] += 1
                unique_bfunc.add(tk.string)
            else:
                token_count[IDENTIFIER] += 1
                unique_identifiers.add(tk.string)
        elif tk.type == token.STRING:
            token_count[STRING] += 1
            unique_strings.add(tk.string)
        else:
            token_count[tk.exact_type] += 1

def __set_token_attributes(obj, unique_identifiers, unique_btype, unique_bfunc):
    setattr(obj, 'builtin_type_unique', len(unique_btype) if unique_btype else 0)
    setattr(obj, 'builtin_func_unique', len(unique_bfunc) if unique_bfunc else 0)
    setattr(obj, 'identifiers_unique', len(unique_identifiers) if unique_identifiers else 0)
    setattr(obj, 'identifiers_max_len', max([len(x) for x in unique_identifiers]) if unique_identifiers else 0)
    setattr(obj, 'identifiers_min_len', min([len(x) for x in unique_identifiers]) if unique_identifiers else 0)
    setattr(obj, 'identifiers_mean_len', statistics.mean([len(x) for x in unique_identifiers]) if unique_identifiers else 0)

def extract_token_metrics(obj: Any, code: str) -> None:
    """Extracts and sets token count metrics as attributes of the object."""
    try:
        # Token analysis initialization
        token_count = defaultdict(int)
        unique_identifiers, unique_strings, unique_btype, unique_bfunc = set(), set(), set(), set()
        
        # Temporary code file writing and token extraction
        temp_file_path = os.path.join(os.getcwd(), 'temp_code.py')
        with open(temp_file_path, mode='w', encoding=DEFAULT_FILE_ENCODING) as temp_code:
            temp_code.write(code)
        with tokenize.open(temp_file_path) as f:
            try:
                tokens = tokenize.generate_tokens(f.readline)
                __analyze_tokens(tokens, token_count, unique_identifiers, unique_strings, unique_btype, unique_bfunc)
            except BaseException as err:
                pass

        # Setting token count attributes
        for k, v in Counter(token_count).items():
            setattr(obj, TOKEN_NAMES[k], v)
        __set_token_attributes(obj, unique_identifiers, unique_btype, unique_bfunc)
    except BaseException as err:
        Logger.error(f'\t\tError while extracting code token based metrics: {err}')
        

def extract_user_logins(semester, course, user, path: str):
    """
    Extracts user login information from a specified file.
    
    Parameters:
        semester (str): The semester of the user.
        course (str): The course of the user.
        user (str): The user identifier.
        path (str): The path to the file containing login data.
    
    Returns:
        list: A list of Login objects created from the file data.
    """
    user_logins = []
    with open(path, mode='r', encoding=DEFAULT_FILE_ENCODING) as file:
        for line in file: # Direct iteration to save memory
            parts = line.split('#') # Strip to remove newline and split on '#'
            login_date, login_time = parts[0][:10], parts[0][11:]
            event = parts[1][:-1]  # Assume removing the last character is to remove newline, strip is used earlier
            user_logins.append(model.Login(semester, course, user, login_date, login_time, event))
    return user_logins

def extract_grade(semester, course, assignment, user, path: str):
    """
    Extracts a grade from a specified file.
    
    Parameters:
        semester (str): The semester of the user.
        course (str): The course of the user.
        assignment (str): The assignment associated with the grade.
        user (str): The user identifier.
        path (str): The path to the file containing the grade data.
    
    Returns:
        Grade: A Grade object created from the file data.
    """
    with open(path, mode='r', encoding=DEFAULT_FILE_ENCODING) as file:
        grade_line = file.readline().strip()
        np_line = file.readline()  # Skip line not needed
        correct_line = file.readline().strip()
        wrong_line = file.readline().strip()
        blank_line = file.readline().strip()
    
    # Extract the actual data after known prefixes
    grade = grade_line[19:]
    n_problems = np_line[26:]
    correct = correct_line[14:]
    wrong = wrong_line[16:]
    blank = blank_line[12:]
    return model.Grade(semester, course, assignment, user, grade, n_problems, correct, wrong, blank)
 

def extract_codemirror_events(semester, course, assignment, user, problem, path: str):
    """
    Extracts CodeMirror events from a given file.

    This function reads a file line by line, filtering for lines that match
    a predefined pattern (CODEMIRROR_PATTERN). Each matching line is parsed to
    extract event details, which are used to construct CodeMirror event objects.

    Parameters:
        semester (str): The current semester.
        course (str): The course code.
        assignment (str): The assignment identifier.
        user (str): The user identifier.
        problem (str): The problem identifier.
        path (str): Path to the file containing the events.

    Returns:
        list: A list of CodeMirror event objects.
    """
    codemirror_events = []
    with open(path, mode='r', encoding=DEFAULT_FILE_ENCODING) as file:
        for line in file: # Iterate through each line in the file
            if CODEMIRROR_PATTERN.match(line): # Filter lines matching the pattern
                datetime_str, action_str = line.strip().split('#', 1) # Split the line by '#' and strip whitespace
                date_str, time_str = datetime_str.split(' ')
                
                # Parse the datetime string to a datetime object and then to a timestamp
                timestamp = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M:%S.%f').timestamp()
                
                event, msg = action_str.split('#', 1)

                # Construct a CodeMirror event object with parsed data
                codemirror_event = model.CodeMirror(semester, course, assignment, user, problem, timestamp, date_str, time_str, event, msg)
                codemirror_events.append(codemirror_event)
    return codemirror_events

def save_to_csv(data_dict):
    """
    Saves data to a CSV file.
    
    This function takes a list of data rows, a header for the CSV file, and a file path.
    It then creates a DataFrame from the data and saves it as a CSV file at the specified path.
    CSV files are encoded in UTF-8 and do not include the index column.
    Text fields are quoted to ensure that commas within text are correctly interpreted.
    
    Args:
        rows (list of list): The data to be saved, where each inner list represents a row.
        header (list): The header row of the CSV file. Each item in the list represents a column name.
        path (str): The file path where the CSV file will be saved.
    
    Returns:
        None
    """
    # Log the path where the data will be saved for debugging and tracking purposes.
    Logger.info(f'Saving data into disk')

    os.makedirs(os.path.join(os.getcwd(), CSV_FILE_OUTPUT_DIR)) 

    for key in data_dict.keys():
        if data_dict[key]:
            # Create a DataFrame using the provided rows and header.
            df = pd.DataFrame(data_dict[key], columns=CSV_HEADERS[key]())

            # Save the DataFrame to a CSV file at the specified path.
            # - sep=',': Use a comma as the column separator.
            # - index=False: Do not write row indices.
            # - encoding='utf-8': Encode the file using UTF-8.
            # - quoting=2: Quote all text fields to handle commas within text correctly.
            df.to_csv(f'{CSV_FILE_OUTPUT_DIR}/{CSV_FILENAMES[key]}', sep=',', index=False, encoding='utf-8', quoting=2)
