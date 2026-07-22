import tkinter as tk

root = tk.Tk()
root.title("Simple App")


email_entry = tk.Entry(root)
email_entry.pack(padx=10, pady=30)


os_entry = tk.Entry(root)
os_entry.pack(padx=10, pady=30)


tracking_num_entry = tk.Entry(root)
tracking_num_entry.pack(padx=10, pady=30)


button = tk.Button(root, text="Submit Form!", font=('Arial', 18))
button.pack(padx=10, pady=30)





root.mainloop()

