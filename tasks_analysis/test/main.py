import itertools
import json
import os
import shutil
import subprocess
import sys
import unittest

EXCLUDED_SMELLS = [
    'line-too-long', 'trailing-whitespace', 'invalid-name',
    'consider-using-from-import', 'missing-module-docstring',
    'missing-class-docstring', 'missing-function-docstring'
]


def create_test_suite(task) -> unittest.TestSuite:
    # It's necessary to refresh the modules and import them every time,
    # otherwise they would only use the first project file
    if task == 'task1':
        if 'T1_US01' in sys.modules:
            del sys.modules['T1_US01']
            del sys.modules['T1_US02']
            del sys.modules['T1_US03']
            del sys.modules['T1_US04']
            del sys.modules['T1_US05']

        import T1_US01 as US01, T1_US02 as US02, \
            T1_US03 as US03, T1_US04 as US04, T1_US05 as US05
        if 'IntelligentOffice' in sys.modules:
            del sys.modules['IntelligentOffice']
    else:
        if 'T2_US01' in sys.modules:
            del sys.modules['T2_US01']
            del sys.modules['T2_US02']
            del sys.modules['T2_US03']
            del sys.modules['T2_US04']
            del sys.modules['T2_US05']

        import T2_US01 as US01, T2_US02 as US02, \
            T2_US03 as US03, T2_US04 as US04, T2_US05 as US05
        if 'CleaningRobot' in sys.modules:
            del sys.modules['CleaningRobot']

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromModule(US01))
    suite.addTests(loader.loadTestsFromModule(US02))
    suite.addTests(loader.loadTestsFromModule(US03))
    suite.addTests(loader.loadTestsFromModule(US04))
    suite.addTests(loader.loadTestsFromModule(US05))

    return suite


def run_tests() -> None:
    for job in itertools.product(*[['task1', 'task2'], ['tdd', 'no-tdd']]):
        task = job[0]
        category = job[1]
        print('Generating test results for {} in the {} category...'.format(task, category))

        # Paths to the main project directories
        path_to_projects = os.path.join('..', task + '_results', category)
        projects = os.listdir(path_to_projects)
        file_name = 'IntelligentOffice.py' if task == 'task1' else 'CleaningRobot.py'
        project_name = 'intelligent_office' if task == 'task1' else 'cleaning_robot'

        # Full paths of the main source files for the projects
        source_paths = [os.path.join(path_to_projects, p, file_name) for p in projects]
        student_names = [s.replace('_' + project_name, '') for s in projects]

        for student_name, source_file in zip(student_names, source_paths):
            print('Evaluating for student: {}...'.format(student_name))

            shutil.copyfile(source_file, os.path.join('..', file_name))
            with open(os.path.join('..\\test_results', task, category, student_name) + '.log', 'w') as test_log:
                try:
                    test_suite = create_test_suite(task)
                    test_runner = unittest.TextTestRunner(test_log, verbosity=2)
                    test_runner.run(test_suite)
                except Exception as e:
                    print(e)
                    test_log.write('Project contained syntactical errors')

            # Evaluates code smells for the source file
            check_code_smells_pylint(
                source_file,
                os.path.join('..\\test_results', task, category, student_name) + '_code_smells_pylint.json'
            )


def check_code_smells_pylint(source, destination) -> None:
    with open(destination, 'w') as smells_file:
        subprocess.run(['pylint', '--output-format', 'json', source], stdout=smells_file)


def parse_code_smells_pylint() -> None:
    for job in itertools.product(*[['task1', 'task2'], ['tdd', 'no-tdd']]):
        # Paths to the main project directories
        path_to_logs = os.path.join('..', 'test_results', job[0], job[1])
        log_files = [f for f in os.listdir(path_to_logs) if f.endswith('.json') and
                     not f.endswith('_parsed.json')]

        for f in log_files:
            parsed_objects = []
            with open(os.path.join(path_to_logs, f), 'r') as json_file:
                data = json.load(json_file)
                for i, obj in enumerate(data):
                    if data[i]['symbol'] not in EXCLUDED_SMELLS:
                        parsed_objects.append(obj)
                    else:
                        continue

                f_ = f.replace('.json', '_parsed.json')
                f_path = os.path.join(path_to_logs, f_)

                if os.path.exists(f_path):
                    os.remove(f_path)
                with open(f_path, 'w') as parsed_json:
                    json.dump(parsed_objects, parsed_json, indent=4)


def extract_results() -> None:
    print('Generating test summary...')

    with open('..\\test_results\\summary.log', 'w') as log_summary:
        for job in itertools.product(*[['task1', 'task2'], ['tdd', 'no-tdd']]):
            task = job[0]
            category = job[1]
            task_ = 'Task 1' if task == 'task1' else 'Task 2'
            category = 'TDD' if category == 'tdd' else 'No-TDD'
            path_to_logs = os.path.join('..', 'test_results', task, category)

            log_summary.writelines('------------------------------\n')
            log_summary.writelines(task_ + ' ' + category + ' summary:\n')
            log_summary.writelines('------------------------------\n')

            log_files = [f for f in os.listdir(path_to_logs) if f.endswith('.log')]
            total_passes = 0
            total_failures = 0
            total_errors = 0

            for i, file in enumerate(log_files):
                student_name = file[: file.find('.')].replace('_', ' ')
                stories_passes = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

                with open(os.path.join(path_to_logs, file), 'r') as log_file:
                    passes = 0
                    failures = 0
                    errors = 0
                    tackled_tasks = 0
                    dnf = False

                    log_summary.writelines(student_name + ':\n')
                    lines = log_file.readlines()
                    for line in lines:
                        if line == 'Project contained syntactical errors':
                            log_summary.writelines('Project does not compile.\n')
                            dnf = True
                            break
                        if not line.strip():
                            break

                        story_num = int(line[: line.find('...')][-3: -2]) - 1
                        line = line[line.find('...') + 4:].strip()

                        t = (0, 0, 0)
                        match line:
                            case 'ok':
                                passes += 1
                                total_passes += 1
                                t = (1, 0, 0)
                            case 'FAIL':
                                failures += 1
                                total_failures += 1
                                t = (0, 1, 0)
                            case 'ERROR':
                                errors += 1
                                total_errors += 1
                                t = (0, 0, 1)
                        stories_passes[story_num] = tuple([sum(tup) for tup in zip(stories_passes[story_num], t)])

                    if dnf is False:
                        log_summary.writelines('PASSES: ' + str(passes) + '\n')
                        log_summary.writelines('FAILURES: ' + str(failures) + '\n')
                        log_summary.writelines('ERRORS: ' + str(errors) + '\n')

                        for j, story in enumerate(stories_passes):
                            story_passes = story[0]
                            story_failures = story[1]
                            story_errors = story[2]
                            story_total = story_passes + story_failures + story_errors
                            if story_passes > 0:
                                tackled_tasks += 1

                            log_summary.writelines('\nUS0 ' + str(j + 1) + ':\n')
                            log_summary.writelines('PASSES: ' + str(story_passes) + '\n')
                            log_summary.writelines('FAILURES: ' + str(story_failures) + '\n')
                            log_summary.writelines('ERRORS: ' + str(story_errors) + '\n')
                            log_summary.writelines('TOTAL: ' + str(story_total) + '\n')
                            log_summary.writelines('QLTY' + str(j + 1) + ': ' + str(story_passes / story_total) + '\n')
                    log_summary.writelines('\n')
                    log_summary.writelines('#TUS: ' + str(tackled_tasks) + '\n\n\n')

            log_summary.writelines('TOTAL PASSES: ' + str(total_passes) + '\n')
            log_summary.writelines('TOTAL FAILURES: ' + str(total_failures) + '\n')
            log_summary.writelines('TOTAL ERRORS: ' + str(total_errors) + '\n')
            log_summary.writelines('\n\n\n')

    print('Summary generated')


if __name__ == '__main__':
    extract_results()
