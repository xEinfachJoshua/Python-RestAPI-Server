# Python-RestAPI-Server

## Projektbeschreibung
Dieses Projekt stellt einen einfachen HTTP-Server bereit, der verschiedene API-Endpunkte unterstützt. Die Konfiguration erfolgt über eine zentrale JSON-Datei.

## Voraussetzungen
- Python 3.x

## Installation
1. Klone das Repository:
    ```bash
    git clone <repository-url>
    ```
2. Wechsle in das Projektverzeichnis:
    ```bash
    cd <projektverzeichnis>
    ```
3. Installiere die benötigten Pakete:
    ```bash
    pip install -r requirements.txt
    ```

## Konfiguration
Die Konfiguration des Servers und der API-Endpunkte erfolgt in der Datei `config/config.json`. Beispiel:

```json
{
    "Server": {
        "port": 3000,
        "host": "",
        "path": "/htdocs/"
    },
    "Routing": [
        {
            "API": "senddata",
            "url": "/senddata",
            "method": "POST",
            "auth": false,
            "func": "send_data"
        },
        {
            "API": "home",
            "url": "/",
            "method": "GET",
            "auth": false,
            "func": "home"
        }
    ]
}
```
## Verwendung
1. Starte den Server:
    ```bash
    python main.py
    ```
2. Verwende die Anweisungen im Terminal, um den Server zu starten, zu stoppen, neu zu starten oder den Status zu überprüfen.

## API-Endpunkte
### `POST /senddata`
- **Beschreibung**: Sendet Daten an den Server.
- **Authentifizierung**: Nein
- **Funktion**: `send_data`

### `GET /`
- **Beschreibung**: Liefert die Startseite.
- **Authentifizierung**: Nein
- **Funktion**: `home`

## Eigene API-Endpunkte erstellen
### Route hinzufügen
Öffne die `config.json` und füge unter "Routing" eine neue Route hinzu:
```json
{
    "API": "neue_api",
    "url": "/neue_api",
    "method": "POST",
    "auth": false,
    "func": "neue_funktion"
}
```
### Funktion definieren
Implementiere in `apihandler.py` die Funktion `neue_funktion`, die der neuen API-Route zugeordnet ist:
```python
def neue_funktion(self):
    # Implementierung der API-Logik hier
    pass
```
## Fehlerbehebung
### Häufige Probleme
- **Konfigurationsdatei nicht gefunden**: Stelle sicher, dass die Datei `config/config.json` existiert und korrekt formatiert ist.
- **Server startet nicht**: Überprüfe die Log-Datei `server.log` für detaillierte Fehlermeldungen.
