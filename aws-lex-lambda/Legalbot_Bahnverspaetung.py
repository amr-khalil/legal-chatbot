"""
Lexbot Lambda handler.
"""
from urllib.request import Request, urlopen
import json

#### mein Code ####

def Bahnverspaetung(f_n_verkehr="nahverkehr", fahrtstand="abgeschlossen", verspaetung = 60,
                    karte="nahverkehr", klasse="2", frageEins="nein"):
    
##### Fernverkehr #####
    if f_n_verkehr.lower().strip() in ["fernverkehr", "fern"]:
        
        # Fahrtstand abgeschlossen, unterwegs oder Noch nicht angetreten
        if  "abgeschlossen" in fahrtstand.lower().strip():
            if verspaetung >= 60 and verspaetung < 120:
                erstattung = "25%"
            elif verspaetung >= 120:
                erstattung = "50%"
            else:
                erstattung = "0 Euro"
                  
        elif "unterwegs" in fahrtstand.lower().strip():
            if verspaetung >= 60:
                erstattung = "eines anderen Verkehrsmittel bis 80€"
                # frageEins = Hast du das Ziel nicht mehr vor 00:00 Uhr oder letzte Verbindung am Tag?
                if frageEins.lower() =="ja":
                    erstattung = "einer Übernachtung"
            else:
                erstattung = "0 Euro"
        else:
            erstattung = "das urlabniss, den Vertrag zurückzutreten"
            
##### Nahverkehr #####          
    else:
        if verspaetung >= 60:
            # Bahn Card 100
            if karte.lower() in ['bahncard100', 'bahncard 100', '100']:
                if klasse in ["1", "klasse1", "klasse 1", "1.klasse", "1 klasse", "1klasse"]:
                    erstattung = "15 Euro"
                else:
                    erstattung = "10 Euro"
            # Zeitkarte 
            elif karte.lower() in ['zeitkarte', 'zeit', 'zeitkart']:
                if klasse in ["1", "klasse1", "klasse 1", "1.klasse", "1 klasse", "1klasse"]:
                    erstattung = "7,50 Euro"
                else:
                    erstattung = "5,00 Euro"

            else:      
                if klasse in ["1", "klasse1", "klasse 1", "1.klasse", "1 klasse", "1klasse"]:
                    erstattung = "2,25 Euro"
                else:
                    erstattung = "1,50 Euro"        

        else:
            erstattung = "0 Euro"
    
    return "Du bekommst eine Erstatung {}".format(erstattung)

Bahnverspaetung(f_n_verkehr="fern", fahrtstand="unterwegs", verspaetung = 120,
                    karte="zeit", klasse="2", frageEins="nein")
    



##### MAIN ####

def lambda_handler(event, context):
    print('received request: ' + str(event))
    f_n_verkehr = event['currentIntent']['slots']['f_n_verkehr']
    fahrtstand = event['currentIntent']['slots']['fahrtstand']
    verspaetung = int(event['currentIntent']['slots']['verspaetung'])
    karte = event['currentIntent']['slots']['verspaetung']
    klasse = event['currentIntent']['slots']['klasse']
    frageEins = event['currentIntent']['slots']['frageEins']
    


    
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
