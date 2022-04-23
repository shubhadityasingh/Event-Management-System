import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

try:
  cnx = mysql.connector.connect(user='root',
                                database='event_manager')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()


'''
we have used:
sum
count
join
avg
min
max

'''


def add_event(event_id,user_id,event_name,manager_name,event_type,sponsors,tags,organizer,payment,timedate,venue_name):
    cnx = mysql.connector.connect(user='root', database='event_manager')
    cursor = cnx.cursor()

    #tomorrow = datetime.now().date() + timedelta(days=1)
    #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

    add = ("INSERT INTO events "
                   "(event_id,user_id ,event_name, manager_name, event_type, sponsors,tags,organizer,payment) "
                   "VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(add,(event_id,user_id,event_name,manager_name,event_type,sponsors,tags,organizer,payment))
    cnx.commit()

    add2= ("INSERT INTO venue "
                   "(event_id,timedate,venue_name) "
                   "VALUES (%s,%s, %s)")

    cursor.execute(add2,(event_id,timedate,venue_name))
    cnx.commit()
    
    

    cursor.close()
    cnx.close()


#add_event(2,2,"Wedding","Mark","Celebration","None","Wedding+Celebration+Bride+Groom","Elizabeth Oliver",1000,"2022-05-21 11:07:19","Taj Hotel, Chennai, 600010")




def edit_event(event_id,user_id,event_name,manager_name,event_type,sponsors,tags,organizer,payment,timedate,venue_name):
    cnx = mysql.connector.connect(user='root', database='event_manager')
    cursor = cnx.cursor()

    #tomorrow = datetime.now().date() + timedelta(days=1)
    #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

    edit = ("UPDATE events "
                   "SET event_name = %s, payment=%s, manager_name = %s, event_type=%s, sponsors=%s, tags=%s, organizer=%s  "
                   "WHERE user_id=%s and event_id=%s")
    
    cursor.execute(edit,(event_name,payment,manager_name,event_type,sponsors,tags,organizer,user_id, event_id))
    cnx.commit()

    edit2= ("UPDATE venue "
                   "SET event_id=%s,timedate=%s,venue_name=%s WHERE event_id=%s")

    cursor.execute(edit2,(event_id,timedate,venue_name,event_id))    
    cnx.commit()

    cursor.close()
    cnx.close()


#edit_event(4,4,"shubs and aryans birthday","aryan mohan","21th birthday","none","birthday+friends only+celebration","aryan",100,"2022-04-22 12:07:19","not aryans ghar")


def delete_event(event_id):
    cnx = mysql.connector.connect(user='root', database='event_manager')
    cursor = cnx.cursor()

    #tomorrow = datetime.now().date() + timedelta(days=1)
    #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

    delete = (""" DELETE FROM venue WHERE event_id="""+str(event_id)+""" """)
    
    cursor.execute(delete)
    cnx.commit()

    delete2 = (""" DELETE FROM events WHERE event_id="""+str(event_id)+""" """)
    cursor.execute(delete2)    
    cnx.commit()

    cursor.close()
    cnx.close()

#delete_event(1)





def total_participants(event_id):
    #from payments table, get total participants in that event
    print("\n\nTotal Participants:")
    cnx = mysql.connector.connect(user='root', database='event_manager')
    cursor = cnx.cursor()

    #tomorrow = datetime.now().date() + timedelta(days=1)
    #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

    count = (""" SELECT count(payment_id) from payment WHERE event_id="""+str(event_id)+""" """)
    
    cursor.execute(count)
    result=cursor.fetchall()
    print("Number of Participants in event "+str(event_id)+" is : ",result[0][0])
    cnx.commit()

    cursor.close()
    cnx.close()

total_participants(1)



def total_payment_collected(event_id):
    #add all payment
    print("\n\nTotal Payment Collected:")
    cnx = mysql.connector.connect(user='root', database='event_manager')
    cursor = cnx.cursor()

    #tomorrow = datetime.now().date() + timedelta(days=1)
    #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

    count = (""" SELECT sum(amount) from payment WHERE event_id="""+str(event_id)+""" """)
    
    cursor.execute(count)
    result=cursor.fetchall()
    print("Total Amount Collected for event "+str(event_id)+" is : ",result[0][0])
    cnx.commit()

    cursor.close()
    cnx.close()

total_payment_collected(1)






def add_user(user_id, name, user_type, contact, gender, username, password):
  cnx = mysql.connector.connect(user='root', database='event_manager')
  cursor = cnx.cursor()

  create_user = ("INSERT INTO event_manager.user "
                "(user_id, name, user_type, contact, gender, username, password) "
                "VALUES (%s, %s,%s,%s,%s,%s,%s)")

  cursor.execute(create_user,(user_id, name, user_type, contact, gender, username, password))
  cnx.commit()

  cursor.close()
  cnx.close()


#add_user(2, 'Max', 'premium', '9813235678', 'male', 'maxx', 'max123')


def get_user_details(user_id):
  print("\n\nUser Details:")
  cnx = mysql.connector.connect(user='root', database='event_manager')
  cursor = cnx.cursor(buffered=True)

  fetch_user = (f"select name, contact, gender from user where user_id={str(user_id)}")

  cursor.execute(fetch_user)
  for row in cursor:
    print("\nName: ",row[0])
    print("Contact Number: ",row[1])
    print("Gender : ",row[2])


  cursor.close()
  cnx.close()

get_user_details(1)


def get_event_details(event_id):
  print("\n\nEvent Details:")
  cnx = mysql.connector.connect(user='root', database='event_manager')
  cursor = cnx.cursor(buffered=True)

  fetch_event = (f"select c.event_name, c.manager_name, c.event_type,v.venue_name, v.timedate,c.sponsors, c.organizer,c.tags from events as c join venue as v on v.event_id = c.event_id where c.event_id={str(event_id)}")

  cursor.execute(fetch_event)
  result=cursor.fetchall()
  
    
  print("\nEvent Name : ",result[0][0])
  print("Manager Name : ",result[0][1])
  print("Event Type: ",result[0][2])
  print("Event Sponsor(s): ",result[0][5])
  print("Organizer: ",result[0][6])
  print("Tags: ",', '.join(result[0][7].split('+')))
  print("Venue Name: ",result[0][3])
  print("Date: ",result[0][4].date())
  print("Time : ",result[0][4].time())




  cursor.close()
  cnx.close()


get_event_details(1)



def price_info(event_id):
  print("\n\nPrice Information:")
  cnx = mysql.connector.connect(user='root', database='event_manager')
  cursor = cnx.cursor()

  #tomorrow = datetime.now().date() + timedelta(days=1)
  #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

  price = (""" SELECT avg(amount),min(amount),max(amount) from payment WHERE event_id="""+str(event_id)+""" """)
  
  cursor.execute(price)
  result=cursor.fetchall()

  event_name = (""" SELECT event_name from events WHERE event_id="""+str(event_id)+""" """)
  cursor.execute(event_name)
  result2=cursor.fetchall()
  print("\nAvg Price for Event '"+str(result2[0][0])+"' is : ",result[0][0])
  print("Minimum Price for Event '"+str(result2[0][0])+"' is : ",result[0][1])
  print("Maximum Price for Event '"+str(result2[0][0])+"' is : ",result[0][2])
  cnx.commit()

  cursor.close()
  cnx.close()

price_info(1)



def buy_ticket(event_id,user_id ,payment_mode, amount):
  cnx = mysql.connector.connect(user='root', database='event_manager')
  cursor = cnx.cursor()

  #tomorrow = datetime.now().date() + timedelta(days=1)
  #event_id   user_id event_name  manager_name    event_type  sponsors    tags    organizer   payment

  buy = ("INSERT INTO payment "
                 "(event_id,user_id ,payment_mode, amount) "
                 "VALUES (%s, %s, %s, %s)")
  cursor.execute(buy,(event_id,user_id ,payment_mode, amount))
  cnx.commit()

  cursor.close()
  cnx.close()

#buy_ticket(1,2,'physical',1600)
