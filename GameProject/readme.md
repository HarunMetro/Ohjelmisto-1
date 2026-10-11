# One Morning, Many Choices

**Tekijä:** Haroon Hashemi
**Kurssi:** Ohjelmointiprojekti 1 (tekstiseikkailupeli)

Komentorivillä pelattava tekstiseikkailupeli, jossa pelaaja valitsee, miten pääsee kouluun (kävely, pyörä, bussi tai auto) ja tekee valintoja matkan varrella. Valinnat vaikuttavat siihen, miten aamu päättyy.

## Pelin idea ja tavoite

On tavallinen koulupäivän aamu ja herätyskello on soinut, aurinko paistaa ja pelaaja makaa vielä kotisohvalla. Tavoitteena on päästä kouluun ja tehdä matkalla mahdollisimman hyviä päätöksiä.

Jokainen reitti sisältää omia yllätyksiä: koira, kivi tiellä, myöhästyvä bussi, unohtunut eväs ja niin edelleen. Perillä koulussa peli näyttää yhteenvedon matkan tapahtumista ja arvioi, oliko aamu täydellinen, hieman ikävä vai täysi sekasorto. Pelin jälkeen voi pelata uudestaan ja kokeilla toista reittiä.

## Kestävä kehitys

Peli käsittelee arkista kysymystä: miten kuljen kouluun? Kestävän kehityksen näkökulma on mukana seuraavasti:

- **Kestävät kulkutavat:** kävely, pyöräily ja bussi ovat täysin toimivia ja hauskoja vaihtoehtoja, ja niitä on kolme neljästä reitistä. Auto on rajattu 18 vuotta täyttäneille, ja sen reitillä pelaaja kohtaa liikenneruuhkan, pysäköintiongelman ja eksymisen riskin.
- **Roskaaminen:** kävelyreitillä pelaaja voi poimia maassa olevan roskan reppuunsa. Teko huomataan ja siitä saa kehun loppuyhteenvedossa.

## Käynnistys

Aja `Main.py` kansiosta `GameProject`:

    python Main.py

## Pelaaminen

1. Anna käyttäjätunnus ja ikä (12-99).
2. Uudessa pelissä näytetään intro, alkuvalikko ja matkustustavan valinta.
3. Valitse reitti numerolla: `1` kävely, `2` pyörä, `3` bussi, `4` auto (vain 18+). Numerot `5` (reppu) ja `6` (sijainti) näyttävät tietoja.
4. Matkan aikana vastataan kirjoittamalla koko sana sulkeissa, esim. `yes/no` tai `hill/road`.
5. Jokaisen tapahtuman jälkeen aukeaa **pieni valikko**:
   - `1` reppu ja sen paino
   - `2` reittikartta ja sijainti
   - `3` status (nimi, ikä, sijainti, reppu, tunteet)
   - `4` tai Enter jatkaa matkaa
6. `quit` sulkee pelin (kysyy varmistuksen kahdesti).

## Reitit

Pelissä on neljä reittiä, ja valinnat vaikuttavat siihen, miten matka päättyy.

- **Kävely:** roska, risteys, ystävät, koira ja oikotie.
- **Pyörä:** mäki, koira ja kivi tiellä (7 sekunnin aikaraja).
- **Bussi:** myöhästyvä bussi, lippu, istumapaikka ja kuulokkeet.
- **Auto (18+):** unohtunut eväs, ruuhka ja parkkipaikka.

### Reitinvaihdot

Joskus reitti vaihtuu kesken matkan:

- **Kävely → bussi:** jos pelaaja luovuttaa risteyksessä.
- **Bussi → kävely:** jos pelaaja ei jaksa odottaa bussia tai ajaa pysäkin ohi.
- **Pyörä → kävely:** jos pelaaja törmää kiveen.

## Toiminnallisuudet

- **Nimi ja ikä:** ikä päättää, saako ajaa autoa.
- **Reppu:** esineillä on paino, ja ne voivat hajota tai jäädä matkalle.
- **Tunteet ja tapahtumat:** peli muistaa valinnat ja kertoo ne lopussa.
- **Tallennus:** peli tallentuu automaattisesti jokaisen tapahtuman alussa tiedostoon `tallennus_<käyttäjätunnus>.txt`. Samalla käyttäjätunnuksella voi jatkaa myöhemmin. Tallennus poistetaan, kun peli on pelattu loppuun.
- **Ajastettu kysymys:** pyöräreitin kivi (7 sekuntia).
- **Virheiden käsittely:** väärät syötteet tai rikkinäinen tallennus eivät kaada peliä. Ctrl+C sulkee pelin siististi.

## Tiedostorakenne

| Tiedosto | Sisältö |
|---|---|
| `Main.py` | Pelin käynnistys ja pääsilmukka |
| `Class.py` | Luokat `Pelaaja`, `Esine` ja `Paikka`, kartta ja pelaajan luonti |
| `Function.py` | Valikot, tallennus, yhteenveto ja kaikkien reittien tapahtumat |
| `Intro.txt` | Pelin tarinateksti |
| `Instructions.txt` | Pelin ohjeet |
| `readme.md` | Tämä tiedosto |

## Oliorakenne

- **`Pelaaja`:** nimi, ikä, reppu, sijainti, tunteet ja tapahtumat. Metodeilla lisätään asioita ja näytetään reppu, sijainti, status ja kartta.
- **`Esine`:** nimi ja paino.
- **`Paikka`:** nimi.