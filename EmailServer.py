import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    port = 587  
    smtp_server = "smtp.gmail.com"
    sender_email = "matrix00siete@hotmail.com"
    password = "homework"
    receiver_email = ""
    firstName = ""
    host = ""
    token = ""


    def __init__(self, email, name, host, token):
        self.receiver_email = email
        self.firstName = name
        self.host = host
        self.token = token
        
    
            

    def constructHtml(self):
        str1 = '<html>'
        str2 = '<body>' 
        str3 = '<h1 style="text-align:center;color:rgb(0, 153, 0)">RoomR</h1>'
        str4 = '<h3 style="text-align:center;color:#404040">Improving the relationship between landlord and tenant.</h3>'
        str5 = f'<p style="margin-left: 20%">Hi, {self.firstName}</p>'
        str6 = '<p style="margin-left: 20%">Thank you for authenticating RoomR. Please click on the link below to verify login.</p>'
        str7 = f'<form style="text-align:center; color:color:rgb(0, 153, 0)" action="{self.host}/AddLandlord/{self.token}/{self.receiver_email}">'
        str8 = '<input style="background-color:  rgb(255, 255, 255);'+ 'border: 1px solid rgb(0, 0, 0);'+ 'color: rgb(0, 153, 0);'+'padding: 16px 32px;'+'margin: 4px 2px;"'+'type="submit" value="Verify login" />'
        str9 = '</form>'
        str10 = '</body>'
        str11 = '</html>'

        return str1 + str2 + str3 + str4 + str5 + str6 + str7 +str8 + str9 + str10 + str11
        

    def sendContactProfileEmail(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "RoomR Listing"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        
        text = "Hello " + self.firstName + ",\n\n\tI saw your add on my house and I would like to have you as a tenant. Please email me back as soon as possible to schedule a tour of the house.\n\nThanks"
        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())

    def sendEmail(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verify Login for RoomR"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        
        html = self.constructHtml()
        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
