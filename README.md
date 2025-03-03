# Task Bot - Automatyzacja Wyzwania na task.zostansecurity.ninja

## Opis projektu  
Task Bot to skrypt automatyzujący rozwiązanie wyzwania dostępnego na stronie [task.zostansecurity.ninja](https://task.zostansecurity.ninja).  
Bot przechodzi przez kolejne etapy zadania, pobiera dynamiczne parametry, wykonuje odpowiednie zapytania HTTP i finalnie dekoduje zakodowaną wiadomość Base64.  

## Funkcjonalności  
- Pobiera dynamiczne parametry `challenge` i `timestamp` ze strony zadania.  
- Wysyła odpowiednie żądania GET i POST, uwzględniając wymagane nagłówki.  
- Oblicza wartość SHA256 dla przekazanych danych, jeśli jest to wymagane.  
- Automatycznie dekoduje zakodowaną wiadomość Base64, aż do uzyskania pełnej treści.  
- Kończy działanie po otrzymaniu docelowego adresu e-mail.  

## Wymagania  
- Python 3.x  
- Biblioteki: `requests`, `re`, `hashlib`, `base64`, `time`  

Można je zainstalować za pomocą polecenia:  

pip install requests

Uruchomienie

    Sklonuj repozytorium:

git clone https://github.com/[twoja-nazwa-użytkownika]/task.zostansecurity.ninja.git

    Przejdź do katalogu:

cd task.zostansecurity.ninja

    Uruchom skrypt:

python task_bot.py

Działanie skryptu

    Pobiera stronę główną zadania i wyodrębnia dynamiczne parametry.
    Wysyła odpowiednie zapytania do serwera, przechodząc przez kolejne etapy.
    Przetwarza wymagane dane, w tym generowanie SHA256.
    W przypadku otrzymania zakodowanej wiadomości w Base64, automatycznie ją dekoduje do pełnej treści.
    Wyświetla finalną wiadomość, w tym adres e-mail do aplikacji.
    
Licencja
Projekt wykonany na potrzeby zadania task.zostansecurity.ninja.
Kod udostępniany na zasadach MIT License. Można go dowolnie używać i modyfikować.
