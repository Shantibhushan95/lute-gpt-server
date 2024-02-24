import http.server
import socketserver
import urllib.parse
import requests
import json
import argparse

class CurlRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            language=""
            phrase=""
            api_key_openai="" # Paste your OpenAI api key within the double quotes
            api_key_ai21="" # Paste your AI21Studio api key within the double quotes
            option=1

            if args.theme and args.theme.lower() == "dark":
                text_color = "white"
            elif args.theme and args.theme.lower() == "light":
                text_color = "black"
            else:
                text_color = "red"  


            if args.service and args.service.lower() == "openai":
                endpoint = "https://api.openai.com/v1/chat/completions"
                api_key=api_key_openai
            elif args.service and args.service.lower() == "ai21":
                endpoint = "https://api.ai21.com/studio/v1/j2-ultra/chat"
                api_key=api_key_ai21
                option=2

            query_string = urllib.parse.urlparse(self.path).query
            payload = urllib.parse.parse_qs(query_string).get('payload', [None])[0]
            if query_string:
                phrase,language = payload.split('|')

            print(language)
            print(phrase)
            print(args.service)
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {api_key}", 
            }


            if option==1:
                newpayload = {
                "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": f"You are an experienced {language} language teacher in an English speaking land, explain the prompted {language} word or phrase with apt meanings and added example usages. Treat chinese characters in japanese words as japanese Kanji. Also state other relevant grammatical information if applicable and if it is a conjugation of some word, list all its conjugations. Basically, act like a Dictionary plus Thesaurus, and make your explanation as verbose as possible. Provide your response as a HTML code containing nice formatting. Use the following as outer template: <!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title style=\"color:{text_color}\">Your page title</title></head><body style=\"color:{text_color}\"></body></html>"},
                        {"role": "user", "content": phrase}
                    ],
                "seed":123,
                "temperature":0.5
                }
            elif option==2:
                newpayload = {
                    "messages":[{ "text": phrase, "role": "user" }],
                    "system": f"you are an experienced {language} language teacher in an English speaking land, explain the prompted {language} word or phrase in a dictionary like manner. Also provide usage examples and conjugations if applicable.",
                    "numResults": 1,
                    "epoch": 0,
                    "maxTokens": 420,
                    "temperature": 0.0,
                    "topP":1,
                    "stopSequences":[]
                }

            curl_response = requests.post(endpoint, headers=headers, json=newpayload)
            json_response=json.loads(curl_response.text)
            # print(json_response)

            if "error" in json_response:
                error_message = json_response["error"]
                response_content = f"Error: {error_message}"
            elif option==1:
                if "choices" in json_response:
                    choices = json_response["choices"]
                    if choices:
                        response_content = choices[0]["message"]["content"]
                    else:
                        response_content = "No content."
                else:
                    response_content = "No content."
            elif option==2:
                outputs = json_response.get('outputs', [])
                if outputs:
                    response_content = outputs[0].get('text', '')

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if option==1:
                self.wfile.write(response_content.encode('utf-8'))
            elif option==2:
                formatted = f"<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title style=\"color:{text_color}\">{phrase}</title></head><body style=\"color:{text_color}\">{plain_text_to_html(response_content)}</body></html>"
                self.wfile.write(formatted.encode('utf-8'))
        except Exception as e:
            print("Exception occurred:", e)
            self.send_error(500, "Internal Server Error")


def plain_text_to_html(plain_text):
    plain_text = plain_text.replace('"', '&quot;')
    paragraphs = plain_text.split('\n\n')
    html_paragraphs = ['<p>{}</p>'.format(paragraph) for paragraph in paragraphs]
    html_body = '\n'.join(html_paragraphs)
    return html_body


parser = argparse.ArgumentParser()
parser.add_argument("--theme", help="Set the theme, black or white")
parser.add_argument("--service", help="Set the service, openai or ai21")
args = parser.parse_args()


PORT = 8000
httpd = socketserver.TCPServer(("", PORT), CurlRequestHandler)
print(f"Serving at http://localhost:{PORT}")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Server shutting down...")
    httpd.shutdown()
