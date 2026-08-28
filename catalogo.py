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

    # --- normalização dos dados ---
    def _normalizar_rating(
        self,
        rating: int | float | str | None,
    ) -> float | None:
        if rating is None:
            return None

        return float(rating)

    def _achatar_generos(self, generos: str | list) -> list[str]:
        if isinstance(generos, str):
            return [generos]

        generos_achatados = []

        for genero in generos:
            generos_achatados.extend(self._achatar_generos(genero))

        return generos_achatados

    def _normalizar_data(self, data: str) -> str:
        if "/" not in data:
            return data

        dia, mes, ano = data.split("/")
        return f"{ano}-{mes}-{dia}"

    def _normalizar_execucoes(
        self,
        execucoes: int | str | None,
    ) -> int | None:
        if execucoes is None:
            return None

        if isinstance(execucoes, str):
            execucoes = execucoes.replace(",", "")

        return int(execucoes)

    def _somar_duracoes_das_faixas(self, faixas: list[dict]) -> int:
        duracao_total = 0

        for faixa in faixas:
            duracao = faixa.get("duracao_seg")

            if duracao is not None:
                duracao_total += duracao

        return duracao_total

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
