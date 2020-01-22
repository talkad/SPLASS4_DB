import sys

from PersistenceLayer import psl, Coffee_stand, Employee, Product, Supplier


def insert_to_db(line):

    array = line.split(", ")
    if array[0] == "C":
        coffee_stand = Coffee_stand(array[1], array[2], array[3])
        psl.coffee_stands.insert(coffee_stand)
    elif array[0] == "E":
        employee = Employee(array[1], array[2], array[3], array[4])
        psl.employees.insert(employee)
    elif array[0] == "P":
        product = Product(array[1], array[2], array[3], 0)
        psl.products.insert(product)
    elif array[0] == "S":
        supplier = Supplier(array[1], array[2], array[3])
        psl.suppliers.insert(supplier)


# args
def main(argv):
    filename = argv[1]
    with open(filename) as f:
        content = f.readlines()
    psl.create_tables()
    # want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    for line in content:
        insert_to_db(line)


# sys.argv
if __name__ == '__main__':
    main(sys.argv)
