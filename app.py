import os
import json
import typer
import openai
from typing_extensions import Annotated

API_KEY_FILE = ".secrets/openai_key.txt"
HISTORY_PATH = "history/"

app = typer.Typer()

def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as file:
            api_key = file.read()
            os.environ["OPENAI_API_KEY"] = api_key

def store_api_key(api_key):
    if not os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'w') as file:
            file.write(f"{api_key}")

def load_memory(file):
    if os.path.exists(file):
        with open(file, 'r') as file:
            memory = file.read()
        return json.loads(memory)

load_api_key()

@app.command()
def chat(
    api_key: Annotated[str, typer.Option(envvar="OPENAI_API_KEY", prompt=True)],
    model: Annotated[str, typer.Option("--model")] = "gpt-3.5-turbo",
    memory_limit: Annotated[int, typer.Option("--memory-limit", "-ml")] = 0,
    load: Annotated[str, typer.Option("--load")] = None,
    temperature: Annotated[float, typer.Option("--temp", "-t")] = 0.7
    ):

    store_api_key(api_key)

    openai.api_key = api_key

    memory = []

    if load:
        memory = load_memory(load)

    while True:

        user_content = typer.prompt("User")

        if user_content.lower() == "exit":
            typer.echo("Goodbye!")
            break

        if user_content.lower() == "save":
            file_name = typer.prompt("File name") # TODO sanitize the name
            with open(HISTORY_PATH + file_name + '.txt', 'w') as file:
                file.write(json.dumps(memory))
            continue

        memory.append({"role": "user", "content": user_content})

        completion = openai.ChatCompletion.create(
            model=model,
            messages=memory,
            temperature=temperature
        )

        response = completion.choices[0].message.content

        memory.append({"role": "assistant", "content": response})

        # limit memory size
        if memory_limit > 0:
            memory = memory[-memory_limit:]

        typer.secho(response, fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
