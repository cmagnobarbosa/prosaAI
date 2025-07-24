# Integração Maritaca.AI

Este documento descreve como usar a nova integração com a API Maritaca.ai no sistema ProsaAI.

## Sobre a Maritaca.ai

A Maritaca.ai é uma empresa brasileira que desenvolveu modelos de linguagem especializados em português, incluindo a família de modelos Sabiá. Estes modelos são especialmente adequados para gerar temas de redação do ENEM, pois foram treinados especificamente para o idioma português brasileiro.

## Configuração

### 1. Variáveis de Ambiente

Adicione as seguintes variáveis de ambiente ao seu arquivo `.env`:

```bash
# Maritaca.ai Configuration
MARITACA_API_KEY=sua_chave_api_maritaca_aqui
```

### 2. Provedores Suportados

O sistema agora suporta os seguintes provedores:
- `openai` - Modelos OpenAI (GPT-4, GPT-3.5, etc.)
- `gemini` - Modelos Google Gemini
- `deepseek` - Modelos DeepSeek
- `maritaca` - Modelos Maritaca.ai (Sabiá)

### 3. Modelos Maritaca Disponíveis

- `sabia-2` - Modelo principal da segunda geração
- `sabia-2-small` - Versão menor e mais rápida
- `sabia-2-medium` - Versão média, equilibrio entre qualidade e velocidade

## Uso

### Usando ChatAPI Diretamente

```python
from core.chat_api import ChatAPI

# Criar instância da API
api = ChatAPI('maritaca', 'sabia-2', 'sua-api-key')

# Gerar conteúdo
contexto = "Você é um especialista em temas de redação do ENEM."
prompt = "Gere um tema de redação baseado em educação."

resposta = api.gera_conteudo(contexto, prompt)
print(resposta)
```

### Usando make_llm_call

```python
from core.servico_llm import make_llm_call

# Fazer chamada para o modelo
resposta = make_llm_call(
    provider='maritaca',
    model='sabia-2',
    contexto='Você é um especialista em temas de redação do ENEM.',
    prompt='Gere um tema de redação sobre sustentabilidade.',
    api_key='sua-api-key'
)
```

### Integração com o Pipeline Existente

Para usar Maritaca.ai como provedor principal ou secundário, atualize as variáveis de ambiente:

```bash
# Para usar Maritaca como provedor principal
PROVIDER1=maritaca
PROVIDER1_API_KEY=sua_chave_maritaca
MODEL1=sabia-2

# Para usar Maritaca como provedor secundário  
PROVIDER2=maritaca
PROVIDER2_API_KEY=sua_chave_maritaca
MODEL2=sabia-2-small
```

## Vantagens dos Modelos Maritaca.ai

1. **Especialização em Português**: Modelos treinados especificamente para o português brasileiro
2. **Contexto Cultural**: Melhor compreensão do contexto cultural brasileiro
3. **Temas ENEM**: Particularmente adequados para gerar temas de redação do ENEM
4. **Custo-benefício**: Potencialmente mais econômicos que modelos internacionais

## Formato da API

A API Maritaca.ai utiliza formato compatível com OpenAI:

```json
{
  "model": "sabia-2",
  "messages": [
    {"role": "system", "content": "Contexto do sistema"},
    {"role": "user", "content": "Prompt do usuário"}
  ]
}
```

## Endpoint da API

```
URL: https://chat.maritaca.ai/api/chat/completions
Método: POST
Headers: 
  - Content-Type: application/json
  - Authorization: Bearer {sua-api-key}
```

## Exemplo Completo

Veja o arquivo `example_maritaca.py` para um exemplo completo de uso da integração Maritaca.ai.

## Testes

Execute os testes específicos da integração Maritaca:

```bash
python -m pytest tests/test_chat_api.py::TestChatAPIProviders -v
```

## Suporte e Limitações

- A integração assume compatibilidade com formato OpenAI
- Documentação oficial da API pode estar em https://www.maritaca.ai/
- Em caso de problemas, verifique a chave da API e conectividade
- Os modelos podem ter limites de taxa específicos

## Contribuições

Para melhorar esta integração:
1. Verifique a documentação oficial mais recente da Maritaca.ai
2. Atualize nomes de modelos conforme necessário
3. Ajuste endpoints se a API mudar
4. Adicione testes adicionais conforme necessário