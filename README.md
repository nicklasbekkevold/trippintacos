# TrippinTacos

Dette prosjektet er en reservasjonsside for restauranten TrippinTacos. Prosjektet gjør det mulig for gjester å reservere bord ved restauranten, ansatte å reservere
walk-ins og innringere og restauranteier å se statistikk over restauranten.

# Motivasjon

Restauranten TrippinTacos opplevde stor pågang av innringere som ville reservere bord og ønsket en
reservasjonsside for gjester, samt mulighet for ansatte å reservere for de. De ønsket også oversikt over statistikk over restauranten.


# Build Status

[![pipeline status](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-29/badges/master/pipeline.svg)](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-29/commits/master)

Her ses statusen på vår "pipeline". Denne sier om det siste som ble pushet til master-brancen var suksessfullt eller ikke. Hvis alt er i orden, er det automatisk
lagt ut på [TrippinTacos hjemmeside](https://trippintacos.herokuapp.com/ "TrippinTacos hjemmeside").

# Kodestil

Variabelnavn skal være beskrivende og skrives på engelsk. Disse skal også skrives med små bokstaver og ord som er sammensatt skal skilles med understrek ("_").
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
  3. ```pip3 install -r requirements.txt ```

# API Referanser

  * [Django Dokumentasjon](https://docs.djangoproject.com/en/2.1/ "Django dokumentasjon")
  * [Bootstrap Dokumentasjon](https://getbootstrap.com/docs/4.3/getting-started/introduction/ "Bootstrap dokumentasjon")

# Tester

For å kjøre testene våre, åpne terminal/cmd og naviger inn i mappen gruppe-29. Skriv deretter inn disse tre kommandoene:
```shell
python3 manage.py test reservations
```
```shell
python3 manage.py test employee/tests
```
```shell
python3 manage.py test guest/tests
```

# Hvordan bruke?

For å sette opp prosjektet følg innstallasjon over. Åpne terminal/cmd og naviger inn i gruppe-29. Kjør kommandoen:  
```shell
python3 manage.py runserver
```
Åpne deretter nettleseren din og gå til "localhost:8000". 

# Bidra
Måten en kan bidra til prosjektet er ved å sende forslag til endringer og forbedringer til *trippintacosrestaurant@gmail.com*

# Credits

Hvis dere har noen dere har fulgt spesielt for å gjøre noe spesifikt imot dette prosjektet kan dere legge inn navnet deres her, og en liten beskrivelse?

### Hjelp til Heroku og CI/CD

  * Vemund Santi
  * Kristian Flatheim Jensen