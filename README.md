# lute-gpt-server
A python server to make either ChatGPT or Ai21Studio as a dictionary in Lute (language learning software https://github.com/LuteOrg/lute-v3 ) through their API

Disclaimer: OpenAI API has a free tier, but will require paid access for greater limit usage. (Tier 1 requires USD $5) Refer https://platform.openai.com/docs/guides/rate-limits/usage-tiers 

AI21Studio (https://studio.ai21.com) has 3 months free usage with $90 USD free initial credit and no card requirement.

For OpenAI, First try something in Playground -> Chat to check if everything's working alright.



### Instructions:

- Download the folder.

- Edit the `lute-gpt-server.py` file to add your personal API tokens at the place indicated in code (you may find resources elsewhere about how to obtain the token, and a new token must be created after plan upgrade).

- Edit the prompt content and LLM model to your liking BUT keep the part about HTML formatting as it is (unless you know what you are doing).

- Open a new terminal/cmd tab at the script's location, and run the following:

  - `python -m venv myenv` (only once during install)

  - `source myenv/bin/activate` (every time)

  - `pip install -r requirements.txt` (only once during install)

- Then run the server with `python lute-gpt-server.py --theme light --service openai`

  - For `--service` use either `openai` or `ai21`

  - Themes `light` and `dark` just reverse the text color.

- Within Lute language settings add a new dictionary with the options `Terms` and `Embedded` and the url: `http://localhost:8000/?payload=###|language` and save.
For example for German `http://localhost:8000/?payload=###|german`

- Now after clicking on a term or dragging over phrase and sentences, an additional tab with the name 'localhost' will be opened with the nicely formatted (hopefully) AI response.

<img width="1868" alt="Screenshot 2024-02-22 at 19 42 20" src="https://github.com/Shantibhushan95/lute-gpt-server/assets/16492795/2c8af6e2-6397-48a5-ba49-a96d7f986b31">
<img width="1868" alt="Screenshot 2024-02-22 at 20 50 05" src="https://github.com/Shantibhushan95/lute-gpt-server/assets/16492795/d93dc7f7-65f0-44f5-8347-f192f3181802">
