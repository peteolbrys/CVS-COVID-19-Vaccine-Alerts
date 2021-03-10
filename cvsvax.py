#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:21:04 2021

@author: cabrown802
Updated by: peteolbrys
"""

import os
import smtplib
import ssl
import threading
import urllib.request

email_password = os.getenv("VAX_EMAIL_PASSWORD")
email_receiver = os.getenv("VAX_EMAIL_RECEIVER")
email_sender = os.getenv("VAX_EMAIL_SENDER")
vax_state = os.getenv("VAX_STATE")

# How often to refresh the page, in seconds
page_refresh_period = 60.0 

# Port for SSL
ssl_port = 465  

# Message in the email.
email_message = "Book an appointment at CVS! https://www.cvs.com/immunizations/covid-19-vaccine"

# Create a secure SSL context
context = ssl.create_default_context()

# This function repeatedly reads the CVS website, and if any appointments are
# available in your state, it emails you.
def sendit():
    
    # Initializes threading (repition / refreshing of website)
    threading.Timer(page_refresh_period, sendit).start()
    print("Checking vax status.")
    
    # Reads website into var 'html'
    html = urllib.request.urlopen('https://www.cvs.com/immunizations/covid-19-vaccine').read()
    
    # If not all appointments are booked...
    lookforstring = f"At this time, all appointments in {vax_state} are booked."
    if lookforstring.encode() not in html:    
        # Login via STMP and send email
        with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, email_message)
    else:
        print(lookforstring)
    
sendit()


    

        




