import http.server
import socketserver
import urllib.parse
import requests
import json

class CurlRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract payload from the query string
        query_string = urllib.parse.urlparse(self.path).query
        if query_string:
            payload = urllib.parse.parse_qs(query_string).get('payload', [None])[0]
        else:
            payload = None

        # Construct headers and payload for the curl request
        headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer $OPENAI_API_KEY",  # Replace $OPENAI_API_KEY with the actual API key
        }
        newpayload = {
        "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a language teacher, explain the prompted word or phrase with apt contextual or standalone meanings and added examples and usages. Also state whether which figure of speech it is and if it is a conjugation of some word. List all its conjugations. Provide your response as a nicely formatted HTML code with emphases and utf-8 support."},
                {"role": "user", "content": payload}
            ]
        }

        # Process the payload using curl
        curl_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=newpayload)
        json_response=json.loads(curl_response.text)

        # Send the curl response as HTML text
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json_response["choices"][0]["message"]["content"].encode('utf-8'))


PORT = 8000
httpd = socketserver.TCPServer(("", PORT), CurlRequestHandler)
print(f"Serving at http://localhost:{PORT}")
httpd.serve_forever()
