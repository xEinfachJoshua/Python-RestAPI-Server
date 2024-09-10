import sys
import logging
from api import Api
import subprocess
import os
import signal
from enum import Enum
import json

# Logging-Konfiguration
logging.basicConfig(filename="data/server.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Command(Enum):
    """
    Enum class representing different commands.

    Attributes:
        START (str): The start command.
        STOP (str): The stop command.
        RESTART (str): The restart command.
        STATUS (str): The status command to check if the server is running.
        EXIT (str): The exit command.
    """
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    STATUS = "status"
    EXIT = "exit"

class Main:
    def __init__(self):
        """
        Initializes an instance of the class.
        """
        self.server_process = None 
        try:
            with open("config/config.json", "r") as config_file:
                config = json.load(config_file)
                self.api_config = config["Routing"]
        except Exception as e:
            logging.error(f"Failed to read config file: {e}")
            print("Failed to read config file. Check logs for details.")

    def start(self):
        """
        Start the server.

        If the server is already running, it prints "Server is already running" and returns.
        Otherwise, it prints "Starting server..." and starts the server process using subprocess.Popen.
        """
        if self.server_process and self.server_process.poll() is None:
            print("Server is already running")
            return
        print("Starting server...")
        try:
            self.server_process = subprocess.Popen(
                ["cmd.exe", "/c", "python", "server.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

            for conf in self.api_config:
                self.api.register_api(conf["API"], conf["url"], conf["type"], conf["auth"], conf["func"]) 
            logging.info("Server started successfully.")
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            print("Failed to start server. Check logs for details.")

    def stop(self):
        """
        Stop the server.

        If the server is not running, it prints "Server is not running" and returns.
        If the server is running, it prints "Stopping server..." and terminates the server process.
        It then waits for the server to stop for a maximum of 5 seconds. If the server does not stop within the timeout,
        it prints "Force killing the server..." and kills the server process.
        Finally, it resets the server process to None.
        """
        if not self.server_process or self.server_process.poll() is not None:
            print("Server is not running")
            return
        print("Stopping server...")
        self.server_process.terminate()
        try:
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force killing the server...")
            self.server_process.kill()
        finally:
            logging.info("Server stopped.")
            self.server_process = None

    def restart(self):
        """
        Restart the server by stopping it and then starting it again.
        """
        print("Restarting server...")
        self.stop()
        self.start()

    def status(self):
        """
        Check the status of the server.

        Prints whether the server is currently running or not.
        """
        if self.server_process and self.server_process.poll() is None:
            print("Server is running.")
        else:
            print("Server is not running.")

def signal_handler(sig, frame):
    """
    Handle termination signals and stop the server gracefully.
    """
    print("Interrupt received, stopping server...")
    main_instance.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Signalbehandlung
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Erstelle eine Instanz der Main-Klasse
    main_instance = Main()

    # Hauptschleife für Benutzereingaben
    try:
        while True:
            command = input("Enter the command (start, stop, restart, status, exit): ").strip().lower()
            if command in Command._value2member_map_:
                if command == Command.START.value:
                    main_instance.start()
                elif command == Command.STOP.value:
                    main_instance.stop()
                elif command == Command.RESTART.value:
                    main_instance.restart()
                elif command == Command.STATUS.value:
                    main_instance.status()
                elif command == Command.EXIT.value:
                    main_instance.stop()
                    break
            else:
                print(f"Unknown command: '{command}'. Valid commands are: start, stop, restart, status, exit.")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, stopping server...")
        main_instance.stop()
        sys.exit(0)