import http.server
import socketserver
import urllib.parse
import requests
import json

class CurlRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract payload from the query string
        language=""
        query_string = urllib.parse.urlparse(self.path).query
        if query_string:
            payloads = query_string.split('|')
            print(payloads[0])
            language = urllib.parse.parse_qs(payloads[1]).get('payload', [None])[0]
            payload = urllib.parse.parse_qs(payloads[0]).get('payload', [None])[0]
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
                {"role": "system", "content": f"You are an experienced {language} language teacher in an English speaking land, explain the prompted {language} word or phrase with apt meanings and added example usages. Treat chinese characters in japanese words as japanese Kanji. Also state other relevant grammatical information if applicable and if it is a conjugation of some word, list all its conjugations. Provide your response as a nicely formatted HTML code with emphases, utf-8 support and the text color should respect the time of day for GMT (white for night, dark-grey for day) with no background color. I stress again, do not forget utf-8 support."},
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
