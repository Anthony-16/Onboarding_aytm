
#final output for tkinter gui
def run_final_output(variables):
    output = ""

    if variables['ms_account_created'] == True:
        output = "\n\nMicrosoft Account: Created Successfully\n"
    else:
        output = "\n\nMircrosoft Account: Unsuccessful Creation\n"

    if variables['ms_usage_location_assigned'] == True:
        output = output + "\nMicrosoft Account: Usage Location Assigned Successfully\n"
    else:
        output = output + "\nMicrosoft Account: Unable to Assign Usage Location\n"

    if variables['ms_license_assigned'] == True:
        output = output + "\nMicrosoft Account: Premium Business License Assigned Successfully\n"
    else:
        output = output + "\nMicrosoft Account: Unable to Assign Premium Business License\n"

    if variables['ms_default_group_assigned'] == True:
        output = output + "\nMicrosoft Account: app-google-sso Assigned Successfully\n"
    else:
        output = output + "\nMicrosoft Account: Unable to Assign to app-google-sso\n"

    if variables['ms_os_group_assigned'] == True:
        output = output + "\nMicrosoft Account: users-windows/users-macOS Assigned Successfully\n"
    else:
        output = output + "\nMicrosoft Account: Unable to Assign to users-windows/users-macOS\n"

    if variables['sent_email'] == True:
        output = output + "\nEmail Send Successfully\n"
    else:
        output = output + "\nUnsuccessful Email Delivery\n" 

    if variables['google_account_created'] == True:
        output = output + "\nGoogle Account: Created Successfully\n"
    else:
        output = output + "\nGoogle Account: Unsuccessful Creation\n"

    if variables['default_google_group_assigned'] == True:
        output = output + "\nGoogle Account: Onboarding group Assigned Successfully\n"
    else:
        output = output + "\nGoogle Account: Unable to Assign to Onboarding group\n"

    if variables['slack_msg_sent'] == True:
        output = output + "\nSlack Message Sent Successfully\n"
    else:
        output = output + "\nUnable to Send Slack Message\n"

    return output


