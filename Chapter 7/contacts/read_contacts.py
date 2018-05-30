import contacts_pb2

contacts = contacts_pb2.Contacts()

# Read the existing contacts.
with open("my_contacts", "rb") as f:
    contacts.ParseFromString(f.read())

# Print out the contacts
for contact in contacts.list:
    # print contact
    print contact.first, contact.last,
    for phone in contact.phones:
        print phone.number,
    print

f.close()