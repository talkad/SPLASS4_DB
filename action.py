import functools
import sys

from PersistenceLayer import Activity, psl
from printdb import printTables, print_total_sells, print_activities


def execute_line(line):
    fields = line.split(", ")
    activity = Activity(fields[0], fields[1], fields[2], fields[3])
    product_id = int(fields[0])
    result = psl.products.get_quantity_of_id(product_id)
    if result:
        res = functools.reduce(lambda sub, ele: sub * 10 + ele, result)
        if res + int(fields[1]) >= 0:
            psl.products.update_quantity_of_id(res + int(fields[1]), product_id)
            psl.activities.insert(activity)


def main(argv):
    filename = argv[1]
    with open(filename) as f:
        content = f.readlines()
    # want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    for line in content:
        execute_line(line)
    printTables()
    print_total_sells()
    print_activities()


if __name__ == '__main__':
    main(sys.argv)
