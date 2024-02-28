import tkinter
import customtkinter
import mysql.connector
import time
import os
from twilio.rest import Client

myconn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="SOSer"
)

print(myconn)
cur = myconn.cursor(buffered=True)
print(cur)

app = customtkinter.CTk()
app.geometry("400x650")
app.title("SOS-er")
app.config(background="black")

email_for_updation = ""
volunteer_latitude_for_updation = ""
volunteer_longitude_for_updation = ""
personalsos_user_email = ""
sosmsg = ""
public_sos_description = ""

def insertCredentials(username: str,password: str):
    sql = "INSERT INTO credentials_Volunteer(userName,passWord) VALUES(%s,%s)"
    val = (username,password)
    cur.execute(sql,val)
    myconn.commit()

def insertCredentials_User(username: str,password: str):
    sql = "INSERT INTO credentials_User(userName,passWord) VALUES(%s,%s)"
    val = (username,password)
    cur.execute(sql,val)
    myconn.commit()

soser_title = customtkinter.CTkLabel(master=app,text="SOS-er",font=("Hanson",30),fg_color="black",bg_color="black")
soser_title.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)

def userPressed():
    print("User Pressed")
    soserUser_app = customtkinter.CTk()
    soserUser_app.geometry("1920x1080")
    soserUser_app.title("SOS-er: User Login")
    soserUser_app.config(background="black")

    soser_title = customtkinter.CTkLabel(master=soserUser_app,text="SOS-er",font=("Hanson",30),fg_color="black",bg_color="black")
    soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

    user_title = customtkinter.CTkLabel(master=soserUser_app,text="User Login",text_color="white",font=("Poppins",18),
                    fg_color="black",bg_color="black")
    user_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

    def returnPressed():
        print("Return Pressed from User Login")
        soserUser_app.destroy()

    return_button = customtkinter.CTkButton(master=soserUser_app,fg_color="black",bg_color="black",text_color="grey",
                    text="Return to Home",command=returnPressed)
    return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

    loginstatus_User = customtkinter.CTkLabel(master=soserUser_app,text="",text_color="white",fg_color="black",
                        bg_color="black")
    loginstatus_User.place(relx=0.5,rely=0.40,anchor=tkinter.CENTER)

    username_User = customtkinter.CTkEntry(master=soserUser_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Username",placeholder_text_color="grey")
    username_User.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

    password_User = customtkinter.CTkEntry(master=soserUser_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Password",placeholder_text_color="grey")
    password_User.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

    def loginUser():
        print("User Login Button Pressed")
        
        import hashlib

        def mailCheck():
            print("Email Checking...")
            if('@gmail.com' in username_User.get()):
                loginstatus_User.configure(text="")
            else:
                loginstatus_User.configure(text="Enter Valid Mail ID")

        if(username_User.get() == "" and password_User.get() == ""):
            print("Username and Password Fields are Empty")
            loginstatus_User.configure(text="Enter Credentials")
        elif(username_User.get() == "" and password_User.get() != ""):
            print("Username Field is Empty")
            loginstatus_User.configure(text="Enter Username")
        elif(username_User.get() != "" and password_User.get() == ""):
            print("Password Field is Empty")
            loginstatus_User.configure(text="Enter Password")
        elif(username_User.get() != "" and password_User.get() != ""):
            print("Login Initiated")
            loginstatus_User.configure(text="")
            username = username_User.get()
            personalsos_user_email = username
            password = password_User.get()
            passwordmd5 = hashlib.md5(password.encode())
            print(passwordmd5.digest())
            sql = "SELECT * from credentials_User\
            WHERE userName = %s and passWord = %s"
            val = (username,passwordmd5.hexdigest())
            cur.execute(sql, val)
            result = cur.fetchone()
            print(result)
            if(result==None):
                loginstatus_User.configure(text="Incorrect Username or Password",text_color="red")
            else:
                loginstatus_User.configure(text="")
                #personalsos_user_email = username

                #Screen after Login
                mainscreen_User = customtkinter.CTk()
                mainscreen_User.geometry("1920x1080")
                mainscreen_User.title("SOS-er: User")
                mainscreen_User.config(background="black")

                soser_title = customtkinter.CTkLabel(master=mainscreen_User,text="SOS-er",font=("Hanson",30),fg_color="black",
                                bg_color="black")
                soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

                def personalSOSpressed():
                    print("Personal SOS button pressed")
                    personalSOS_app = customtkinter.CTk()
                    personalSOS_app.geometry("1920x1080")
                    personalSOS_app.title("SOS-er: Personal SOS")
                    personalSOS_app.config(background="black")

                    soser_title = customtkinter.CTkLabel(master=personalSOS_app,text="SOS-er",font=("Hanson",30),fg_color="black",bg_color="black")
                    soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

                    user_title = customtkinter.CTkLabel(master=personalSOS_app,text="Personal SOS",text_color="white",font=("Poppins",18),
                                    fg_color="black",bg_color="black")
                    user_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

                    def returnPressed():
                        print("Return Pressed from Personal SOS")
                        personalSOS_app.destroy()

                    return_button = customtkinter.CTkButton(master=personalSOS_app,fg_color="black",bg_color="black",text_color="grey",
                                    text="Return to Home",command=returnPressed)
                    return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

                    sql_personalsos = "SELECT * from sosDetails_Personal\
                    WHERE mailID = %s"
                    val_personalsos = (personalsos_user_email)
                    cur.execute(sql_personalsos,(val_personalsos,))
                    result = cur.fetchone()
                    if(result == None):
                        print("User Details not avilable")
                        fullname_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Full Name")
                        fullname_entry.place(relx=0.5,rely=0.40,anchor=tkinter.CENTER)

                        mailID_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Mail ID")
                        mailID_entry.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

                        personalNumber_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Mobile Number")
                        personalNumber_entry.place(relx=0.5,rely=0.50,anchor=tkinter.CENTER)

                        contactNumber1_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Contact Number 1")
                        contactNumber1_entry.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

                        contactNumber2_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Contact Number 2")
                        contactNumber2_entry.place(relx=0.5,rely=0.60,anchor=tkinter.CENTER)

                        bloodgroup_select = customtkinter.CTkComboBox(master=personalSOS_app,values=["Choose Blood Group","A+", "A-","B+", "B-","O+", "O-","AB+", "AB-"],
                                            width=400,height=38,corner_radius=10,border_width=1)
                        bloodgroup_select.place(relx=0.5,rely=0.65,anchor=tkinter.CENTER)

                        activeIllness_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Active Illness")
                        activeIllness_entry.place(relx=0.5,rely=0.70,anchor=tkinter.CENTER)

                        disability_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Disability")
                        disability_entry.place(relx=0.5,rely=0.75,anchor=tkinter.CENTER)

                        pastIllness_entry = customtkinter.CTkEntry(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,placeholder_text="Past Illness")
                        pastIllness_entry.place(relx=0.5,rely=0.80,anchor=tkinter.CENTER)

                        def checkpageEmail():
                            print("Checking Email")
                            email4check = mailID_entry.get()
                            if('@gmail.com' in email4check):
                                return 1
                            else:
                                return 0
                                user_title.configure(text = "EMail Format Wrong")
                        
                        def checkMobileNumber(mobileNo):
                            print("Checking Mobile Number")
                            if(len(mobileNo) == 10):
                                return 1
                            else:
                                return 0

                        def submitDetails_PersonalSOS():
                            print("Submit Details button pressed in Personal SOS")
                            z = checkpageEmail()
                            y = checkMobileNumber(personalNumber_entry.get())
                            x = checkMobileNumber(contactNumber1_entry.get())
                            w = checkMobileNumber(contactNumber2_entry.get())
                            if(z == 1 and y == 1 and x == 1 and w == 1):
                                fn = fullname_entry.get()
                                mID = mailID_entry.get()
                                mob = personalNumber_entry.get()
                                cn1 = contactNumber1_entry.get()
                                cn2 = contactNumber2_entry.get()
                                bg = bloodgroup_select.get()
                                ai = activeIllness_entry.get()                                
                                di = disability_entry.get()
                                pi = pastIllness_entry.get()

                                sql_submitDetails = "INSERT into sosDetails_Personal(fullName, mailID, personalMobile, contactNumber1, contactNumber2, bloodGroup, activeIllness, disability, pastIllness)\
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                val_submitDetails = (fn, mID, mob, cn1, cn2, bg, ai, di, pi)
                                cur.execute(sql_submitDetails, val_submitDetails)
                                myconn.commit()

                                personalSOS_app.destroy()
                            else:
                                user_title.configure(text = "Invalid EMail or Mobile Number")

                        submitDetails_button = customtkinter.CTkButton(master=personalSOS_app,width=400,height=38,
                                            corner_radius=10,border_width=1,text="Submit Details",command=submitDetails_PersonalSOS)
                        submitDetails_button.place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)

                    else:
                        print("User Details avilable")
                        sql_userAvailable = "SELECT * from sosDetails_Personal\
                        WHERE mailID = %s"
                        val_userAvailable = (personalsos_user_email)
                        cur.execute(sql_userAvailable,(val_userAvailable,))
                        result = cur.fetchone()

                        fullname = result[0]
                        mailID = result[1]
                        personalNumber = result[2]
                        contactNumber1 = result[3]
                        contactNumber2 = result[4]
                        bloodGroup = result[5]
                        activeIllness = result[6]
                        disability = result[7]
                        pastIllness = result[8]

                        fullname_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                        text="Full Name: ")
                        fullname_label.place(relx=0.48,rely=0.35,anchor=tkinter.CENTER)

                        fullname_Value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=fullname)
                        fullname_Value.place(relx=0.53,rely=0.35,anchor=tkinter.CENTER)

                        mailID_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                        text="Mail ID: ")
                        mailID_label.place(relx=0.48,rely=0.40,anchor=tkinter.CENTER)

                        mailID_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=mailID)
                        mailID_value.place(relx=0.53,rely=0.40,anchor=tkinter.CENTER)

                        mobileNumber_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                        text="Mobile Number: ")
                        mobileNumber_label.place(relx=0.48,rely=0.45,anchor=tkinter.CENTER)

                        mobileNumber_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=fullname)
                        mobileNumber_value.place(relx=0.53,rely=0.45,anchor=tkinter.CENTER)

                        contactNumber1_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                                            text="Contact Number 1:")
                        contactNumber1_label.place(relx=0.48,rely=0.5,anchor=tkinter.CENTER)

                        contactNumber1_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=contactNumber1)
                        contactNumber1_value.place(relx=0.53,rely=0.5,anchor=tkinter.CENTER)

                        contactNumber2_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                                            text="Contact Number 2:")
                        contactNumber2_label.place(relx=0.48,rely=0.55,anchor=tkinter.CENTER)

                        contactNumber2_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=contactNumber2)
                        contactNumber2_value.place(relx=0.53,rely=0.55,anchor=tkinter.CENTER)

                        bloodGroup_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                                            text="Blood Group: ")
                        bloodGroup_label.place(relx=0.48,rely=0.6,anchor=tkinter.CENTER)

                        bloodGroup_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=bloodGroup)
                        bloodGroup_value.place(relx=0.53,rely=0.6,anchor=tkinter.CENTER)

                        activeIllness_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                                            text="Active Illness: ")
                        activeIllness_label.place(relx=0.48,rely=0.65,anchor=tkinter.CENTER)

                        activeIllness_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=activeIllness)
                        activeIllness_value.place(relx=0.53,rely=0.65,anchor=tkinter.CENTER)

                        disability_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                                            text="Disability: ")
                        disability_label.place(relx=0.48,rely=0.7,anchor=tkinter.CENTER)

                        disability_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=disability)
                        disability_value.place(relx=0.53,rely=0.7,anchor=tkinter.CENTER)

                        pastIllness_label = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="white",
                                            text="Past Illness: ")
                        pastIllness_label.place(relx=0.48,rely=0.75,anchor=tkinter.CENTER)

                        pastIllness_value = customtkinter.CTkLabel(master=personalSOS_app,fg_color="black",bg_color="black",text_color="orange",
                                            text=pastIllness)
                        pastIllness_value.place(relx=0.53,rely=0.75,anchor=tkinter.CENTER)

                        def initiate_personalSOS():
                            print("Personal SOS initiated")

                            from playsound import playsound
                            from gtts import gTTS

                            tts = gTTS(text="SOS sequence initiated",lang='en')
                            tts.save("sos.mp3")
                            playsound("sos.mp3")

                            account_sid = 'AC5282113049e6afd8321daec0131ac62c'
                            auth_token = 'c8a2a5f5602951ddd3fc477be55ac9cc'
                            client = Client(account_sid, auth_token)
                            
                            t = time.localtime()
                            current_time = time.strftime("%H:%M:%S", t)

                            import json
                            from urllib.request import urlopen
                            from geopy.geocoders import Nominatim
                    
                            urlopen("http://ipinfo.io/json")
                            data = json.load(urlopen("http://ipinfo.io/json"))
                            lat = data['loc'].split('.')[0]
                            lon = data['loc'].split('.')[1]

                            geolocator = Nominatim(user_agent="geoApi")
                            Latitude = lat
                            Longitude = lon

                            sosmsg = """ This is an SOS message from SOS-er

        Sent at: {}

        Sent From:
            Latitude: {}
            Longitude: {}

        Details of {} :
            Mobile Number: {}
            Contact Number 1: {}
            Contact Number 2: {}
            Blood Group: {}
            Active Illness: {}
            Disability: {}
            Past Illness: {}
                    
                            """.format(current_time,lat,lon,fullname,personalNumber,contactNumber1,contactNumber2,bloodGroup,activeIllness,disability,pastIllness)
                            print(sosmsg)

                            message = client.messages.create(
                                body=sosmsg,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+919446574962'
                            )

                            message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body=sosmsg,
                                to='whatsapp:+917736977523'
                            )

                            message = client.messages.create(
                                body=sosmsg,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+917736789303'
                            )

                            message = client.messages.create(
                                body=sosmsg,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+919207586249'
                            )

                            t = time.localtime()
                            current_time = time.strftime("%H:%M:%S", t)

                            import json
                            from urllib.request import urlopen
                            from geopy.geocoders import Nominatim
                    
                            urlopen("http://ipinfo.io/json")
                            data = json.load(urlopen("http://ipinfo.io/json"))
                            lat = data['loc'].split('.')[0]
                            lon = data['loc'].split('.')[1]

                            geolocator = Nominatim(user_agent="geoApi")
                            Latitude = lat
                            Longitude = lon

                            sql_sosUpdate = "INSERT into personalSOS_Log(time, fullName, mailID, latitude, longitude)\
                            VALUES(%s, %s, %s, %s, %s)"
                            val_sosUpdate = (current_time,fullname,mailID,lat,lon)
                            cur.execute(sql_sosUpdate, val_sosUpdate)
                            myconn.commit()

                        initiate_personalSOS_button = customtkinter.CTkButton(master=personalSOS_app,width=400,height=200,
                                        corner_radius=10,border_width=1,hover_color="orange",text="SOS",command=initiate_personalSOS,
                                        fg_color="white",text_color="black")
                        initiate_personalSOS_button.place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)

                    personalSOS_app.mainloop()

                personalSOS_button = customtkinter.CTkButton(master=mainscreen_User,width=500,height=500,corner_radius=10,
                                        border_width=1,hover_color="orange",text="PERSONAL \n SOS",
                                        font=("Poppins-Bold",30),command=personalSOSpressed)
                personalSOS_button.place(relx=0.3,rely=0.6,anchor=tkinter.CENTER)

                def initiate_publicSOS():
                    print("Public SOS initiated")
                    publicSOS_app = customtkinter.CTk()
                    publicSOS_app.geometry("1920x1080")
                    publicSOS_app.title("SOS-er: Public SOS")
                    publicSOS_app.config(background="black")

                    soser_title = customtkinter.CTkLabel(master=publicSOS_app,text="SOS-er",font=("Hanson",30),fg_color="black",bg_color="black")
                    soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

                    user_title = customtkinter.CTkLabel(master=publicSOS_app,text="Public SOS",text_color="white",font=("Poppins",18),
                                    fg_color="black",bg_color="black")
                    user_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

                    def returnPressed():
                        print("Return Pressed from Personal SOS")
                        personalSOS_app.destroy()

                    return_button = customtkinter.CTkButton(master=publicSOS_app,fg_color="black",bg_color="black",text_color="grey",
                                    text="Return to Home",command=returnPressed)
                    return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

                    latitude_label = customtkinter.CTkLabel(master=publicSOS_app,fg_color="black",bg_color="black",text_color="white",
                        text="Latitude: ")
                    latitude_label.place(relx=0.48,rely=0.35,anchor=tkinter.CENTER)

                    latitude_value = customtkinter.CTkLabel(master=publicSOS_app,fg_color="black",bg_color="black",text_color="orange",
                            text="")
                    latitude_value.place(relx=0.53,rely=0.35,anchor=tkinter.CENTER)

                    longitude_label = customtkinter.CTkLabel(master=publicSOS_app,fg_color="black",bg_color="black",text_color="white",
                            text="Longitude: ")
                    longitude_label.place(relx=0.48,rely=0.4,anchor=tkinter.CENTER)

                    longitude_value = customtkinter.CTkLabel(master=publicSOS_app,fg_color="black",bg_color="black",text_color="orange",
                            text="")
                    longitude_value.place(relx=0.53,rely=0.4,anchor=tkinter.CENTER)

                    def getCoordinates():
                        print("Get Coordinates Pressed")

                        import json
                        from urllib.request import urlopen
                        from geopy.geocoders import Nominatim
                    
                        urlopen("http://ipinfo.io/json")
                        data = json.load(urlopen("http://ipinfo.io/json"))
                        lat = data['loc'].split('.')[0]
                        lon = data['loc'].split('.')[1]

                        geolocator = Nominatim(user_agent="geoApi")
                        Latitude = lat
                        Longitude = lon

                        latitude_value.configure(text=lat)
                        longitude_value.configure(text=lon)

                        volunteer_latitude_for_updation = str(lat)
                        volunteer_longitude_for_updation = str(lon)

                    getcoordinates_button = customtkinter.CTkButton(master=publicSOS_app,width=200,
                            height=38,corner_radius=10,border_width=1,text="Get Coordinates",command=getCoordinates)   
                    getcoordinates_button.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

                    event_description = customtkinter.CTkEntry(master=publicSOS_app,width=300,height=100,border_width=1,
                            text_color="white",bg_color="black",placeholder_text="Event Description")
                    event_description.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

                    def activatePublicSOS():
                        print("SOS Button in Public SOS Pressed")

                        from playsound import playsound
                        from gtts import gTTS

                        publicsosaudio = gTTS("Public SOS Initiated")
                        publicsosaudio.save("publicsos.mp3")
                        playsound("publicsos.mp3")

                        public_sos_description = event_description.get()

                        import datetime
                        current_time = datetime.datetime.now()
                        current_time = current_time.strftime("%H:%M:%S")

                        import json
                        from urllib.request import urlopen
                        from geopy.geocoders import Nominatim
                    
                        urlopen("http://ipinfo.io/json")
                        data = json.load(urlopen("http://ipinfo.io/json"))
                        lat = data['loc'].split('.')[0]
                        lon = data['loc'].split('.')[1]

                        geolocator = Nominatim(user_agent="geoApi")
                        Latitude = lat
                        Longitude = lon

                        desc = event_description.get()

                        from twilio.rest import Client

                        sosmsg = """ Hey Volunteer. A Pulic SOS has been registered

        From:
            Latitude: {}
            Longitude: {}
                    
                        """.format(lat,lon,desc)
                        print(sosmsg)

                        account_sid = 'AC5282113049e6afd8321daec0131ac62c'
                        auth_token = 'c8a2a5f5602951ddd3fc477be55ac9cc'
                        client = Client(account_sid, auth_token)

                        sql_sendmessage = "SELECT * from Volunteer_Coordinates\
                        WHERE latitude = %s and longitude = %s"
                        val_sendmessage = (lat,lon)
                        cur.execute(sql_sendmessage,val_sendmessage)
                        result = cur.fetchall()
                        if(result != None):
                            message = client.messages.create(
                                body=sosmsg,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+919446574962'
                            )

                            message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body=sosmsg,
                                to='whatsapp:+917736977523'
                            )

                            message = client.messages.create(
                                body=sosmsg,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+917736789303'
                            )

                            message = client.messages.create(
                                body=sosmsg,
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+919207586249'
                            )

                        sql_updatePublicSOS = "INSERT INTO publicSOS_Log\
                        VALUES (%s,%s,%s,%s)"
                        val_updatePublicSOS = (current_time,lat,lon,public_sos_description)
                        cur.execute(sql_updatePublicSOS,val_updatePublicSOS)
                        myconn.commit()

                        publicSOS_register_confirmation = customtkinter.CTk()
                        publicSOS_register_confirmation.geometry("200x100")
                        publicSOS_register_confirmation.title("SOS-er: Public SOS Confirmation")
                        publicSOS_register_confirmation.config(background="black")

                        confirmation_message = customtkinter.CTkLabel(master=publicSOS_register_confirmation,text="Public SOS Registered",
                                                text_color="white")
                        confirmation_message.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)
                        time.sleep(3)
                        publicSOS_register_confirmation.destroy()

                        publicSOS_register_confirmation.mainloop()

                    initiate_publicSOS_button = customtkinter.CTkButton(master=publicSOS_app,width=300,height=300,
                            hover_color="orange",corner_radius=10,border_width=1,command=activatePublicSOS,text="SOS")
                    initiate_publicSOS_button.place(relx=0.5,rely=0.80,anchor=tkinter.CENTER)

                    publicSOS_app.mainloop()

                publicSOS_button = customtkinter.CTkButton(master=mainscreen_User,width=500,height=500,corner_radius=10,
                                    border_width=1,hover_color="orange",text="PUBLIC \n SOS",
                                    font=("Poppins-Bold",30),command=initiate_publicSOS)
                publicSOS_button.place(relx=0.7,rely=0.6,anchor=tkinter.CENTER)

                mainscreen_User.mainloop()

    loginbutton_User = customtkinter.CTkButton(master=soserUser_app,width=300,height=38,corner_radius=10,border_width=1,
                        bg_color="black",fg_color="white",hover_color="green",command=loginUser,text_color="black",
                        text="LOGIN")
    loginbutton_User.place(relx=0.5,rely=0.63,anchor=tkinter.CENTER)

    def registerPressed():
        print("User Register Pressed")

        soserRegister_User = customtkinter.CTk()
        soserRegister_User.geometry("1920x1080")
        soserRegister_User.title("SOS-er: Register User")
        soserRegister_User.config(background="black")

        soser_title = customtkinter.CTkLabel(master=soserRegister_User,text="SOS-er",font=("Hanson",30),fg_color="black",
                        bg_color="black")
        soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        user_title = customtkinter.CTkLabel(master=soserRegister_User,text="User Registration",text_color="white",font=("Poppins",18),
                        fg_color="black",bg_color="black")
        user_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

        def returnPressed():
            print("Return Pressed from User Login")
            soserUser_app.destroy()

        return_button = customtkinter.CTkButton(master=soserRegister_User,fg_color="black",bg_color="black",text_color="grey",
                        text="Return to Login",command=returnPressed)
        return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

        fullname_User = customtkinter.CTkEntry(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Enter Fullname",placeholder_text_color="grey")
        fullname_User.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

        mailid_User = customtkinter.CTkEntry(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Enter Mail ID",placeholder_text_color="grey")
        mailid_User.place(relx=0.5,rely=0.50,anchor=tkinter.CENTER)

        def checkMail():
            print("Checking Mail ID")
            if('@gmail.com' in mailid_User.get()):
                user_title.configure(text = "Invalid Mail ID format")
                return 1
            else:
                return 0

        password_User = customtkinter.CTkEntry(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Enter Password",placeholder_text_color="grey")
        password_User.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

        passwordconf_User = customtkinter.CTkEntry(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Confirm Password",placeholder_text_color="grey")
        passwordconf_User.place(relx=0.5,rely=0.60,anchor=tkinter.CENTER)

        def checkPassword():
            print("Checking Password")
            #Password Criteria
            password4check = password_User.get()
            if(len(password4check)<8):
                user_title.configure(text = "Password too short")
                print("Password too short")
                return 0
            elif(len(password4check) > 8 and len(password4check) < 16):
                if('@' in password4check or '!' in password4check or '#' in password4check):
                    print("Special Character Found")
                    if('0' in password4check or '1' in password4check or '2' in password4check or '3' in password4check or '4' in password4check or '5' in password4check):
                        print("Number Found")
                        return 1
                    else:
                        user_title.configure(text = "No Number in Password")
                        return 0
                else:
                    user_title.configure(text = "No Special Characrter ['@' or '!' or '#']")
                    return 0
            elif(len(password_User.get())>16):
                user_title.configure(text = "Password too long")
                print("Password too long")
                return 0

        def registerUser():
            print("Register User Pressed")
            import hashlib

            if(mailid_User.get() != "" and password_User.get() != "" and passwordconf_User.get() != "" and fullname_User.get() != ""):
                if(password_User.get() == passwordconf_User.get()):
                    a = checkMail()
                    b = checkPassword()
                    if(a == 1 and b == 1):
                        username = mailid_User.get()
                        password = passwordconf_User.get()
                        passwordmd5 = hashlib.md5(password.encode()).hexdigest()
                        print(passwordmd5)
                        sql = "SELECT * from credentials_User\
                        WHERE userName = %s and passWord = %s"
                        val = (username,password)
                        cur.execute(sql, val)
                        result = cur.fetchone()
                        print(result)
                        if(result == None):
                            insertCredentials_User(mailid_User.get(), passwordmd5)
                            sql1 = "INSERT INTO details_User(fullName,mailID) VALUES(%s,%s)"
                            val1 = (fullname_User.get(),username)
                            cur.execute(sql1,val1)
                            myconn.commit()
                            user_title.configure(text="User Registered")
                            import time
                            time.sleep(2)
                            soserRegister_User.destroy()
                            soserUser_app.destroy()
                            loginstatus_User.destroy()
                        else:
                            user_title.configure(text="User Already Exists")    

        registerbutton_User = customtkinter.CTkButton(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                        bg_color="black",fg_color="white",hover_color="green",command=registerUser,text_color="black",
                        text="REGISTER")
        registerbutton_User.place(relx=0.5,rely=0.70,anchor=tkinter.CENTER)

        def loginPressed():
            print("Login Pressed")
            soserRegister_User.destroy()

        loginbutton_User = customtkinter.CTkButton(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                            bg_color="black",fg_color="black",command=loginPressed,text_color="grey",
                            text="Have an account? Login Now!")
        loginbutton_User.place(relx=0.5,rely=0.75,anchor=tkinter.CENTER)

        soserRegister_User.mainloop()

    registerbutton_User = customtkinter.CTkButton(master=soserUser_app,width=300,height=38,corner_radius=10,border_width=1,
                        bg_color="black",fg_color="black",command=registerPressed,text_color="grey",
                        text="Don't have an account? Register Now!")
    registerbutton_User.place(relx=0.5,rely=0.68,anchor=tkinter.CENTER)

    soserUser_app.mainloop()

#User Button
user_button = customtkinter.CTkButton(master=app,width=200,height=190,corner_radius=10,command=userPressed,text="User",
                hover_color="orange",text_color="white",font=("Poppins-Bold",20))
user_button.place(relx=0.5,rely=0.4,anchor=tkinter.CENTER)

def loginscreen_Volunteer():
    print("Volunteer Login Screen")
    volunteerlogin_app = customtkinter.CTk()
    volunteerlogin_app.geometry("1920x1080")
    volunteerlogin_app.title("SOS-er: Volunteer Login")
    volunteerlogin_app.config(background="black")

    soser_title = customtkinter.CTkLabel(master=volunteerlogin_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                    bg_color="black")
    soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

    volunteer_title = customtkinter.CTkLabel(master=volunteerlogin_app,text="Volunteer Login",text_color="white",font=("Poppins",18),
                    fg_color="black",bg_color="black")
    volunteer_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

    def returnPressed():
        print("Return to Home")
        volunteerlogin_app.destroy()

    return_button = customtkinter.CTkButton(master=volunteerlogin_app,fg_color="black",bg_color="black",text_color="grey",
                    text="Return to Home",command=returnPressed)
    return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

    loginstatus_Volunteer = customtkinter.CTkLabel(master=volunteerlogin_app,text="",text_color="white",fg_color="black",
                        bg_color="black")
    loginstatus_Volunteer.place(relx=0.5,rely=0.40,anchor=tkinter.CENTER)

    username_Volunteer = customtkinter.CTkEntry(master=volunteerlogin_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Username",placeholder_text_color="grey")
    username_Volunteer.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

    password_Volunteer = customtkinter.CTkEntry(master=volunteerlogin_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Password",placeholder_text_color="grey")
    password_Volunteer.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

    def loginVolunteer():
        print("Volunteer Login Pressed")
        import hashlib

        if(username_Volunteer.get() == "" and password_Volunteer.get() == ""):
            loginstatus_Volunteer.configure(text="Enter Credentials")
        elif(username_Volunteer.get() == "" and password_Volunteer.get() != ""):
            loginstatus_Volunteer.configure(text="Enter Username")
        elif(username_Volunteer.get() != "" and password_Volunteer.get() == ""):
            loginstatus_Volunteer.configure(text="Enter Password")
        elif(username_Volunteer.get() != "" and password_Volunteer.get() != ""):
            print("Login Initiated")
            username = username_Volunteer.get()
            password = password_Volunteer.get()
            passwordmd5 = hashlib.md5(password.encode()).hexdigest()
            print(passwordmd5)
            sql = "SELECT * from credentials_Volunteer\
            WHERE userName = %s and passWord = %s"
            val = (username,passwordmd5)
            cur.execute(sql, val)
            result = cur.fetchone()
            if(result == None):
                loginstatus_Volunteer.configure(text="User doesn't exist")
            else:
                loginstatus_Volunteer.configure(text="Login Successful")
                time.sleep(2)

                #Volunteer Main Screen
                volunteermain_app = customtkinter.CTk()
                volunteermain_app.geometry("1920x1080")
                volunteermain_app.title("SOS-er: Volunteer")
                volunteermain_app.config(background="black")

                soser_title = customtkinter.CTkLabel(master=volunteermain_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                        bg_color="black")
                soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

                volunteer_title = customtkinter.CTkLabel(master=volunteermain_app,text="Volunteer",text_color="white",font=("Poppins",18),
                        fg_color="black",bg_color="black")
                volunteer_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

                def returnPressed():
                    print("Return to Home")
                    volunteermain_app.destroy()
                
                return_button = customtkinter.CTkButton(master=volunteermain_app,fg_color="black",bg_color="black",text_color="grey",
                        text="Return to Home",command=returnPressed)
                return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

                latitude_label = customtkinter.CTkLabel(master=volunteermain_app,fg_color="black",bg_color="black",text_color="white",
                        text="Latitude: ")
                latitude_label.place(relx=0.48,rely=0.4,anchor=tkinter.CENTER)

                latitude_value = customtkinter.CTkLabel(master=volunteermain_app,fg_color="black",bg_color="black",text_color="orange",
                        text="")
                latitude_value.place(relx=0.53,rely=0.4,anchor=tkinter.CENTER)

                longitude_label = customtkinter.CTkLabel(master=volunteermain_app,fg_color="black",bg_color="black",text_color="white",
                        text="Longitude: ")
                longitude_label.place(relx=0.48,rely=0.45,anchor=tkinter.CENTER)

                longitude_value = customtkinter.CTkLabel(master=volunteermain_app,fg_color="black",bg_color="black",text_color="orange",
                        text="")
                longitude_value.place(relx=0.53,rely=0.45,anchor=tkinter.CENTER)

                def getCoordinates():
                    print("Get Coordinates Pressed")

                    import json
                    from urllib.request import urlopen
                    from geopy.geocoders import Nominatim
                    
                    urlopen("http://ipinfo.io/json")
                    data = json.load(urlopen("http://ipinfo.io/json"))
                    lat = data['loc'].split('.')[0]
                    lon = data['loc'].split('.')[1]

                    geolocator = Nominatim(user_agent="geoApi")
                    Latitude = lat
                    Longitude = lon

                    latitude_value.configure(text=lat)
                    longitude_value.configure(text=lon)

                    volunteer_latitude_for_updation = str(lat)
                    volunteer_longitude_for_updation = str(lon)

                getcoordinates_button = customtkinter.CTkButton(master=volunteermain_app,width=200,
                        height=38,corner_radius=10,border_width=1,text="Get Coordinates",command=getCoordinates)   
                getcoordinates_button.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

                def updateCoordinates():
                    print("Update Coordinates Button Pressed")
                    updateCoordinates_app = customtkinter.CTk()
                    updateCoordinates_app.geometry("400x200")
                    updateCoordinates_app.title("SOS-er: Update Coordinates")
                    updateCoordinates_app.config(background="black")

                    emailID_field = customtkinter.CTkEntry(master=updateCoordinates_app,width=300,
                        height=38,corner_radius=10,border_width=1,placeholder_text="Email ID")
                    emailID_field.place(relx=0.5,rely=0.4,anchor=tkinter.CENTER)
                    
                    def submitEmail():
                        print("Submit Email Button Pressed")
                        email_for_updation = emailID_field.get()
                        print(email_for_updation)
                        
                        if(emailID_field.get() == username_Volunteer.get()):
                            import json
                            from urllib.request import urlopen
                            from geopy.geocoders import Nominatim
                    
                            urlopen("http://ipinfo.io/json")
                            data = json.load(urlopen("http://ipinfo.io/json"))
                            lat = data['loc'].split('.')[0]
                            lon = data['loc'].split('.')[1]

                            geolocator = Nominatim(user_agent="geoApi")
                            Latitude = lat
                            Longitude = lon

                            sql_check = "SELECT * FROM Volunteer_Coordinates\
                            WHERE mailID = %s"
                            val_check = email_for_updation
                            cur.execute(sql_check,(val_check,))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                            result = cur.fetchone()
                            if(result == None):
                                sql1 = "INSERT INTO Volunteer_Coordinates(mailID,latitude,longitude)\
                                VALUES(%s,%s,%s)"
                                val1 = (email_for_updation,lat,lon)
                                cur.execute(sql1,val1)
                                myconn.commit()
                            else:
                                sql2 = "UPDATE Volunteer_Coordinates SET latitude = %s, longitude = %s WHERE mailID = %s"
                                val2 = (lat,lon,email_for_updation)
                                cur.execute(sql2,(val2))
                                myconn.commit()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                            
                            updateCoordinates_app.destroy()

                    submitEmail_button = customtkinter.CTkButton(master=updateCoordinates_app,width=50,
                        height=38,corner_radius=10,border_width=1,text="Submit",command=submitEmail)
                    submitEmail_button.place(relx=0.5,rely=0.65,anchor=tkinter.CENTER)

                    updateCoordinates_app.mainloop()

                updatecoordinates_button = customtkinter.CTkButton(master=volunteermain_app,width=200,
                        height=38,corner_radius=10,border_width=1,text="Update Coordinates",
                        command=updateCoordinates,fg_color="black")   
                updatecoordinates_button.place(relx=0.5,rely=0.60,anchor=tkinter.CENTER)

                def nearbyEvents():
                    print("Nearby Events Button Pressed")
                    nearbyEvents_app = customtkinter.CTk()
                    nearbyEvents_app.geometry("500x500")
                    nearbyEvents_app.title("SOS-er: Nearby Events")
                    nearbyEvents_app.config(background="black")

                    sql_nearby = "SELECT * FROM publicSOS_Log"
                    cur.execute(sql_nearby)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                    results = cur.fetchmany()

                    event1_label = customtkinter.CTkLabel(master=nearbyEvents_app,text=results,text_color="white",
                    width=500,height=500)
                    event1_label.place(relx=0.5,rely=0.1,anchor=tkinter.CENTER)

                    nearbyEvents_app.mainloop()

                nearbyevents_button = customtkinter.CTkButton(master=volunteermain_app,width=200,height=38,
                        corner_radius=10,border_width=1,text="Nearby Events",fg_color="black",command=nearbyEvents)
                nearbyevents_button.place(relx=0.5,rely=0.70,anchor=tkinter.CENTER)

                volunteermain_app.mainloop()

    loginbutton_Volunteer = customtkinter.CTkButton(master=volunteerlogin_app,width=300,height=38,corner_radius=10,border_width=1,
                        bg_color="black",fg_color="white",hover_color="green",command=loginVolunteer,text_color="black",
                        text="LOGIN")
    loginbutton_Volunteer.place(relx=0.5,rely=0.63,anchor=tkinter.CENTER)

    def registerPressed():
        print("User Register Pressed")

        soserRegister_Volunteer_app = customtkinter.CTk()
        soserRegister_Volunteer_app.geometry("1920x1080")
        soserRegister_Volunteer_app.title("SOS-er: Register User")
        soserRegister_Volunteer_app.config(background="black")

        soser_title = customtkinter.CTkLabel(master=soserRegister_Volunteer_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                        bg_color="black")
        soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        volunteer_title = customtkinter.CTkLabel(master=soserRegister_Volunteer_app,text="Volunteer Registration",text_color="white",font=("Poppins",18),
                        fg_color="black",bg_color="black")
        volunteer_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

        def returnPressed():
            print("Return Pressed from User Login")
            soserRegister_Volunteer_app.destroy()

        return_button = customtkinter.CTkButton(master=soserRegister_Volunteer_app,fg_color="black",bg_color="black",text_color="grey",
                        text="Return to Login",command=returnPressed)
        return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

        fullname_Volunteer = customtkinter.CTkEntry(master=soserRegister_Volunteer_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Enter Fullname",placeholder_text_color="grey")
        fullname_Volunteer.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

        mailid_Volunteer = customtkinter.CTkEntry(master=soserRegister_Volunteer_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Enter Mail ID",placeholder_text_color="grey")
        mailid_Volunteer.place(relx=0.5,rely=0.50,anchor=tkinter.CENTER)

        password_User = customtkinter.CTkEntry(master=soserRegister_Volunteer_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Enter Password",placeholder_text_color="grey")
        password_User.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

        passwordconf_User = customtkinter.CTkEntry(master=soserRegister_Volunteer_app,width=300,height=38,corner_radius=10,border_width=1,
                    placeholder_text="Confirm Password",placeholder_text_color="grey")
        passwordconf_User.place(relx=0.5,rely=0.60,anchor=tkinter.CENTER)

        def registerUser():
            print("Register User Pressed")
            import hashlib

            if(mailid_Volunteer.get() != "" and password_User.get() != "" and passwordconf_User.get() != "" and fullname_Volunteer.get() != ""):
                if(password_User.get() == passwordconf_User.get()):
                    username = mailid_Volunteer.get()
                    password = passwordconf_User.get()
                    passwordmd5 = hashlib.md5(password.encode()).hexdigest()
                    print(passwordmd5)
                    sql = "SELECT * from credentials_Volunteer\
                    WHERE userName = %s and passWord = %s"
                    val = (username,password)
                    cur.execute(sql, val)
                    result = cur.fetchone()
                    print(result)
                    if(result == None):
                        insertCredentials(username, passwordmd5)
                        sql1 = "INSERT INTO details_User(fullName,mailID) VALUES(%s,%s)"
                        val1 = (fullname_Volunteer.get(),username)
                        cur.execute(sql1,val1)
                        myconn.commit()

                        soserRegister_Volunteer_app.destroy()

        registerbutton_User = customtkinter.CTkButton(master=soserRegister_Volunteer_app,width=300,height=38,corner_radius=10,border_width=1,
                        bg_color="black",fg_color="white",hover_color="green",command=registerUser,text_color="black",
                        text="REGISTER")
        registerbutton_User.place(relx=0.5,rely=0.70,anchor=tkinter.CENTER)

        def loginPressed():
            print("Login Pressed")
            soserRegister_User.destroy()

        loginbutton_User = customtkinter.CTkButton(master=soserRegister_User,width=300,height=38,corner_radius=10,border_width=1,
                            bg_color="black",fg_color="black",command=loginPressed,text_color="grey",
                            text="Have an account? Login Now!")
        loginbutton_User.place(relx=0.5,rely=0.75,anchor=tkinter.CENTER)

        soserRegister_User.mainloop()

    registerbutton_User = customtkinter.CTkButton(master=volunteerlogin_app,width=300,height=38,corner_radius=10,border_width=1,
                        bg_color="black",fg_color="black",command=registerPressed,text_color="grey",
                        text="Don't have an account? Register Now!")
    registerbutton_User.place(relx=0.5,rely=0.68,anchor=tkinter.CENTER)

    volunteerlogin_app.mainloop()

#Volunteer Button
volunteer_button = customtkinter.CTkButton(master=app,width=200,height=190,corner_radius=10,command=loginscreen_Volunteer,
                text="Volunteer",hover_color="orange",text_color="white",font=("Poppins-Bold",20))
volunteer_button.place(relx=0.5,rely=0.7,anchor=tkinter.CENTER)

def showTips():
    print("Show tips pressed")
    tips_app = customtkinter.CTk()
    tips_app.geometry("1920x1080")
    tips_app.title("SOS-er: Tips")
    tips_app.config(background="black")

    soser_title = customtkinter.CTkLabel(master=tips_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                    bg_color="black")
    soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

    volunteer_title = customtkinter.CTkLabel(master=tips_app,text="Volunteer Login",text_color="white",font=("Poppins",18),
                    fg_color="black",bg_color="black")
    volunteer_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

    def returnPressed():
        print("Return to Home")
        tips_app.destroy()

    return_button = customtkinter.CTkButton(master=tips_app,fg_color="black",bg_color="black",text_color="grey",
                    text="Return to Home",command=returnPressed)
    return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

    def floods_button_pressed():
        print("Floods Button Pressed")
        floods_app = customtkinter.CTk()
        floods_app.geometry("1920x1080")
        floods_app.title("SOS-er: Flood")
        floods_app.config(background="black")

        soser_title = customtkinter.CTkLabel(master=floods_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                    bg_color="black")
        soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        def returnPressed():
            print("Return to Home")
            floods_app.destroy()

        return_button = customtkinter.CTkButton(master=floods_app,fg_color="black",bg_color="black",text_color="grey",
                    text="Return to Home",command=returnPressed)
        return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

        floodtext = """
1. Stay informed: Keep updated on weather forecasts, flood warnings, and evacuation orders through local news, weather apps, or emergency services.

2. Evacuation: If authorities issue an evacuation order, follow it immediately. Don't wait until the last moment. Have a predetermined plan and know the safest routes to higher ground or designated shelters.

3. Create an emergency kit: Prepare an emergency kit in advance, including essentials such as non-perishable food, drinking water, medication, flashlights, batteries, a first aid kit, important documents, cash, and clothing.

4. Secure your home: If you have enough time before the flood, take steps to protect your property. Move valuables and essential items to higher floors or elevate them. Clear gutters and drains to allow water to flow freely. Turn off electricity, gas, and water supplies.

5. Avoid floodwater: Never attempt to walk, swim, or drive through floodwaters. The depth and current of the water can be deceptive and dangerous. It may contain hazards such as debris, pollutants, or live electrical wires.

6. Seek higher ground: If you're caught in a flood and cannot evacuate, move to higher ground, such as the upper floors of your home or a sturdy building. Avoid basements or ground-level areas.

7. Use caution with electricity: Turn off the electrical power to your home if you can safely reach the main switch. Avoid contact with electrical equipment or outlets if you're standing in water or on wet surfaces.

8. Communicate: Keep your cell phone charged and have a backup power source available. Maintain contact with family, friends, and emergency services. Let others know your whereabouts and any developments.

9. Heed warnings: Follow instructions from local authorities and emergency services. If they advise you to evacuate, do so promptly and calmly.

10. After the flood: Be cautious when returning home after the floodwaters recede. Watch out for structural damage, contamination, or other hazards. Clean and disinfect your property thoroughly. Consult professionals for assistance with electrical, gas, or water systems that may have been compromised.

Remember, personal safety is the utmost priority during a flood. Always follow the guidance of emergency services and be prepared to adapt to changing conditions.
        """

        floods_label = customtkinter.CTkLabel(master=floods_app,width=1500,height=300,text_color="white",
        text=floodtext,fg_color="black",bg_color="black",wraplength=1300)
        floods_label.place(relx=0.5,rely=0.6,anchor=tkinter.CENTER)

        floods_app.mainloop()

    floods_button = customtkinter.CTkButton(master=tips_app,width=300,height=300,corner_radius=10,
                hover_color="orange",command=floods_button_pressed,text="FLOOD",font=("Poppins-Bold",30),
                bg_color="black")
    floods_button.place(relx=0.25,rely=0.5,anchor=tkinter.CENTER)

    def cyclone_button_pressed():
        print("Cyclone Button Pressed")
        cyclones_app = customtkinter.CTk()
        cyclones_app.geometry("1920x1080")
        cyclones_app.title("SOS-er: Cyclone")
        cyclones_app.config(background="black")

        soser_title = customtkinter.CTkLabel(master=cyclones_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                    bg_color="black")
        soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        volunteer_title = customtkinter.CTkLabel(master=cyclones_app,text="Cyclone Tips",text_color="white",font=("Poppins",18),
                    fg_color="black",bg_color="black")
        volunteer_title.place(relx=0.5,rely=0.19,anchor=tkinter.CENTER)

        def returnPressed():
            print("Return to Home")
            cyclones_app.destroy()

        return_button = customtkinter.CTkButton(master=cyclones_app,fg_color="black",bg_color="black",text_color="grey",
                    text="Return to Home",command=returnPressed)
        return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

        cyclonetext = """
1. Stay Informed: Stay updated on weather forecasts and warnings through local news, radio, or official meteorological sources. Follow the instructions and advice provided by local authorities and emergency services.

2. Evacuation Planning: If you live in a cyclone-prone area, have a predetermined plan in place for evacuation. Know the evacuation routes, designated shelters, and follow any evacuation orders issued by authorities.

3. Secure Your Property: Reinforce your home in advance by securing windows, doors, and other vulnerable areas. Trim trees and remove any loose objects in your yard that could become projectiles in strong winds.

4. Stock Up on Supplies: Have an emergency kit ready with essential supplies including food, water, medications, flashlights, batteries, a first aid kit, important documents, cash, and clothing. Ensure you have enough supplies to last for several days.

5. Stay Indoors: During the cyclone, stay inside a sturdy building, preferably in a small, windowless, and centrally located room on the ground floor. Avoid areas near windows, glass, or exterior walls.

6. Maintain Communication: Keep your cell phone charged and have a backup power source available. Maintain contact with family, friends, and emergency services. Use text messages instead of calls, as they have a higher chance of going through during high network congestion.

7. Listen to Authorities: Follow the instructions given by local authorities and emergency services. Be prepared to adapt to changing conditions and heed evacuation orders if necessary.

8. Stay Away from Coastal Areas: If you are in a coastal area, move to higher ground and stay away from beaches, low-lying areas, and water bodies as cyclones can cause storm surges and flooding.

9. Avoid Going Outside: Do not venture outside during the cyclone, even during a lull in the storm. The eye of the cyclone may provide a temporary calm, but strong winds will resume shortly.

10. Be Prepared for Power Outages: Cyclones can cause widespread power outages. Have alternative lighting sources such as flashlights and candles, and avoid using candles if there's a risk of gas leaks.

11. Post-Cyclone Safety: After the cyclone passes, be cautious when venturing outside. Watch out for downed power lines, debris, and damaged structures. Avoid standing water, as it may be contaminated or hiding hazards.
        """

        floods_label = customtkinter.CTkLabel(master=cyclones_app,width=1500,height=300,text_color="white",
        text=cyclonetext,fg_color="black",bg_color="black",wraplength=1300)
        floods_label.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        cyclones_app.mainloop()

    cyclone_button = customtkinter.CTkButton(master=tips_app,width=300,height=300,corner_radius=10,
                hover_color="orange",command=cyclone_button_pressed,text="CYCLONE",font=("Poppins-Bold",30),
                bg_color="black")
    cyclone_button.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

    def earthquake_button_pressed():
        print("Cyclone Button Pressed")
        earthquakes_app = customtkinter.CTk()
        earthquakes_app.geometry("1920x1080")
        earthquakes_app.title("SOS-er: Cyclone")
        earthquakes_app.config(background="black")

        soser_title = customtkinter.CTkLabel(master=earthquakes_app,text="SOS-er",font=("Hanson",30),fg_color="black",
                    bg_color="black")
        soser_title.place(relx=0.5,rely=0.15,anchor=tkinter.CENTER)

        def returnPressed():
            print("Return to Home")
            earthquakes_app.destroy()

        return_button = customtkinter.CTkButton(master=earthquakes_app,fg_color="black",bg_color="black",text_color="grey",
                    text="Return to Home",command=returnPressed)
        return_button.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

        earthquaketext = """
1. Drop, Cover, and Hold On: When the shaking begins, drop to the ground, take cover under a sturdy piece of furniture, and hold on until the shaking stops. Stay away from windows, glass, heavy furniture, and other objects that may pose a risk of falling or shattering.

2. Stay Indoors: Unless you are in immediate danger, it is generally safer to stay indoors during an earthquake. Trying to exit a building while the ground is shaking can be extremely hazardous due to falling debris or collapsing structures.

3. Seek Shelter: If you're unable to get under a sturdy piece of furniture, seek shelter against an interior wall away from windows, glass, and heavy objects. Protect your head and neck with your arms and take cover.

4. Stay away from Hazards: Move away from potential hazards such as bookcases, cabinets, appliances, chimneys, and anything that may topple or fall during the shaking.

5. Avoid Elevators: Do not use elevators during an earthquake, as they may get stuck or malfunction. Use stairs instead, but proceed with caution.

6. Stay Clear of Exterior Walls and Windows: Avoid standing or taking cover near exterior walls or windows as they may shatter during the shaking. Broken glass can cause severe injuries.

7. Stay Calm: Try to stay calm and reassure others around you, especially children. Panicking can hinder your ability to react safely and make sound decisions.

8. If Outdoors, Move to an Open Area: If you are outside when an earthquake occurs, move away from buildings, streetlights, and utility wires. Find an open area away from potential falling objects and take cover by crouching down.

9. If Driving, Pull Over Safely: If you are driving, safely pull over to the side of the road, away from overpasses, bridges, and power lines. Stay inside the vehicle until the shaking stops. Avoid stopping near buildings, trees, or other structures that could collapse.

10. Be Prepared for Aftershocks: Aftershocks are common after an earthquake. Be prepared for additional shaking and take the same safety measures as during the initial earthquake.
        """

        floods_label = customtkinter.CTkLabel(master=earthquakes_app,width=1500,height=300,text_color="white",
        text=earthquaketext,fg_color="black",bg_color="black",wraplength=1300)
        floods_label.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

        earthquakes_app.mainloop()

    earthquake_button = customtkinter.CTkButton(master=tips_app,width=300,height=300,corner_radius=10,
                hover_color="orange",command=earthquake_button_pressed,text="EARTHQUAKE",font=("Poppins-Bold",30),
                bg_color="black")
    earthquake_button.place(relx=0.75,rely=0.5,anchor=tkinter.CENTER)
    #firstaid_button = customtkinter.CTkButton(master=tips_app,width=1025,height=50,corner_radius=10,
    #            hover_color="orange",command=print("First Aid Pressed"),text="FIRST AID",font=("Poppins-Bold",25),
    #            bg_color="black")
    #firstaid_button.place(relx=0.5,rely=0.75,anchor=tkinter.CENTER)

    tips_app.mainloop()

tips_button = customtkinter.CTkButton(master=app,width=200,height=50,corner_radius=10,border_width=1,
            bg_color="black",fg_color="black",hover_color="orange",text_color="white",command=showTips,
            text="QUICK TIPS")
tips_button.place(relx=0.5,rely=0.90,anchor=tkinter.CENTER)

app.mainloop()