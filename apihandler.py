import json
import cgi
from urllib.parse import parse_qs

class ApiHandler:
    def default(self, cls):
        return "API Handler not found"
    def test(self, cls):
        return "API Handler test"
    def send_data(self, cls):
      
        post_data = cls.rfile.read(int(cls.headers['Content-Length'])).decode("utf-8")
        result = parse_qs(post_data, strict_parsing=True)

        for key in result:
            if len(result[key]) == 1:
                result[key] = result[key][0]
            
        

        
        post_data = json.dumps(post_data, indent=4)

    
        # Write the data to a file
        with open("data.txt", "w") as data_file:
            data_file.write(post_data)

        return "Data written to file"
    def home(self, cls):
        print("Home")
        with open("htdocs/index.html", "r") as index_file:
            return index_file.read()