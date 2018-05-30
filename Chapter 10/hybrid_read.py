#
# Introducing the MySQL 8 Document Store 
#
# This file contains a demonstration of how to read a hybrid table
# that contains JSON columns. It shows how to iterate over embedded
# data in the form of lists rather than a dependent table.
#
# Database name = contact_list2
#
# Dr. Charles Bell, 2017
#
import mysqlx
from json import JSONDecoder

GET_BILL = """
SELECT * FROM contact_list2.contacts
WHERE last = 'Smith' AND first = 'Bill'
"""

# Connect to database
session = mysqlx.get_session("root:password@localhost:33060")

# Read the row
row = session.sql(GET_BILL).execute().fetch_one()

# Convert JSON strings to Python dictionaries
addresses = JSONDecoder().decode(row["addresses"])["addresses"]
phones = JSONDecoder().decode(row["phones"])["phones"]
email_addresses = JSONDecoder().decode(row["email_addresses"])["email_addresses"]

# Display the data
print("Contact List (Hybrid)")
print("---------------------")
print("Name: {0} {1}".format(row["first"],row["last"]))
print("\nAddresses:")
for address in addresses:
    print("\t({0})".format(address["address_type"].upper()))
    print("\t{0}".format(address["street1"]))
    if address["street2"]:
        print("\t{0}".format(address["street2"]))
    print("\t{0}, {1} {2}".format(address["city"],
                                  address["state"],
                                  address["zip"]))
print("\nPhones:")
for phone in phones:
    print("\t({0}) {1}-{2}".format(phone["area_code"],
                                   phone["exchange"],
                                   phone["number"]))
print("\neMail Addresses:")
for email in email_addresses:
    print("\t{0}".format(email))

print("")
