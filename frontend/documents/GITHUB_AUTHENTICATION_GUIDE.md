# Guia de Autenticação do GitHub

O GitHub não aceita mais autenticação por senha desde agosto de 2021. Este guia explica como configurar métodos de autenticação alternativos para trabalhar com repositórios GitHub.

## Opção 1: Usar um Token de Acesso Pessoal (Recomendado)

### Passo 1: Criar um Token de Acesso Pessoal (PAT)

1. Acesse [GitHub.com](https://github.com) e faça login na sua conta.
2. Clique na sua foto de perfil no canto superior direito e selecione **Settings** (Configurações).
3. No menu lateral esquerdo, role para baixo e clique em **Developer settings** (Configurações de desenvolvedor).
4. Clique em **Personal access tokens** (Tokens de acesso pessoal) e depois em **Tokens (classic)**.
5. Clique em **Generate new token** (Gerar novo token) e depois **Generate new token (classic)**.
6. Dê um nome ao seu token em **Note** (Nota), por exemplo "Token para site_mibitech".
7. Selecione um prazo de expiração em **Expiration** (Expiração).
8. Em **Select scopes** (Selecionar escopos), marque a caixa **repo** para acesso completo aos repositórios.
9. Clique em **Generate token** (Gerar token).
10. **IMPORTANTE**: Copie o token gerado e guarde-o em um local seguro. Você não poderá vê-lo novamente!

### Passo 2: Usar o Token para Autenticação

#### Método 1: Armazenar Credenciais

No Windows, você pode usar o Gerenciador de Credenciais:

```bash
git config --global credential.helper wincred
```

Na próxima vez que você fizer um push, use o token como senha (deixe o nome de usuário como está).

#### Método 2: Incluir o Token na URL

Você pode incluir o token diretamente na URL do repositório:

```bash
git remote set-url origin https://USERNAME:TOKEN@github.com/USERNAME/REPOSITORY.git
```

Substitua:
- `USERNAME` pelo seu nome de usuário do GitHub
- `TOKEN` pelo token que você acabou de criar
- `REPOSITORY` pelo nome do repositório (site_mibitech)

Por exemplo:
```bash
git remote set-url origin https://rlcunha:ghp_SuaTokenAqui123456789@github.com/rlcunha/site_mibitech.git
```

### Passo 3: Tentar Novamente o Push

Depois de configurar a autenticação, tente fazer o push novamente:

```bash
git push -u origin main
```

## Opção 2: Configurar Autenticação SSH

### Passo 1: Gerar uma Chave SSH

1. Abra o terminal (Git Bash no Windows).
2. Execute o comando:
   ```bash
   ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
   ```
   Substitua pelo seu email do GitHub.
3. Quando solicitado a "Enter a file in which to save the key", pressione Enter para aceitar o local padrão.
4. Digite uma senha segura quando solicitado (ou pressione Enter para não usar senha).

### Passo 2: Adicionar a Chave SSH ao ssh-agent

1. Inicie o ssh-agent em segundo plano:
   ```bash
   eval "$(ssh-agent -s)"
   ```
2. Adicione sua chave privada ao ssh-agent:
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

### Passo 3: Adicionar a Chave SSH à sua Conta GitHub

1. Copie a chave pública para a área de transferência:
   ```bash
   clip < ~/.ssh/id_ed25519.pub
   ```
   No macOS, use `pbcopy < ~/.ssh/id_ed25519.pub`
   No Linux, use `xclip -sel clip < ~/.ssh/id_ed25519.pub` ou `cat ~/.ssh/id_ed25519.pub` e copie manualmente.

2. Acesse [GitHub.com](https://github.com) e faça login na sua conta.
3. Clique na sua foto de perfil e selecione **Settings** (Configurações).
4. No menu lateral, clique em **SSH and GPG keys** (Chaves SSH e GPG).
5. Clique em **New SSH key** (Nova chave SSH).
6. Dê um título à sua chave, como "Computador Pessoal".
7. Cole a chave no campo "Key".
8. Clique em **Add SSH key** (Adicionar chave SSH).

### Passo 4: Alterar o Repositório para Usar SSH

1. Obtenha a URL SSH do seu repositório no GitHub (botão "Code" > SSH).
2. Altere a URL remota:
   ```bash
   git remote set-url origin git@github.com:rlcunha/site_mibitech.git
   ```

3. Verifique se a alteração foi bem-sucedida:
   ```bash
   git remote -v
   ```

4. Tente fazer o push novamente:
   ```bash
   git push -u origin main
   ```

## Solução de Problemas

### Erro de Autenticação Persistente

Se você continuar enfrentando problemas de autenticação:

1. Verifique se o token ou a chave SSH foram configurados corretamente.
2. Certifique-se de que o token tem as permissões necessárias (escopo "repo").
3. Verifique se o repositório existe e se você tem permissão para fazer push.
4. Tente limpar as credenciais armazenadas:
   ```bash
   git config --global --unset credential.helper
   ```

### Verificar o URL Remoto

Se você não tiver certeza de qual URL remota está configurada:

```bash
git remote -v
```

Isso mostrará os URLs remotos configurados para fetch e push.

## Conclusão

Depois de configurar um desses métodos de autenticação, você poderá fazer push para o GitHub sem problemas. Lembre-se de que os tokens de acesso pessoal devem ser tratados como senhas - mantenha-os seguros e não os compartilhe.

Para mais informações, consulte a [documentação oficial do GitHub sobre autenticação](https://docs.github.com/en/authentication).