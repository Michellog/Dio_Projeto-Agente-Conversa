"""
Módulo de IA - Integração com OpenAI (Whisper + ChatGPT).
Responsável por transcrição de áudio e processamento de linguagem natural.
"""

from openai import OpenAI

from config import Config


class AIEngine:
    """Motor de IA usando OpenAI para transcrição e chat."""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.historico: list[dict] = [
            {"role": "system", "content": Config.SYSTEM_PROMPT}
        ]

    def transcrever(self, filepath: str) -> str:
        """
        Transcreve áudio para texto usando Whisper.

        Args:
            filepath: Caminho do arquivo de áudio.

        Returns:
            Texto transcrito ou string vazia em caso de erro.
        """
        try:
            with open(filepath, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=Config.TRANSCRIPTION_MODEL,
                    file=audio_file,
                    language="pt"
                )
            return transcript.text.strip()
        except Exception as e:
            print(f"❌ Erro na transcrição: {e}")
            return ""

    def perguntar(self, texto: str) -> str:
        """
        Envia texto para o ChatGPT e retorna a resposta.
        Mantém histórico da conversa para contexto.

        Args:
            texto: Pergunta ou comando do usuário.

        Returns:
            Resposta do ChatGPT.
        """
        try:
            self.historico.append({"role": "user", "content": texto})

            response = self.client.chat.completions.create(
                model=Config.CHAT_MODEL,
                messages=self.historico,
                max_tokens=300,
                temperature=0.7
            )

            resposta = response.choices[0].message.content.strip()
            self.historico.append({"role": "assistant", "content": resposta})

            # Limita histórico para não exceder tokens (mantém últimas 20 msgs)
            if len(self.historico) > 21:
                self.historico = [self.historico[0]] + self.historico[-20:]

            return resposta
        except Exception as e:
            print(f"❌ Erro no ChatGPT: {e}")
            return "Desculpe, tive um problema ao processar sua pergunta."

    def resetar_historico(self) -> None:
        """Limpa o histórico de conversa, mantendo apenas o system prompt."""
        self.historico = [
            {"role": "system", "content": Config.SYSTEM_PROMPT}
        ]
        print("🔄 Histórico de conversa resetado.")
