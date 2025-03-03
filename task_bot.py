import requests
import re
import time
import hashlib
import base64

BASE_URL = "https://task.zostansecurity.ninja/"

def get_initial_parameters():
    """ Pobiera stronę główną i wyciąga dynamiczne parametry challenge i timestamp """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=2)
        response.raise_for_status()

        match = re.search(r'step=(\d+)&challenge=([a-f0-9]+)&timestamp=(\d+)', response.text)
        if match:
            return {
                "step": match.group(1),
                "challenge": match.group(2),
                "timestamp": match.group(3)
            }
        else:
            print("Nie znaleziono parametrów na stronie głównej!")
            return None

    except requests.exceptions.RequestException as e:
        print("Błąd pobierania strony głównej:", e)
        return None

def extract_parameters(response_text):
    """ Analizuje odpowiedź serwera i pobiera dynamiczne parametry GET lub nagłówki """
    step_match = re.search(r'step=(\d+)', response_text)
    challenge_match = re.search(r'challenge: ([a-f0-9]+)', response_text)
    timestamp_match = re.search(r'timestamp: (\d+)', response_text)

    if step_match:
        return {
            "step": step_match.group(1),
            "challenge": challenge_match.group(1) if challenge_match else None,
            "timestamp": timestamp_match.group(1) if timestamp_match else None,
            "headers_required": challenge_match is not None and timestamp_match is not None
        }
    return None

def calculate_sha256_hash(dictionary):
    """ Konwertuje słownik do formatu key=value&key=value, sortuje alfabetycznie i liczy SHA256 """
    sorted_items = sorted(dictionary.items())  # Sortowanie po kluczach
    formatted_string = "&".join(f"{k}={v}" for k, v in sorted_items)  # Tworzenie stringa
    sha256_hash = hashlib.sha256(formatted_string.encode()).hexdigest()  # Obliczenie SHA256
    return sha256_hash

def send_request(step_data, method="GET", data=None):
    """ Wysyła GET lub POST request do danego kroku """
    params = {"step": step_data["step"]}
    headers = {"User-Agent": "Mozilla/5.0"}

    if step_data.get("headers_required"):
        headers["X-challenge"] = step_data["challenge"]
        headers["X-timestamp"] = step_data["timestamp"]
    elif step_data.get("challenge") and step_data.get("timestamp"):
        params["challenge"] = step_data["challenge"]
        params["timestamp"] = step_data["timestamp"]

    try:
        if method == "POST":
            response = requests.post(BASE_URL, params=params, headers=headers, data=data, timeout=2)
        else:
            response = requests.get(BASE_URL, params=params, headers=headers, timeout=2)

        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia na kroku {step_data['step']}:", e)
        return None

def decode_base64(encoded_text):
    """ Dekoduje Base64 wielokrotnie, aż uzyskamy pełny tekst """
    decoded_text = encoded_text
    rounds = 0

    while True:
        try:
            new_decoded_text = base64.b64decode(decoded_text).decode("utf-8")
            rounds += 1
            decoded_text = new_decoded_text
            print(f"Dekodowanie - runda {rounds}")

            # Sprawdzenie, czy tekst jest w pełni czytelny
            if "Congratulations" in decoded_text or "email" in decoded_text or "@" in decoded_text:
                print(f"\n Pełna wiadomość po {rounds} dekodowaniach:\n{decoded_text}")
                break
        except Exception:
            print(f"\n Ostateczna pełna wiadomość po {rounds} dekodowaniach:\n{decoded_text}")
            break

# Pętla przechodząca przez kolejne etapy
current_step = 1

while True:
    print(f"\nPobieranie parametrów dla kroku {current_step}...")

    if current_step == 1:
        step_data = get_initial_parameters()
    else:
        step_data = extract_parameters(response_text)

    if not step_data:
        print("Nie udało się pobrać danych. Przerywam działanie.")
        break

    print(f" Krok {current_step} - Parametry: {step_data}")

    if current_step == 3:
        # Pobieramy JSON ze słownikiem i obliczamy SHA256
        match_dict = re.search(r'\{(.*?)\}', response_text, re.DOTALL)
        if match_dict:
            dict_content = match_dict.group(1).strip().replace("\n", "")
            dict_items = re.findall(r'"(.*?)": "(.*?)"', dict_content)
            dictionary = {k: v for k, v in dict_items}

            sha256_hash = calculate_sha256_hash(dictionary)
            data = {
                "challenge": step_data["challenge"],
                "timestamp": step_data["timestamp"],
                "hash": sha256_hash
            }
            method = "POST"
        else:
            print("Nie udało się znaleźć słownika w odpowiedzi serwera!")
            break
    else:
        method = "GET"
        data = None

    response_text = send_request(step_data, method, data)

    if response_text:
        print(f"Odpowiedź z serwera (krok {current_step}):\n{response_text}")

        # Automatyczne dekodowanie Base64, jeśli znaleziono zakodowaną wiadomość
        if "encoded with an unknown number of rounds of base64" in response_text:
            match = re.search(r'([A-Za-z0-9+/=]{100,})', response_text)  # Dłuższy ciąg Base64
            if match:
                encoded_message = match.group(1)
                print("\nZnaleziono zakodowaną wiadomość! Rozpoczynam dekodowanie...\n")
                decode_base64(encoded_message)
            break

        if "@" in response_text:
            print("\nZADANIE ZAKOŃCZONE! Otrzymano e-mail do aplikacji \n")
            break

        current_step += 1
        time.sleep(0.5)
    else:
        print(f"Błąd na kroku {current_step}. Przerywam działanie.")
        break
