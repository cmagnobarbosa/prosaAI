# Autenticação JWT - ProsaAI API

## Visão Geral

A ProsaAI API implementa autenticação baseada em JWT (JSON Web Tokens) para proteger os endpoints da aplicação. Esta documentação descreve como usar a autenticação para acessar os recursos protegidos da API.

## Configuração

### Variáveis de Ambiente

Antes de iniciar o servidor, configure as seguintes variáveis de ambiente:

```bash
# Obrigatória: Chave secreta para assinar os tokens JWT
export SECRET_KEY="sua-chave-secreta-aqui-altere-em-producao"

# Opcionais: Configurações dos provedores de LLM
export PROVIDER1="openai"
export PROVIDER1_API_KEY="sua-chave-openai"
export MODEL1="gpt-3.5-turbo"
export PROVIDER2="openai"
export PROVIDER2_API_KEY="sua-chave-openai"
export MODEL2="gpt-3.5-turbo"
```

**⚠️ Importante**: Em produção, use uma chave secreta forte e única. A chave padrão é apenas para desenvolvimento.

## Endpoints

### 1. Login - Obter Token JWT

**POST** `/login`

Endpoint para autenticar usuário e obter token JWT.

#### Parâmetros (form-data)

| Campo    | Tipo   | Obrigatório | Descrição        |
|----------|--------|-------------|------------------|
| username | string | Sim         | Nome do usuário  |
| password | string | Sim         | Senha do usuário |

#### Credenciais Padrão

Para demonstração, use as seguintes credenciais:
- **Username**: `admin`
- **Password**: `admin123`

#### Exemplo de Requisição

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

#### Resposta de Sucesso (200)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Resposta de Erro (401)

```json
{
  "detail": "Nome de usuário ou senha incorretos"
}
```

### 2. Gerar Tema - Endpoint Protegido

**GET** `/gerar_tema`

Gera um tema de redação baseado em notícias recentes. **Requer autenticação JWT**.

#### Headers

| Header        | Valor                          |
|---------------|--------------------------------|
| Authorization | `Bearer {seu_access_token}`    |

#### Exemplo de Requisição

```bash
# Primeiro, obtenha o token
TOKEN=$(curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123" | jq -r '.access_token')

# Depois, use o token para acessar o endpoint protegido
curl -X GET "http://localhost:8000/gerar_tema" \
     -H "Authorization: Bearer $TOKEN"
```

#### Resposta de Sucesso (200)

```json
{
  "tema": "Tema gerado baseado em notícias recentes",
  "contexto": "Contexto do tema...",
  "fonte": "URLs das notícias utilizadas"
}
```

#### Resposta de Erro - Token Inválido (401)

```json
{
  "detail": "Token de autorização inválido"
}
```

#### Resposta de Erro - Token Ausente (403)

```json
{
  "detail": "Not authenticated"
}
```

## Especificações do Token JWT

### Configurações

- **Algoritmo**: HS256
- **Tempo de Expiração**: 30 minutos (padrão)
- **Campo Subject**: Nome do usuário autenticado

### Estrutura do Payload

```json
{
  "sub": "admin",
  "exp": 1640995200
}
```

### Validação

O token JWT é validado a cada requisição para endpoints protegidos. A validação verifica:

1. **Assinatura**: Token assinado com a chave secreta correta
2. **Expiração**: Token não expirado
3. **Formato**: Payload contém campos obrigatórios
4. **Usuário**: Usuário existe no sistema

## Tratamento de Erros

### Códigos de Status HTTP

| Código | Descrição                    | Quando Ocorre                           |
|--------|------------------------------|----------------------------------------|
| 200    | Sucesso                      | Login realizado com sucesso           |
| 401    | Não autorizado              | Credenciais inválidas ou token inválido |
| 403    | Proibido                    | Token ausente                          |
| 422    | Erro de validação           | Parâmetros de entrada inválidos        |

### Mensagens de Erro Comuns

| Erro                                      | Causa                               | Solução                                    |
|-------------------------------------------|-------------------------------------|--------------------------------------------|
| "Nome de usuário ou senha incorretos"    | Credenciais inválidas              | Verificar username e password             |
| "Token de autorização inválido"          | Token expirado ou malformado       | Fazer login novamente                     |
| "Not authenticated"                       | Header Authorization ausente       | Incluir header com token válido           |

## Exemplos de Uso

### Python com requests

```python
import requests

# 1. Login
login_data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post("http://localhost:8000/login", data=login_data)
token = response.json()["access_token"]

# 2. Usar token para acessar endpoint protegido
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get("http://localhost:8000/gerar_tema", headers=headers)
tema = response.json()
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

async function exemploJWT() {
  try {
    // 1. Login
    const loginResponse = await axios.post('http://localhost:8000/login', 
      'username=admin&password=admin123',
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    
    const token = loginResponse.data.access_token;
    
    // 2. Usar token
    const temaResponse = await axios.get('http://localhost:8000/gerar_tema', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    console.log(temaResponse.data);
    
  } catch (error) {
    console.error('Erro:', error.response?.data || error.message);
  }
}
```

## Segurança

### Boas Práticas

1. **Chave Secreta**: Use uma chave secreta forte e única em produção
2. **HTTPS**: Sempre use HTTPS em produção para proteger tokens em trânsito
3. **Armazenamento**: Armazene tokens de forma segura no cliente
4. **Expiração**: Tokens expiram em 30 minutos por padrão
5. **Renovação**: Implemente lógica para renovar tokens expirados

### Limitações

- **Usuário Único**: Atualmente suporta apenas um usuário demonstrativo
- **Armazenamento**: Credenciais hardcoded (em produção, usar banco de dados)
- **Revogação**: Tokens não podem ser revogados antes da expiração

## Iniciando o Servidor

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variável de ambiente obrigatória
export SECRET_KEY="sua-chave-secreta-forte"

# Iniciar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Documentação Interativa

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

A documentação interativa permite testar os endpoints diretamente no navegador.