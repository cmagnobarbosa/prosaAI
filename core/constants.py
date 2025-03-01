"""Constants for the project"""
from decouple import config

NEWS_PATH = "source/rss_source.json"

NUM_NOTICIAS = 3
SIM_THRESHOLD = 0.7

# Provedor mais poderoso
PROVIDER1 = config("PROVIDER1")
PROVIDER1_API_KEY = config("PROVIDER1_API_KEY")
MODEL1 = config("MODEL1")

# Provedor menos poderoso
PROVIDER2 = config("PROVIDER2")
PROVIDER2_API_KEY = config("PROVIDER2_API_KEY")
MODEL2 = config("MODEL2")

GUARDRAIL_MSG = "Tema inapropriado: %s"
# disable linting for the next line
# pylint: disable=line-too-long
temas_enem = {
    1998: "Viver e aprender",
    1999: "Cidadania e participação social",
    2000: "Direitos da criança e do adolescente: como enfrentar esse desafio nacional?",
    2001: "Desenvolvimento e preservação ambiental: como conciliar interesses em conflito?",
    2002: "O direito de votar: como fazer dessa conquista um meio para promover as transformações sociais de que o Brasil necessita?",
    2003: "A violência na sociedade brasileira: como mudar as regras desse jogo?",
    2004: "Como garantir a liberdade de informação e evitar abusos nos meios de comunicação",
    2005: "O trabalho infantil na realidade brasileira",
    2006: "O poder de transformação da leitura",
    2007: "O desafio de se conviver com a diferença",
    2008: "Como preservar a floresta Amazônica",
    2009: "O indivíduo frente à ética nacional",
    2010: "O trabalho na construção da dignidade humana",
    2011: "Viver em rede no século XXI: os limites entre o público e o privado",
    2012: "Movimento imigratório para o Brasil no século 21",
    2013: "Efeitos da implantação da Lei Seca no Brasil",
    2014: "Publicidade infantil em questão no Brasil",
    2015: "A persistência da violência contra a mulher na sociedade brasileira",
    2016: "Caminhos para combater a intolerância religiosa no Brasil",
    2017: "Desafios para a formação educacional de surdos no Brasil",
    2018: "Manipulação do comportamento do usuário pelo controle de dados na internet",
    2019: "Democratização do acesso ao cinema no Brasil",
    2020: "O estigma associado às doenças mentais na sociedade brasileira",
    2021: "Invisibilidade e registro civil: garantia de acesso à cidadania no Brasil",
    2022: "Desafios para a valorização de comunidades e povos tradicionais no Brasil",
    2023: "Desafios do envelhecimento populacional no Brasil",
}

# esses termos são inapropriados para temas de redação
# Essa lista deve ser atualizada conforme a necessidade

# Essa é somente uma lista de exemplo, sendo a primeira camada de proteção
# para temas inapropriados. A segunda camada é a validação por embedding.
# A terceira camada é a validação por um modelo de linguagem mais poderoso.
termos_inapropriados = [
    "impuros",
    "inadequados",
    "morte",
    "linchamento",
    "limpeza étnica",
]
