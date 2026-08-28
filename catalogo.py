"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""

import json
from collections import deque


class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.conteudos_por_id = {
            conteudo["id"]: conteudo
            for conteudo in dados["conteudos"]
        }

        self.usuarios_por_id = {
            usuario["id"]: usuario
            for usuario in dados["usuarios"]
        }

        self.ids_por_nome_de_usuario = {
            usuario["nome"].lower(): usuario["id"]
            for usuario in dados["usuarios"]
        }

        self.fila = deque()

    # --- usuários e playlists ---
    def listar_usuarios(self) -> list[str]:
        nomes = [
            usuario["nome"]
            for usuario in self.usuarios_por_id.values()
        ]
        return sorted(nomes)

    def buscar_usuario_por_nome(self, nome: str) -> str | None:
        return self.ids_por_nome_de_usuario.get(nome.lower())

    def playlist_de(self, usuario_id: str) -> list[str] | None:
        usuario = self.usuarios_por_id.get(usuario_id)

        if usuario is None:
            return None

        return list(usuario["playlist"])

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None:
        playlist = self.playlist_de(usuario_id)

        if playlist is None or not 0 <= posicao < len(playlist):
            return None

        return playlist[posicao]

    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]:
        if not usuario_ids:
            return []

        playlists = []

        for usuario_id in usuario_ids:
            playlist = self.playlist_de(usuario_id)

            if playlist is None:
                return []

            playlists.append(set(playlist))

        conteudos_em_comum = playlists[0]

        for playlist in playlists[1:]:
            conteudos_em_comum.intersection_update(playlist)

        return sorted(conteudos_em_comum)

    # --- dados de um conteúdo ---
    def rating_de(self, conteudo_id: str) -> float | None: ...
    def duracao_total_de(self, conteudo_id: str) -> int | None: ...
    def generos_de(self, conteudo_id: str) -> list[str] | None: ...
    def plataformas_de(self, conteudo_id: str) -> list[str] | None: ...
    def data_adicionado_de(self, conteudo_id: str) -> str | None: ...
    def execucoes_de(self, conteudo_id: str) -> int | None: ...
    def conteudos_do_genero(self, genero: str) -> list[str]: ...

    # --- fila de reprodução ---
    def enfileirar(self, conteudo_id: str) -> bool: ...
    def proximo(self) -> str | None: ...
    def fila_atual(self) -> list[str]: ...
