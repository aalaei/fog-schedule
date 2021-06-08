import os
import random
# import names

transaction_count = 100000
problem_count = 10


def main():
    problems = ["problem" + str(x) + ".txt" for x in range(1, problem_count + 1)]
    for problem in problems:
        f = open(problem, "w")
        for i in range(transaction_count):
            f.write(chr(random.randint(ord('A'), ord('Z'))))
            # f.write(names.get_first_name())
            f.write(">")
            f.write(chr(random.randint(ord('A'), ord('Z'))))
            # f.write(names.get_first_name())
            f.write(":")
            f.write(str(random.randint(0, 10000000)/100))
            f.write('\n')
        f.write('---------------------\nNonce=?\n->Me:1')
        f.close()


if __name__ == '__main__':
    main()
