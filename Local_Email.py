import smtplib
from datetime import datetime
def email_module(temp, temp_unit):
    try:
        with smtplib.SMTP("smtp.gmail.com",587) as smtp:
            smtp.ehlo()
            smtp.starttls()

            smtp.login('machinemonitoringcenter@gmail.com','hlvekejgxyslqiet')
                #gmail for this project: machinemonitoringcenter@gmail.com
                #gmail password: MMC#2022
            subject = 'Temperature Error'
            if temp_unit == '°C':
                temp_unit = 'Celcius'
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            body = 'The temperature was recorded at '+str(round(float(temp),2))+'  '+str(temp_unit)+' at '+str(current_time)
            msg = f'Subject: {subject}\n\n{body}'
            print(msg)
            
            smtp.sendmail('machinemonitoringcenter@gmail.com',['dylangessert@gmail.com','dgessert@wisc.edu'], msg)
            #'minlab@office365.wisc.edu'   #minlab mailing list
    except:
        try:
            #Safe Message, Possible there's a charecter in the message that caused it to fail
            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                smtp.ehlo()
                smtp.starttls()

                smtp.login('machinemonitoringcenter@gmail.com','hlvekejgxyslqiet')
                    #gmail for this project: machinemonitoringcenter@gmail.com
                    #gmail password: MMC#2022
                subject = 'Temperature Error'
                body = 'There was an out of range temp recorded I can not tell you the exact number'
                msg = f'Subject: {subject}\n\n{body}'
                print(msg)
                
                smtp.sendmail('machinemonitoringcenter@gmail.com',['dylangessert@gmail.com','dgessert@wisc.edu'], msg)
                #'minlab@office365.wisc.edu'   #minlab mailing list
        except:
            print('emailing error')
            pass