import contacts_pb2

# Open the file
f = open("my_contacts", "wb")

contacts = contacts_pb2.Contacts()

# Create a new contact message
new_contact = contacts.list.add()
new_contact.id = 90125
new_contact.first = "Andrew"

# Add phone numbers
phone_number = new_contact.phones.add()
phone_number.number = '212-555-1212'
phone_number = new_contact.phones.add()
phone_number.number = '212-555-1213'

# Create a new contact message
new_contact = contacts.list.add()
new_contact.id = 90126
new_contact.first = "William"
new_contact.last = "Edwards"

# Add phone numbers
phone_number = new_contact.phones.add()
phone_number.number = '301-555-1111'
phone_number = new_contact.phones.add()
phone_number.number = '301-555-3333'

# Write the data
f.write(contacts.SerializeToString())

# Close the file
f.close()