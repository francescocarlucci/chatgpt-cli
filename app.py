import os
import typer
import openai

ENV_VARIABLES_FILE = ".secrets/env_variables.txt"

app = typer.Typer()

def load_env_variables(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            os.environ[key] = value

def set_api_keys():

    if os.path.exists(ENV_VARIABLES_FILE):

        load_env_variables(ENV_VARIABLES_FILE)

    if "OPENAI_API_KEY" not in os.environ:
    
        openai_key = typer.prompt("Enter your OpenAI API key")

        os.environ["OPENAI_API_KEY"] = openai_key

        with open(ENV_VARIABLES_FILE, 'w') as file:

            file.write(f"OPENAI_API_KEY={openai_key}\n")

        typer.echo("OPENAI_API_KEY successfully set!")

set_api_keys()

openai.api_key = os.environ["OPENAI_API_KEY"]

@app.command()
def reset():

    with open(ENV_VARIABLES_FILE, 'w') as file:
        pass

    set_api_keys()

@app.command()
def chat(verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode.")):

    memory = []

    while True:

        user_content = typer.prompt("Enter your query")

        if user_content.lower() == "exit":
            typer.echo("Goodbye!")
            break

        memory.append({"role": "user", "content": user_content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
