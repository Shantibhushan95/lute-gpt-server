import http.server
import socketserver
import urllib.parse
import requests
import json
import sys
import argparse


class CurlRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract payload from the query string
        language=""
        phrase=""
        theme=args.theme
        query_string = urllib.parse.urlparse(self.path).query
        payload = urllib.parse.parse_qs(query_string).get('payload', [None])[0]
        if query_string:
            phrase,language = payload.split('|')

        print(language)
        print(phrase)

        # Determine theme color based on the argument passed
        if theme.lower() == "dark":
            theme_color = "white"
        elif theme.lower() == "light":
            theme_color = "black"
        else:
            theme_color = "red"

        # Construct headers and payload for the curl request
        headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer $OPENAI_API_KEY",  # Replace $OPENAI_API_KEY with the actual API key
        }
        newpayload = {
        "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"You are an experienced {language} language teacher in an English speaking land, explain the prompted {language} word or phrase with apt meanings and added example usages. Treat chinese characters in japanese words as japanese Kanji. Also state other relevant grammatical information if applicable and if it is a conjugation of some word, list all its conjugations. Basically, act like a Dictionary plus Thesaurus. Provide your response as a HTML code containing nice formatting and use {theme_color} as text color. Use the following as outer template: <!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title style=\"color:{theme_color}\">Your page title</title></head><body></body></html>"},
                {"role": "user", "content": phrase}
            ],
        "seed":123,
        "temperature":0
        }

        # Process the payload using curl
        curl_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=newpayload)
        json_response=json.loads(curl_response.text)

        # Send the curl response as HTML text
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json_response["choices"][0]["message"]["content"].encode('utf-8'))



parser = argparse.ArgumentParser()
parser.add_argument("--theme", help="Set the theme for the server")
args = parser.parse_args()



PORT = 8000
httpd = socketserver.TCPServer(("", PORT), CurlRequestHandler)
print(f"Serving at http://localhost:{PORT}")
httpd.serve_forever()
