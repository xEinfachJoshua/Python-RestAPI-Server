class Api:
   
    
   
   
    def __init__(self):
        """
        Initializes an instance of the Api class.
        """
        self.__APIs = []
        return

    def register_api(self, API, url, type="GET", auth=False, func="default"):
        """
        Registers an API with the specified details.
        Parameters:
            API (str): The name of the API.
            url (str): The URL of the API.
            type (str, optional): The type of the API request. Defaults to "GET".
            auth (bool, optional): Indicates whether authentication is required. Defaults to False.
            func (str, optional): The name of the function to be called. Defaults to "default".
        """
        print(API, url, type, auth, func)
        self.__APIs.append({"API": API, "func": func, "method": type, "auth": auth, "url": url})
        return

    def get_apis(self):
        """
        Returns the list of registered APIs.
        Returns:
        list: The list of registered APIs.
        """
     
        return self.__APIs