# Configurando Redis na Vercel (Vercel KV / Upstash)

A Vercel é uma plataforma *Serverless*, o que significa que ela não roda servidores persistentes (como um computador ligado 24h). Por isso, **você não instala o Redis diretamente dentro da Vercel**.

Em vez disso, você usa um **banco de dados gerenciado** (como o **Upstash**, que é parceiro oficial da Vercel) e conecta sua aplicação a ele.

## Passo 1: Criar o Banco Redis (Vercel KV / Upstash)

A maneira mais fácil e gratuita é usar o **Vercel KV**:

1.  Acesse seu painel na **Vercel**.
2.  Entre no seu projeto `mcp-redis`.
3.  Vá na aba **Storage**.
4.  Clique em **Create Database** e escolha **Redis (Upstash)**.
5.  Selecione a região (escolha a mesma do seu Function do passo anterior, ex: `us-east-1`).
6.  Clique em **Create**.

## Passo 2: Conectar Automaticamente

Ao criar o banco pela aba Storage, a Vercel define automaticamente as variáveis de ambiente necessárias (`KV_URL`, `KV_REST_API_URL`, etc).

No entanto, este projeto espera uma variável chamada `REDIS_URL`.

1.  Vá na aba **Settings** > **Environment Variables** do seu projeto na Vercel.
2.  Veja o valor da variável `KV_URL` (que foi criada automaticamente).
3.  Crie uma nova variável:
    *   **Key:** `REDIS_URL`
    *   **Value:** (Cole o valor da `KV_URL` aqui).
4.  Salve.

## Passo 3: Testar

Após configurar, a Vercel fará um novo deploy automático (ou você pode forçar um indo em **Deployments** > **Redeploy**).

Acesse a URL do seu projeto (ex: `https://mcp-redis-seu-projeto.vercel.app/`).
Se tudo der certo, você verá uma mensagem confirmando que o servidor está rodando e conectado!

---

## Diferença entre "Hospedar" e "Usar"
*   **Seu Código (MCP Server):** Está na Vercel. É o cérebro.
*   **Seu Banco (Redis):** Está no Upstash (Vercel KV). É a memória.

Você não precisa configurar "Master-Replica" ou "Snapshots" manualmente aqui; o Upstash cuida disso para você na nuvem.
