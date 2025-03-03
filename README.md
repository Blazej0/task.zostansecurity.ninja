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
```sh
pip install requests
