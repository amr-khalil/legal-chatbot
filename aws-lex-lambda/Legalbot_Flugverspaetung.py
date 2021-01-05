"""
Lexbot Lambda handler.
"""
from urllib.request import Request, urlopen
import json

def Flugverspaetung(strecke=1600, verspaetung=120, frageEins="ja", frageZwei="nein"):
    
    # frageEins = Bsit du nach EU oder von EU geflogen?
    # frageZwei = Hattest du Ankunftsverspätung  ?
    # Wie lange ist die Strecke?
    # Kurzstrecke (bis 1.500 km)
    if strecke > 100 and strecke < 1500:
        #verspätung in Minuten ?
        if verspaetung >= 2*60 and verspaetung < 3*60:
            erstattung = "Die Airline muss kostenfrei Getränke und Snacks anbieten"
        elif verspaetung >= 3*60 or frageZwei=="ja":
             erstattung = "Du bekommst 250 € pro Person. Du hast Anspruch auf Entschädigung auf Anschlussflügen"
        else:
            erstattung = "Du hast kein Anspruch"

    # Mittelstrecke (1.500 - 3.500 km)
    elif strecke >= 1500 and strecke < 3500:
        if verspaetung > 2*60 and verspaetung < 3*60:
            erstattung = "Die Airline muss kostenfrei Getränke und Snacks anbieten."
        elif verspaetung >= 3*60:
            erstattung = "Die Fluggesellschaft ist verpflichtet Versorgungsleistungen anzubieten."
            if frageZwei == "ja":
                erstattung = "Du bekommst 400 € pro Person. Du hast Anspruch auf Entschädigung auf Anschlussflügen." 
        else:
            erstattung = "Du hast kein Anspruch"

    # Langstrecke (ab 3.500 km)        
    elif strecke > 3500 and strecke <= 17000:
        if verspaetung > 2*60 and verspaetung < 3*60 :
            erstattung = "Die Airline muss kostenfrei Getränke und Snacks anbieten"

        elif (verspaetung >= 3*60 and verspaetung < 4*60) or frageZwei == "ja":
            erstattung = "Du bekommst 600 € pro Person. Du hast Anspruch auf Entschädigung auf Anschlussflügen." 

        elif verspaetung >= 4*60 or frageZwei == "ja":
            erstattung = "Du bekommst 600 € pro Person. Du hast Anspruch auf Entschädigung auf Anschlussflügen."\
            " Passagiere haben Anspruch auf Getränke und Snacks."

        else:
            erstattung = "Du hast kein Anspruch" 

    elif strecke > 17000:
        erstattung = "Die Angaben ist nicht richtig. Die Linienflüge weltweit ist 17000"
    else:
        erstattung = "Du hast kein Anspruch"        
        
        
    if  verspaetung > 5*60:
        erstattung = "Du kannst vom Flug zurücktreten. Die Airline muss die Ticketkosten erstatten."\
        " Du hast Anspruch auf Entschädigung auf Anschlussflügen"

    if  verspaetung > 12*60:
        erstattung = "Du kannst vom Flug zurücktreten. Die Airline muss die Ticketkosten erstatten."\
        " Du hast Anspruch auf Entschädigung auf Anschlussflügen."\
        " Wenn die Flug im nächsten Tag ist, dann hast du Anspruch auf eine Hotelübernachtung inklusive"
   
    if frageEins == "nein":
        erstattung = "Du hast kein Anspruch" 
        

    return erstattung
    
Flugverspaetung(strecke=101, verspaetung=3*60, frageEins="ja", frageZwei="nein")  


##### MAIN ####

def lambda_handler(event, context):
    print('received request: ' + str(event))
    frageEins = event['currentIntent']['slots']['frageEins']
    frageZwei = event['currentIntent']['slots']['frageZwei']
    strecke = int(event['currentIntent']['slots']['strecke'])
    verspaetung = int(event['currentIntent']['slots']['verspaetung'])


    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": str(Flugverspaetung(strecke=strecke, verspaetung=verspaetung, frageEins=frageEins, frageZwei=frageZwei))
            },
        }
    }
    print('result = ' + str(response))
    return response
