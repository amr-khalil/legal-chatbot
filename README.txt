#Project structure

juristischer-chatbot
├── app
│   ├── __init__.py
│   ├── algorithm.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── index.css
│   │   ├── img
│   │   │   ├── amr.png
│   │   │   ├── bg.jpg
│   │   │   ├── chatbot3.gif
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   └── lex.png
│   │   └── js
│   │       ├── api.js
│   │       ├── aws-lex-audio.js
│   │       └── renderer.js
│   └── templates
│       ├── _post.html
│       ├── base.html
│       ├── chatbot.html
│       ├── edit_profile.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── user.html
│       └── voice_assistant.html
├── aws-lex-lambda
│   ├── Legalbot_Bahnverspaetung.py
│   ├── Legalbot_Bussgeld_Geschwindigkeit.py
│   └── Legalbot_Flugverspaetung.py
├── chatbot.db
├── config.py
├── data
│   └── csv
│       ├── Anwaltsrecht,\ Gebu?\210hrenrecht.csv
│       ├── Arbeitsrecht.csv
│       ├── Ausla?\210nderrecht.csv
│       ├── Baurecht,\ Architektenrecht.csv
│       ├── Datenschutzrecht.csv
│       ├── Erbrecht.csv
│       ├── Familienrecht.csv
│       ├── Generelle\ Themen.csv
│       ├── Gesellschaftsrecht.csv
│       ├── Inkasso,\ Mahnungen.csv
│       ├── Insolvenzrecht.csv
│       ├── Internationales\ Recht.csv
│       ├── Internetauktionen.csv
│       ├── Internetrecht,\ Computerrecht.csv
│       ├── Kaufrecht.csv
│       ├── Medienrecht.csv
│       ├── Medizinrecht.csv
│       ├── Mietrecht,\ Wohnungseigentum.csv
│       ├── Nachbarschaftsrecht.csv
│       ├── Reiserecht.csv
│       ├── Schadensersatz.csv
│       ├── Sozialrecht.csv
│       ├── Sozialversicherungsrecht.csv
│       ├── Steuerrecht.csv
│       ├── Strafrecht.csv
│       ├── Tierrecht,\ Tierkaufrecht.csv
│       ├── Transportrecht,\ Speditionsrecht.csv
│       ├── Urheberrecht,\ Markenrecht,\ Patentrecht.csv
│       ├── Verkehrsrecht.csv
│       ├── Versicherungsrecht,\ Privatversicherungsrecht.csv
│       ├── Vertragsrecht.csv
│       ├── Verwaltungsrecht.csv
│       └── Wirtschaftsrecht,\ Bankrecht,\ Wettbewerbsrecht.csv
├── requirements.txt
└── server.py

15 directories, 81 files