import tkinter as tk
from tkinter import messagebox
import os
import socket
from datetime import datetime
# import pymysql
# import pyodbc
import pypyodbc


# def connection():
#     conn_str = (
#         "Driver={ODBC Driver 17 for SQL Server};"
#         "Server=192.168.0.31;"
#         "Database=HRMIS;"
#         "UID=sa;"
#         "PWD=sa@123;"
#     )
#     db = pyodbc.connect(conn_str)
#     cur = db.cursor()
#     return cur, db




# def connection():
#     db = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='root',
#         database='NDA',
#     )
#     cur = db.cursor()
#     return cur, db

# def on_accept():
#     username = os.getlogin()
#     print(username)
#     domain_name = socket.getfqdn()
#     print(domain_name)
    
#     try:
#         cur, db = connection()
#         query = """
#             INSERT INTO nda_acceptance (username, domain_name, accepted_at)
#             VALUES  (%s,%s, %s)
#         """
#         cur.execute(query, (username,domain_name, datetime.now()))
#         db.commit()
#         db.close()
#         messagebox.showinfo("Accepted", f"Thank you {username}.\nYour NDA has been recorded.")
#         root.destroy()

#     except Exception as e:
#         messagebox.showerror("Database Error", f"Could not save NDA.\n\nError: {e}")



# # def on_accept():
# #     messagebox.showinfo("Accepted", "Thank you for accepting. Proceeding to next step...")
# #     root.destroy()


# def has_accepted(username):
#     try:
#         cur, db = connection()
#         query = "SELECT COUNT(*) FROM nda_acceptance WHERE username = %s"
#         cur.execute(query, (username,))
#         result = cur.fetchone()
#         db.close()
#         return result[0] > 0
#     except Exception as e:
#         messagebox.showerror("Error", f"Could not check NDA status.\n\nError: {e}")
#         return False



# def disable_event():
#     pass  # Disable close button


# username = os.getlogin()

# if has_accepted(username):
#     tk.Tk().withdraw()  # hide empty Tk window
#     # messagebox.showinfo("Already Accepted", f"Hello {username}, you have already accepted the NDA.")
# else:

# print(pyodbc.drivers())

# def connection():
#     conn_str = (
#         "Driver={ODBC Driver 18 for SQL Server};"
#         "Server=192.168.0.31;"
#         "Database=HRMIS;"
#         "UID=sa;"
#         "PWD=sa@123;"
#          "TrustServerCertificate=yes;" 
#     )
#     db = pyodbc.connect(conn_str)
#     cur = db.cursor()
#     return cur, db



def connection():
    try:
        conn = pypyodbc.connect("Driver={SQL Server}; Server=192.168.0.31; Database=HRMIS; "
                                "uid=sa;pwd=sa@123;")
        
        cur = conn.cursor()
    except pypyodbc.Error as e:
        print(e)

    return cur , conn


conn = connection()





# def connection():
#     try:
#         conn = pypyodbc.connect(
#         "Driver={ODBC Driver 18 for SQL Server};"
#         "Server=192.168.0.31;"
#         "Database=HRMIS;"
#         "UID=sa;"
#         "PWD=sa@123;"
#          "TrustServerCertificate=yes;" 
#                                 )
#     except pypyodbc.Error as e:
#         print(e)

#     return conn


# conn = connection()

def on_accept():
    username = os.getlogin()
    hostname = socket.gethostname()
    operation = "INSERT"

    try:
        cur, db = connection()

        # Execute stored procedure
        cur.execute("""
            EXEC SP_InsertNDA_Acceptance @EmployeeID=?, @Hostname=?, @Operation=?
        """, (username, hostname, operation))

        db.commit()
        db.close()

        messagebox.showinfo("Accepted", f"Thank you {username}.\nYour NDA has been recorded.")
        root.destroy()

    except Exception as e:
        messagebox.showerror("Database Error", f"Could not save NDA.\n\nError: {e}")


def has_accepted(username):
    try:
        cur, db = connection()
        query = "SELECT COUNT(*) FROM nda_accepct_log WHERE EmpCode = ?"
        cur.execute(query, (username,))
        result = cur.fetchone()
        db.close()
        return result[0] > 0
    except Exception as e:
        # messagebox.showerror("Error", f"Could not check NDA status.\n\nError: {e}")
        return False


def disable_event():
    pass

username = os.getlogin()

if has_accepted(username):
    tk.Tk().withdraw()
    # messagebox.showinfo("Already Accepted", f"Hello {username}, you have already accepted the NDA.")
else:

    root = tk.Tk()
    root.title("NDA Agreement")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.protocol("WM_DELETE_WINDOW", disable_event)
    root.bind("<Alt-F4>", lambda e: "break")
    root.bind("<Escape>", lambda e: "break")
    root.configure(bg="#f0f2f5")

    # Title
    title_label = tk.Label(
        root, text="Non-Disclosure Agreement",
        font=("Helvetica", 28, "bold"),
        bg="#f0f2f5", fg="#333"
    )
    title_label.pack(pady=(30, 10))


    username_label = tk.Label(
    root,
    text=f"Logged in as: {username}",
    font=("Helvetica", 16),
    bg="#f0f2f5",
    fg="#555"
    )
    username_label.pack(pady=(0, 20))


    # Content container
    container = tk.Frame(root, bg="white", bd=2, relief="groove")
    container.pack(expand=True, fill="both", padx=80, pady=10)

    scrollbar = tk.Scrollbar(container)
    scrollbar.pack(side="right", fill="y")

    text = tk.Text(
        container, wrap="word", yscrollcommand=scrollbar.set,
        font=("Georgia", 14), padx=20, pady=20,
        relief="flat", bg="white", fg="#333"
    )
    text.pack(expand=True, fill="both")
    scrollbar.config(command=text.yview)


    # Full NDA Text Content (shortened for brevity here, but you will paste the full version)
    nda_text = """

    Declaration and undertaking for Prevention of Sexual Harassment at workplace

    I hereby acknowledge that I will not indulge into any kind of sexual harassment towards any women colleagues or staff, including employer,
    permanent & temporary employees, trainees and employees on contract at the workplace or at client sites.
    The Organization has a zero-tolerance policy towards sexual harrasment and will take strict and immediate action including termination of 
    employment.

    I understand that Sexual harassment includes, but is not limited to, the following unwelcome acts or behaviour – 

        . Physical contact and advances
        . A demand or request for sexual favours 
        . Making sexually coloured remarks
        . Showing pornography
        . Any other unwelcome physical, verbal, non-verbal conduct of sexual nature

    I understand that Sexual harassment may occur in various forms including – 

        . Verbal Harassment (name calling, whistling, comments about body, sexual jokes, spreading rumours etc)
        . Physical Harassment (touching, hugging, kissing, patting or stroking, standing too close etc)
        . Written/visual Harassment (elevator eyes, staring, blocking path, winking, throwing kisses and flicking lips etc)
        . Quid pro quo (Offering a favour or advantage in return for something sexual)
        . Hostile environment (Creating an environment that is unfavourable for others to work in)

    The workplace includes:

        . All offices or other premises where the company’s business is conducted
        . All company related activities performed at any other site away from the company’s premises
        . Any social, business or other functions where the conduct or comments may have an adverse impact on the workplace or workplace relations
          and all level of transport facility provided by company.

    Provisions:

        1. Any aggrieved women may in writing make a complaint of sexual harassment at workplace to ICC members or can send an email within 3 months
           of last occurrence of act.
        2. The Complaint will be handled confidentially to the extent possible.
        3. The company will ensure that neither victim nor any witness is victimized or discriminated against for lodging complaint or participating 
           in any investigation.
        4. Disciplinary action will be initiated against any employee who registers a false complaint or who does so with the  intent of reprisal or
           personal gain.
    ________________________________________________________________________________________________________

    Declaration and Undertaking for usage of Social Media

    I hereby acknowledge that I will not misuse or misrepresent the Organization’s brand name in any social media post association with Organization.

    Posting defamatory comments or material against someone, sharing confidential information, or misusing the Organization’s brand name is also an 
    offence under Section 66A of the IT Act and is punishable with imprisonment and/or penalty.

    All employees and ex-employees of One Point One Solutions Limited are prohibited from establishing or promoting any group or community on 
    any internet sites, which uses the name or logo of 1Point1/One Point One Solutions/Pvt.Ltd/Ltd.

    I also hereby declare that:

        . I will not become a member of any such group or community unless such group is expressly created or permitted by One Point One Solutions
          Limited will not create any social network profile by using Organization brand name or logo
        . will not write, express, or post any remarks, views, or content on any internet site or social media platform; including but not limited 
          to blogs,wikis, microblogs, message boards, chat rooms, electronic newsletters, online forums that may damage the reputation of the 
          Organization or any of its employees in their official capacity.
        . will not engage in discussions or criticize the management, processes, policies or operations of the Organization on the social media or
          any other online platform.
        . will not engage in any form of collusive behaviour or illegal activity with other employees or any third parties on socaial media 
          or  internet platforms
        . will not share any confidential, proprietary, or sensitive information of the Organization on social media or any online platform. 
          This includes but is not limited to financial data, trade secrets, internal communications, and employee details.
        . will make it clear that any views or opinions I express on personal social media are my own and do not represent the views of the
          Organization unless explicitly authorized by the Organization to do so.
        . will comply with the Organization's social media usage policy and guidelines, which may be updated from time to time.

        . acknowledge that I am personally responsible for my online conduct and any potential consequences arising from my use of social media,
          including any legal,financial, or reputational repercussions for the Organization

    ________________________________________________________________________________________________________



    Non-Disclosure of Data and Information Security

    I hereby acknowledge that I will not engage in any unauthorized disclosure of confidential information or data of One Point One Solutions Limited 
    through verbal,written or any other form of communication.

    I will not divulge any information regarding the data, information or project I am working on, which may be detrimental to Organization interest.

    One Point One Solutions Limited reserves all rights to recover any losses or penalities arising out of damage caused by unauthorized disclosure 
    of information.
    I agree and authorize my employer to deduct such amount from my salary.

    I understand that severe disciplinary action may be initiated against me including termination of employment, if I am found involved in unauthorized 
    disclosure of data or confidential information. and I accept the consequences as per Company’s Code of Conduct.

    ________________________________________________________________________________________________________

    I hereby acknowledge that I have read the above mentioned clauses related to:
        1.Prevention of Sexual Harassment at workplace
        2.Usage of Social media
        3.Data and Information Security 

    I, hereby acknowledge that I have received and fully understand the Company's Non-Disclosure Agreement (NDA) and I agree to abide by its terms,
    including maintaining the confidentiality of all confidential information as defined therein.

    I understand that any breach of this agreement may result in disciplinary action, up to and including termination of employment, as well as legal
    action if necessary.
    """

    # Insert and lock text
    text.insert("1.0", nda_text)
    text.config(state="disabled")

    # Accept button below the form
    accept_btn = tk.Button(
        root, text="ACCEPT", font=("Helvetica", 16, "bold"),
        bg="royalblue", fg="white", padx=20, pady=10,
        command=on_accept, relief="raised", bd=3
    )
    accept_btn.pack(pady=(10, 30))

    # Lock interaction
    root.grab_set()
    root.focus_force()
    root.mainloop()
