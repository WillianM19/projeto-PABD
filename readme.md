# Projeto MovieLens 20M - Migração e Visualização de Dados

## Referências ao Dataset Utilizado

O conjunto de dados MovieLens 20M é um recurso abrangente que fornece informações detalhadas sobre a atividade de classificação e marcação de filmes pelos usuários do serviço de recomendação MovieLens. O dataset contém:

- Mais de 20 milhões de classificações.
- Quase meio milhão de tags para mais de 27 mil filmes.
- Dados coletados de janeiro de 1995 a março de 2015.

**Arquivos do Dataset:**
- `ratings.csv`
- `tags.csv`
- `movies.csv`
- `links.csv`
- `genome-scores.csv`
- `genome-tags.csv`


## Detalhes do Projeto

Este projeto tem como objetivo migrar os dados do conjunto MovieLens 20M, através do envio de arquivos csv para o banco de dados. De forma a garantir a integridade e a eficiência das operações, exibindo o tempo de processamento, inserções no banco e possíveis erros.

## Passos Seguidos Durante o Desenvolvimento

1. **Configuração do Ambiente:**
   - Configuração do ambiente de desenvolvimento com Django e ferramentas associadas.
   - Configuração do banco de dados para armazenar os dados do MovieLens.

2. **Migração dos Dados e otimizações:**
   - Criação de fomulário para ler os arquivos CSV e inserir os dados no banco de dados.
   - Otimização de inserção no banco de dados utilizando o bulk_create_list.
   - Uso de filas para processamento assincrono dos arquivos CSV, evitando que o usuário fique travado na página de envio.

3. **Desenvolvimento do frontend:**
   - Página para listagem de dados de filmes cadastrados, com busca e filtros.
   - Página para detalhes de um filme.
   - Página de upload, onde o usuário poderá subir seus arquivos CSV.
   - Página de detalhes de um upload.

## Diagrama Lógico da Persistência dos Dados

O diagrama lógico da persistência dos dados mostra as relações entre as tabelas do banco de dados para armazenar as informações do dataset MovieLens 20M. As principais tabelas e suas relações incluem:

![diagrama-logico](https://github.com/user-attachments/assets/ee41142f-fb86-4de8-a583-c0cf9bb8db30)

## Passos para a Execução

### 1. Clonar o Repositório

Clone o repositório do projeto para o seu ambiente local:

```bash
git clone https://github.com/WillianM19/projeto-PABD
```

### 2. Configurar o Ambiente Virtual

Crie e ative um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv env
source env/bin/activate  # No Windows, use: env\Scripts\activate
```

### 3. Instalar Dependências

Instale as dependências do projeto listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Configurar arquivo .ENV

Renomeie o arquivo ".env-EXAMPLE" para ".env" e insira os dados correspondentes ao banco postgres que será utilizado.

```env
NAME_DB=movielens_db
USER_DB=postgres
PASSWORD_DB=1234
```

### 5. Aplicar Migrações

Crie e aplique as migrações para configurar o banco de dados:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Instale o Redis

Veja mais aqui: https://redis.io/

### 7. Execute o celery

Já foi configurado no projeto um script para a execução do celery, você pode executa-lo assim:
```bash
python manage.py runcelery
```

### 8. Execute o Django

```bash
python manage.py runserver
```
