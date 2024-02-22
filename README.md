# lute-gpt-server
A python server to make chatGPT as a dictionary in Lute (language learning software)

Instructions:

Add the lute-gpt-server.py file into the root of your Lute folder (or anywhere else).
Edit the file and add your personal OpenAI API token at the place indicated in code (You may find resources elsewhere about how to obtain the token).
Edit the prompt content and model to your liking.

Run the server with `python lute-gpt-server.py`

Within Lute language settings add a new dictionary with the options Terms and Embedded and the url: `http://localhost:8000/?payload=###` and save.

Now after clicking on a term or dragging over phrase and sentences, an additional tab with the name 'localhost' will be opened with the nicely formatted (hopefully) ChatGPT response.
