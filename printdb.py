import sys

from PersistenceLayer import psl


def printTables():
    print("Activities")
    for item in psl.activities.get_activities():
        print("{}".format(str(item)))
    print("Coffee_stands")
    for item in psl.coffee_stands.get_coffee_stand():
        print("{}".format(str(item)))
    print("Employees")
    for item in psl.employees.get_employee():
        print("{}".format(str(item)))
    print("Products")
    for item in psl.products.get_products():
        print("{}".format(str(item)))
    print("Suppliers")
    for item in psl.suppliers.get_supplier():
        print("{}".format(str(item)))


def print_total_sells():
    print("\nEmployees report")
    for item in psl.get_total_sales():
        line= "{} {} {} ".format(item[0], item[1], item[2])
        if not item[3]:
            line += "0"
        else:
            line += str(item[3])
        print(line)


def print_activities():
    elements = psl.get_activities_join()
    if elements:
        print("\nActivities")
        for item in elements:
            print("{}".format(str(item)))


def main(args):
    printTables()
    print_total_sells()
    print_activities()


if __name__ == '__main__':
    main(sys.argv)
