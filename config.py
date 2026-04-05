"""
Configurações centralizadas do assistente de voz Ana.
Carrega variáveis de ambiente do arquivo .env
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações do assistente carregadas do .env"""

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    TRANSCRIPTION_MODEL: str = os.getenv("TRANSCRIPTION_MODEL", "gpt-4o-transcribe")

    # Assistente
    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "Ana")
    WAKE_WORD: str = os.getenv("WAKE_WORD", "ana").lower()

    # Áudio
    TTS_LANG: str = os.getenv("TTS_LANG", "pt-br")
    LISTEN_DURATION: int = int(os.getenv("LISTEN_DURATION", "3"))
    COMMAND_DURATION: int = int(os.getenv("COMMAND_DURATION", "7"))
    SAMPLE_RATE: int = int(os.getenv("SAMPLE_RATE", "44100"))

    # Caminhos
    AUDIO_DIR: str = os.path.join(os.path.dirname(__file__), "temp_audio")

    # Prompt do sistema para o ChatGPT
    SYSTEM_PROMPT: str = (
        f"Você é a {ASSISTANT_NAME}, uma assistente virtual inteligente e simpática. "
        "Responda sempre em português do Brasil de forma clara e concisa. "
        "Seja natural e amigável, como se estivesse conversando com um amigo. "
        "Mantenha as respostas curtas para serem faladas em voz alta (máximo 3 frases)."
    )

    @classmethod
    def validate(cls) -> bool:
        """Valida se as configurações essenciais estão preenchidas."""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "sk-sua-chave-aqui":
            print("❌ ERRO: Configure sua OPENAI_API_KEY no arquivo .env")
            print("   Copie o arquivo .env.example para .env e preencha sua chave.")
            return False
        return True
