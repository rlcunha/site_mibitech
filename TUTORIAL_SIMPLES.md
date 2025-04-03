# Tutorial: Como Implantar uma Aplicação Web em uma VPS

Olá! Este tutorial vai te mostrar como colocar uma aplicação web simples em um servidor na internet. Vamos usar algumas ferramentas legais como Docker, Django e Nginx. Não se preocupe se você nunca ouviu falar dessas coisas antes - vamos explicar tudo passo a passo!

## O que você vai precisar

- Uma VPS (Servidor Privado Virtual) rodando Ubuntu 24.04
- Acesso SSH à sua VPS (um nome de usuário e senha ou chave)
- Um domínio apontando para o IP da sua VPS (no nosso caso, appteste.mibitech.com.br)
- Um programa para se conectar ao servidor (como PuTTY no Windows ou Terminal no Mac/Linux)

## Passo 1: Conectar-se à sua VPS

1. Abra seu programa de terminal (PuTTY ou Terminal)
2. Digite o comando para se conectar:
   ```
   ssh seu_usuario@endereco_ip_da_sua_vps
   ```
3. Digite sua senha quando solicitado

## Passo 2: Instalar o Docker

Docker é como uma caixa mágica que guarda todos os programas que precisamos. Vamos instalá-lo:

```bash
# Atualizar a lista de pacotes
sudo apt update

# Instalar pacotes necessários
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Adicionar a chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Adicionar o repositório do Docker
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Atualizar a lista de pacotes novamente
sudo apt update

# Instalar o Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Adicionar seu usuário ao grupo docker para não precisar usar sudo
sudo usermod -aG docker $USER

# Iniciar e habilitar o Docker para iniciar na inicialização
sudo systemctl start docker
sudo systemctl enable docker
```

Agora, saia do servidor e conecte-se novamente para que as alterações de grupo tenham efeito:

```bash
exit
```

Reconecte-se:
```bash
ssh seu_usuario@endereco_ip_da_sua_vps
```

## Passo 3: Inicializar o Docker Swarm

Docker Swarm é como um maestro que coordena vários contêineres Docker:

```bash
docker swarm init
```

## Passo 4: Instalar o Portainer

Portainer é uma interface gráfica que facilita o gerenciamento dos contêineres:

```bash
# Criar a rede que vamos usar
docker network create --driver=overlay --attachable network_public

# Criar um volume para o Portainer
docker volume create portainer_data

# Executar o Portainer
docker run -d -p 9000:9000 --name portainer --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

## Passo 5: Instalar o Traefik

Traefik é como um porteiro que direciona as pessoas para os lugares certos:

```bash
# Criar pasta para o Traefik
mkdir -p /opt/traefik

# Criar arquivo de configuração
cat > /opt/traefik/traefik.yml << EOF
api:
  dashboard: true
  insecure: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    swarmMode: true
    exposedByDefault: false
    network: network_public

certificatesResolvers:
  letsencryptresolver:
    acme:
      email: seu_email@exemplo.com
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web

log:
  level: INFO

accessLog: {}
EOF

# Criar pasta para certificados
mkdir -p /opt/traefik/letsencrypt

# Executar o Traefik
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  --name traefik \
  --network network_public \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /opt/traefik/traefik.yml:/etc/traefik/traefik.yml:ro \
  -v /opt/traefik/letsencrypt:/letsencrypt \
  traefik:v2.10
```

## Passo 6: Baixar e Configurar Nossa Aplicação

Agora vamos baixar a aplicação que criamos:

```bash
# Instalar o Git
sudo apt install -y git

# Criar pasta para o projeto
mkdir -p /opt/apptraefik

# Entrar na pasta
cd /opt/apptraefik

# Clonar o repositório (substitua pelo seu repositório real)
git clone https://github.com/seu-usuario/apptraefik.git .

# Dar permissão de execução ao script de implantação
chmod +x deploy.sh
```

## Passo 7: Implantar a Aplicação

Agora vamos executar o script que faz toda a mágica acontecer:

```bash
# Executar o script de implantação
./deploy.sh
```

## Passo 8: Verificar se Está Funcionando

Vamos verificar se tudo está funcionando corretamente:

```bash
# Verificar os serviços em execução
docker service ls
```

Você deve ver algo parecido com isto:
```
ID             NAME                MODE         REPLICAS   IMAGE                 PORTS
abc123def456   django-app_django   replicated   1/1        django_app:latest     
ghi789jkl012   django-app_nginx    replicated   1/1        nginx_app:latest      
```

## Passo 9: Acessar Sua Aplicação

Abra seu navegador e acesse:
- https://appteste.mibitech.com.br

Você deve ver a mensagem "Hello, World!" com um texto sobre a aplicação Django rodando com Docker Swarm, Traefik e Nginx.

## Solução de Problemas

Se algo não funcionar como esperado, aqui estão algumas dicas:

### Verificar logs dos serviços

```bash
# Ver logs do serviço Django
docker service logs django-app_django

# Ver logs do serviço Nginx
docker service logs django-app_nginx
```

### Verificar se os volumes foram criados corretamente

```bash
docker volume ls
```

### Reiniciar um serviço

```bash
docker service update --force django-app_django
```

## Parabéns!

Você acabou de implantar uma aplicação web em um servidor real! Isso é algo que muitos desenvolvedores profissionais fazem todos os dias. Continue explorando e aprendendo mais sobre desenvolvimento web!

## Próximos Passos

Agora que você tem sua aplicação rodando, que tal:
- Personalizar a mensagem "Hello World"
- Adicionar mais páginas à aplicação Django
- Aprender mais sobre Docker e contêineres
- Explorar o painel do Portainer (http://seu_ip:9000)

Lembre-se: a tecnologia é como um superpoder - quanto mais você aprende, mais coisas incríveis você pode criar!