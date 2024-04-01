# -*- coding: utf-8 -*-
### Codebench Dataset Extractor by Marcos Lima (marcos.lima@icomp.ufam.edu.br)
### Universidade Federal do Amazonas - UFAM
### Instituto de Computação - IComp


class CodebenchObject:
    """General class that specifies model object base structure."""

    def as_list(self):
        """Return a list with model object attributes values."""
        pass

    @staticmethod
    def get_attr_names():
        """Return a list with model object attributes names ."""
        pass


class Semester(CodebenchObject):
    """
    Model object that represents a semester.
    
    Attributes:
        desc (str): A string describing the semester.
        n_courses (int): The number of courses in the semester.
        n_assignments (int): The number of assignments in the semester.
        n_users (int): The number of users associated with the semester.
        n_codes (int): The number of users codes associated with the semester.
        n_executions (int): The number of users code executions in the semester.
        n_mirrors (int): The number of code mirrors events in the semester.
        n_grades (int): The number of users grades associated with the semester.
        n_mousemoves (int): The number of mouse moves events recorded in the semester.

    Methods:
        as_list(): Returns the attributes of the academic term as a list.
        get_attr_names(): Returns a list of attribute names for the academic term.
    """

    def __init__(self, description):
        """Initialize a Periodo object with a semester description."""
        self.desc = description
        self.n_courses = 0
        self.n_assignments = 0
        self.n_users = 0
        self.n_codes = 0
        self.n_executions = 0
        self.n_mirrors = 0
        self.n_grades = 0

    def as_list(self):
        """Return a list of attribute names of the Periodo class."""
        return [
            self.desc,
            self.n_courses,
            self.n_assignments,
            self.n_users,
            self.n_codes,
            self.n_executions,
            self.n_mirrors,
            self.n_grades
        ]

    @staticmethod
    def get_attr_names():
        return [
            'desc',
            'n_courses',
            'n_assignments',
            'n_users',
            'n_codes',
            'n_executions',
            'n_mirrors',
            'n_grades'
        ]


class Course(CodebenchObject):
    """
    Model object that represents a course of the academic term.
    
    Attributes:
        semester (str): The academic term or semester the course belongs to.
        code (str): The code or identifier of the course.
        desc (str): Description of the course.
        n_assignments (int): Number of assignments associated with the course.
        n_users (int): Number of users enrolled in the course.
    
    Methods:
        as_list(): Returns the attributes of the course as a list.
        get_attr_names(): Returns a list of attribute names for the course.
    """

    def __init__(self, semester, code, desc):
        """
        Initializes a new instance of Turma.

        Args:
            semester (str): The academic term or semester.
            code (str): The code or identifier of the course.
            desc (str): Description of the course.
        """
        self.semester = semester
        self.code = code
        self.desc = desc
        self.n_assignments = 0
        self.n_users = 0

    def as_list(self):
        """
        Returns the attributes of the Turma instance as a list.

        Returns:
            list: A list containing semester, code, desc, number of assignments,
                and number of users.
        """
        return [
            self.semester,
            self.code,
            self.desc,
            self.n_assignments,
            self.n_users
        ]

    @staticmethod
    def get_attr_names():
        """
        Returns the names of attributes of the Turma class.

        Returns:
            list: A list containing names of attributes: semester, code, desc, 
                n_assignments, and n_users.
        """
        return [
            'semester',
            'code',
            'desc',
            'n_assignments',
            'n_users'
        ]


class Assignment(CodebenchObject):
    """
    Model object that represents an assignment.

    Attributes:
        semester (str): The semester during which the assignment is conducted.
        course (str): The course to which the assignment belongs.
        code (str): Unique identifier for the assignment.
        title (str or None): The title of the assignment.
        open_date (str or None): The date when the assignment opens.
        close_date (str or None): The date when the assignment closes.
        programming_lang (str or None): The programming language used for the assignment.
        assignment_type (str or None): The type of the assignment (e.g., homework, project).
        weight (float or None): The weight/importance of the assignment.
        n_blocks (int or None): The number of code blocks in the assignment.
        blocks (list): A list containing the code blocks for the assignment.

    Methods:
        as_list(): Returns the attributes of the assignment as a list.
        get_attr_names(): Returns a list of attribute names for the assignment.
    """

    def __init__(self, semester, course, code):
        """
        Initialize an instance of Atividade.

        Args:
            semester (str): The semester during which the assignment is conducted.
            course (str): The course to which the assignment belongs.
            code (str): Unique identifier for the assignment.
        """
        self.semester = semester
        self.course = course
        self.code = code
        self.title = None
        self.open_date = None
        self.close_date = None
        self.programming_lang = None
        self.assignment_type = None
        self.weight = None
        self.n_blocks = None
        self.blocks = []

    def as_list(self):
        """
        Return the attributes of the assignment as a list.

        Returns:
            list: A list containing the attributes of the assignment.
        """
        return [
            self.semester,
            self.course,
            self.code,
            self.title,
            self.open_date,
            self.close_date,
            self.programming_lang,
            self.assignment_type,
            self.weight,
            self.n_blocks,
            self.blocks
        ]

    @staticmethod
    def get_attr_names():
        """
        Return a list of attribute names for the assignment.

        Returns:
            list: A list containing the names of attributes for the assignment.
        """
        return [
            'semester',
            'course',
            'code',
            'title',
            'open_date',
            'close_date',
            'programming_lang',
            'assignment_type',
            'weight',
            'n_blocks',
            'blocks'
        ]


class User(CodebenchObject):
    """
    A User class for representing and storing various attributes of a user,
    including personal, educational, and work-related information.

    Attributes:
        semester (str): The current semester of the user.
        course (str): The name of the course the user is enrolled in.
        code (str): A unique identifier code for the user.
        course_id (str): The unique identifier for the course.
        course_name (str): The name of the course.
        institution_id (str): The unique identifier for the institution.
        institution_name (str): The name of the institution.
        high_school_name (str): The name of the high school attended by the user.
        school_type (str): The type of the high school (e.g., public, private).
        shift (str): The shift in which the user attended high school.
        graduation_year (int): The year the user graduated from high school.
        has_a_pc (bool): Whether the user has a personal computer.
        share_this_pc (bool): Whether the user shares their personal computer.
        this_pc_has (str): Specifications or features of the user's personal computer.
        previous_experience_of (str): Previous experience of the user in the field.
        worked_or_interned (bool): Whether the user has worked or interned.
        company_name (str): The name of the company where the user worked or interned.
        year_started_working (int): The year when the user started working.
        year_stopped_working (int): The year when the user stopped working.
        started_other_degree (bool): Whether the user started another degree.
        degree_course (str): The name of the other degree course.
        institution_name_2 (str): The name of the institution of the other degree.
        year_started_this (int): The year the user started the other degree.
        year_stopped_this (int): The year the user stopped the other degree.
        sex (str): The sex of the user.
        year_of_birth (int): The year of birth of the user.
        civil_status (str): The civil status of the user (e.g., single, married).
        have_kids (bool): Whether the user has kids.
    """

    def __init__(self, semester, course, code):
        """
        Initializes a new User object with the given semester, course, and code.
        Other attributes are initialized to None and can be set later.
        """
        self.semester = semester
        self.course = course
        self.code = code
        # Initialize other attributes to None
        self.course_id = None
        self.course_name = None
        self.institution_id = None
        self.institution_name = None
        self.high_school_name = None
        self.school_type = None
        self.shift = None
        self.graduation_year = None
        self.has_a_pc = None
        self.share_this_pc = None
        self.this_pc_has = None
        self.previous_experience_of = None
        self.worked_or_interned = None
        self.company_name = None
        self.year_started_working = None
        self.year_stopped_working = None
        self.started_other_degree = None
        self.degree_course = None
        self.institution_name_2 = None
        self.year_started_this = None
        self.year_stopped_this = None
        self.sex = None
        self.year_of_birth = None
        self.civil_status = None
        self.have_kids = None

    def as_list(self):
        """
        Returns a list of all user attributes in the order defined.

        Returns:
            list: A list of user attributes.
        """
        return [
            self.semester,
            self.course,
            self.code,
            self.course_id,
            self.course_name,
            self.institution_id,
            self.institution_name,
            self.high_school_name,
            self.school_type,
            self.shift,
            self.graduation_year,
            self.has_a_pc,
            self.share_this_pc,
            self.this_pc_has,
            self.previous_experience_of,
            self.worked_or_interned,
            self.company_name,
            self.year_started_working,
            self.year_stopped_working,
            self.started_other_degree,
            self.degree_course,
            self.institution_name_2,
            self.year_started_this,
            self.year_stopped_this,
            self.sex,
            self.year_of_birth,
            self.civil_status,
            self.have_kids
        ]

    @staticmethod
    def get_attr_names():
        """
        Returns a list of all user attribute names in the order defined.

        Returns:
            list: A list of attribute names as strings.
        """
        return [
            'semester',
            'course',
            'code',
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
            'institution_name_2',
            'year_started_this',
            'year_stopped_this',
            'sex',
            'year_of_birth',
            'civil_status',
            'have_kids'
        ]


class Execution(CodebenchObject):
    """
    Model object that represents a Codebench User Code Execution (Submition or Test).

    Attributes:
        semester (str): The semester during which the login event occurred.
        course (str): The course associated with the login event.
        user (str): The user unique identifier .
        assigment (str): The crouse assignment.
        problem  (str): The problema id.
        seq (int): The execution sequential order.
        ex_type (str): The execution type (Submition | Test).
        datetime (str): The execution date and time.
    
    Methods:
        as_list(): Returns the attributes of the User Code Execution as a list.
        get_attr_names(): Returns the names of the attributes as a list.
    """

    def __init__(self, semester, course, user, assignment, problem, seq, ex_type, datetime):
        """
        Initialize an Execution object with the provided parameters.

        Parameters:
        - semester (str): The semester of the execution.
        - course (str): The course associated with the execution.
        - user (str): The user who performed the execution.
        - assignment (str): The assignment associated with the execution.
        - problem (str): The problem or task being executed.
        - seq (int): The sequence number of the attempt.
        - ex_type (str): The type of execution (e.g., 'submission', 'test').
        - datetime: The timestamp of the execution.
        """
        self.datetime = datetime
        self.semester = semester
        self.course = course
        self.user = user
        self.assignment = assignment
        self.problem = problem
        self.seq_attempt = seq
        self.ex_type = ex_type
        #self.code = code
        self.has_err = False
        self.err_msg = None
        self.err_type = None
        self.exec_time = None
        self.tcases_results = None
        self.n_tcases = None
        self.grade = None
        self.complexity = None
        self.n_classes = None
        self.n_functions = None
        self.funcs_complexity = None
        self.classes_complexity = None
        self.total_complexity = None
        self.n_blocks = None
        self.loc = None
        self.lloc = None
        self.sloc = None
        self.comments = None
        self.single_comments = None
        self.multi_comments = None
        self.blank_lines = None
        self.h1 = None
        self.h2 = None
        self.N1 = None
        self.N2 = None
        self.h = None
        self.N = None
        self.calculated_N = None
        self.volume = None
        self.difficulty = None
        self.effort = None
        self.bugs = None
        self.time = None
        self.endmarker = None
        self.name = None
        self.number = None
        self.string = None
        self.newline = None
        self.indent = None
        self.dedent = None
        self.lpar = None
        self.rpar = None
        self.lsqb = None
        self.rsqb = None
        self.colon = None
        self.comma = None
        self.semi = None
        self.plus = None
        self.minus = None
        self.star = None
        self.slash = None
        self.vbar = None
        self.amper = None
        self.less = None
        self.greater = None
        self.equal = None
        self.dot = None
        self.percent = None
        self.lbrace = None
        self.rbrace = None
        self.eq_equal = None
        self.not_eq = None
        self.less_eq = None
        self.greater_eq = None
        self.tilde = None
        self.circumflex = None
        self.lshift = None
        self.rshift = None
        self.dbl_star = None
        self.plus_eq = None
        self.minus_eq = None
        self.star_eq = None
        self.slash_eq = None
        self.percent_eq = None
        self.amper_eq = None
        self.vbar_eq = None
        self.circumflex_eq = None
        self.lshift_eq = None
        self.rshift_eq = None
        self.dbl_star_eq = None
        self.dbl_slash = None
        self.dbl_slash_eq = None
        self.at = None
        self.at_eq = None
        self.rarrow = None
        self.ellipsis = None
        self.colon_eq = None
        self.op = None
        self.error_token = None
        self.comment = None
        self.nl = None
        self.encoding = None
        self.number_int = None
        self.number_float = None
        self.kwd_and = None
        self.kwd_or = None
        self.kwd_not = None
        self.kwd_none = None
        self.kwd_false = None
        self.kwd_true = None
        self.kwd_as = None
        self.kwd_assert = None
        self.kwd_async = None
        self.kwd_await = None
        self.kwd_break = None
        self.kwd_class = None
        self.kwd_continue = None
        self.kwd_def = None
        self.kwd_del = None
        self.kwd_if = None
        self.kwd_elif = None
        self.kwd_else = None
        self.kwd_except = None
        self.kwd_finally = None
        self.kwd_for = None
        self.kwd_while = None
        self.kwd_import = None
        self.kwd_from = None
        self.kwd_global = None
        self.kwd_in = None
        self.kwd_is = None
        self.kwd_lambda = None
        self.kwd_nonlocal = None
        self.kwd_pass = None
        self.kwd_raise = None
        self.kwd_return = None
        self.kwd_try = None
        self.kwd_with = None
        self.kwd_yield = None
        self.keyword = None
        self.identifier = None
        self.builtin_type = None
        self.builtin_func = None
        self.kwd_print = None
        self.kwd_input = None
        self.builtin_type_unique = None
        self.builtin_func_unique = None
        self.identifiers_unique = None
        self.identifiers_max_len = None
        self.identifiers_min_len = None
        self.identifiers_mean_len = None

    def as_list(self):
        """
        Returns the attributes of the Execution object as a list.

        Returns:
        - list: List containing the attributes of the Execution object in a specific order.
        """
        return [
            self.datetime,
            self.semester,
            self.course,
            self.user,
            self.assignment,
            self.problem,
            self.seq_attempt,
            self.ex_type,
            self.has_err,
            self.err_msg,
            self.err_type,
            self.exec_time,
            self.tcases_results,
            self.n_tcases,
            self.grade,
            self.complexity,
            self.n_classes,
            self.n_functions,
            self.funcs_complexity,
            self.classes_complexity,
            self.total_complexity,
            self.n_blocks,
            self.loc,
            self.lloc,
            self.sloc,
            self.comments,
            self.single_comments,
            self.multi_comments,
            self.blank_lines,
            self.h1,
            self.h2,
            self.N1,
            self.N2,
            self.h,
            self.N,
            self.calculated_N,
            self.volume,
            self.difficulty,
            self.effort,
            self.bugs,
            self.time,
            self.endmarker,
            self.name,
            self.number,
            self.string,
            self.newline,
            self.indent,
            self.dedent,
            self.lpar,
            self.rpar,
            self.lsqb,
            self.rsqb,
            self.colon,
            self.comma,
            self.semi,
            self.plus,
            self.minus,
            self.star,
            self.slash,
            self.vbar,
            self.amper,
            self.less,
            self.greater,
            self.equal,
            self.dot,
            self.percent,
            self.lbrace,
            self.rbrace,
            self.eq_equal,
            self.not_eq,
            self.less_eq,
            self.greater_eq,
            self.tilde,
            self.circumflex,
            self.lshift,
            self.rshift,
            self.dbl_star,
            self.plus_eq,
            self.minus_eq,
            self.star_eq,
            self.slash_eq,
            self.percent_eq,
            self.amper_eq,
            self.vbar_eq,
            self.circumflex_eq,
            self.lshift_eq,
            self.rshift_eq,
            self.dbl_star_eq,
            self.dbl_slash,
            self.dbl_slash_eq,
            self.at,
            self.at_eq,
            self.rarrow,
            self.ellipsis,
            self.colon_eq,
            self.op,
            self.error_token,
            self.comment,
            self.nl,
            self.encoding,
            self.number_int,
            self.number_float,
            self.kwd_and,
            self.kwd_or,
            self.kwd_not,
            self.kwd_none,
            self.kwd_false,
            self.kwd_true,
            self.kwd_as,
            self.kwd_assert,
            self.kwd_async,
            self.kwd_await,
            self.kwd_break,
            self.kwd_class,
            self.kwd_continue,
            self.kwd_def,
            self.kwd_del,
            self.kwd_if,
            self.kwd_elif,
            self.kwd_else,
            self.kwd_except,
            self.kwd_finally,
            self.kwd_for,
            self.kwd_while,
            self.kwd_import,
            self.kwd_from,
            self.kwd_global,
            self.kwd_in,
            self.kwd_is,
            self.kwd_lambda,
            self.kwd_nonlocal,
            self.kwd_pass,
            self.kwd_raise,
            self.kwd_return,
            self.kwd_try,
            self.kwd_with,
            self.kwd_yield,
            self.keyword,
            self.identifier,
            self.builtin_type,
            self.builtin_func,
            self.kwd_print,
            self.kwd_input,
            self.builtin_type_unique,
            self.builtin_func_unique,
            self.identifiers_unique,
            self.identifiers_max_len,
            self.identifiers_min_len,
            self.identifiers_mean_len
        ]

    @staticmethod
    def get_attr_names():
        """
        Returns a list of attribute names of the Execution object.

        Returns:
        - list: List containing the names of the attributes of the Execution object.
        """
        return [
            'datetime',
            'semester',
            'course',
            'user',
            'assignment',
            'problem',
            'seq_attempt',
            'ex_type',
            'has_err',
            'err_msg',
            'err_type',
            'exec_time',
            'tcases_results',
            'n_tcases',
            'grade',
            'complexity',
            'n_classes',
            'n_functions',
            'funcs_complexity',
            'classes_complexity',
            'total_complexity',
            'n_blocks',
            'loc',
            'lloc',
            'sloc',
            'comments',
            'single_comments',
            'multi_comments',
            'blank_lines',
            'h1',
            'h2',
            'N1',
            'N2',
            'h',
            'N',
            'calculated_N',
            'volume',
            'difficulty',
            'effort',
            'bugs',
            'time',
            'endmarker',
            'name',
            'number',
            'string',
            'newline',
            'indent',
            'dedent',
            'lpar',
            'rpar',
            'lsqb',
            'rsqb',
            'colon',
            'comma',
            'semi',
            'plus',
            'minus',
            'star',
            'slash',
            'vbar',
            'amper',
            'less',
            'greater',
            'equal',
            'dot',
            'percent',
            'lbrace',
            'rbrace',
            'eq_equal',
            'not_eq',
            'less_eq',
            'greater_eq',
            'tilde',
            'circumflex',
            'lshift',
            'rshift',
            'dbl_star',
            'plus_eq',
            'minus_eq',
            'star_eq',
            'slash_eq',
            'percent_eq',
            'amper_eq',
            'vbar_eq',
            'circumflex_eq',
            'lshift_eq',
            'rshift_eq',
            'dbl_star_eq',
            'dbl_slash',
            'dbl_slash_eq',
            'at',
            'at_eq',
            'rarrow',
            'ellipsis',
            'colon_eq',
            'op',
            'error_token',
            'comment',
            'nl',
            'encoding',
            'number_int',
            'number_float',
            'kwd_and',
            'kwd_or',
            'kwd_not',
            'kwd_none',
            'kwd_false',
            'kwd_true',
            'kwd_as',
            'kwd_assert',
            'kwd_async',
            'kwd_await',
            'kwd_break',
            'kwd_class',
            'kwd_continue',
            'kwd_def',
            'kwd_del',
            'kwd_if',
            'kwd_elif',
            'kwd_else',
            'kwd_except',
            'kwd_finally',
            'kwd_for',
            'kwd_while',
            'kwd_import',
            'kwd_from',
            'kwd_global',
            'kwd_in',
            'kwd_is',
            'kwd_lambda',
            'kwd_nonlocal',
            'kwd_pass',
            'kwd_raise',
            'kwd_return',
            'kwd_try',
            'kwd_with',
            'kwd_yield',
            'keyword',
            'identifier',
            'builtin_type',
            'builtin_func',
            'kwd_print',
            'kwd_input',
            'builtin_type_unique',
            'builtin_func_unique',
            'identifiers_unique',
            'identifiers_max_len',
            'identifiers_min_len',
            'identifiers_mean_len'
        ]


class Login(CodebenchObject):
    """Model object that represents a Codebench User Login Event.

    This class represents a user login event in the Codebench system. It contains
    information such as the semester, course, date, time, user, and event type.

    Attributes:
        semester (str): The semester during which the login event occurred.
        course (str): The course associated with the login event.
        date (str): The date of the login event.
        time (str): The time of the login event.
        user (str): The user who performed the login.
        event (str): The type of event (e.g., "login", "logout").

    Methods:
        as_list(): Returns the attributes of the login event as a list.
        get_attr_names(): Returns the names of the attributes as a list.

    """

    def __init__(self, semester, course, user, date, time, event):
        """
        Initialize a Login object with provided attributes.

        Args:
            semester (str): The semester during which the login event occurred.
            course (str): The course associated with the login event.
            user (str): The user who performed the login.
            date (str): The date of the login event.
            time (str): The time of the login event.
            event (str): The type of event (e.g., "login", "logout").

        """
        self.semester = semester
        self.course = course
        self.date = date
        self.time = time
        self.user = user
        self.event = event

    def as_list(self):
        """
        Return the attributes of the login event as a list.

        Returns:
            list: A list containing the semester, course, date, time, user, and event.

        """
        return [
            self.semester,
            self.course,
            self.date,
            self.time,
            self.user,
            self.event,
        ]

    @staticmethod
    def get_attr_names():
        """
        Return the names of the attributes as a list.

        Returns:
            list: A list containing the names of the attributes.

        """
        return [
            'semester',
            'course',
            'date',
            'time',
            'user',
            'event',
        ]


class CodeMirror(CodebenchObject):
    """
    Model object that represents a CodeMirror User Events.

    Attributes:
        semester (str): The semester associated with the event.
        course (str): The course associated with the event.
        assignment (str): The assignment associated with the event.
        user (str): The user associated with the event.
        problem (str): The problem associated with the event.
        timestamp (str): The timestamp of the event.
        date (str): The date of the event.
        time (str): The time of the event.
        event (str): The type of event.
        msg (str): Additional message related to the event.
    """

    def __init__(self, semester, course, assignment, user, problem, timestamp, date, time, event, msg):
        """
        Initializes a CodeMirror object.

        Args:
            semester (str): The semester associated with the event.
            course (str): The course associated with the event.
            assignment (str): The assignment associated with the event.
            user (str): The user associated with the event.
            problem (str): The problem associated with the event.
            timestamp (str): The timestamp of the event.
            date (str): The date of the event.
            time (str): The time of the event.
            event (str): The type of event.
            msg (str): Additional message related to the event.
        """
        self.semester = semester
        self.course = course
        self.assignment = assignment
        self.user = user
        self.problem = problem
        self.timestamp = timestamp
        self.date = date
        self.time = time
        self.event = event
        self.msg = msg

    def as_list(self):
        """
        Returns the attributes of the CodeMirror object as a list.

        Returns:
            list: A list containing the attributes of the CodeMirror object.
        """
        return [
            self.semester,
            self.course,
            self.assignment,
            self.user,
            self.problem,
            self.timestamp,
            self.date,
            self.time,
            self.event,
            self.msg
        ]

    @staticmethod
    def get_attr_names():
        """
        Returns the names of attributes of the CodeMirror class.

        Returns:
            list: A list containing the names of attributes of the CodeMirror class.
        """
        return [
            'semester',
            'course',
            'assignment',
            'user',
            'problem',
            'timestamp',
            'date',
            'time',
            'event',
            'msg'
        ]


class Grade(CodebenchObject):
    """
    Model object that represents a User's Assignment Grade.

    Attributes:
        semester (str): The semester in which the assignment was completed.
        course (str): The course to which the assignment belongs.
        assignment (str): The name or identifier of the assignment.
        user (str): The user to whom the grade belongs.
        grade (float): The actual grade obtained by the user.
        n_problems (int): The number of problems in assignment.
        n_correct (int): The number of questions answered correctly.
        n_wrong (int): The number of questions answered incorrectly.
        n_blank (int): The number of questions left blank.
    """

    def __init__(self, semester, course, assignment, user, grade, n_problems, n_correct, n_wrong, n_blank):
        """
        Initializes a Grade object with the provided attributes.
        
        Args:
            semester (str): The semester in which the assignment was completed.
            course (str): The course to which the assignment belongs.
            assignment (str): The name or identifier of the assignment.
            user (str): The user to whom the grade belongs.
            grade (float): The actual grade obtained by the user.
            n_problems (int): The number of problems in assignment.
            n_correct (int): The number of questions answered correctly.
            n_wrong (int): The number of questions answered incorrectly.
            n_blank (int): The number of questions left blank.
        """
        self.semester = semester
        self.course = course
        self.assignment = assignment
        self.user = user
        self.grade = grade
        self.n_problems = n_problems
        self.n_correct = n_correct
        self.n_wrong = n_wrong
        self.n_blank = n_blank

    def as_list(self):
        """
        Returns the attributes of the Grade object as a list.
        
        Returns:
            list: A list containing the attributes of the Grade object.
        """
        return [
            self.semester,
            self.course,
            self.assignment,
            self.user,
            self.grade,
            self.n_problems,
            self.n_correct,
            self.n_wrong,
            self.n_blank
        ]

    @staticmethod
    def get_attr_names():
        """
        Returns the names of the attributes of the Grade object.
        
        Returns:
            list: A list containing the names of the attributes of the Grade object.
        """
        return [
            'semester',
            'course',
            'assignment',
            'user',
            'grade',
            'n_problems',
            'n_correct',
            'n_wrong',
            'n_blank'
        ]


class SolutionMetrics(CodebenchObject):
    """Model object that represents a Code Solution Metrics."""

    def __init__(self, semester, course, assignment, user, problem):
        """
        Initializes a SolutionMetrics object with provided parameters.

        Args:
            semester (str): The semester of the solution.
            course (str): The course the solution belongs to.
            assignment (str): The assignment the solution is for.
            user (str): The user code associated with the solution.
            problem (str): The problem the solution addresses.
            complexity (int or None): The complexity metric of the solution.
            classes (int or None): The number of classes in the solution.
            n_functions (int or None): The number of functions in the solution.
            funcs_complexity (int or None): The complexity of functions in the solution.
            classes_complexity (int or None): The complexity of classes in the solution.
            total_complexity (int or None): The total complexity of the solution.
            n_blocks (int or None): The number of code blocks in the solution.
            loc (int or None): The lines of code (LOC) in the solution.
            lloc (int or None): The logical lines of code (LLOC) in the solution.
            sloc (int or None): The source lines of code (SLOC) in the solution.
            comments (None): Placeholder for storing comments in the solution.
            single_comments (None): Placeholder for storing single-line comments in the solution.
            multi_comments (None): Placeholder for storing multi-line comments in the solution.
            blank_lines (None): Placeholder for storing blank lines in the solution.
            h1, h2 (None): Various tokens used for lexical analysis.
            N1, N2 (None): Various tokens used for lexical analysis.
            h, N (None): Various tokens used for lexical analysis.
            calculated_N (None): Placeholder for storing calculated N value.
            volume, difficulty, effort (None): Metrics related to code volume, difficulty, and effort.
            bugs (None): Placeholder for storing bugs found in the code.
            time (None): Placeholder for storing time-related metrics.
            endmarker, name, number, string, newline, indent, dedent, lpar, rpar, lsqb, rsqb, colon, comma,
            semi, plus, minus, star, slash, vbar, amper, less, greater, equal, dot, percent, lbrace, rbrace,
            eq_equal, not_eq, less_eq, greater_eq, tilde, circumflex, lshift, rshift, dbl_star, plus_eq,
            minus_eq, star_eq, slash_eq, percent_eq, amper_eq, vbar_eq, circumflex_eq, lshift_eq, rshift_eq,
            dbl_star_eq, dbl_slash, dbl_slash_eq, at, at_eq, rarrow, ellipsis, colon_eq, op, error_token,
            comment, nl, encoding, number_int, number_float, kwd_and, kwd_or, kwd_not, kwd_none, kwd_false,
            kwd_true, kwd_as, kwd_assert, kwd_async, kwd_await, kwd_break, kwd_class, kwd_continue, kwd_def,
            kwd_del, kwd_if, kwd_elif, kwd_else, kwd_except, kwd_finally, kwd_for, kwd_while, kwd_import,
            kwd_from, kwd_global, kwd_in, kwd_is, kwd_lambda, kwd_nonlocal, kwd_pass, kwd_raise, kwd_return,
            kwd_try, kwd_with, kwd_yield, keyword, identifier, builtin_type, builtin_func, kwd_print, kwd_input,
            builtin_type_unique, builtin_func_unique, identifiers_unique, identifiers_max_len, identifiers_min_len,
            identifiers_mean_len (float): Various tokens and metrics used for lexical and syntactical analysis.
        """
        self.semester = semester
        self.course = course
        self.assignment = assignment
        self.user = user
        self.problem = problem
        self.complexity = None
        self.classes = None
        self.functions = None
        self.functions_complexity = None
        self.classes_complexity = None
        self.total_complexity = None
        self.blocks = None
        self.loc = None
        self.lloc = None
        self.sloc = None
        self.comments = None
        self.single_comments = None
        self.multi = None
        self.blank = None
        self.h1 = None
        self.h2 = None
        self.N1 = None
        self.N2 = None
        self.vocabulary = None
        self.length = None
        self.calculated_length = None
        self.volume = None
        self.difficulty = None
        self.effort = None
        self.bugs = None
        self.time = None
        self.endmarker = 0.0
        self.name = 0.0
        self.number = 0.0
        self.string = 0.0
        self.newline = 0.0
        self.indent = 0.0
        self.dedent = 0.0
        self.lpar = 0.0
        self.rpar = 0.0
        self.lsqb = 0.0
        self.rsqb = 0.0
        self.colon = 0.0
        self.comma = 0.0
        self.semi = 0.0
        self.plus = 0.0
        self.minus = 0.0
        self.star = 0.0
        self.slash = 0.0
        self.vbar = 0.0
        self.amper = 0.0
        self.less = 0.0
        self.greater = 0.0
        self.equal = 0.0
        self.dot = 0.0
        self.percent = 0.0
        self.lbrace = 0.0
        self.rbrace = 0.0
        self.eq_equal = 0.0
        self.not_eq = 0.0
        self.less_eq = 0.0
        self.greater_eq = 0.0
        self.tilde = 0.0
        self.circumflex = 0.0
        self.lshift = 0.0
        self.rshift = 0.0
        self.dbl_star = 0.0
        self.plus_eq = 0.0
        self.minus_eq = 0.0
        self.star_eq = 0.0
        self.slash_eq = 0.0
        self.percent_eq = 0.0
        self.amper_eq = 0.0
        self.vbar_eq = 0.0
        self.circumflex_eq = 0.0
        self.lshift_eq = 0.0
        self.rshift_eq = 0.0
        self.dbl_star_eq = 0.0
        self.dbl_slash = 0.0
        self.dbl_slash_eq = 0.0
        self.at = 0.0
        self.at_eq = 0.0
        self.rarrow = 0.0
        self.ellipsis = 0.0
        self.colon_eq = 0.0
        self.op = 0.0
        self.error_token = 0.0
        self.comment = 0.0
        self.nl = 0.0
        self.encoding = 0.0
        self.number_int = 0.0
        self.number_float = 0.0
        self.kwd_and = 0.0
        self.kwd_or = 0.0
        self.kwd_not = 0.0
        self.kwd_none = 0.0
        self.kwd_false = 0.0
        self.kwd_true = 0.0
        self.kwd_as = 0.0
        self.kwd_assert = 0.0
        self.kwd_async = 0.0
        self.kwd_await = 0.0
        self.kwd_break = 0.0
        self.kwd_class = 0.0
        self.kwd_continue = 0.0
        self.kwd_def = 0.0
        self.kwd_del = 0.0
        self.kwd_if = 0.0
        self.kwd_elif = 0.0
        self.kwd_else = 0.0
        self.kwd_except = 0.0
        self.kwd_finally = 0.0
        self.kwd_for = 0.0
        self.kwd_while = 0.0
        self.kwd_import = 0.0
        self.kwd_from = 0.0
        self.kwd_global = 0.0
        self.kwd_in = 0.0
        self.kwd_is = 0.0
        self.kwd_lambda = 0.0
        self.kwd_nonlocal = 0.0
        self.kwd_pass = 0.0
        self.kwd_raise = 0.0
        self.kwd_return = 0.0
        self.kwd_try = 0.0
        self.kwd_with = 0.0
        self.kwd_yield = 0.0
        self.keyword = 0.0
        self.identifier = 0.0
        self.builtin_type = 0.0
        self.builtin_func = 0.0
        self.kwd_print = 0.0
        self.kwd_input = 0.0
        self.builtin_type_unique = 0.0
        self.builtin_func_unique = 0.0
        self.identifiers_unique = 0.0
        self.identifiers_max_len = 0.0
        self.identifiers_min_len = 0.0
        self.identifiers_mean_len = 0.0

    def as_list(self):
        """
        Returns the attributes of the SolutionMetrics object as a list.

        Returns:
            list: A list containing the attributes of the SolutionMetrics object.
        """
        return [
            self.semester,
            self.course,
            self.assignment,
            self.user,
            self.problem,
            self.complexity,
            self.classes,
            self.functions,
            self.functions_complexity,
            self.classes_complexity,
            self.total_complexity,
            self.blocks,
            self.loc,
            self.lloc,
            self.sloc,
            self.comments,
            self.single_comments,
            self.multi,
            self.blank,
            self.h1,
            self.h2,
            self.N1,
            self.N2,
            self.vocabulary,
            self.length,
            self.calculated_length,
            self.volume,
            self.difficulty,
            self.effort,
            self.bugs,
            self.time,
            self.endmarker,
            self.name,
            self.number,
            self.string,
            self.newline,
            self.indent,
            self.dedent,
            self.lpar,
            self.rpar,
            self.lsqb,
            self.rsqb,
            self.colon,
            self.comma,
            self.semi,
            self.plus,
            self.minus,
            self.star,
            self.slash,
            self.vbar,
            self.amper,
            self.less,
            self.greater,
            self.equal,
            self.dot,
            self.percent,
            self.lbrace,
            self.rbrace,
            self.eq_equal,
            self.not_eq,
            self.less_eq,
            self.greater_eq,
            self.tilde,
            self.circumflex,
            self.lshift,
            self.rshift,
            self.dbl_star,
            self.plus_eq,
            self.minus_eq,
            self.star_eq,
            self.slash_eq,
            self.percent_eq,
            self.amper_eq,
            self.vbar_eq,
            self.circumflex_eq,
            self.lshift_eq,
            self.rshift_eq,
            self.dbl_star_eq,
            self.dbl_slash,
            self.dbl_slash_eq,
            self.at,
            self.at_eq,
            self.rarrow,
            self.ellipsis,
            self.colon_eq,
            self.op,
            self.error_token,
            self.comment,
            self.nl,
            self.encoding,
            self.number_int,
            self.number_float,
            self.kwd_and,
            self.kwd_or,
            self.kwd_not,
            self.kwd_none,
            self.kwd_false,
            self.kwd_true,
            self.kwd_as,
            self.kwd_assert,
            self.kwd_async,
            self.kwd_await,
            self.kwd_break,
            self.kwd_class,
            self.kwd_continue,
            self.kwd_def,
            self.kwd_del,
            self.kwd_if,
            self.kwd_elif,
            self.kwd_else,
            self.kwd_except,
            self.kwd_finally,
            self.kwd_for,
            self.kwd_while,
            self.kwd_import,
            self.kwd_from,
            self.kwd_global,
            self.kwd_in,
            self.kwd_is,
            self.kwd_lambda,
            self.kwd_nonlocal,
            self.kwd_pass,
            self.kwd_raise,
            self.kwd_return,
            self.kwd_try,
            self.kwd_with,
            self.kwd_yield,
            self.keyword,
            self.identifier,
            self.builtin_type,
            self.builtin_func,
            self.kwd_print,
            self.kwd_input,
            self.builtin_type_unique,
            self.builtin_func_unique,
            self.identifiers_unique,
            self.identifiers_max_len,
            self.identifiers_min_len,
            self.identifiers_mean_len
        ]

    @staticmethod
    def get_attr_names():
        """
        Returns the names of the attributes of the SolutionMetrics object.

        Returns:
            list: A list containing the names of the attributes of the SolutionMetrics object.
        """
        return [
            'semester',
            'course',
            'assignment',
            'user',
            'problem',
            'complexity',
            'classes',
            'functions',
            'functions_complexity',
            'classes_complexity',
            'total_complexity',
            'blocks',
            'loc',
            'lloc',
            'sloc',
            'comments',
            'single_comments',
            'multi',
            'blank',
            'h1',
            'h2',
            'N1',
            'N2',
            'vocabulary',
            'length',
            'calculated_length',
            'volume',
            'difficulty',
            'effort',
            'bugs',
            'time',
            'endmarker',
            'name',
            'number',
            'string',
            'newline',
            'indent',
            'dedent',
            'lpar',
            'rpar',
            'lsqb',
            'rsqb',
            'colon',
            'comma',
            'semi',
            'plus',
            'minus',
            'star',
            'slash',
            'vbar',
            'amper',
            'less',
            'greater',
            'equal',
            'dot',
            'percent',
            'lbrace',
            'rbrace',
            'eq_equal',
            'not_eq',
            'less_eq',
            'greater_eq',
            'tilde',
            'circumflex',
            'lshift',
            'rshift',
            'dbl_star',
            'plus_eq',
            'minus_eq',
            'star_eq',
            'slash_eq',
            'percent_eq',
            'amper_eq',
            'vbar_eq',
            'circumflex_eq',
            'lshift_eq',
            'rshift_eq',
            'dbl_star_eq',
            'dbl_slash',
            'dbl_slash_eq',
            'at',
            'at_eq',
            'rarrow',
            'ellipsis',
            'colon_eq',
            'op',
            'error_token',
            'comment',
            'nl',
            'encoding',
            'number_int',
            'number_float',
            'kwd_and',
            'kwd_or',
            'kwd_not',
            'kwd_none',
            'kwd_false',
            'kwd_true',
            'kwd_as',
            'kwd_assert',
            'kwd_async',
            'kwd_await',
            'kwd_break',
            'kwd_class',
            'kwd_continue',
            'kwd_def',
            'kwd_del',
            'kwd_if',
            'kwd_elif',
            'kwd_else',
            'kwd_except',
            'kwd_finally',
            'kwd_for',
            'kwd_while',
            'kwd_import',
            'kwd_from',
            'kwd_global',
            'kwd_in',
            'kwd_is',
            'kwd_lambda',
            'kwd_nonlocal',
            'kwd_pass',
            'kwd_raise',
            'kwd_return',
            'kwd_try',
            'kwd_with',
            'kwd_yield',
            'keyword',
            'identifier',
            'builtin_type',
            'builtin_func',
            'kwd_print',
            'kwd_input',
            'builtin_type_unique',
            'builtin_func_unique',
            'identifiers_unique',
            'identifiers_max_len',
            'identifiers_min_len',
            'identifiers_mean_len'
        ]


class MouseEvent(CodebenchObject):
    """
    Model object that represents a Codebench User Login Event.
    """

    def __init__(self, assignment, problem, date, event, x, y):
        """
        Initialize a MouseEvent object.

        Args:
            assignment (str): The assignment associated with the event.
            problem (str): The problem associated with the event.
            date (str): The date of the event.
            event (str): The type of event (e.g., "click", "hover").
            x (int): The x-coordinate of the event.
            y (int): The y-coordinate of the event.
        """
        self.assignment = assignment
        self.problem = problem
        self.date = date
        self.event = event
        self.x = x
        self.y = y

    def as_list(self):
        """
        Return MouseEvent attributes as a list.

        Returns:
            list: A list containing assignment, problem, date, event, x, and y.
        """
        return [
            self.assignment,
            self.problem,
            self.date,
            self.event,
            self.x,
            self.y
        ]

    @staticmethod
    def get_attr_names():
        """
        Get attribute names of MouseEvent class.

        Returns:
            list: A list of attribute names.
        """
        return [
            'assignment',
            'problem',
            'date',
            'event',
            'x',
            'y'
        ]
