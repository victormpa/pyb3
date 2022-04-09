from email.policy import default
import click
import json
import os
import zipfile


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CURR_DIR = os.getcwd()
CONF_DIR = os.path.join(os.path.expanduser('~'), '.pyb3')
CRED_PATH = os.path.join(CONF_DIR, 'credentials.json')


@click.group()
def cli():

    pass


@cli.command()
@click.option('--path', type=click.Path(), default=None, help='Load config from this path. Must be a zip file.')
@click.option('--show', is_flag=True, default=False, help='Show configuration and exit.')
def config(path, show):
    """
    Load the configuration from the auth bundle.
    """

    # List the configuration, path is not passed
    if show:

        with open(CRED_PATH, 'r') as file:

            print(file.read())

        return

    # Creates the configuration dir and file
    os.makedirs(CONF_DIR, exist_ok=True)

    config = {
        'ssl': {
            'cer': None,
            'key': None,
        },
        'client_id': None,
        'secret': None,
    }

    # Reads the zip file
    filepath = os.path.abspath(os.path.join(CURR_DIR, path))

    with zipfile.ZipFile(filepath, 'r') as zip:

        for file in zip.filelist:

            filename = file.filename

            # SSL Certificate
            if filename.endswith('.cer'):

                config['ssl']['cer'] = zip.read(filename).decode()

            # SSL Key
            elif filename.endswith('.key'):

                config['ssl']['key'] = zip.read(filename).decode()

            # Client ID and Secret
            elif filename.endswith('_client_id_secret.txt'):

                data = zip.read(filename).decode().split('\n')[0:-1]

                for row in data:

                    key, val = row.split(': ')

                    config[key.lower()] = val

            # Opt-in link
            elif filename.endswith('link_autorizacao.txt'):

                config['optin'] = zip.read(filename).decode().split(': ')[1]

    # Writes the config file
    with open(CRED_PATH, 'w+') as file:

        file.write(json.dumps(config, indent=3))


if __name__ == '__main__':

    cli()
