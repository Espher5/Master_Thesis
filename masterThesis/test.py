import json

def main():
    l = [1, 2, 3]
    fitness = max(l) * (-1)
    print(fitness)


if __name__ == '__main__':
    with open('tests.json', 'r') as out:
        test_cases = json.load(out)
    for test_case in test_cases:
        for i in range(len(test_case)):
            test_case[i] = tuple(test_case[i])

    print(test_cases)

