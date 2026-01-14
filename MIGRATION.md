# Guia de Migração e Replicação do Redis

Este documento descreve como clonar instâncias do Redis, configurar replicação e garantir alta disponibilidade para uso com o servidor MCP.

> **Nota:** O `mcp-redis` é um *cliente* que se conecta ao Redis. Para que ele tenha acesso aos mesmos dados em ambientes diferentes (ex: Dev vs Prod), você precisa migrar os dados do banco Redis em si.

## 1. Replicação Master-Replica (Tempo Real)
Ideal para copiar dados de um servidor para outro sem inatividade e manter sincronia.

### Passo a Passo:
1.  **No Servidor de Destino (Réplica):**
    *   Certifique-se que o Redis está rodando e acessível.
    *   Conecte-se via terminal:
        ```bash
        redis-cli -h SEU_IP_DESTINO -p 6379
        ```
    *   Execute o comando para iniciar a réplica:
        ```redis
        REPLICAOF <IP_DO_MASTER> <PORTA_DO_MASTER>
        # Exemplo: REPLICAOF 192.168.1.100 6379
        ```
    *   Se o Master tiver senha, configure-a no destino:
        ```redis
        CONFIG SET masterauth <SENHA_DO_MASTER>
        ```

2.  **Verificar Sincronia:**
    *   Use o comando `INFO replication` para ver o status `master_link_status`. Deve estar `up`.

3.  **Promover a Réplica a Master (Tornar Independente):**
    *   Quando quiser que o novo servidor seja independente (pare de copiar):
        ```redis
        REPLICAOF NO ONE
        ```

---

## 2. Migração via Snapshot RDB (Manual)
Ideal para mover dados "frios" ou fazer backups pontuais (ex: mover do Local para um servidor Cloud VPS).

### Passo a Passo:
1.  **No Servidor de Origem (Master):**
    *   Gere o snapshot dos dados atuais:
        ```bash
        redis-cli bgsave
        ```
    *   Aguarde a finalização. O arquivo `dump.rdb` geralmente fica em `/var/lib/redis/` (Linux) ou no diretório de instalação.

2.  **Transferência:**
    *   Copie o arquivo para o novo servidor:
        ```bash
        scp /var/lib/redis/dump.rdb user@novo-servidor:/var/lib/redis/
        ```

3.  **No Servidor de Destino:**
    *   Pare o serviço Redis:
        ```bash
        sudo systemctl stop redis
        ```
    *   Certifique-se que o arquivo `dump.rdb` tem as permissões corretas (usuário redis):
        ```bash
        chown redis:redis /var/lib/redis/dump.rdb
        ```
    *   Inicie o Redis:
        ```bash
        sudo systemctl start redis
        ```

---

## 3. Redis Cluster (Alta Disponibilidade)
Para ambientes de produção crítica que precisam de distribuição de dados (Sharding). Requer 6 nós no mínimo (3 masters, 3 réplicas).

### Criação Básica:
Use o utilitário do redis-cli:

```bash
redis-cli --cluster create \
  192.168.1.1:6379 \
  192.168.1.2:6379 \
  192.168.1.3:6379 \
  192.168.1.4:6379 \
  192.168.1.5:6379 \
  192.168.1.6:6379 \
  --cluster-replicas 1
```

---

## Como conectar seu `mcp-redis`
Após configurar seu novo servidor Redis, atualize a variável de ambiente no seu projeto (ou na Vercel):

```bash
REDIS_URL=redis://usuario:senha@ip-do-novo-servidor:6379/0
```
