# TrippinTacos

Dette prosjektet er en reservasjonsside for restauranten Trippin Tacos. Prosjektet gjør det mulig for gjester å reservere bord på egenhånd. 
Ansatte kan legge inn både walk-in (gjester som dukker opp uanmeldt) og gjester som ringer for å bestille bord. 
Restauranteier kan se statistikk over restauranten.

# Motivasjon

Restauranten Trippin Tacos opplevde stor pågang av innringere som ville reservere bord og ønsket en
reservasjonsside for gjester, samt mulighet for ansatte å reservere for de. De ønsket også oversikt over statistikk for restauranten.


# Build Status

[![pipeline status](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-29/badges/master/pipeline.svg)](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-29/commits/master)

Her er statusen på vår siste "pipeline". Denne sier om det siste som ble pushet til master-brancen var suksessfullt eller ikke. Hvis alt er i orden, og alle testene bestås, blir siste versjon automatisk
lagt ut på [Trippin Tacos sin hjemmeside](https://trippintacos.herokuapp.com/ "Trippin Tacos sin hjemmeside").

# Kodestil

All kode skal være beskrivende og skrives på engelsk. Variabelnavn skal skrives med små bokstaver og ord som er sammensatt skal skilles med understrek ("_").
Funksjonsnavn derimot skal skrives i camelCase. 

# Screenshots

### Logo
![Logo](https://i.imgur.com/bdMGRYJ.png)

### Reservasjonsside for gjester  
![Reservasjonsside for gjester](https://i.imgur.com/KNc1WS0.png)

### Oversikt over bord og reservasjonsside for ansatte
![Oversikt over bord og reservasjonsside for ansatte](https://i.imgur.com/BQURYiT.png)

### Statistikk for restauranteier
![Statistikk for restauranteier](https://i.imgur.com/n8MxIya.png)

# Teknologi/rammeverk brukt

**Built with:**
*  Python 3.7
*  Django
*  Bootstrap4
*  MySQL

# Kjernefunksjonalitet

Kjernefunksjonalitet i prosjektet vårt:  

 *  Bordreservasjon for gjester
 *  Bordreservasjon for ansatte
 *  Statistikk for restauranteier


# Kodeeksempel
Her følger et eksempel på hvordan lage en side på nettsiden. I Django henger filer sammen for å vise en side: Views.py, Urls.py og en template.html:

### Views.py
```python
def terms_and_conditions(request):
    return render(request, 'termsandconditions.html')
```
Views.py håndterer GET eller POST requests. Her kan en gjøre mye, som å sjekke om en bruker er logget inn, ta inn informasjon fra et skjema sendt inn fra bruker
og mye mer.  

### Urls.py
```python
urlpatterns = [
    path('', views.guest_page, name='guest'),
    path('ajax/load-available-times/', views.load_available_times, name='ajax_load_available_times'),
    path('deleteme/', views.delete_me, name='deleteme'),
    path('termsandconditions/', views.terms_and_conditions, name='terms_and_conditions')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Urls.py bestemmer hvilken funksjon i views.py som skal kjøres når en skriver noe spesifikt i urlen. Her ser vi når en skriver /termsandconditions, vil terms_and_conditions
funksjonen fra views.py kjøre. Denne returnerer en template som heter "termsandconditions.html":  
### Termsandconditions.html
```html
{% extends 'base.html' %}
{% load static %}

{%  load static %}

{%  block content %}'
  <div class="container" style="margin-top: 150px">
    <div class = ".container-fluid">
        <div class="card">
            <div class="card-body">

              <h2 class="card-title">Brukervilkår og personvernpolicy:</h2>
                <br>
                <h5 class="card-subtitle mb-2 text-muted"> 1. Behandlingsansvarlig: </h5>
                    Gruppe 29 i Programvareutvikling 2019 er på vegne av Trippin' Tacos behandlingsansvarlig for selskapets behandling av personopplysninger.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 2. Personopplysninger som lagres: </h5>
                    Vi lagrer følgende personopplysninger om våre kunder:
                <b>Navn</b> og <b>e-postadresse</b>. Vi lagrer i tillegg reservasjonene i vår database.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 3. Formål med behandling: </h5>
                    Vi behandler opplysningene for å kunne gjennomføre våre forpliktelser etter avtale med deg som kunde.
                    Vi benytter også opplysningene for å kunne gi deg informasjon og service i forbindelse med din reservasjon via e-post.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 4. Grunnlaget for behandlingen: </h5>
                    Informasjon om navn og e-postadresse benyttes for å oppfylle kjøpsavtalen. Grunnlaget for denne behandlingen er personvernforordningens artikkel Art 6 (b).
                    Der du har samtykket til det benyttes også opplysningene til å gi deg informasjon og service i forbindelse med ditt kjøp via e-post. Grunnlaget for denne behandlingen er personvernforordningen Art 6 (a). Du kan ved å ikke huke av for "påminnelse" unngå å motta slik informasjon fra oss.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 5. Utlevering av opplysninger til tredjeparter: </h5>
                    For å kunne oppfylle våre forpliktelser etter avtalen utleveres nødvendige opplysninger til våre samarbeidspartnere; studentassister i faget TDT4140.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 6. Sletting av personopplysninger: </h5>
                    Opplysninger vi har mottatt i forbindelse med din reservasjon lagres i vårt aktive kunderegister i to (2) år.
                    Opplysninger vi etter bokføringsloven er forpliktet til å bevare vil lagres i inntil fem (5) år, i henhold til lovens krav.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 7. Rettigheter for den registrerte: </h5>
                    Vi behandler dine personopplysninger i henhold til personopplysningsloven og gjeldende forskrifter. Det gjøres oppmerksom på at du kan kreve innsyn i og flytting av egne personopplysninger, samt kreve retting eller sletting av opplysninger.
                    Det kan klages til Datatilsynet på behandling i strid med reglene.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 8. Personvernombud: </h5>
                    Vi har et personvernombud, August Meo, som påser at personopplysningslovens regler om behandling av personopplysninger blir fulgt.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 9. Informasjonssikkerhet </h5>
                    Vi sikrer dine personopplysninger ved passord- og tilgangskontroll, og deler ikke sensitiv informasjon med andre enn bedriften.
                <br> <br>
                <h5 class="card-subtitle mb-2 text-muted"> 10. Kontaktinformasjon </h5>
                    Henvendelser om hvilke opplysninger som er registrert, retting og sletting kan sendes skriftlig til følgende adresse: <br> <br>
                    E-post: augustlonningmeo@gmail.com <br>
                    Trippin' Tacos
            </div>
        </div>
    </div>
  </div>

{% endblock%}
```
HTML i Django er litt annerledes enn "vanlig" HTML. Det er mulig å skrive python i HTML i Django. Dette skrives på følgende måte:  
```html
{{ for i in range(10) }}
    <div>Hei</div>
{{ endfor }}
```
Denne kodesnutten vil lage 10 "div" elementer på html-siden. Som kanskje oppdaget i termsandconditions.html har den ingen <html> eller <body> tags som vanlig. Dette
er på grunn av {% extends 'base.html' %}. Base.html er en template som termsandconditions.html arver fra:  

### Base.html
```html
{% load static %}
{% load auth_extras %}
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="{% static 'css/bootstrap.css' %}">
    <link rel="shortcut icon" href="media/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="{% static 'css/formstyling.css' %}">
    <meta charset="UTF-8">
    {% if title %}
        <title>Trippin' Tacos - {{ title }}</title>
    {% else %}
        <title>Trippin' Tacos</title>
{% endif %}

{% block head %}
{% endblock %}
</head>

<body>
<header class="site-header">
    <nav class="navbar navbar-expand-xl navbar-light bg-warning fixed-top">
        <div class="container">
            <a class="navbar-brand mr-4" href="{% url 'guest' %}">
                <img src="media/favicon.ico" width="40" height="40" class="d-inline-block align-top" alt="">
                Trippin' Tacos
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle"
                    aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarToggle">
                    <div class="navbar-nav mr-auto">
                        <a class="nav-item nav-link" href="{% url 'guest' %}">Hjem</a>
                        <a class="nav-item nav-link" href="{% url 'guest' %}">Meny</a>
                        <a class="nav-item nav-link" href="{% url 'guest' %}">...</a>
                    </div>
                    <!-- Navbar Right Side -->
                    <div class="navbar-nav">
                        {% if user.is_authenticated %}
                            <div class="dropdown">
                              <button class="dropbtn">Ansatt</button>
                              <div class="dropdown-content">
                                  <a class="nav-item nav-link" href="{% url 'employee' %}">Reservasjoner</a>
                                  <a class="nav-item nav-link" href="{% url 'edit' %}">Endre reservasjon</a>
                                  <a class="nav-item nav-link" href="{% url 'editTable' %}">Endre bord</a>
                                  {% if request.user|has_group:"owner" %}
                                        <a class="nav-item nav-link" href="{% url 'statistics' %}">Statistikk</a>
                                  {% endif %}
                                 <b><a class="nav-item nav-link" href="{% url 'logout' %}">Logg ut</a></b>
                              </div>
                            </div>
                        {% else %}
                            <i><a class="nav-item nav-link" href="{% url 'login' %}">Ansatt</a></i>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </nav>
</header>
<main role="main">
    {% block content %}
    {% endblock %}
</main>
</body>

</html>
```
Alle templates som arver fra base.html vil ha all denne koden. For å lage egen kode i andre templates, skrives det inne i {% block content %} {% endblock %} blokker.
Hvis en ser i base.html ser en disse blokkene. Koden en da skriver i andre templates vil havne inne i denne. 

# Innstallasjon

For å innstallere prosjektet, åpne terminal/cmd og skriv følgende (gitt at git og python er installert):
  1. ``` git clone https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-29.git ```
  2. ```cd gruppe-29 ```
  3. ```pip install -r requirements.txt ```

Vi bruker NTNU sine MySQL-servere som lokal database. For å bruke denne må du lage en fil ved navn *local_settings.py*, med følgene innhold:
```
import os
from .settings import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'stud_pu-29_trippinTacos',
        'USER': 'stud_pu-29',
        'PASSWORD': 'GruppE29',
        'HOST': 'mysql.stud.ntnu.no',
        'PORT': '3306',
    },
}

DEBUG = True
```
Denne må legges i gruppe-29/trippinTacos, dette vil overskrive databaseinstillingene i settings.py lokalt, men ikke på Herouk-siden.
I tillegg kreves det tilkobling til NTNU-sitt nettverk: enten ved å være tilkoblet på campus eller ved å følge [denne linken](https://innsida.ntnu.no/wiki/-/wiki/Norsk/Installere+VPN) for instruskjoner på hvordan å sette opp VPN.

# API Referanser

Vi buker Heroku sitt API for automatisk opplasting av kode fra GitLab til Trippin Tacos sin hjemmeside. 
Denne er lagret som en variabel ved navn HEROKU_API_KEY og er lagret i CI/CD instillingene til GitLab. Denne brukes bare i .gitlab-ci.yml-filen og bør holdes hemmelig. 

Nyttige lenker til Django og Bootstrap sin dokumentasjon:
  * [Django Dokumentasjon](https://docs.djangoproject.com/en/2.1/ "Django dokumentasjon")
  * [Bootstrap Dokumentasjon](https://getbootstrap.com/docs/4.3/getting-started/introduction/ "Bootstrap dokumentasjon")

# Tester

For å kjøre testene våre, åpne terminal/cmd og naviger inn i mappen gruppe-29. Skriv deretter kommandoen:
```shell
python manage.py test
```
For å bare kjøre testene til én app:
```shell
python manage.py test employee
```
*Dette vil kjøre alle testene som ligger i tests-mappen eller tests.py filen til den valgte app-en.*

# Hvordan bruke?

For å sette opp prosjektet følg innstallasjon over. Åpne terminal/cmd og naviger inn i gruppe-29. Kjør kommandoen:  
```shell
python manage.py runserver
```
Åpne deretter nettleseren din og gå til [localhost:8000](http://localhost:8000/ "localhost:8000"). 

# Bidra
Måten en kan bidra til prosjektet er ved å sende forslag til endringer og forbedringer til *trippintacosrestaurant@gmail.com*

# Credits

### Hjelp med Heroku
Stor takk til
  * Vemund Santi
  * Kristian Flatheim Jensen

for å bruke både tid og energi på oppsett av Heroku-siden 