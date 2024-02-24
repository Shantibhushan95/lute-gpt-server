# lute-gpt-server
A python server to make ChatGPT as a dictionary in Lute (language learning software)

Disclaimer: OpenAI API has a free tier, but will require paid access for greater limit usage. (Tier 1 requires USD $5)

Instructions:

Add the lute-gpt-server.py file into the root of your Lute folder (or anywhere else).

Edit the file and add your personal OpenAI API token at the place indicated in code (You may find resources elsewhere about how to obtain the token).

Edit the prompt content and ChatGPT model to your liking BUT keep the last part about HTML formatting as it is (unless you know what you are doing).

Open a new terminal/cmd tab.

First install dependencies with `pip install -r requirements.txt`

Then run the server with `python lute-gpt-server.py --theme light` 

Themes `light` and `dark` just reverse the text color.

Within Lute language settings add a new dictionary with the options Terms and Embedded and the url: `http://localhost:8000/?payload=###|language` and save.
For example for German `http://localhost:8000/?payload=###|german`

Now after clicking on a term or dragging over phrase and sentences, an additional tab with the name 'localhost' will be opened with the nicely formatted (hopefully) ChatGPT response.

<img width="1868" alt="Screenshot 2024-02-22 at 19 42 20" src="https://github.com/Shantibhushan95/lute-gpt-server/assets/16492795/2c8af6e2-6397-48a5-ba49-a96d7f986b31">
<img width="1868" alt="Screenshot 2024-02-22 at 20 50 05" src="https://github.com/Shantibhushan95/lute-gpt-server/assets/16492795/d93dc7f7-65f0-44f5-8347-f192f3181802">
