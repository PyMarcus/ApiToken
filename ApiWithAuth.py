import getpass
import json
import time

import requests


class ApiWithAuthorization:
    def __init__(self, login: str, senha: str, url: str) -> None:
        self.__user: str = login
        self.__senha: str = senha
        self.__url: str = url

    def __login(self):
        """faz post das credenciais para logar"""
        payload: dict = {
            "user": self.__user,
            "pass": self.__senha
        }
        time.sleep(0.05)
        print("[*]Logando...")
        session = requests.Session()  # mantém logado
        send_credentials = session.post(self.__url,
                                        json=payload)
        session.headers.update({'authorization': json.loads(send_credentials.content)['token']})
        time.sleep(1)
        print("[*]Login efetuado com sucesso!")
        return json.loads(send_credentials.content), session

    def get(self, url_to_get=""):
        """faz a solicitação ao método get da api , com o token que foi gerado pelo acesso"""
        token = {"token": self.__login()[0]["token"]}
        session = self.__login()[1]
        print("[*]Aguarde...")
        time.sleep(1)
        respond = session.get(url_to_get, headers=token)
        print(respond.content)
        return respond



if __name__ == '__main__':
    try:
        login: str = input("user: ")
        senha = getpass.getpass(prompt="pass: ", stream=None)
        url: str = input("url de login: ")
        time.sleep(1)
        url_to: str = input("url solicitada para get")
    except Exception:
        print("Erro ao inserir os dados!")
    else:
        api = ApiWithAuthorization(login, senha, url)
        api.get(url_to)
