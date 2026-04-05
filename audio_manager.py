"""
Módulo de áudio - Captura e reprodução de áudio.
Responsável por gravar do microfone e reproduzir respostas em voz.
"""

import os
import uuid
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from gtts import gTTS
from playsound import playsound

from config import Config


class AudioManager:
    """Gerencia captura e reprodução de áudio."""

    def __init__(self):
        os.makedirs(Config.AUDIO_DIR, exist_ok=True)

    def gravar(self, duracao: int = None, filename: str = None) -> str:
        """
        Grava áudio do microfone.

        Args:
            duracao: Duração da gravação em segundos.
            filename: Nome do arquivo (gerado automaticamente se não fornecido).

        Returns:
            Caminho completo do arquivo gravado.
        """
        if duracao is None:
            duracao = Config.COMMAND_DURATION
        if filename is None:
            filename = f"audio_{uuid.uuid4().hex[:8]}.wav"

        filepath = os.path.join(Config.AUDIO_DIR, filename)

        try:
            audio = sd.rec(
                int(duracao * Config.SAMPLE_RATE),
                samplerate=Config.SAMPLE_RATE,
                channels=1,
                dtype=np.int16
            )
            sd.wait()
            wav.write(filepath, Config.SAMPLE_RATE, audio)
            return filepath
        except Exception as e:
            print(f"❌ Erro ao gravar áudio: {e}")
            return ""

    def falar(self, texto: str) -> None:
        """
        Converte texto em fala e reproduz.

        Args:
            texto: Texto para converter em áudio.
        """
        if not texto:
            return

        filepath = os.path.join(Config.AUDIO_DIR, f"resp_{uuid.uuid4().hex[:8]}.mp3")

        try:
            tts = gTTS(text=texto, lang=Config.TTS_LANG)
            tts.save(filepath)
            playsound(filepath)
        except Exception as e:
            print(f"❌ Erro ao reproduzir áudio: {e}")
        finally:
            # Limpa arquivo temporário
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass

    def escutar_wake_word(self) -> str:
        """
        Grava um trecho curto de áudio para detectar a wake word.

        Returns:
            Caminho do arquivo gravado.
        """
        return self.gravar(
            duracao=Config.LISTEN_DURATION,
            filename="wake_listen.wav"
        )

    def escutar_comando(self) -> str:
        """
        Grava áudio do comando do usuário (duração mais longa).

        Returns:
            Caminho do arquivo gravado.
        """
        print(f"🎤 Escutando seu comando ({Config.COMMAND_DURATION}s)...")
        return self.gravar(
            duracao=Config.COMMAND_DURATION,
            filename="comando.wav"
        )

    def limpar_temp(self) -> None:
        """Remove todos os arquivos temporários de áudio."""
        if os.path.exists(Config.AUDIO_DIR):
            for f in os.listdir(Config.AUDIO_DIR):
                try:
                    os.remove(os.path.join(Config.AUDIO_DIR, f))
                except OSError:
                    pass
