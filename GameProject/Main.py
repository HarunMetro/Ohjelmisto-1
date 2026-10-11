from Class import *
from Function import *

pelaaja = None

try:
    while True: # yksi kierros = yksi peli
        pelaaja, reitti, vaihe = aloita_tai_jatka() # uusi peli tai tallennettu peli

        if reitti is None: # uusi peli: intro, alkuvalikko ja reitin valinta
            reitti = valitse_reitti(pelaaja)
            vaihe = 0 # uusi matka alkaa reitin ensimmäisestä tapahtumasta
        else: # tallennettu peli: "Welcome back" näkyy hetken ja jatketaan
            odota_enter()
            tyhjennä_ruutu()

        pelaaja.matka_alkanut = True
        peli_ohi = False

        while not peli_ohi: # käydään reitin tapahtumat läpi yksi kerrallaan
            tallenna_peli(pelaaja, reitti, vaihe)           # tallennus jokaisen tapahtuman alussa
            peli_ohi = REITIT[reitti][vaihe](pelaaja)       # suoritetaan tapahtuma (loppu palauttaa True)
            vaihe += 1

            if reitti == "1" and pelaaja.sijainti.nimi == BUSSIPYSÄKKI: # kävelijä vaihtoi bussiin
                reitti = "3"
                vaihe = 1 # jatketaan bussireitin toisesta tapahtumasta (bussipysäkille on jo kävelty)

        pelaaja.matka_alkanut = False # matka on ohi, tallennusta ei enää ole

        if kysy_valinta("yes", "no", kehote="\nPlay again? (yes/no): ") == "no":
            break

        tyhjennä_ruutu()

    print(f"\nThanks for playing, {pelaaja.käyttäjätunnus}! Have a great day at school!")

except (KeyboardInterrupt, EOFError): # Ctrl+C tai syöte loppui: peli sulkeutuu siististi
    print("\n\nGame closed.")
    if pelaaja is not None and pelaaja.matka_alkanut:
        print("Your progress was saved at the start of the last event. Use the same username to continue.")