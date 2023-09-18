import os
import typer
import openai
from typing_extensions import Annotated

API_KEY_FILE = ".secrets/openai_key.txt"

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

load_api_key()

@app.command()
def chat(
    api_key: Annotated[str, typer.Option(envvar="OPENAI_API_KEY", prompt=True)],
    model: Annotated[str, typer.Option("--model")] = "gpt-3.5-turbo"
    ):

    store_api_key(api_key)

    openai.api_key = api_key

    memory = []

    while True:

        user_content = typer.prompt("User")

        if user_content.lower() == "exit":
            typer.echo("Goodbye!")
            break

        memory.append({"role": "user", "content": user_content})

        completion = openai.ChatCompletion.create(
            model=model,
            messages=memory
        )

        response = completion.choices[0].message.content

        memory.append({"role": "assistant", "content": response})

        typer.secho(response, fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
