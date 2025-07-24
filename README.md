[![Pylint](https://github.com/cmagnobarbosa/prosaAI/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/cmagnobarbosa/prosaAI/actions/workflows/pylint.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b4ab63e63ae540c4b68e7640d16e3773)](https://app.codacy.com/gh/cmagnobarbosa/prosaAI/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
# ProsaAI

ProsaAI é um gerador de temas de redações para o ENEM que utiliza inteligência artificial e notícias atuais em formato RSS para inspirar estudantes com temas relevantes e contemporâneos.

Você está pronto para a próxima Prosa?

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Tokens) para proteger os endpoints. 

### Início Rápido

1. **Configure a chave secreta**:
   ```bash
   export SECRET_KEY="sua-chave-secreta-forte"
   ```

2. **Faça login para obter token**:
   ```bash
   curl -X POST "http://localhost:8000/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=admin123"
   ```

3. **Use o token para acessar endpoints protegidos**:
   ```bash
   curl -X GET "http://localhost:8000/gerar_tema" \
        -H "Authorization: Bearer SEU_TOKEN_AQUI"
   ```

### Credenciais Padrão
- **Username**: `admin`
- **Password**: `admin123`

📚 **Documentação completa**: [JWT Authentication Guide](docs/jwt-authentication.md)

## 🚀 Instalação e Execução

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure variáveis de ambiente**:
   ```bash
   export SECRET_KEY="sua-chave-secreta-forte"
   export PROVIDER1_API_KEY="sua-chave-openai"
   # ... outras configurações opcionais
   ```

3. **Inicie o servidor**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Acesse a documentação interativa**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Arquitetura

Definição de fontes de noticias (RSS) -> Geração de Resumo de diversas fontes -> Geração de tema do dia -> Agente de Checagem de Tema -> disponibilização

## Valores

- Desenvolver uma solução de código aberto para auxiliar na preparação para o ENEM.
- Gerar um impacto social positivo na educação
- Ser um espaço para experimentação e aprendizado rápido 

## Contribuição

Contribuir para o ProsaAI é simples e incentivado! Sinta-se à vontade para fazer um fork do projeto, explorar o código e propor melhorias ou novas funcionalidades. Sugestões e contribuições de qualquer tipo são bem-vindas, sejam elas relacionadas a desenvolvimento, documentação ou novas ideias para funcionalidades.

