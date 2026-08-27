import tkinter as tk
from tkinter import ttk
import sys
import subprocess

def submit_form():
    name_text = name_entry.get()
    email_text = email_entry.get()
    tracking_text = tracking_num_entry.get()
    delivery_text =  delivery_entry.get()
    os_text = os_combobox.get()
    location_text = location_entry.get()

    f = open("data.py", "w")
    f.write("name = "+'"'+name_text+'"\n')
    f.write("email = "+'"'+email_text+'"\n')
    f.write("tracking = "+'"'+tracking_text+'"\n')
    f.write("delivery = "+'"'+delivery_text+'"\n')
    f.write("os = "+'"'+os_text+'"\n')
    f.write("location = "+'"'+location_text+'"\n') 
    f.close()


    out = subprocess.run([sys.executable, "bamboo.py"], capture_output = True, text = True)    
    output_entry.insert(tk.END, out.stdout)

    out = subprocess.run([sys.executable, "ms_entra.py"], capture_output = True, text = True)    
    output_entry.insert(tk.END, out.stdout)

    out = subprocess.run([sys.executable, "send_email.py"], capture_output = True, text = True)    
    output_entry.insert(tk.END, out.stdout)

    out = subprocess.run([sys.executable, "google_workspace.py"], capture_output = True, text = True)    
    output_entry.insert(tk.END, out.stdout)

    out = subprocess.run([sys.executable, "slack.py"], capture_output = True, text = True)    
    output_entry.insert(tk.END, out.stdout)

    out = subprocess.run([sys.executable, "final_output.py"], capture_output = True, text = True)    
    output_entry.insert(tk.END, out.stdout)
    

def submit_auth():
    bambooHR_key = bambooHR_entry.get()
    msapp_text = msapp_entry.get()
    msten_text = msten_entry.get()
    mssecret_text = mssecret_entry.get()
    google_json = google_entry.get()
    slack_text = slack_entry.get()
    
    f = open("service-account.json", 'w')
    f.write(google_json)
    f.close()

    f = open(".env", 'w')
    f.write("bambooKey="+bambooHR_key+"\nappID="+msapp_text+"\nsecret="+mssecret_text+"\ntenID="+msten_text+"\nslack_token="+slack_text)
    f.close()

def clear_window():
    output_entry.delete("1.0", tk.END)

root = tk.Tk()
root.title("New Hire Automation App")

notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text = "Form")
notebook.add(tab2, text = "Authentication")
notebook.pack(expand=1, fill = "both")

#tab1 - Form
name_label = tk.Label(tab1, text="First and Last Name (As in BammbooHR)")
name_label.pack(padx=20, pady=6)

name_entry = tk.Entry(tab1)
name_entry.pack(padx=20, pady=6)

email_label = tk.Label(tab1, text="Email to Send Account Info")
email_label.pack(padx=20, pady=6)

email_entry = tk.Entry(tab1)
email_entry.pack(padx=20, pady=6)

location_label = tk.Label(tab1, text="Usage Location Country Two Letter Abbreviation Ex. US AU GB")
location_label.pack(padx=20, pady=6)

location_entry = tk.Entry(tab1)
location_entry.pack(padx=20, pady=6)

os_label = tk.Label(tab1, text="Device OS")
os_label.pack(padx=20, pady=6)

os_combobox = ttk.Combobox(tab1, values = ["Windows", "Mac"], state="readonly")
os_combobox.pack(padx=20, pady=6)

tracking_label = tk.Label(tab1, text="Tracking URL (if applicable)")
tracking_label.pack(padx=20, pady=6)

tracking_num_entry = tk.Entry(tab1)
tracking_num_entry.pack(padx=20, pady=6)

delivery_label = tk.Label(tab1, text="Delivery Date (if applicable)")
delivery_label.pack(padx=20, pady=6)

delivery_entry = tk.Entry(tab1)
delivery_entry.pack(padx=20, pady=6)

submit_button = tk.Button(tab1, text="Submit Form!", font=('Arial', 18), command=submit_form)
submit_button.pack(padx=20, pady=20)

output_entry = tk.Text(tab1, height=24, width=120)
output_entry.pack(padx=20, pady=20)

clear_button = tk.Button(tab1, text="Clear Window", font=('Arial', 18), command=clear_window)
clear_button.pack(padx=20, pady=20)

#tab2 - Authentication
bambooHR_label = tk.Label(tab2, text="BambooHR Api Key")
bambooHR_label.pack(padx=20, pady=6)

bambooHR_entry = tk.Entry(tab2, show="*")
bambooHR_entry.pack(padx=20, pady=6)

msapp_label = tk.Label(tab2, text="Microsoft AppID")
msapp_label.pack(padx=20, pady=6)

msapp_entry = tk.Entry(tab2, show="*")
msapp_entry.pack(padx=20, pady=6)

mssecret_label = tk.Label(tab2, text="Mircosoft Secret")
mssecret_label.pack(padx=20, pady=6)

mssecret_entry = tk.Entry(tab2, show="*")
mssecret_entry.pack(padx=20, pady=6)

msten_label = tk.Label(tab2, text="Mircosoft TenID")
msten_label.pack(padx=20, pady=6)

msten_entry = tk.Entry(tab2, show="*")
msten_entry.pack(padx=20, pady=6)

google_label = tk.Label(tab2, text="Google Cloud Service Account Json")
google_label.pack(padx=20, pady=6)

google_entry = tk.Entry(tab2, show="*")
google_entry.pack(padx=20, pady=6)

slack_label = tk.Label(tab2, text="Slack New Hire Automation App Access Token")
slack_label.pack(padx=20, pady=6)

slack_entry = tk.Entry(tab2, show="*")
slack_entry.pack(padx=20, pady=6)

auth_button = tk.Button(tab2, text="Input Api Keys", font=('Arial', 18), command=submit_auth)
auth_button.pack(padx=20, pady=20)


root.mainloop()

