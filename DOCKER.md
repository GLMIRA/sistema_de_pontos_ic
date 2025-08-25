# 🐳 Sistema de Ponto Acadêmico - Docker

Guia para executar o Sistema de Ponto Acadêmico usando Docker Compose com MySQL e Nginx.

## 📋 Pré-requisitos

- Docker Engine 20.10+
- Docker Compose 2.0+

## 🚀 Instalação e Execução

### 1. Clone o Repositório
```bash
git clone [URL_DO_REPOSITORIO]
cd sistema-ponto-academico
```

### 2. Configure as Variáveis de Ambiente

Crie o arquivo `.env.docker` na raiz do projeto:

```env
# Configurações do Banco de Dados
DB_HOST=db
DB_PORT=3306
DB_NAME=sistema_pontos
DB_USER=pontos_user
DB_PASSWORD=senha_segura_aqui
DB_ROOT_PASSWORD=root_senha_segura

# Configurações do Django
SECRET_KEY=sua_chave_secreta_segura_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Configurações de Produção
ENVIRONMENT=production
```

⚠️ **Importante**: Altere as senhas e chave secreta para valores seguros!

### 3. Execute o Sistema

```bash
# Construir e iniciar todos os serviços
docker compose up -d

# Verificar se os serviços estão rodando
docker compose ps
```

### 4. Primeiro Acesso

O sistema criará automaticamente um usuário administrador:
- **Usuário**: admin
- **Senha**: admin123

Acesse: http://localhost

## 🏗️ Arquitetura dos Containers

### 📊 Serviços

| Serviço | Container | Porta | Descrição |
|---------|-----------|-------|-----------|
| **nginx** | sistema_de_pontos_nginx | 80 | Proxy reverso e arquivos estáticos |
| **web** | sistema_de_pontos_web | 8000 | Aplicação Django |
| **db** | sistema_de_pontos_db | 3306 | Banco MySQL 8.0 |

### 🌐 Rede
- **Network**: `sistema_de_pontos_network`
- **Driver**: bridge
- Comunicação interna entre containers

### 💾 Volumes
- **mysql_data**: Dados do banco MySQL
- **static_volume**: Arquivos estáticos do Django
- **media_volume**: Arquivos de mídia upload

## 📱 Acesso ao Sistema

### Interface Web
```
http://localhost
```

### Admin Django
```
http://localhost/admin/
Usuário: admin
Senha: admin123
```

## 🔧 Comandos Úteis

### Gerenciamento dos Containers
```bash
# Iniciar serviços
docker compose up -d

# Parar serviços
docker compose down

# Ver logs
docker compose logs -f web
docker compose logs -f db
docker compose logs -f nginx

# Status dos serviços
docker compose ps

# Reconstruir containers
docker compose up -d --build
```

### Comandos Django
```bash
# Executar comandos Django
docker compose exec web python nextechlab/manage.py [comando]

# Criar migrações
docker compose exec web python nextechlab/manage.py makemigrations

# Aplicar migrações
docker compose exec web python nextechlab/manage.py migrate

# Criar superusuário
docker compose exec web python nextechlab/manage.py createsuperuser

# Shell Django
docker compose exec web python nextechlab/manage.py shell
```

### Banco de Dados
```bash
# Acessar MySQL
docker compose exec db mysql -u root -p

# Backup do banco
docker compose exec db mysqldump -u root -p sistema_pontos > backup.sql

# Restaurar backup
docker compose exec -T db mysql -u root -p sistema_pontos < backup.sql
```

## 🔍 Monitoramento

### Health Checks
O sistema possui verificações de saúde automáticas:

- **Web**: Verifica endpoint `/admin/login/` a cada 30s
- **Database**: Ping MySQL a cada 10s  
- **Nginx**: Verifica proxy a cada 30s

### Verificar Status
```bash
# Status detalhado dos containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Recursos utilizados
docker stats
```

## 🐛 Solução de Problemas

### Container não inicia
```bash
# Ver logs detalhados
docker compose logs [nome_do_servico]

# Reconstruir container específico
docker compose up -d --build [nome_do_servico]
```

### Erro de conexão com banco
```bash
# Verificar se MySQL está rodando
docker compose exec db mysqladmin ping -u root -p

# Verificar variáveis de ambiente
docker compose exec web env | grep DB_
```

### Problemas com arquivos estáticos
```bash
# Recoletarr arquivos estáticos
docker compose exec web python nextechlab/manage.py collectstatic --noinput

# Verificar volume
docker compose exec web ls -la /app/nextechlab/staticfiles/
```

### Reset completo
```bash
# Parar e remover tudo
docker compose down -v

# Remover imagens
docker compose down --rmi all

# Rebuild completo
docker compose up -d --build
```

## 🔒 Configurações de Rede Local

Para usar apenas na rede local, configure no `.env.docker`:

```env
# Permitir apenas rede local
ALLOWED_HOSTS=192.168.1.*,10.0.0.*,172.16.*,localhost
```

E no docker-compose, mapeie para IP específico:
```yaml
ports:
  - "192.168.1.100:80:80"  # Substitua pelo IP do servidor
```

## 📋 Manutenção

### Backup Automático
```bash
#!/bin/bash
# script-backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db mysqldump -u root -p$DB_ROOT_PASSWORD sistema_pontos > "backup_$DATE.sql"
echo "Backup criado: backup_$DATE.sql"
```

### Limpeza de Logs
```bash
# Limpar logs dos containers
docker compose logs --no-log-prefix > /dev/null

# Limpar volumes não utilizados
docker volume prune
```

## ⚡ Dicas de Performance

- **MySQL**: Buffer pool configurado para 256M
- **Gunicorn**: 2 workers com timeout de 120s
- **Nginx**: Cache de arquivos estáticos
- **Healthchecks**: Monitoramento automático

---

Sistema pronto para produção em rede local! 🎯