# Tutorial: Configurando e Enviando o Repositório site_mibitech para o GitHub

Este tutorial explica como configurar o Git para o projeto site_mibitech e enviá-lo para um repositório no GitHub.

## Pré-requisitos

- Uma conta no GitHub (crie uma em [github.com](https://github.com) se ainda não tiver)
- Git instalado no seu computador
- O projeto site_mibitech em seu computador

## Passo 1: Criar um Novo Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login na sua conta.

2. No canto superior direito, clique no ícone "+" e selecione "New repository".

3. Preencha as informações do repositório:
   - **Repository name**: site_mibitech
   - **Description**: Site da MibiTech com frontend JavaScript e backend Django
   - **Visibility**: Public (ou Private, se preferir)
   - **Initialize this repository with**: Deixe todas as opções desmarcadas

4. Clique em "Create repository".

## Passo 2: Configurar o Git no Projeto Local

### Opção 1: Usando o Script Automatizado

O projeto já inclui um script `git_setup.sh` que facilita todo o processo:

1. Abra um terminal e navegue até a pasta do projeto:
   ```bash
   cd caminho/para/site_mibitech
   ```

2. Torne o script executável (Linux/Mac):
   ```bash
   chmod +x git_setup.sh
   ```

3. Execute o script com a URL do seu repositório:
   ```bash
   ./git_setup.sh --all https://github.com/seu-usuario/site_mibitech.git
   ```

   No Windows, você pode usar:
   ```bash
   bash git_setup.sh --all https://github.com/seu-usuario/site_mibitech.git
   ```

   Substitua `seu-usuario` pelo seu nome de usuário do GitHub.

### Opção 2: Configuração Manual

Se preferir configurar manualmente, siga estes passos:

1. Abra um terminal e navegue até a pasta do projeto:
   ```bash
   cd caminho/para/site_mibitech
   ```

2. Inicialize o repositório Git (se ainda não estiver inicializado):
   ```bash
   git init
   ```

3. Adicione todos os arquivos ao Git:
   ```bash
   git add .
   ```

4. Faça o commit inicial:
   ```bash
   git commit -m "Commit inicial do projeto site_mibitech"
   ```

5. Adicione o repositório remoto do GitHub:
   ```bash
   git remote add origin https://github.com/seu-usuario/site_mibitech.git
   ```
   Substitua `seu-usuario` pelo seu nome de usuário do GitHub.

6. Envie o código para o GitHub:
   ```bash
   git push -u origin main
   ```
   
   Se o seu branch principal for chamado "master" em vez de "main", use:
   ```bash
   git push -u origin master
   ```

## Passo 3: Verificar o Repositório

1. Acesse `https://github.com/seu-usuario/site_mibitech` no seu navegador.

2. Verifique se todos os arquivos foram enviados corretamente.

## Configurando o .gitignore

O projeto já deve incluir um arquivo `.gitignore` adequado. Caso precise adicionar mais arquivos ou diretórios para serem ignorados pelo Git, edite o arquivo `.gitignore` e adicione os padrões desejados:

```bash
# Edite o arquivo .gitignore
nano .gitignore

# Adicione os novos padrões, por exemplo:
# logs/
# .env.local
# *.bak

# Depois, adicione e faça commit das alterações
git add .gitignore
git commit -m "Atualiza .gitignore"
git push
```

## Atualizando o Repositório

Depois de fazer alterações no código, você pode enviá-las para o GitHub com os seguintes comandos:

1. Verifique quais arquivos foram modificados:
   ```bash
   git status
   ```

2. Adicione os arquivos alterados:
   ```bash
   git add .
   ```

3. Faça um commit com uma mensagem descritiva:
   ```bash
   git commit -m "Descrição das alterações feitas"
   ```

4. Envie as alterações para o GitHub:
   ```bash
   git push
   ```

## Trabalhando com Branches

Para trabalhar com recursos específicos ou correções, é recomendável usar branches:

1. Crie uma nova branch:
   ```bash
   git checkout -b nome-da-feature
   ```

2. Faça suas alterações, adicione e faça commit normalmente.

3. Envie a branch para o GitHub:
   ```bash
   git push -u origin nome-da-feature
   ```

4. Quando terminar, você pode mesclar a branch com a principal através de um Pull Request no GitHub ou localmente:
   ```bash
   git checkout main
   git merge nome-da-feature
   git push
   ```

## Conclusão

Agora você tem o projeto site_mibitech armazenado com segurança no GitHub. Isso facilita o controle de versão, a colaboração com outros desenvolvedores e o deploy em servidores.

Para informações sobre como implantar o projeto em um servidor VPS, consulte o tutorial `TUTORIAL_VPS_DEPLOYMENT.md`.