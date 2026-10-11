import sys

class Pelaaja:
    def __init__(self, käyttäjätunnus, ikä):
        self.käyttäjätunnus = käyttäjätunnus
        self.ikä = ikä
        self.tunteet = []
        self.tapahtumat = []  # tapahtumat jotka vaikuttavat loppuun (esim. "late", "muddy shoes")
        self.reppu = [
            Esine("phone", 0.15),
            Esine("headphones", 0.05),
            Esine("bus card", 0.01),
            Esine("3 books", 1.2),
            Esine("lunch", 0.5),
            Esine("keys", 0.1),
        ]
        self.sijainti = Paikka("at home on the couch chilling")
        self.matka_alkanut = False

    def lisää_reppuun(self, nimi, paino=0.1):
        uusi_esine = Esine(nimi, paino)
        self.reppu.append(uusi_esine)

    def lisää_tunteet(self, tunne):
        self.tunteet.append(tunne)

    def lisää_tapahtuma(self, tapahtuma):
        self.tapahtumat.append(tapahtuma)

    def reppu_paino(self):
        return round(sum(esine.paino for esine in self.reppu), 2)

    def näytä_reppu(self):
        print("\nYour backpack contains:")
        for esine in self.reppu:
            print(f"- {esine.nimi} ({esine.paino} kg)")
        print(f"\nTotal weight: {self.reppu_paino()} kg")

    def näytä_sijainti(self):
        self.näytä_kartta()
        print(f"\nYou are currently: {self.sijainti.nimi}")

    def näytä_status(self):
        print("\n--- Status ---")
        print(f"Name: {self.käyttäjätunnus}")
        print(f"Age: {self.ikä}")
        print(f"Location: {self.sijainti.nimi}")
        print(f"Backpack: {len(self.reppu)} items ({self.reppu_paino()} kg)")
        if self.tunteet:
            print(f"Feelings: {', '.join(self.tunteet)}")
        else:
            print("Feelings: none yet")

    def näytä_kartta(self):
        kartta = """
    ╔═══════════════════════════════════════════════════════╗
    ║                   [  ROUTE MAP  ]                     ║
    ╠═══════════════════════════════════════════════════════╣
    ║                                                       ║
    ║   Walking   Home ●━━●━━●━━●━━●━━●━━●━━─┐              ║
    ║                                        │              ║
    ║   Bicycle   Home ●━━●━━●━━●━━──────────┤              ║
    ║                                        ├──▶ SCHOOL    ║
    ║   Bus       Home ●━━●━━●━━●━━●━━───────┤              ║
    ║                                        │              ║
    ║   Car       Home ●━━●━━●━━●━━●━━───────┘              ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
        """
        print(kartta)

def kysy_käyttäjätunnus():
    käyttäjätunnus = input("Enter username: ").strip()

    while käyttäjätunnus == "":
        print("Username cannot be empty.")
        käyttäjätunnus = input("Enter username: ").strip()

    return käyttäjätunnus

def luo_pelaaja(käyttäjätunnus):
    while True:
        try:
            käyttäjä_ikä = int(input("Enter age: ").strip())
            break
        except ValueError:
            print("Please enter a number.")


    if käyttäjä_ikä < 12:
        print("You are too young to play this game, thank you and bye bye.")
        sys.exit()
    elif käyttäjä_ikä > 99:
        print("You're too old to play this game, thank you and bye bye.")
        sys.exit()  # peli sammuu

    return Pelaaja(käyttäjätunnus, käyttäjä_ikä)

class Esine:
    def __init__(self, nimi, paino):
        self.nimi = nimi
        self.paino = paino

class Paikka:
    def __init__(self, nimi):
        self.nimi = nimi


