import requests
import urllib3

from typing import Dict

urllib3.disable_warnings()


class Client:

    def __init__(self, *args, **kwargs):

        pass

    def get_auth_bundle(self, name:str, email:str, document:str) -> Dict[str, str]:
        """
        Send the email containing the auth bundle.

        For more information:
        https://developers.b3.com.br/index.php?option=com_apiportal&view=documentation&id=pacote-de-acesso

        :param name: name to register the credentials
        :param email: email to send the bundle
        :param document: valid CNPJ

        :return: success status
        :rtype: bool
        """

        request = {
            'method': 'POST',
            'url': 'https://apib3i-cert.b3.com.br/api/acesso/autosservico',
            'json': {
                'nome': name,
                'email': email,
                'documento': document,
            },
            'headers': {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            'verify': False,
        }

        response = requests.request(**request)

        response = response.json()

        return response
