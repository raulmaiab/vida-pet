# Vida Pet

Sistema de terminal em Python para cuidar da vida dos seus pets. Cadastro, histórico de saúde, metas e até um "Tinder" para encontros entre pets, com uma lógica bem criativa, com manipulação de arquivos. Todos os dados ficam salvos em arquivos de texto. Realizado como parte da disciplina de Fundamentos de Programação.

## Funcionalidades

- **Pets**: adicionar, listar, editar e excluir.
- **Eventos**: registrar vacinação, consulta ou remédio de um pet e listar o histórico.
- **Sugestões**: brinquedos e atividades conforme a espécie e a idade do pet.
- **Metas**: criar metas de saúde (únicas ou recorrentes) e marcar quando forem cumpridas.
- **Tinder de Pets**: cria um perfil para o pet, busca pets da mesma espécie e sexo oposto, envia e recebe pedidos de encontro.

## Como rodar

Requisitos: Python 3.6 ou superior. Não precisa instalar nada.

```bash
python main.py
```

Os arquivos de dados são criados automaticamente na primeira execução.

## Menu

```
=== Vida Pet ===
1 - Pets
2 - Eventos
3 - Sugestões
4 - Metas
5 - Tinder de Pets
0 - Sair
```

## Sugestões por espécie

Disponíveis para `cachorro`, `gato` e `hamster`. O texto muda para pets com menos de 1 ano. Outras espécies mostram "Sem sugestões para esta espécie".

## Arquivos de dados

Cada linha é um registro, com campos separados por `|`.

| Arquivo | Campos |
|---|---|
| `pets.txt` | nome, espécie, raça, nascimento (DD/MM/AAAA), peso (kg) |
| `eventos.txt` | nome do pet, tipo, data (DD/MM/AAAA), observações |
| `metas.txt` | nome do pet, descrição, tipo (1 única, 2 recorrente), frequência, vezes cumprida |
| `tinder.txt` | nome, espécie, sexo, descrição |
| `caixapostal_<nome>.txt` | pedidos de encontro recebidos pelo pet |

## Como usar o Tinder de Pets

1. Cadastre o pet em **Pets**.
2. Entre em **Tinder de Pets** e digite o nome do pet.
3. Informe uma descrição e o sexo (Masculino ou Feminino).
4. Escolha uma opção:
   - **Procurar match**: lista pets da mesma espécie e sexo oposto. Escolha um número para enviar o pedido.
   - **Ver meus pedidos**: mostra os pedidos recebidos. Escolha um número para aceitar.

Um pet só aparece para os outros depois de entrar no Tinder pelo menos uma vez.
