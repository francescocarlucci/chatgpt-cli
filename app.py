import os
import typer
import openai

ENV_VARIABLES_FILE = ".secrets/env_variables.txt"

app = typer.Typer()

def load_env_variables():
    with open(ENV_VARIABLES_FILE, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            os.environ[key] = value

def load_config():

    if os.path.exists(ENV_VARIABLES_FILE):

        load_env_variables()

    options = [
        {"key": "OPENAI_API_KEY", "required": True},
        {"key": "OPENAI_MODEL", "required": False, "default": "gpt-3.5-turbo"}
    ]

    for option in options:

        key = option["key"]

        if key not in os.environ:

            if option["required"]:

                set_key = typer.prompt(f"{key}")

            else:

                default = option["default"]

                set_key = typer.prompt(f"{key} (Press - for default: {default})")

                if set_key == "-":

                    set_key = default

            os.environ[key] = set_key

            with open(ENV_VARIABLES_FILE, 'a') as file:

                file.write(f"{key}={set_key}\n")

            typer.echo(f"{key} successfully set!")

@app.command()
def config():
    with open(ENV_VARIABLES_FILE, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            typer.echo(f"{key}: {value}")

@app.command()
def reset():
    with open(ENV_VARIABLES_FILE, 'w') as file:
        pass

    load_config()

@app.command()
def chat(verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode.")):

    load_config()

    openai.api_key = os.environ["OPENAI_API_KEY"]

    openai_model = os.environ["OPENAI_MODEL"]

    memory = []

    while True:

        user_content = typer.prompt("User")

        if user_content.lower() == "exit":
            typer.echo("Goodbye!")
            break

        memory.append({"role": "user", "content": user_content})

        completion = openai.ChatCompletion.create(
            model=openai_model,
            messages=memory
        )

        response = completion.choices[0].message.content

        memory.append({"role": "assistant", "content": response})

        # debug memory
        if verbose:
            typer.secho(memory, fg=typer.colors.RED)

        typer.secho(response, fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
