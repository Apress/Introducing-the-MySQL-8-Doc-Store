#
# Introducing the MySQL 8 Document Store 
#
# This file contains a demonstration of how to read a document from a
# collection. It shows how to iterate over embedded
# data in the form of lists rather than a dependent collection.
#
# Database name = contact_list3
#
# Dr. Charles Bell, 2017
#
import mysqlx

# Connect to server
session = mysqlx.get_session("root:password@localhost:33060")

# Get the schema
schema = session.get_schema("contact_list3")

# Get the collection
contacts = schema.get_collection("contacts")

# Read the row
row = contacts.find("first = '{0}' and last = '{1}'".format('Bill',
                                                            'Smith')).execute()
contact = row.fetch_one()

addresses = contact["addresses"]
phones = contact["phones"]
email_addresses = contact["email_addresses"]

# Display the data
print("Contact List (DocStore)")
print("-----------------------")
suffix = ""
if "suffix" in contact.keys():
    suffix = ", {0}".format(contact["suffix"])    
print("Name: {0} {1}{2}".format(contact["first"],contact["last"],suffix))
if "title" in contact.keys():
    print("Title: {0}".format(contact["title"]))
print("\nAddresses:")
for address in addresses:
    print("\t({0})".format(address["address_type"].upper()))
    print("\t{0}".format(address["street1"]))
    if "street2" in address.keys():
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
