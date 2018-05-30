
MacBook-Pro:project3 cbell$ mysqlsh user:password@localhost:33060 --py
mysqlx: [Warning] Using a password on the command line interface can be insecure.
Creating a session to 'root@localhost:33060'
Your MySQL connection id is 2087 (X protocol)
Server version: 8.0.3-rc-log MySQL Community Server (GPL)
No default schema selected; type \use <schema> to set one.
MySQL Shell 8.0.3-dmr

Copyright (c) 2016, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type '\help' or '\?' for help; '\quit' to exit.

 MySQL  localhost:33060+ ssl  Py > import mysqlx
 MySQL  localhost:33060+ ssl  Py > session = mysqlx.get_session("user:password@localhost:33060")
 MySQL  localhost:33060+ ssl  Py > schema = session.get_schema("library_v3")
 MySQL  localhost:33060+ ssl  Py > schema = session.create_schema("library_v3")
 MySQL  localhost:33060+ ssl  Py > schema.create_collection("books", True)
<mysqlx.crud.Collection object at 0x106ee0d90>
 MySQL  localhost:33060+ ssl  Py > books = schema.get_collection("books")
 MySQL  localhost:33060+ ssl  Py > books.find().execute().fetch_all();


from library_v3 import Book
books = Book()
books.connect(<user>, <password>,'localhost',33060)
rows = books.get_books()


import mysqlx
session = mysqlx.get_session("user:password@localhost:33060")
schema = session.get_schema("library_v3")
schema.drop_collection("books")
books = schema.create_collection("books")
print ">", books.find().execute().fetch_all();
books.add('{"ISBN":"978-1-4842-1174-8","Title":"3D Printing with Delta Printers","Pub_Year":2015,"Language":"English","Authors":[{"LastName":"Bell","FirstName":"Charles"}],"Publisher":{"Name":"Apress","City":"New York, NY","URL":"http://apress.com"}}').execute()
books.add('{"ISBN":"978-1-4842-1294-3","Title":"MySQL for the Internet of Things","Pub_Year":2016,"Language":"English","Authors":[{"LastName":"Bell","FirstName":"Charles"}],"Publisher":{"Name":"Apress","City":"New York, NY","URL":"http://apress.com"}}').execute()
books.add('{"ISBN":"978-1-4842-2107-5","Title":"Windows 10 for the Internet of Things","Pub_Year":2017,"Language":"English","Authors":[{"LastName":"Bell","FirstName":"Charles"}],"Publisher":{"Name":"Apress","City":"New York, NY","URL":"http://apress.com"}}').execute()
books.add('{"ISBN":"978-1-4842-2724-4","Title":"Introducing the MySQL 8 Document Store","Pub_Year":2018,"Language":"English","Authors":[{"LastName":"Bell","FirstName":"Charles"}],"Publisher":{"Name":"Apress","City":"New York, NY","URL":"http://apress.com"}}').execute()
books.add('{"ISBN":"978-1-4842-3122-7","Title":"MicroPython for the Internet of Things","Pub_Year":2017,"Language":"English","Authors":[{"LastName":"Bell","FirstName":"Charles"}],"Publisher":{"Name":"Apress","City":"New York, NY","URL":"http://apress.com"}}').execute()
books.add('{"ISBN":"978-1449339586","Title":"MySQL High Availability","Pub_Year":2014,"Language":"English","Authors":[{"LastName":"Bell","FirstName":"Charles"},{"LastName":"Kindahl","FirstName":"Mats"},{"LastName":"Thalmann","FirstName":"Lars"}],"Publisher":{"Name":"OReilly","City":"Boston, MA","URL":"http://oreilly.com"}}').execute()
rows = books.find().execute().fetch_all()
