# MCSI_TuxKart

Projet réalisé par Quentin DUBREUIL, Loic GLEMAREC et Gwendal PATON dans le cadre de l'UE MCSI du master SIIA

Interacteurs utilisés : clavier midi, drumpants et microphone

## Setup

Lancer le serveur `STK_input_server.py`

Lancer les différents `STK_input_client_drumpants.py`, `STK_input_client_piano.py`, `STK_input_client_microphone.py`

Dans le code, changer la ligne `input_main(x)` et remplacer `x` par l'id du périphérique midi. Le client affiche l'id de tous les péripéhriques midi connectés au démarrage.
