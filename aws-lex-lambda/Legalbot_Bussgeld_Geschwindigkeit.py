"""
Lexbot Lambda handler.
"""
from urllib.request import Request, urlopen
import json


#############
#Bußgeldrechner für Verkehrsverstöße mit Pkw oder Lkw
def Geschwindigkeitsverstoss(fahrzeug='pkw', pkw_mit_anhaenger= 'nein',
                             inner_ausser='innerorts', schnell=10,
                             gewicht='nein', schritt='ja'):

    # strafe = [0,0,0] # [Bußgeld, Punkte, Fahrverbot]

    # Pkw - Überschreitung der Höchstgeschwindigkeit außerorts 
    if fahrzeug == 'pkw':
        # PKW mit Anhänger
        if pkw_mit_anhaenger == 'ja':
            if inner_ausser == 'außerorts':
                if schnell<= 10:
                    strafe = [15, 0, 0]
                elif schnell<= 15:
                    strafe = [25, 0, 0]
                elif schnell<= 20:
                    strafe = [70, 1, 0]
                elif schnell<= 25:
                    strafe = [80 , 1, 0]
                elif schnell<= 30:
                    strafe = [95, 1, 1]
                elif schnell<= 40:
                    strafe = [120, 2, 1]
                elif schnell<= 50:
                    strafe = [160, 2, 1]
                elif schnell<= 60:
                    strafe = [240, 2, 1]
                else:
                    strafe = [600, 2, 3]

            elif inner_ausser == 'innerorts':
                if schnell<= 10:
                    strafe = [20, 0, 0]
                elif schnell<= 15:
                    strafe = [30, 0, 0]
                elif schnell<= 20:
                    strafe = [80, 1, 0]
                elif schnell<= 25:
                    strafe = [95, 2, 1]
                elif schnell<= 30:
                    strafe = [140, 2, 1]
                elif schnell<= 40:
                    strafe = [200, 2, 1]
                elif schnell<= 50:
                    strafe = [280, 2, 1]
                elif schnell<= 60:
                    strafe = [480, 2, 2]
                else:
                    strafe = [680, 2, 3]

        # PKW ohne Anhänger
        else:
            if inner_ausser == 'außerorts':
                if schnell<= 10:
                    strafe = [10, 0, 0]
                elif schnell<= 15:
                    strafe = [20, 0, 0]
                elif schnell<= 20:
                    strafe = [30, 0, 0]
                elif schnell<= 25:
                    strafe = [70 , 1, 0]
                elif schnell<= 30:
                    strafe = [80, 1, 0]
                elif schnell<= 40:
                    strafe = [120, 1, 0]
                elif schnell<= 50:
                    strafe = [160, 2, 1]
                elif schnell<= 60:
                    strafe = [240, 2, 1]
                elif schnell<= 70:
                    strafe = [440, 2, 2]
                else:
                    strafe = [600, 2, 3]
        # Pkw - Überschreitung der Höchstgeschwindigkeit innerorts
            elif inner_ausser == 'innerorts':
                if schnell<= 10:
                    strafe = [15, 0, 0]
                elif schnell<= 15:
                    strafe = [25, 0, 0]
                elif schnell<= 20:
                    strafe = [35, 0, 0]
                elif schnell<= 25:
                    strafe = [80, 1, 0]
                elif schnell<= 30:
                    strafe = [100, 1, 0]
                elif schnell<= 40:
                    strafe = [160, 2, 1]
                elif schnell<= 50:
                    strafe = [200, 2, 1]
                elif schnell<= 60:
                    strafe = [280, 2, 2]
                elif schnell<= 70:
                    strafe = [480, 2, 3]
                else:
                    strafe = [680, 2, 3]
                print("Achtung: Wird die angegebene Höchstgeschwindigkeit in einem Jahr zwei Mal um mindestens 26 km/h überschritten, droht ein 1-monatiges Fahrverbot.")

                
    elif fahrzeug == 'lkw':
        
        # Geschwindigkeitsüberschreitung mit Lkw bis 3,5 t
        if gewicht == 'nein':
            if inner_ausser == 'außerorts':
                if schnell<= 10:
                    strafe = [20, 0, 0]
                elif schnell<= 15:
                    strafe = [40, 0, 0]
                elif schnell<= 20:
                    strafe = [60, 0, 0]
                elif schnell<= 25:
                    strafe = [70 , 1, 0]
                elif schnell<= 30:
                    strafe = [80, 1, 1]
                elif schnell<= 40:
                    strafe = [120, 1, 1]
                elif schnell<= 50:
                    strafe = [160, 2, 1]
                elif schnell<= 60:
                    strafe = [240, 2, 1]
                elif schnell<= 70:
                    strafe = [440, 2, 2]
                else:
                    strafe = [600, 2, 3]

            elif inner_ausser == 'innerorts':
                if schnell<= 10:
                    strafe = [30, 0, 0]
                elif schnell<= 15:
                    strafe = [50, 0, 0]
                elif schnell<= 20:
                    strafe = [70, 0, 0]
                elif schnell<= 25:
                    strafe = [80, 1, 1]
                elif schnell<= 30:
                    strafe = [100, 1, 1]
                elif schnell<= 40:
                    strafe = [160, 2, 1]
                elif schnell<= 50:
                    strafe = [200, 2, 1]
                elif schnell<= 60:
                    strafe = [280, 2, 1]
                elif schnell<= 70:
                    strafe = [480, 2, 2]
                else:
                    strafe = [680, 2, 3]
                    
        # Geschwindigkeitsüberschreitung mit Lkw über 3,5 t zGG oder mit Anhänger
        else:
            if inner_ausser == 'außerorts':
                if schnell<= 10:
                    strafe = [15, 0, 0]
                elif schnell<= 15:
                    strafe = [25, 0, 0]
                elif schnell<= 20:
                    strafe = [70, 0, 0]
                elif schnell<= 25:
                    strafe = [80 , 1, 0]
                elif schnell<= 30:
                    strafe = [95, 1, 1]
                elif schnell<= 40:
                    strafe = [160, 2, 1]
                elif schnell<= 50:
                    strafe = [240, 2, 1]
                elif schnell<= 60:
                    strafe = [440, 2, 2]
                else:
                    strafe = [600, 2, 3]

            elif inner_ausser == 'innerorts':
                
                if schnell<= 10:
                    strafe = [20, 0, 0]
                elif schnell<= 15:
                    strafe = [30, 0, 0]
                elif schnell<= 20:
                    strafe = [80, 1, 0]
                elif schnell<= 25:
                    strafe = [95, 2, 1]
                elif schnell<= 30:
                    strafe = [140, 2, 1]
                elif schnell<= 40:
                    strafe = [200, 2, 1]
                elif schnell<= 50:
                    strafe = [280, 2, 1]
                elif schnell<= 60:
                    strafe = [480, 2, 2]
                else:
                    strafe = [680, 2, 3]
                    
               #beim Rechtsabbiegen innerorts nicht Schrittgeschwindigkeit gefahren ?
                if schritt == "ja":
                    strafe = [70, 1, 0]
                else:
                    pass
       
        
    return "Sie bezahlen {} Euro Bußgeld. Sie haben {} Punkt/e verloren und {} Monat/e Fahrverbot.".format(strafe[0], strafe[1], strafe[2])
    
Geschwindigkeitsverstoss()


##### MAIN ####
    
def lambda_handler(event, context):
    print('received request: ' + str(event))
    fahrzeug = event['currentIntent']['slots']['fahrzeug']
    pkw_mit_anhaenger = event['currentIntent']['slots']['pkw_mit_anhaenger']
    inner_ausser = event['currentIntent']['slots']['inner_ausser']
    schnell = int(event['currentIntent']['slots']['schnell'])
    gewicht = event['currentIntent']['slots']['gewicht']
    schritt = event['currentIntent']['slots']['schritt']

    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": str(Geschwindigkeitsverstoss(fahrzeug=fahrzeug, pkw_mit_anhaenger=pkw_mit_anhaenger,
                             inner_ausser=inner_ausser, schnell=schnell,
                             gewicht=gewicht, schritt=schritt))
            },
        }
    }
    print('result = ' + str(response))
    return response