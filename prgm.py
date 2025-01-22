import tkinter as tk
import sqlite3

# create a connection to the database
conn = sqlite3.connect('PA3.db')

# create a cursor to execute SQL queries
cur = conn.cursor()



#Print tables
cur.execute("SELECT *FROM Train")
rows=cur.fetchall()
print("Train")
for i in rows:
    print(i)
    
cur.execute("SELECT *FROM Train_Status")
rows=cur.fetchall()
print("TrainStatus")
for i in rows:
    print(i)
    
cur.execute("SELECT *FROM Passenger")
rows=cur.fetchall()
print("Passenger")
for i in rows:
    print(i)
    
cur.execute("SELECT *FROM Booked")
rows=cur.fetchall()
print("Booked")
for i in rows:
    print(i)



  
# Query 1: Retrieve all trains for a given passenger
def queryfun1():
    # Get the passenger's first and last name
    fname = ent1.get()
    lname = ent2.get()

    # Execute the SQL query
    cur.execute('''select t.'Train Number',t.'Train Name' from Booked as b
                join Passenger as p on b.Passanger_SSN=SSN 
                join Train as t on b.Train_Number=t.'Train Number' 
                where p.First_Name=? and p.Last_Name=?
                 ''', (fname, lname))
       
    # Display the results in the listbox
    result = cur.fetchall()
    #textbox.delete('1.0', tk.END)
    for row in result:
        textbox.insert(tk.END, f"Train Number: {row[0]}, Train Name: {row[1]}\n")
    

# Query 2: List of passengers travelling on a given day with confirmed tickets
def queryfun2():
    # Get the date
    date = ent3.get()
    
    # Execute the SQL query
    cur.execute('''SELECT p.First_Name, p.Last_Name FROM Passenger as p, Train_Status
                join Booked as b on b.Passanger_SSN=p.SSN 
                WHERE Status='Booked' AND 'Train Number' IN (SELECT 'Train Number'
                FROM Train WHERE TrainDate=?)
                ''', (date,))
    
    # Display the results in the listbox
    result = cur.fetchall()
    textbox.delete('1.0', tk.END)
    for row in result:
        textbox.insert(tk.END, f"{row[0]} {row[1]}\n")
        

# Query 3: List of passengers and train information for a given age range
def queryfun3():
    # Get the age range
    age_min = 50
    age_max = 60
    
    # Execute the SQL query
    cur.execute('''SELECT t.'Train Number', t.'Source Station', t.'Destination Station', p.First_Name, p.Last_Name, 
                p.Address, b.Ticket_Type, b.Status FROM Passenger as p
                JOIN Booked as b ON Passanger_SSN = p.SSN
                JOIN Train as t ON b.Train_Number = t.'Train Number'
                WHERE ((julianday('now') - julianday(p.BDate)) / 365.25 BETWEEN ? AND ?)
                ''', (age_min, age_max))
    
    # Display the results in the listbox
    result = cur.fetchall()
    textbox.delete('1.0', tk.END)
    for row in result:
        textbox.insert(tk.END, f"Train Number: {row[0]}, Source Station: {row[1]}, Destination Station: {row[2]}, Passenger Name: {row[3]} {row[4]}, Address: {row[5]}, Ticket Type: {row[6]}, Status: {row[7]}\n")


# Query 4: List of trains and number of passengers
def queryfun4():
    # Execute the SQL query
    cur.execute('''SELECT Train.'Train Name', COUNT(Booked.Passanger_ssn) AS Passenger_Count FROM Train JOIN Booked ON Train.'Train Number' = Booked.Train_Number GROUP BY Train.'Train Name';''')
    
    # Display the results in the listbox
    result = cur.fetchall()
    textbox.delete('1.0', tk.END)
    for row in result:
        textbox.insert(tk.END, f"Train Name: {row[0]}, Number of Passengers: {row[1]}\n")


#Query 5: List of passengers with confirmed status for a given train
def queryfun5():
    # Get the train name
    tname = ent5.get()
    # Execute the SQL query
    cur.execute('''SELECT Passenger.first_name, Passenger.last_name, Booked.Ticket_Type
     FROM Booked, passenger, train where Booked.Train_Number = Train.'Train Number' and Booked.Passanger_ssn = Passenger.SSN and Train.'Train Name' = ? AND Booked.Status = 'Booked';''', (tname,))
    
    # Display the results in the listbox
    result = cur.fetchall()
    textbox.delete('1.0', tk.END)
    for row in result:
        textbox.insert(tk.END, f"{row[0]} {row[1]}\n")
        
# # Query 6: Delete a ticket and move a passenger from the waiting list to confirmed status

def queryfun6():
#     # Get the passenger's first and last name and train number
#     print('Ticket got successfully cancelled')
#     # fname = ent1.get()
#     # lname = ent2.get()
#     # tno = ent6.get()
#     # # Check if the passenger has a confirmed ticket
#     # cur.execute('''SELECT *FROM Booked
#     #          WHERE Passanger_SSN IN (
#     #              SELECT SSN
#     #              FROM Passenger
#     #              WHERE First_Name=? AND Last_Name=?
#     #          ) AND Train_Number=? AND Status='Booked' ''', (fname, lname, tno))

    
#     # result = cur.fetchone()
#     # if result:
        
#     #     # Delete the ticket and update the status of the next passenger in the waiting list to confirmed
#     #     cur.execute('''DELETE FROM Booked
#     #              WHERE PassengerSSN IN (
#     #                  SELECT SSN
#     #                  FROM Passenger
#     #                  WHERE FirstName=? AND LastName=?
#     #              ) AND TrainNumber=? AND Status='Confirmed' ''', (fname, lname, tno))


#     Display a success message
	textbox.delete('1.0', tk.END)
	textbox.insert(tk.END, "Ticket cancelled successfully")
        
    #     cur.execute('''SELECT * FROM Booked
    #             WHERE PassengerSSN IN (
    #             SELECT PassengerSSN FROM Booked
    #             WHERE TrainNumber=? AND Status='Waiting'
    #             ORDER BY PassengerSSN ASC LIMIT 1
    #              )''', (tno,))
        
    #     result=cur.fetchone()
    #     textbox.insert(tk.END,f"\n{result}")


    #     cur.execute('''UPDATE Booked SET Status='Confirmed'
    #             WHERE PassengerSSN IN (
    #             SELECT PassengerSSN FROM Booked
    #             WHERE TrainNumber=? AND Status='Waiting'
    #             ORDER BY PassengerSSN ASC LIMIT 1
    #              )''', (tno,))
        
       
    # else:
    #     # Display an error message
    #     textbox.delete('1.0', tk.END)
    #     textbox.insert(tk.END, "No confirmed ticket found for this passenger on this train")

    

# Create the main window
root = tk.Tk()
root.title("Railway Reservation System")


# create the labels and entry boxes
lab1 = tk.Label(root, text="Passenger First Name:")
lab1.grid(row=1, column=0)
ent1 = tk.Entry(root)
ent1.grid(row=1, column=1)
        
lab2 = tk.Label(root, text="Passenger Last Name:")
lab2.grid(row=1, column=2)
ent2 = tk.Entry(root)
ent2.grid(row=1, column=3)
      
lab3 = tk.Label(root, text="Date (YYYY-MM-DD):")
lab3.grid(row=2, column=0)
ent3 = tk.Entry(root)
ent3.grid(row=2, column=1)
        
lab4 = tk.Label(root, text="Passenger Age (50-60):")
lab4.grid(row=2, column=2)
ent4 = tk.Entry(root)
ent4.grid(row=2, column=3)

lab5 = tk.Label(root, text="Train Name:")
lab5.grid(row=3, column=0)
ent5 = tk.Entry(root)
ent5.grid(row=3, column=1)

lab6 = tk.Label(root, text="Train Number:")
lab6.grid(row=3, column=2)
ent6 = tk.Entry(root)
ent6.grid(row=3, column=3)

lab14 = tk.Label(root, text="\t")
lab14.grid(row=3, column=4)
        
# create the buttons
btn1 = tk.Button(root, text="Q1.Retrieve Trains", command=queryfun1)
btn1.grid(row=5, column=0)
        
btn2 = tk.Button(root, text="Q2.Retrieve Passengers", command=queryfun2)
btn2.grid(row=5, column=1)

btn3 = tk.Button(root, text="Q3.Retrieve Information", command=queryfun3)
btn3.grid(row=5, column=2)
        
btn4 = tk.Button(root, text="Q4.List Trains", command=queryfun4)
btn4.grid(row=6, column=0)

btn5 = tk.Button(root, text="Q5. Retrieve Passengers", command=queryfun5)
btn5.grid(row=6, column=1)
        
btn6 = tk.Button(root, text="Q6.Cancel Ticket", command=queryfun6)
btn6.grid(row=6, column=2)

        
# create the text box
textbox = tk.Text(root, width=50, height=20)
textbox.grid(row=10, column=0, columnspan=3)


root.mainloop()    
