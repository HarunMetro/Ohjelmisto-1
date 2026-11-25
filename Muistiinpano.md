## 27.8 Oppitunti

Muista <CTRL + S> kun teet koodei

Kun tallennat nämä koodit githubiin niin nämä komennot
<git add .> tämä lisää kaikki mitä ei ole ollut vielä
<gid commit -m> tämä committaa ja m jälkeen joku järkevä kommentti "" välissä

Aina kun aloitat vs code tee <git pull> tämä on projekteihin muiden kanssa jotta saat niiden muutokset omaan tietokoneesee

sitten jos haluu mitä on tapahtunut niin käyttää
<git log>
ja kattoo et kaikki on ok 
<git status>

<Print("Hei maailma\nHyvää huomenta")>
sitten lopuksi tulee

Hei maailma
Hyvää huomenta

<CTRL + K + C> muutta rivit kommentiksi 
<CTRL + K + U> muuttaa takaisin koodiksi

Jos haluu kaksi rivii yhdes komennos niin laittaa <\n> ensimmäisen viestin jälkeen esim:

Jos haluaa kysymyksen vastauksen paikka olla sen vieressä tee normisti niinku aina mutta jos haluaa että kysymys on ylhäällä vastaus paikka alhaalla niin laita tällee 
<hedelmä = float(input("anna omenan paino kiloina:\n))> 
laita kysymyksen päätyy vain <\n> 

## 3.9 oppitunti

<while> erilaisempi kun <if> 

<if> tarkistaa vain kerran eikä palaa tarkastamaan uusiksi mutta <while> tarkastaa ja suorittaa niin monta kertaa kun ehto on tosi se lopettaa kunnes ei ole tosi. 

esim. 
ikä = int(input("Anna ikäsi: "))
  while ikä < 18:
      print("Olet alaikäinen.")
      ikä = int(input("Anna ikäsi: "))
print("Olet täysi-ikäinen.") 

Tässä kysytään ikää kunnes vastaat 18 tai yli vaikka laittaisit tuhat kertaa esim 12 se silti kysyy uusiksi koska ehto on tosi 12 on pienempi kuin 18 ja jos laitetaan 18 tai ylempi sillo ehto on väärin koska 20 ei ole pienempi kuin 18.

sitten on kaksi muuta komentoa joka voi pysäyttää ne on:

<break> pysäyttää silmuka siitä kohasta missä se on
<exit()> pysäyttää koko ohjelman 

esim kirjoittaa siten jos oot ala ikänen peli sammuisi käyttämällä <exit()> mutta toi on sitten jos haluu koko ohjelman ja mikää muu koodi sen jälkeen ei enää toimis 

sitten on <break> joka pysäyttää sen yhden silmukan ja muut jatkuu sen jälkeen normaalisti esim.

number = 1
while number < 100:
    if number == 7:
        print("Löysin seiskan!")
        break
    number = number + 1

print("Ohjelma jatkuu tästä eteenpäin normaalisti")

tässä numero printataan 99 asti mutta sen voi pysäyttää jos haluu vaikka numero 7 niin se ei printtaa 99 asti vaan vain 7 asti sit se loppuu siihen. 

tässä toinen esimerkki.

password = input("Enter password: ")

while password != "salainen123":
    if password == "peru":
        print("Kirjautuminen peruttu.")
        break
    print("Väärä salasana, yritä uudelleen.")
    password = input("Enter password: ")

print("Ohjelma jatkuu tästä eteenpäin.")

tossa kysytään salasanaa ja se kysyy sitä kunnes laitat oikean salasanan mutta jos olet unohtanut salasanaa niin sanot vaa peru nii sit se silmukka ei enää kysy sulta joten next silmukka tai koodi jatkuu siitä joten <break> antaa way out siitä silmukasta

MOI MAAILMA