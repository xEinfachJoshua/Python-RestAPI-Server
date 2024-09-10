from http.server import HTTPServer, BaseHTTPRequestHandler
from api import Api
from apihandler import ApiHandler
import json
import logging
import os
from main import Main

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='data/server.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Server(BaseHTTPRequestHandler):
    """
    A class representing a server that handles HTTP requests.
    Attributes:
        api_handler (object): The API handler object.
        httpd (object): The HTTP server object.
    Methods:
        start(api_handler): Starts the server with the specified API handler.
        shutdown(): Shuts down the server.
        HandleRequest(url, apis, method, data=None): Handles the request based on the URL and method.
        do_GET(): Handles GET requests.
        do_POST(): Handles POST requests.
        do_PUT(): Handles PUT requests.
        do_DELETE(): Handles DELETE requests.
    """

    api_handler = None
    httpd = None

    @classmethod
    def start(cls, api_cls):
        """
        Starts the server and serves requests indefinitely.

        Parameters:
        - api_handler: The API handler to be used for processing requests.

        Returns:
        None
        """
        with open("config/config.json", "r") as conf_f:
            conf = json.load(conf_f)
        
        cls.api_config = conf.get("Routing", [])
        cls.server_config = conf.get("Server", {})

        if not isinstance(cls.server_config, dict):
            logging.error("Server configuration is not a dictionary")
            print("Server configuration is not a dictionary. Check logs for details.")
            return

        if "host" not in cls.server_config or "port" not in cls.server_config:
            logging.error("Missing 'host' or 'port' in server configuration")
            print("Missing 'host' or 'port' in server configuration. Check logs for details.")
            return

        for api in cls.api_config:
            try:
                api_cls.register_api(
                    api["API"],
                    api["url"],
                    api["method"],
                    api["auth"],
                    getattr(ApiHandler, api["func"], str(ApiHandler.default))
                )
            except Exception as e:
                logging.error(f"Failed to register API: {e}")
                pass

        cls.api_handler = api_cls
        server_address = (cls.server_config["host"], cls.server_config["port"])
        cls.httpd = HTTPServer(server_address, cls)
        logging.info(f"Server started at {cls.server_config['host']}:{cls.server_config['port']}")
        print(f"Server started at http://{cls.server_config['host']}:{cls.server_config['port']}")
        cls.httpd.serve_forever()

    @classmethod
    def shutdown(cls):
        """
        Shuts down the server.

        This method checks if the server is running and then proceeds to shut it down. It calls the `shutdown()` method of the `httpd` object and prints a message indicating that the server has been stopped.

        Parameters:
            None

        Returns:
            None
        """
        if cls.httpd:
            cls.httpd.shutdown()
            print("Server stopped")
            logging.info("Server stopped")

    @classmethod
    def HandleRequest(cls, url, apis, method, data=None):
        """
        Handles the request based on the URL and method.

        Parameters:
        - url: The requested URL.
        - apis: The list of available APIs.
        - method: The HTTP method of the request.
        - data: The data associated with the request (optional).

        Returns:
        A dictionary containing the error status and the response data.
        """
        error = "404 Not Found"
        url = url.split("?")[0]  # URL without parameters
        for api in apis:
            print(api["url"])
            print(url)
            if api["url"] == url:
                if api["method"] != method:
                    error = "405 Method Not Allowed"
                    continue
                return {"error": False, "data": api["func"](ApiHandler, data)}
        return {"error": True, "data": error}

    def do_GET(self):
        """
        Handles GET requests.
        """
        print("Request received")
        url = self.path
        apis = self.api_handler.get_apis()
        print("apis", apis)
        response = Server.HandleRequest(url, apis, "GET")
        if response["error"]:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response["data"], "utf8"))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response["data"], "utf8"))

    def do_POST(self):
        """
        Handles POST requests.
        """
        url = self.path
        apis = self.api_handler.get_apis()
        response = Server.HandleRequest(url, apis, "POST", self)
        if response["error"]:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response["data"], "utf8"))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(response["data"], "utf8"))

    def do_PUT(self):
        """
        Handles PUT requests.
        """
        pass

    def do_DELETE(self):
        """
        Handles DELETE requests.
        """
        pass


if __name__ == "__main__":
    api = Api()
    
    Server.start(api)