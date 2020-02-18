#mail modules
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
#fire modules
import numpy as np
import cv2
import time
import winsound
from twilio.rest import Client
def sendemail():
    fromaddr = ""
    toaddr = ""
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "FIRE ALERT"
    body = "FIRE CAUGHT AT CAMERA"
    msg.attach(MIMEText(body, 'plain'))
    filename = "fireimage.jpg"
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr,"password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
#fire code
firecascade = cv2.CascadeClassifier('firedetectioncascade.xml')
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = firecascade.detectMultiScale(frame, 1.2, 5)
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        print("FIRE DETECTED")
        cv2.imwrite('fireimage.jpg', frame)
        # Alarm alert
        duration = 1500  # milliseconds
        freq = 600  # Hz
        winsound.Beep(freq, duration)
        #SMS alert
        print("SENDING MESSAGE")
        account_sid = ''
        auth_token = ''
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(body="FIRE CAUGHT AT CAMERA !",
                    from_='',

                    to=''
                    )
        print("MESSAGE SENT TO GIVEN NUMBERS")
        #Email alert
        print("SENDING EMAIL")
        sendemail()
        print("EMAIL SENT")
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
cv2.destroyAllWindows()

