import email
from lib2to3.pgen2 import grammar
from multiprocessing import context
from optparse import Values
from random import random
import smtplib
from email.message import EmailMessage
from socket import timeout
import ssl
import time
from tokenize import group
import random
def get_data():
    file = open("info.txt", "r")
    liu_id_data = file.read().lower()
    liu_id_data = liu_id_data.split("\n")
    file.close()

    file = open("group_names.txt", "r")
    group_data = file.read().lower()
    group_data = group_data.split("\n")
    file.close()

    text_file = open("text.txt", "r")
    data_text = text_file.read()
    file.close()

    return group_data, liu_id_data, data_text

def get_name(liu_id_data):
    list_emails = []
    for name in liu_id_data:
        list_emails.append(name + "@student.liu.se")

    return list_emails

def create_dict(list_emails, group_data):
    dict_data = {}
    for key in list_emails:
        for value in group_data:
            dict_data[key] = value
            group_data.remove(value)
            break
    return dict_data

def sort_dict(dict_data):
    sorted_dict = sorted(dict_data.items(), key=lambda item: item[1])
    return sorted_dict

def create_groups(sorted_dict):
    list_of_lists = [list(elem) for elem in sorted_dict]
    index = 0
    group_nr = 1
    group_length = 0
    for value in list_of_lists:
        if value[1] == list_of_lists[index][1]:
            group_length += 1
            list_of_lists[index].append(group_nr)
        elif value[1] == list_of_lists[index-1][1]:
            group_length += 1
            list_of_lists[index].append(group_nr)
        elif value[1] == list_of_lists[index-2][1]:
            group_length += 1
            list_of_lists[index].append(group_nr)
        else:
            group_length +=1
            list_of_lists[index].append(group_nr)
        if group_nr == 3 and group_length ==12:
            group_length = 0
            group_nr +=1
        if group_length  ==13:
            group_length = 0
            group_nr +=1
        index += 1
        if index >= 51:
            break

    return list_of_lists

def send_mail(receiver,text_send):

    email_sender = "shamji.test@gmail.com"
    email_password = "agnyoczuumyhmlqk"
    subject = "Sittining/Party"
    em = EmailMessage() 
    em["From"] = email_sender
    em["To"] = receiver
    em["Subject"] = subject
    
    for value in receiver:
        time.sleep(4)
        number = value[2]
        mail = value[0]
        group = value[1]
        body = text_send + f"Your starting group number is {number}."
        email_receiver = mail
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver , em.as_string())
        print("Sent", mail, group ,number)

def main():
    
    data_value = get_data()
    liu_id_mails=get_name(data_value[1])
    dict_data=create_dict(liu_id_mails, data_value[0])
    sorted_dict = sort_dict(dict_data)
    groups = create_groups(sorted_dict)
    send_mail(groups,data_value[2])

main()