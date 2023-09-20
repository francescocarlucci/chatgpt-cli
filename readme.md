# ChatGPT from the Command Line

An extra-minimalistic CLI to interact with ChatGPT via OpenAI API.

![ChatGPT CLI](https://github.com/francescocarlucci/chatgpt-cli/blob/main/images/demo.png)

I created this CLI tool because I use ChatGPT a lot in my daily tasks for a variety of purposes including coding, copywriting, brainstorming and "googling". I was looking for a more immediate way to access it, and as I spend lots of time on the CLI, the most usable way for me was to have it built into the CLI itself.

Despite being only 60 lines of code, ChatGPT-CLI allows to:

- interact with ChatGPT with a chat-like experience
- remember conversations using memory
- store conversations locally
- load and continue conversations
- set the temperature of the model
- limit the memory depth to save tokens and contain costs

### Usage

The tool runs as a Python script, so you only need to:

- download the repo
- create the `.secrets` and `history` folders
- install dependencies

```
pip install typer
pip install openai
```

And you are good to invoke it with `python3 app.py`.

For usability, I like to add an alias to my Mac and invoke it with one command:

`echo "alias gptcli='python3 path-to/app.py'" >> ~/.zshrc && source ~/.zshrc`

If you wanna run it as an alias, is a good idea to customize these two environment variables to include the full path of the script.

```
API_KEY_FILE = "path-to/.secrets/openai_key.txt"
HISTORY_PATH = "path-to/history/"
```

### Examples

`python3 app.py` Start a new chat.

`python3 app.py --model=gpt-4` Uses GPT-4 as LLM.

`python3 app.py --model=gpt-4 -ml=4` Uses GPT-4 as LLM and limit the memory to the last 4 messages.

`python3 app.py -t=0.9` Set the temperature to 0.9 (more creative).

`python3 app.py --load=history/marketing_plan.txt` Load an existing conversation into memory.

`python3 app.py --help` to get fresh info about parameters and usage. 

**To save a conversation, type `save` as User prompt.**

To exit, type `exit` as User prompt.

### Development Ideas

- improve the setup process
- save on the same file (when loaded from conversation)
- progress bar for a better experience on long LLM queries

### Contributions

Just fork the repo!

___

By: https://francescocarlucci.com/
