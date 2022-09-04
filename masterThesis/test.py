import csv
import json


def main():
    with open('tests.json', 'r') as out:
        test_cases = json.load(out)
    for test_case in test_cases:
        for i in range(len(test_case)):
            test_case[i] = tuple(test_case[i])

    print('Test cases before truncation: ', len(test_cases))

    # Truncates all test cases to 200 points and deletes the shorter ones
    parsed_cases = []
    max_threshold = 150
    for test_case in test_cases:
        parsed_case = []
        if len(test_case) > max_threshold:
            for tup in test_case[: max_threshold]:
                x = tup[0]
                y = tup[1]
                parsed_case += [x, y]
            parsed_cases.append(parsed_case)

    print('{} test cases were shorter than the {} length threshold and were truncated.'
          .format(len(test_cases) - len(parsed_cases), max_threshold))

    list_to_csv(parsed_cases)


def list_to_csv(items: list):
    """
    Parses the test cases and saves them to a csv file
    """

    # Get the column names for the csv in the form
    # x1, y1, x2, y2, ... x200, y200
    columns = []
    print(len(items[0]))
    i = 0
    while i < len(items[0]) / 2:
        columns += ['x' + str(i), 'y' + str(i)]
        i += 1
    columns.append('difficulty')

    with open('tests.csv', 'w', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=columns)
        writer.writeheader()
        for item in items:
            test_dict = {}
            for i, col in zip(item, columns):
                test_dict.update({
                    col: i
                })
            writer.writerow(test_dict)


if __name__ == '__main__':
    main()
