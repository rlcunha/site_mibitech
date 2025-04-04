# Tutorial: Criando um Repositório no GitHub e Enviando o Código

Este tutorial explica como criar um repositório no GitHub e enviar o código do projeto MibiTech.

## Pré-requisitos

- Uma conta no GitHub (crie uma em [github.com](https://github.com) se ainda não tiver)
- Git instalado no seu computador
- O projeto MibiTech em seu computador

## Passo 1: Criar um Novo Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login na sua conta.

2. No canto superior direito, clique no ícone "+" e selecione "New repository".

3. Preencha as informações do repositório:
   - **Repository name**: mibitech
   - **Description**: Site da MibiTech com frontend JavaScript e backend Django
   - **Visibility**: Public (ou Private, se preferir)
   - **Initialize this repository with**: Deixe todas as opções desmarcadas

4. Clique em "Create repository".

## Passo 2: Preparar o Projeto Local

1. Abra um terminal ou prompt de comando.

2. Navegue até a pasta do projeto MibiTech:
   ```bash
   cd caminho/para/mibitech
   ```

3. Inicialize o repositório Git (se ainda não estiver inicializado):
   ```bash
   git init
   ```

4. Adicione todos os arquivos ao Git:
   ```bash
   git add .
   ```

5. Faça o commit inicial:
   ```bash
   git commit -m "Commit inicial do projeto MibiTech"
   ```

## Passo 3: Conectar e Enviar para o GitHub

1. Adicione o repositório remoto do GitHub:
   ```bash
   git remote add origin https://github.com/seu-usuario/mibitech.git
   ```
   Substitua `seu-usuario` pelo seu nome de usuário do GitHub.

2. Envie o código para o GitHub:
   ```bash
   git push -u origin main
   ```
   
   Se o seu branch principal for chamado "master" em vez de "main", use:
   ```bash
   git push -u origin master
   ```

3. Digite seu nome de usuário e senha do GitHub quando solicitado.
   
   **Nota**: Se você tiver a autenticação de dois fatores ativada, precisará usar um token de acesso pessoal em vez da senha. Consulte [esta página](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) para saber como criar um.

## Passo 4: Verificar o Repositório

1. Acesse `https://github.com/seu-usuario/mibitech` no seu navegador.

2. Verifique se todos os arquivos foram enviados corretamente.

## Usando o Script de Configuração do Git

Para simplificar o processo, você pode usar o script `git_setup.sh` incluído no projeto:

1. Torne o script executável (Linux/Mac):
   ```bash
   chmod +x git_setup.sh
   ```

2. Execute o script com a URL do seu repositório:
   ```bash
   ./git_setup.sh --all https://github.com/seu-usuario/mibitech.git
   ```

   No Windows, você pode usar:
   ```bash
   bash git_setup.sh --all https://github.com/seu-usuario/mibitech.git
   ```

## Atualizando o Repositório

Depois de fazer alterações no código, você pode enviá-las para o GitHub com os seguintes comandos:

1. Adicione os arquivos alterados:
   ```bash
   git add .
   ```

2. Faça um commit com uma mensagem descritiva:
   ```bash
   git commit -m "Descrição das alterações feitas"
   ```

3. Envie as alterações para o GitHub:
   ```bash
   git push
   ```

## Trabalhando em Equipe

Se outras pessoas estiverem trabalhando no mesmo repositório, é importante manter seu código atualizado:

1. Baixe as alterações mais recentes:
   ```bash
   git pull
   ```

2. Resolva quaisquer conflitos que possam surgir.

3. Continue trabalhando no código.

## Conclusão

Agora você tem o projeto MibiTech armazenado com segurança no GitHub. Isso facilita o controle de versão, a colaboração com outros desenvolvedores e o deploy em servidores.

Para mais informações sobre como implantar o projeto em um servidor VPS, consulte o arquivo `VPS_DEPLOYMENT.md`.