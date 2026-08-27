from data import *

#final output for tkinter gui 
if ms_account_created == True:
    print("\n\nMicrosoft Account: Created Successfully\n")
else:
    print("Mircrosoft Account: Unsuccessful Creation\n")

if ms_usage_location_assigned == True:
    print("Microsoft Account: Usage Location Assigned Successfully\n")
else:
    print("Microsoft Account: Unable to Assign Usage Location\n")

if ms_license_assigned == True:
    print("Microsoft Account: Premium Business License Assigned Successfully\n")
else:
    print("Microsoft Account: Unable to Assign Premium Business License\n")

if ms_default_group_assigned == True:
    print("Microsoft Account: app-google-sso Assigned Successfully\n")
else:
    print("Microsoft Account: Unable to Assign to app-google-sso\n")

if ms_os_group_assigned == True:
    print("Microsoft Account: users-windows/users-macOS Assigned Successfully\n")
else:
    print("Microsoft Account: Unable to Assign to users-windows/users-macOS\n")

if sent_email == True:
    print("Email Send Successfully\n")
else:
    print("Unsuccessful Email Delivery\n") 

if google_account_created == True:
    print("Google Account: Created Successfully\n")
else:
    print("Google Account: Unsuccessful Creation\n")

if default_google_group_assigned == True:
    print("Google Account: Onboarding group Assigned Successfully\n")
else:
    print("Google Account: Unable to Assign to Onboarding group\n")

if slack_msg_sent == True:
    print("Slack Message Sent Successfully\n")
else:
    print("Unable to Send Slack Message\n")


