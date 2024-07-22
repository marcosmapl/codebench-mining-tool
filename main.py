# -*- coding: utf-8 -*-
"""
Codebench Dataset Extractor
Author: Marcos Lima (marcos.lima@icomp.ufam.edu.br)
Organization: Universidade Federal do Amazonas - UFAM, Instituto de Computação - IComp

This script extracts educational data from a specified dataset path, processing semester, course, user, and various log information. It supports enabling or disabling specific data extraction features through command-line arguments.
"""
import argparse
import os
import time
import util
import tarfile 

from collections import Counter, defaultdict
from datetime import datetime

# Command-line argument setup
parser = argparse.ArgumentParser(description="Extracts educational data from a specified dataset path.")
parser.add_argument("-ds", '--dataset', help="Codebench dataset path", type=str, default=None)
parser.add_argument('--executions', dest='extract_executions', action='store_true', help="Extract execution logs")
parser.add_argument('--no-executions', dest='extract_executions', action='store_false', help="Do not extract execution logs")
parser.set_defaults(extract_executions=False)
parser.add_argument('--solutions', dest='extract_solutions', action='store_true', help="Extract solution files")
parser.add_argument('--no-solutions', dest='extract_solutions', action='store_false', help="Do not extract solution files")
parser.set_defaults(extract_solutions=False)
parser.add_argument('--logins', dest='extract_logins', action='store_true', help="Extract login logs")
parser.add_argument('--no-logins', dest='extract_logins', action='store_false', help="Do not extract login logs")
parser.set_defaults(extract_logins=False)
parser.add_argument('--grades', dest='extract_grades', action='store_true', help="Extract grades")
parser.add_argument('--no-grades', dest='extract_grades', action='store_false', help="Do not extract grades")
parser.set_defaults(extract_grades=False)
parser.add_argument('--codemirror', dest='extract_codemirror', action='store_true', help="Extract CodeMirror logs")
parser.add_argument('--no-codemirror', dest='extract_codemirror', action='store_false', help="Do not extract CodeMirror logs")
parser.set_defaults(extract_codemirror=False)
args = parser.parse_args()

# Function to process directories and extract data based on command-line flags
def process_directories(dataset_path, data_lists):
    """
    Processes directories in the dataset, extracting data for semesters and delegating to specific functions for courses, users, etc.

    Args:
        dataset_path (str): Path to the dataset directory.
    """
    for semester_entry in os.scandir(dataset_path):
        util.Logger.info(f'New semester found: {semester_entry.path}')
        new_semester = util.extract_semester(semester_entry.path)
        process_courses(semester_entry, new_semester, data_lists)
        data_lists[util.CODE_SEMESTER].append(new_semester.as_list())

def process_courses(semester_entry, semester_obj, data_lists):
    """
    Processes courses within a semester, extracting course data and further delegating to assignment and user processing.

    Args:
        semester_entry (os.DirEntry): The directory entry for the semester.
        semester_obj (Semester): The semester object.
    """
    for course_entry in os.scandir(semester_entry.path):
        util.Logger.info(f'New course found: {course_entry.path}')
        semester_obj.n_courses += 1
        new_course = util.extract_course(semester_obj.desc, course_entry.name, course_entry.path)
        process_assignments(course_entry, semester_obj, new_course, data_lists)
        process_users(course_entry, semester_obj, new_course, data_lists)
        data_lists[util.CODE_COURSE].append(new_course.as_list())


def process_assignments(course_entry, semester_obj, course_obj, data_lists):
    """
    Processes assignment data for a course.

    Args:
        course_entry (os.DirEntry): The directory entry for the course.
        semester_obj (Semester): The semester object.
        course_obj (Course): The course object.
    """
    for assignment_entry in os.scandir(os.path.join(course_entry.path, 'assessments')):
        util.Logger.info(f'New assignment found: {assignment_entry.path}')
        semester_obj.n_assignments += 1
        course_obj.n_assignments += 1
        new_assignment = util.extract_assignment(semester_obj.desc, course_obj.code, assignment_entry.path)
        data_lists[util.CODE_ASSIGNMENT].append(new_assignment.as_list())

def process_executions(user_entry, semester_obj, course_obj, data_lists):
    """
    Processes executions data for a assignment problem.

    Args:
        user_entry (os.DirEntry): The directory entry for the user.
        semester_obj (Semester): The semester object.
        course_obj (Course): The course object.
    """
    for execution_entry in os.scandir(os.path.join(user_entry.path, 'executions')):
        util.Logger.info(f'New execution file found: {execution_entry.path}')
        semester_obj.n_executions += 1
        assignment, problem = os.path.splitext(execution_entry.name)[0].split('_')
        new_executions = util.extract_executions(semester_obj.desc, course_obj.code, assignment, user_entry.name, problem, execution_entry.path)
        data_lists[util.CODE_EXECUTION].extend([execution.as_list() for execution in new_executions])

def process_solutions(user_entry, semester_obj, course_obj, data_lists):
    """
    Processes solutions data for a assignment problem.

    Args:
        user_entry (os.DirEntry): The directory entry for the user.
        semester_obj (Semester): The semester object.
        course_obj (Course): The course object.
    """
    for solution_entry in os.scandir(os.path.join(user_entry.path, 'codes')):
        util.Logger.info(f'New solution code found: {solution_entry.path}')
        semester_obj.n_codes += 1
        assignment, problem = os.path.splitext(solution_entry.name)[0].split('_')
        new_solution = util.extract_solution(semester_obj.desc, course_obj.code, assignment, user_entry.name, problem, solution_entry.path)
        data_lists[util.CODE_SOLUTION].append(new_solution.as_list())

def process_logins(user_entry, semester_obj, course_obj, data_lists):
    """
    Processes solutions data for a assignment problem.

    Args:
        user_entry (os.DirEntry): The directory entry for the user.
        semester_obj (Semester): The semester object.
        course_obj (Course): The course object.
    """
    user_logins_path = os.path.join(user_entry.path, 'logins.log')
    util.Logger.info(f'Novo arquivo de logins de usuário encontrado: {user_logins_path}')
    user_logins = util.extract_user_logins(semester_obj.desc, course_obj.code, user_entry.name, user_logins_path)
    data_lists[util.CODE_LOGIN].extend([logins.as_list() for logins in user_logins])

def process_grades(user_entry, semester_obj, course_obj, data_lists):
    for grade_entry in os.scandir(os.path.join(user_entry.path, 'grades')):
        if not grade_entry.name.startswith('final_grade'):
            util.Logger.info(f'New assignment grade file found: {grade_entry.path}')
            semester_obj.n_grades += 1
            new_grade = util.extract_grade(semester_obj.desc, course_obj.code, grade_entry.name[:-4], user_entry.name, grade_entry.path)
            data_lists[util.CODE_GRADE].append(new_grade.as_list())

def process_codemirror(user_entry, semester_obj, course_obj, data_lists):
    for mirror_entry in os.scandir(os.path.join(user_entry.path, 'codemirror')):
        util.Logger.info(f'New code mirror event log file found: {mirror_entry.path}')
        semester_obj.n_mirrors += 1
        temp = mirror_entry.name[:-4].split('_')
        cdm_logs = util.extract_codemirror_events(
            semester_obj.desc,
            course_obj.code,
            temp[0],
            user_entry.name,
            temp[1],
            mirror_entry.path
        )
        data_lists[util.CODE_CODEMIRROR].extend([events.as_list() for events in cdm_logs])

def process_users(course_entry, semester_obj, course_obj, data_lists):
    for user_entry in os.scandir(os.path.join(course_entry.path, 'users')):
        util.Logger.info(f'New user found: {user_entry.path}')
        semester_obj.n_users += 1
        course_obj.n_users += 1
        new_user = util.extract_user(semester_obj.desc, course_obj.code, user_entry.path)
        data_lists[util.CODE_USER].append(new_user.as_list())

        if args.extract_executions:
            process_executions(user_entry, semester_obj, course_obj, data_lists)

        if args.extract_solutions:
            process_solutions(user_entry, semester_obj, course_obj, data_lists)

        if args.extract_logins:
            process_logins(user_entry, semester_obj, course_obj, data_lists)

        if args.extract_grades:
            process_grades(user_entry, semester_obj, course_obj, data_lists)
        
        if args.extract_codemirror:
            print(f'CODE ==> {args.extract_codemirror}')
            process_codemirror(user_entry, semester_obj, course_obj, data_lists)

# Main execution starts here
if __name__ == "__main__":
    util.Logger.configure() # Configure logging and record start time
    if args.dataset:
        # Initialize lists to hold extracted data
        data_lists = {name: [] for name in [
            util.CODE_SEMESTER,
            util.CODE_COURSE,
            util.CODE_ASSIGNMENT,
            util.CODE_USER,
            util.CODE_EXECUTION,
            util.CODE_SOLUTION,
            util.CODE_LOGIN,
            util.CODE_GRADE,
            util.CODE_CODEMIRROR
        ]}
        util.Logger.info(f'Extracting data from directory: {args.dataset}')
        file = tarfile.open(args.dataset)
        file.extractall('data')
        file.close()

        start_time = time.time()
        util.Logger.info(f'Starting Data Collection: {time.ctime(start_time)}')
        process_directories('data', data_lists)
        end_time = time.time()
        util.Logger.info(f'Task Completed: {time.ctime(end_time)}')
        util.Logger.info(f'Duration: {end_time - start_time}s')

        util.save_to_csv(data_lists)
    else:
        util.Logger.error("Dataset path was not provided. Exiting...")
        exit(1)
