import os
import sys
import threading
import subprocess
from Class import *

## paikat (käytetään myös Main.py:ssä)

KÄVELYPOLKU = "on the walking path"
BUSSIPYSÄKKI = "at the bus stop"

## cls

def tyhjennä_ruutu():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
 
def odota_enter():
    input("\n[Press Enter to continue]")

## ajastettu kysymys

def ajastettu_input(prompt, aikaraja):
    tulos = [None]  # vastaukselle lista

    def kysy():     
        tulos[0] = input(prompt)  # kysytään käyttäjältä ja lisää sen listaan

    threads = threading.Thread(target=kysy) # Säie kysymysfunktiolle
    threads.daemon = True # daemon-säie, jotta se ei estä ohjelman sulkeutumista
    threads.start() # käynnistetään säie
    threads.join(timeout=aikaraja) # odotetaan aikarajan verran

    if threads.is_alive(): 
        return None 
    return tulos[0] # palautetaan käyttäjän vastaus jos se saatiin ajoissa muuten None

## valikot

ALKU_VALIKKO = """
╔══════════════════════════════════╗
║       [   START MENU   ]         ║
╠══════════════════════════════════╣
║                                  ║
║   1- Instructions                ║
║   2- Start Game                  ║
║   Quit                           ║
║                                  ║
║                                  ║
╚══════════════════════════════════╝
"""

PÄÄ_VALIKKO = """
╔════════════════════════════════════════╗
║  [   HOW DO YOU TRAVEL TO SCHOOL?   ]  ║
╠════════════════════════════════════════╣
║                                        ║
║   1- Walking                           ║
║   2- Bicycle                           ║
║   3- Bus                               ║
║   4- Car (18+)                         ║
║   5- Backpack                          ║
║   6- Location                          ║
║   Quit                                 ║
║                                        ║
╚════════════════════════════════════════╝
"""

PIENI_VALIKKO = """
╔════════════════════════════╗
║    [   SMALL MENU   ]      ║
╠════════════════════════════╣
║   1- Backpack              ║
║   2- Location              ║
║   3- Status                ║
║   4- Continue/Enter        ║
║   Quit                     ║
╚════════════════════════════╝
"""

def vahvista_lopetus(pelaaja: Pelaaja):
    vahvistus1 = input("\nAre you sure you want to quit? (yes/no): ").strip().lower()

    if vahvistus1 == "yes":
        vahvistus2 = input("Are you REALLY sure? Like, 100% sure? (yes/no): ").strip().lower()

        if vahvistus2 == "yes":
            if pelaaja.matka_alkanut:
                print("\nYour progress is saved. Use the same username to continue later.")
            print(f"\nThank you for playing, {pelaaja.käyttäjätunnus}! See you next time.")
            sys.exit()
        else:
            print("\nHah, knew it. Let's keep going.")
    else:
        print("\nFalse alarm. Let's keep going.")

def tulosta_pieni_valikko(pelaaja: Pelaaja):
    print(f"\nYou are {pelaaja.sijainti.nimi}.")
    print(PIENI_VALIKKO)

def pieni_valikko_lisäys(pelaaja: Pelaaja):
    tulosta_pieni_valikko(pelaaja)
    komento = input("Enter command: ").strip().lower()

    while komento != "4" and komento != "": # 4 tai Enter - continue 
        if komento == "1": # 1 - backpack
            pelaaja.näytä_reppu()
        elif komento == "2": # 2 - location
            pelaaja.näytä_sijainti() 
        elif komento == "3": # 3 - status
            pelaaja.näytä_status()
        elif komento == "quit":
            vahvista_lopetus(pelaaja)
        else:
            print("\nUnknown command. Please try again.")

        tulosta_pieni_valikko(pelaaja)
        komento = input("Enter command: ").strip().lower()

def näytä_ohjeet():
    polku = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Instructions.txt")
    try:
        with open(polku, "r", encoding="utf-8") as tiedosto:
            print("\n" + tiedosto.read())
    except FileNotFoundError:
        print("\nInstructions file was not found.")

# polku = os.path.join(          # 4. liitetään tiedoston nimi kansion perään
#     os.path.dirname(           # 3. otetaan vain kansio (GameProject)
#         os.path.abspath(       # 2. tehdään täysi osoite (...\GameProject\Function.py)
#             __file__)),        # 1. tämän tiedoston nimi (Function.py)
#     "Instructions.txt")

def näytä_intro():
    polku = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Intro.txt")
    try:
        with open(polku, "r", encoding="utf-8") as tiedosto:
            print("\n" + tiedosto.read())
    except FileNotFoundError:
        print("\nIntro file was not found.")

def alku_valikko_käsittely(pelaaja: Pelaaja):
    print(ALKU_VALIKKO)
    komento = input("Enter command: ").strip().lower()

    while komento != "2": # 2 - start game
        if komento == "1": # 1 - instructions
            näytä_ohjeet()
            odota_enter()
            tyhjennä_ruutu()
        elif komento == "quit":
            vahvista_lopetus(pelaaja)
        else:
            print("\nUnknown command. Please try again.")

        print(ALKU_VALIKKO)
        komento = input("Enter command: ").strip().lower()

    tyhjennä_ruutu()

def aloita_peli(pelaaja: Pelaaja):
    print(f"\nWelcome {pelaaja.käyttäjätunnus}! Let's start the game!")
    print(PÄÄ_VALIKKO)
    return input("Enter command: ").strip().lower()

## tallennus

def tallennuksen_polku(käyttäjätunnus):
    # tiedoston nimeen otetaan vain kirjaimet ja numerot, esim. "Aleksi" - tallennus_aleksi.txt
    puhdas = "".join(merkki for merkki in käyttäjätunnus if merkki.isalnum()).lower()
    kansio = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(kansio, f"tallennus_{puhdas}.txt")

def tallenna_peli(pelaaja: Pelaaja, reitti, vaihe):
    polku = tallennuksen_polku(pelaaja.käyttäjätunnus)

    # lista tekstiksi: kaikki esineet muotoon "nimi:paino" pilkulla erotettuna
    reppu_tekstiksi = ",".join(f"{esine.nimi}:{esine.paino}" for esine in pelaaja.reppu)

    with open(polku, "w", encoding="utf-8") as tiedosto: # "w" = kirjoita (vanha sisältö korvataan)
        tiedosto.write(f"nimi={pelaaja.käyttäjätunnus}\n")
        tiedosto.write(f"ikä={pelaaja.ikä}\n")
        tiedosto.write(f"reitti={reitti}\n")
        tiedosto.write(f"vaihe={vaihe}\n")
        tiedosto.write(f"sijainti={pelaaja.sijainti.nimi}\n")
        tiedosto.write(f"tunteet={','.join(pelaaja.tunteet)}\n")
        tiedosto.write(f"tapahtumat={','.join(pelaaja.tapahtumat)}\n")
        tiedosto.write(f"reppu={reppu_tekstiksi}\n")

def tekstistä_listaksi(teksti):
    if teksti == "":
        return [] # tyhjästä tekstistä tulee tyhjä lista
    return teksti.split(",")

def lataa_peli(käyttäjätunnus):
    polku = tallennuksen_polku(käyttäjätunnus)
    tiedot = {} # sanakirja: avain -> arvo, esim. tiedot["reitti"] = "2"

    try:
        with open(polku, "r", encoding="utf-8") as tiedosto: # "r" = lue
            for rivi in tiedosto:
                rivi = rivi.strip()
                if "=" in rivi:
                    avain, arvo = rivi.split("=", 1) # jaetaan ensimmäisestä =-merkistä
                    tiedot[avain] = arvo

        pelaaja = Pelaaja(tiedot["nimi"], int(tiedot["ikä"]))
        pelaaja.sijainti = Paikka(tiedot["sijainti"])
        pelaaja.tunteet = tekstistä_listaksi(tiedot["tunteet"])
        pelaaja.tapahtumat = tekstistä_listaksi(tiedot["tapahtumat"])

        pelaaja.reppu = [] # tyhjennetään alkureppu ja rakennetaan tallennettu reppu
        for osa in tekstistä_listaksi(tiedot["reppu"]):
            nimi, paino = osa.rsplit(":", 1)
            pelaaja.lisää_reppuun(nimi, float(paino))

        reitti = tiedot["reitti"]
        vaihe = int(tiedot["vaihe"])

        if reitti not in REITIT or vaihe < 0 or vaihe >= len(REITIT[reitti]):
            raise ValueError("Tallennuksen reitti tai vaihe on virheellinen")

    except (OSError, KeyError, ValueError): # tiedostoa ei voi lukea tai se on rikki
        return None

    pelaaja.matka_alkanut = True
    return pelaaja, reitti, vaihe

def poista_tallennus(pelaaja: Pelaaja):
    polku = tallennuksen_polku(pelaaja.käyttäjätunnus)
    if os.path.exists(polku):
        os.remove(polku)

def aloita_tai_jatka():
    """Kysyy nimen. Jos tallennus löytyy, pelaaja voi jatkaa siitä. Palauttaa (pelaaja, reitti, vaihe)."""
    käyttäjätunnus = kysy_käyttäjätunnus()

    if os.path.exists(tallennuksen_polku(käyttäjätunnus)):
        print("\nA saved game was found for this username.")
        print("You continue from the start of the event you were on.")
        print("If you answer 'no', a new game starts and the old save is replaced.")

        if kysy_valinta("yes", "no", kehote="\nContinue the saved game? (yes/no): ") == "yes":
            tulos = lataa_peli(käyttäjätunnus)

            if tulos is not None:
                pelaaja, reitti, vaihe = tulos
                print(f"\nWelcome back {pelaaja.käyttäjätunnus}!")
                return pelaaja, reitti, vaihe

            print("\nThe save file could not be read. Starting a new game.")

    return luo_pelaaja(käyttäjätunnus), None, 0 # None = reittiä ei ole vielä valittu

def valitse_reitti(pelaaja: Pelaaja):
    """Uusi peli: intro, alkuvalikko ja matkustustavan valinta. Palauttaa reitin numeron ("1"-"4")."""
    näytä_intro()
    odota_enter()
    tyhjennä_ruutu()

    alku_valikko_käsittely(pelaaja)

    komento = aloita_peli(pelaaja)

    while True:
        if komento in ("1", "2", "3"): # walking, bicycle, bus
            return komento
        elif komento == "4": # car
            if pelaaja.ikä < 18:
                print("\nYou are under 18, so you can't drive a car. Please choose another way to travel.")
            else:
                return komento
        elif komento == "5": # backpack
            pelaaja.näytä_reppu()
        elif komento == "6": # location
            pelaaja.näytä_sijainti()
        elif komento == "quit":
            vahvista_lopetus(pelaaja)
        else:
            print("\nUnknown command. Please try again.")

        print(PÄÄ_VALIKKO)
        komento = input("Enter command: ").strip().lower()

## loppuyhteenveto

# tapahtuma / tunne -> rivi joka näytetään matkan lopussa
YHTEENVETO_RIVIT = {
    "picked up trash": "A teacher noticed you picking up trash and gave you a compliment.",
    "football": "You agreed to play football with your friends after school.",
    "late": "You were late to school, and your parents will hear about it.",
    "smelly": "You ran the last kilometer, so you smell a bit for the rest of the day.",
    "muddy shoes": "Your muddy shoes left footprints in the hallway. A janitor gave you a disapproving look.",
    "happy": "Petting that friendly dog still makes you smile.",
    "proud": "You are proud that you pedaled all the way up that steep hill.",
    "hurt leg": "Your leg still hurts from the dog bite.",
    "broken bicycle": "Your bicycle needs repairs after hitting the rock.",
    "broken phone": "Your phone broke in the crash, so you could not call anyone.",
    "guilty conscience": "You still feel bad about not paying for your ticket.",
    "gave up seat": "You gave your seat to an elderly passenger and made their day.",
    "awkward": "You still feel a bit awkward about keeping your seat on the bus.",
    "tired legs": "Your legs are tired from the extra walking.",
    "no lunch": "You forgot your lunch and hope that someone will share with you.",
    "wrong turn": "You took a wrong turn on the back roads.",
    "walked from parking": "You had to park far away and walk the last part.",
}

# asiat jotka ovat huonoja (vaikuttavat loppuarvosanaan)
HUONOT = {
    "late", "smelly", "muddy shoes", "broken bicycle", "broken phone", "hurt leg",
    "no lunch", "guilty conscience", "tired legs", "awkward",
}

def näytä_yhteenveto(pelaaja: Pelaaja):
    print("\n--- Your journey summary ---")

    kaikki = list(dict.fromkeys(pelaaja.tapahtumat + pelaaja.tunteet)) # ei tuplia, järjestys säilyy
    rivejä = 0
    for asia in kaikki:
        if asia in YHTEENVETO_RIVIT:
            print(f"- {YHTEENVETO_RIVIT[asia]}")
            rivejä += 1

    if rivejä == 0:
        print("- Nothing special happened on the way.")

    huonoja = len(set(kaikki) & HUONOT)

    if huonoja == 0:
        print("\nWhat a perfect morning!")
    elif huonoja <= 2:
        print("\nA bumpy morning, but you made it.")
    else:
        print("\nWhat a mess of a morning! But you made it.")

    poista_tallennus(pelaaja) # peli on pelattu loppuun, vanha tallennus ei enää tarvita
    return True # kertoo Main.py:lle että peli on ohi

## apufunktiot kysymyksille ja valikolle

def kysy_valinta(*vaihtoehdot, kehote="Enter your choice: "):
    """Kysyy kunnes pelaaja kirjoittaa jonkin vaihtoehdoista (koko sana)."""
    while True:
        vastaus = input(kehote).strip().lower()

        if vastaus in vaihtoehdot:
            return vastaus

        print(f"Unknown command. Please enter {' or '.join(vaihtoehdot)}")

def jatka_valikkoon(pelaaja: Pelaaja):
    """Tapahtuman jälkeen: odota Enter, tyhjennä ruutu ja näytä pieni valikko."""
    odota_enter()
    tyhjennä_ruutu()
    pieni_valikko_lisäys(pelaaja)

## kävely

def reitti_kävely1(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} starts walking to school. The sun is shining and the air is fresh.")
    pelaaja.sijainti = Paikka(KÄVELYPOLKU)

def tapahtuma_kävely_roska(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} sees some trash on the ground. Do they want to pick it up? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        pelaaja.lisää_reppuun("trash")
        pelaaja.lisää_tapahtuma("picked up trash")
        print(f"\n{pelaaja.käyttäjätunnus} picks up the trash. Good deed for the day!")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} leaves the trash and continues walking.")

    jatka_valikkoon(pelaaja)

def tapahtuma_kävely_kyssäri(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} reaches a crossing near the bus stop."
          "\nDo they want to give up walking and take the bus instead? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        print(f"\n{pelaaja.käyttäjätunnus} walks over to the bus stop to wait for the bus.")
        pelaaja.sijainti = Paikka(BUSSIPYSÄKKI)
    else:
        print(f"\n{pelaaja.käyttäjätunnus} keeps walking.")
        pelaaja.sijainti = Paikka(KÄVELYPOLKU)

    jatka_valikkoon(pelaaja)

def tapahtuma_kävely_ystävä(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} sees their friends in the distance"
          "\n\nDo they want to talk to them? (yes/no)"
          "\nIf they answer 'yes' they might be late for school")

    if kysy_valinta("yes", "no") == "yes":
        print(f"\n{pelaaja.käyttäjätunnus} starts talking to their friends for 20 minutes")
        tapahtuma_jalkapallo_kutsu(pelaaja)
    else:
        print(f"\n{pelaaja.käyttäjätunnus} waves at their friends and continues walking to school")
        jatka_valikkoon(pelaaja)

    tapahtuma_kävely_koira(pelaaja)

def tapahtuma_jalkapallo_kutsu(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus}'s friends invite them to play football after school. Do they want to join? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        pelaaja.lisää_tapahtuma("football")
        print(f"\n{pelaaja.käyttäjätunnus} agrees to play football after school!")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} declines and says goodbye to their friends.")

    jatka_valikkoon(pelaaja)
    tapahtuma_kävely_juoksu(pelaaja)

def tapahtuma_kävely_juoksu(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} lost 20 minutes talking and is now running late."
          "\n\nIf they run the last 1 km they will be on time, but they will smell for the rest of the day"
          "\nIf they walk they will be late and their parents will be mad")

    if kysy_valinta("run", "walk", kehote="\nEnter your choice (run/walk): ") == "walk":
        pelaaja.lisää_tapahtuma("late")
        print(f"\n{pelaaja.käyttäjätunnus} keeps walking to school at a calm pace.")
    else:
        pelaaja.lisää_tapahtuma("smelly")
        print(f"\n{pelaaja.käyttäjätunnus} starts running to school with their heavy backpack")

    jatka_valikkoon(pelaaja)

def tapahtuma_kävely_koira(pelaaja: Pelaaja):
    print(f"\nA friendly dog runs up to {pelaaja.käyttäjätunnus} and starts following them."
          "\nDo they want to pet it? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        pelaaja.lisää_tunteet("happy")
        print(f"\n{pelaaja.käyttäjätunnus} pets the dog. It wags its tail happily and then runs off.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} ignores the dog and keeps walking.")

    jatka_valikkoon(pelaaja)
    tapahtuma_kävely_oikotie(pelaaja)

def tapahtuma_kävely_oikotie(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} notices a shortcut through the park that could save some time,"
          "\nbut it looks muddy after last night's rain. Take the shortcut? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        print(f"\n{pelaaja.käyttäjätunnus} takes the shortcut and saves a few minutes, but their shoes get muddy.")
        pelaaja.lisää_tapahtuma("muddy shoes")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} sticks to the paved path, keeping their shoes clean.")

    jatka_valikkoon(pelaaja)

def tapahtuma_kävely_reitti_koulu(pelaaja: Pelaaja):
    if "late" in pelaaja.tapahtumat:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school late. The first lesson has already started.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school.")

    return näytä_yhteenveto(pelaaja)

## pyöräily

def reitti_pyörä1(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} opens the bicycle's lock and starts pedaling.")
    pelaaja.sijainti = Paikka("on the bicycle path")

def tapahtuma_pyörä_mäki(pelaaja: Pelaaja):
    print(f"\nThere's a steep hill ahead. Does {pelaaja.käyttäjätunnus} pedal hard up the hill or take the longer flat road around? (hill/road)")

    if kysy_valinta("hill", "road") == "hill":
        pelaaja.lisää_tunteet("proud")
        print(f"\n{pelaaja.käyttäjätunnus} pedals hard and makes it up the hill, tired but proud.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} takes the longer road around. It takes a bit more time but is easy.")

    jatka_valikkoon(pelaaja)

def tapahtuma_pyörä_koira(pelaaja: Pelaaja):
    print(f"\nA dog starts chasing {pelaaja.käyttäjätunnus}'s bicycle and barking loudly! Do they pedal faster to escape? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        print(f"\n{pelaaja.käyttäjätunnus} pedals as fast as they can and leaves the dog behind.")
    else:
        pelaaja.lisää_tapahtuma("hurt leg")
        print(f"\n{pelaaja.käyttäjätunnus} slows down and the dog bites their leg then wanders off.")

    jatka_valikkoon(pelaaja)

def tapahtuma_pyörä_kivi(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} sees a big rock on the path ahead! Quick, do they swerve to avoid it? (yes/no)")
    print(f"\n{pelaaja.käyttäjätunnus} only has 7 seconds to answer!")

    while True:
        kivi_kyssäri = ajastettu_input("Enter your choice: ", aikaraja=7)

        if kivi_kyssäri is not None:
            kivi_kyssäri = kivi_kyssäri.strip().lower()

        if kivi_kyssäri == "yes":
            print(f"\n{pelaaja.käyttäjätunnus} swerves just in time and avoids the rock. Phew!")
            jatka_valikkoon(pelaaja)

        elif kivi_kyssäri is None or kivi_kyssäri == "no":
            if kivi_kyssäri is None:
                print(f"\n{pelaaja.käyttäjätunnus} didn't answer in time and hit the rock!")
            else:
                print(f"\n{pelaaja.käyttäjätunnus} hits the rock head-on!")

            print("Their bicycle breaks.")
            print("Their phone also flies out of the backpack and the screen cracks.")
            pelaaja.lisää_tapahtuma("broken bicycle")
            pelaaja.lisää_tapahtuma("broken phone")
            pelaaja.reppu = [esine for esine in pelaaja.reppu if esine.nimi != "phone"]
            pelaaja.sijainti = Paikka(KÄVELYPOLKU)
            jatka_valikkoon(pelaaja)
            tapahtuma_kävely_oikotie(pelaaja)

        else:
            print("Unknown command. Please enter yes or no")

def tapahtuma_pyörä_reitti_koulu(pelaaja: Pelaaja):
    if "broken bicycle" in pelaaja.tapahtumat:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school late, pushing a broken bicycle.")
        print("Their legs are tired from walking the rest of the way.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school on the bicycle right on time!")

    return näytä_yhteenveto(pelaaja)

## bussi

def reitti_bussi1(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} walks towards the bus stop.")
    pelaaja.sijainti = Paikka(BUSSIPYSÄKKI)

def tapahtuma_bussi_myöhässä(pelaaja: Pelaaja):
    print(f"\nThe bus is running 10 minutes late. Does {pelaaja.käyttäjätunnus} keep waiting or start walking instead? (wait/walk)")

    if kysy_valinta("wait", "walk") == "wait":
        print(f"\nThe bus finally arrives and {pelaaja.käyttäjätunnus} hops on.")
        jatka_valikkoon(pelaaja)
    else:
        print(f"\n{pelaaja.käyttäjätunnus} decides not to wait any longer and starts walking towards school instead.")
        pelaaja.sijainti = Paikka(KÄVELYPOLKU)
        jatka_valikkoon(pelaaja)
        tapahtuma_kävely_koira(pelaaja)

def tapahtuma_bussi_lippu(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} steps onto the bus. Do they tap their bus card? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        print(f"\n{pelaaja.käyttäjätunnus} taps their bus card and finds a seat. Nice and easy.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} sneaks past the driver without paying. Risky move...")
        pelaaja.lisää_tunteet("guilty conscience")

    jatka_valikkoon(pelaaja)

def tapahtuma_bussi_penkki(pelaaja: Pelaaja):
    print(f"\nThe bus is crowded. An elderly passenger gets on and there's only one free seat, {pelaaja.käyttäjätunnus}'s."
          "\nDo they give up their seat? (yes/no)")

    if kysy_valinta("yes", "no") == "yes":
        pelaaja.lisää_tapahtuma("gave up seat")
        print(f"\n{pelaaja.käyttäjätunnus} stands up and offers their seat. The passenger thanks them with a warm smile.")
    else:
        pelaaja.lisää_tunteet("awkward")
        print(f"\n{pelaaja.käyttäjätunnus} pretends to be asleep and keeps their seat. A bit awkward.")

    jatka_valikkoon(pelaaja)

def tapahtuma_bussi_pysäkki_ohi(pelaaja: Pelaaja):
    if not any(esine.nimi == "headphones" for esine in pelaaja.reppu):
        return # ilman kuulokkeita ei voi nukahtaa musiikkiin

    print(f"\nThe ride is long and boring. Does {pelaaja.käyttäjätunnus} put on their headphones? (yes/no)")

    if kysy_valinta("yes", "no") == "no":
        print(f"\n{pelaaja.käyttäjätunnus} watches the city go by and gets off at the right stop without any trouble.")
        jatka_valikkoon(pelaaja)
        return

    print(f"\n{pelaaja.käyttäjätunnus} dozes off listening to music and almost misses their stop!"
          "\nDo they jump off quickly or ride to the next stop? (jump/ride)")

    if kysy_valinta("jump", "ride") == "jump":
        print(f"\n{pelaaja.käyttäjätunnus} jumps off just in time, a little dizzy but right where they needed to be.")
        jatka_valikkoon(pelaaja)
    else:
        print(f"\n{pelaaja.käyttäjätunnus} rides to the next stop and has to walk back the rest of the way.")
        pelaaja.lisää_tunteet("tired legs")
        pelaaja.sijainti = Paikka(KÄVELYPOLKU)
        jatka_valikkoon(pelaaja)
        tapahtuma_kävely_oikotie(pelaaja)

def tapahtuma_bussi_reitti_koulu(pelaaja: Pelaaja):
    if "tired legs" in pelaaja.tunteet:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school after walking back from the next stop.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school by bus.")

    return näytä_yhteenveto(pelaaja)

def bussi_kävely_tarkistus(pelaaja: Pelaaja):
    if pelaaja.sijainti.nimi == KÄVELYPOLKU:
        return tapahtuma_kävely_reitti_koulu(pelaaja)
    return False

## auto

def reitti_auto1(pelaaja: Pelaaja):
    print(f"\n{pelaaja.käyttäjätunnus} starts the car and drives towards school.")
    pelaaja.sijainti = Paikka("inside the car on the road")

def tapahtuma_auto_unohdettu(pelaaja: Pelaaja):
    # lounas jäi kotiin: otetaan se pois repusta ennen kysymystä
    pelaaja.reppu = [esine for esine in pelaaja.reppu if esine.nimi != "lunch"]

    print(f"\nHalfway there, {pelaaja.käyttäjätunnus} realizes they forgot their lunch at home!"
          "\nDo they turn back or continue without it? (back/continue)")

    if kysy_valinta("back", "continue") == "back":
        print(f"\n{pelaaja.käyttäjätunnus} turns back to grab their lunch, losing a few minutes but avoiding a hungry afternoon.")
        pelaaja.lisää_reppuun("lunch", 0.5)
    else:
        print(f"\n{pelaaja.käyttäjätunnus} decides to continue without their lunch. Hopefully someone shares with them at school!")
        pelaaja.lisää_tapahtuma("no lunch")

    jatka_valikkoon(pelaaja)

def tapahtuma_auto_liikenne(pelaaja: Pelaaja):
    print(f"\nThere's heavy traffic ahead."
          f"\nDoes {pelaaja.käyttäjätunnus} take the highway (slower but safe) or the back roads (faster but risk of getting lost)? (highway/backroads)")

    if kysy_valinta("highway", "backroads") == "highway":
        print(f"\n{pelaaja.käyttäjätunnus} sits patiently in traffic on the highway. Slow but steady.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} takes the back roads and saves some time, though they did take a wrong turn once.")
        pelaaja.lisää_tapahtuma("wrong turn")

    jatka_valikkoon(pelaaja)

def tapahtuma_auto_pysäköinti(pelaaja: Pelaaja):
    print(f"\nAll the parking spots near school are full."
          f"\nDoes {pelaaja.käyttäjätunnus} park far away and walk, or circle around to wait for a closer spot? (walk/wait)")

    if kysy_valinta("walk", "wait") == "walk":
        print(f"\n{pelaaja.käyttäjätunnus} parks far away and starts walking the rest of the way to school.")
        pelaaja.lisää_tapahtuma("walked from parking")
        pelaaja.sijainti = Paikka(KÄVELYPOLKU)
    else:
        print(f"\n{pelaaja.käyttäjätunnus} circles around and finally finds a spot close to school after a few minutes.")

    jatka_valikkoon(pelaaja)

def tapahtuma_auto_reitti_koulu(pelaaja: Pelaaja):
    if "walked from parking" in pelaaja.tapahtumat:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school on foot after parking far away.")
    else:
        print(f"\n{pelaaja.käyttäjätunnus} arrives at school by car.")

    return näytä_yhteenveto(pelaaja)

## reitit: lista tapahtumista järjestyksessä (tallennus muistaa reitin ja kohdan listassa)

REITIT = {
    "1": [reitti_kävely1, tapahtuma_kävely_roska, tapahtuma_kävely_kyssäri,
          tapahtuma_kävely_ystävä, tapahtuma_kävely_reitti_koulu],

    "2": [reitti_pyörä1, tapahtuma_pyörä_mäki, tapahtuma_pyörä_koira,
          tapahtuma_pyörä_kivi, tapahtuma_pyörä_reitti_koulu],

    "3": [reitti_bussi1, tapahtuma_bussi_myöhässä, bussi_kävely_tarkistus,
          tapahtuma_bussi_lippu, tapahtuma_bussi_penkki, tapahtuma_bussi_pysäkki_ohi,
          tapahtuma_bussi_reitti_koulu],

    "4": [reitti_auto1, tapahtuma_auto_unohdettu, tapahtuma_auto_liikenne,
          tapahtuma_auto_pysäköinti, tapahtuma_auto_reitti_koulu],
}