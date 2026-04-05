"""
🤖 Assistente de Voz - Ana
==========================
Assistente virtual inteligente com ativação por voz.

Arquitetura:
  [ Microfone ] → [ Whisper STT ] → [ ChatGPT NLP ] → [ gTTS TTS ] → [ Alto-falante ]

Modos:
  1. Modo único  - Processa um único comando e encerra.
  2. Modo Alexa  - Loop contínuo com ativação por palavra-chave ("Ana").

Uso:
  python main.py              → Modo Alexa (loop contínuo)
  python main.py --single     → Modo único (um comando)
"""

import sys
import signal

from config import Config
from audio_manager import AudioManager
from ai_engine import AIEngine


class AssistenteAna:
    """Assistente de voz principal com suporte a wake word."""

    def __init__(self):
        self.audio = AudioManager()
        self.ai = AIEngine()
        self._rodando = False

    def _banner(self) -> None:
        """Exibe o banner de inicialização."""
        print()
        print("=" * 50)
        print(f"  🤖 Assistente {Config.ASSISTANT_NAME} - Ativada!")
        print("=" * 50)
        print(f"  📢 Diga \"{Config.WAKE_WORD.capitalize()}\" para começar")
        print(f"  🛑 Diga \"sair\" ou \"desligar\" para encerrar")
        print(f"  🔄 Diga \"resetar\" para limpar o histórico")
        print(f"  ⌨️  Ctrl+C para sair a qualquer momento")
        print("=" * 50)
        print()

    def _detectar_wake_word(self, texto: str) -> bool:
        """Verifica se a wake word está no texto transcrito."""
        return Config.WAKE_WORD in texto.lower()

    def _detectar_saida(self, texto: str) -> bool:
        """Verifica se o usuário quer encerrar."""
        comandos_saida = ["sair", "desligar", "encerrar", "tchau", "até mais"]
        texto_lower = texto.lower()
        return any(cmd in texto_lower for cmd in comandos_saida)

    def _detectar_reset(self, texto: str) -> bool:
        """Verifica se o usuário quer resetar o histórico."""
        return "resetar" in texto.lower() or "limpar histórico" in texto.lower()

    def processar_comando_unico(self) -> None:
        """Executa o fluxo completo uma única vez."""
        print(f"\n🤖 {Config.ASSISTANT_NAME}: Olá! Como posso ajudar?")
        print(f"🎤 Gravando ({Config.COMMAND_DURATION}s)...\n")

        # 1. Gravar
        filepath = self.audio.escutar_comando()
        if not filepath:
            return

        # 2. Transcrever
        print("🧠 Transcrevendo...")
        texto = self.ai.transcrever(filepath)
        if not texto:
            print("⚠️ Não consegui entender. Tente novamente.")
            return
        print(f"📝 Você disse: \"{texto}\"")
        print()

        # 3. Processar com ChatGPT
        print("🤔 Pensando...")
        resposta = self.ai.perguntar(texto)
        print(f"💬 {Config.ASSISTANT_NAME}: {resposta}")
        print()

        # 4. Falar resposta
        print("🔊 Falando...")
        self.audio.falar(resposta)

    def modo_alexa(self) -> None:
        """
        Loop contínuo estilo Alexa.
        Escuta continuamente e ativa quando detecta a wake word.
        """
        self._banner()
        self._rodando = True

        # Saudação inicial
        saudacao = f"Olá! Eu sou a {Config.ASSISTANT_NAME}. Diga meu nome quando precisar de ajuda."
        self.audio.falar(saudacao)

        while self._rodando:
            try:
                # --- Fase 1: Escutar wake word ---
                print(f"👂 Aguardando \"{Config.WAKE_WORD.capitalize()}\"...")
                filepath = self.audio.escutar_wake_word()
                if not filepath:
                    continue

                texto_wake = self.ai.transcrever(filepath)
                if not texto_wake:
                    continue

                # Verifica se a wake word foi detectada
                if not self._detectar_wake_word(texto_wake):
                    continue

                # --- Fase 2: Wake word detectada! ---
                print(f"\n✨ \"{Config.WAKE_WORD.capitalize()}\" detectada!")
                self.audio.falar("Sim? Estou ouvindo.")

                # --- Fase 3: Escutar comando ---
                filepath_cmd = self.audio.escutar_comando()
                if not filepath_cmd:
                    continue

                print("🧠 Transcrevendo comando...")
                texto_cmd = self.ai.transcrever(filepath_cmd)

                if not texto_cmd:
                    self.audio.falar("Não consegui entender. Pode repetir?")
                    continue

                print(f"📝 Comando: \"{texto_cmd}\"")

                # Verificar comandos especiais
                if self._detectar_saida(texto_cmd):
                    self.audio.falar("Até mais! Foi um prazer ajudar.")
                    print(f"\n👋 {Config.ASSISTANT_NAME} desligada. Até a próxima!")
                    self._rodando = False
                    break

                if self._detectar_reset(texto_cmd):
                    self.ai.resetar_historico()
                    self.audio.falar("Histórico limpo! Podemos começar do zero.")
                    continue

                # --- Fase 4: Processar com ChatGPT ---
                print("🤔 Processando...")
                resposta = self.ai.perguntar(texto_cmd)
                print(f"💬 {Config.ASSISTANT_NAME}: {resposta}")

                # --- Fase 5: Falar resposta ---
                self.audio.falar(resposta)
                print()

            except KeyboardInterrupt:
                print(f"\n\n👋 {Config.ASSISTANT_NAME} encerrada pelo usuário.")
                self._rodando = False
                break
            except Exception as e:
                print(f"⚠️ Erro inesperado: {e}")
                print("🔄 Continuando...\n")
                continue

        # Limpar temporários ao sair
        self.audio.limpar_temp()

    def parar(self) -> None:
        """Para o loop do modo Alexa."""
        self._rodando = False


def main():
    """Ponto de entrada principal."""

    # Validar configurações
    if not Config.validate():
        sys.exit(1)

    assistente = AssistenteAna()

    # Handler para Ctrl+C
    def signal_handler(sig, frame):
        print(f"\n\n👋 {Config.ASSISTANT_NAME} encerrada.")
        assistente.parar()
        assistente.audio.limpar_temp()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Verificar modo de execução
    if "--single" in sys.argv or "-s" in sys.argv:
        print("▶️ Modo: Comando Único")
        assistente.processar_comando_unico()
    else:
        print("▶️ Modo: Alexa (Loop Contínuo)")
        assistente.modo_alexa()


if __name__ == "__main__":
    main()
