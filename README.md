# 🤖 Assistente de Voz Ana

Assistente virtual inteligente com ativação por voz, construída com Python, OpenAI Whisper, ChatGPT e gTTS.

## 🏗️ Arquitetura

```
[ 🎤 Microfone ]
       ↓
[ 🎵 Captura de Áudio - sounddevice ]
       ↓
[ 🧠 Whisper (Speech-to-Text) ]
       ↓
[ 🤖 ChatGPT (Processamento NLP) ]
       ↓
[ 🔊 gTTS (Text-to-Speech) ]
       ↓
[ 🔈 Saída de Áudio - playsound ]
```

## 📁 Estrutura do Projeto

```
Bradesco_Projetofinal/
├── .env.example      # Template de configuração
├── .env              # Suas configurações (criar a partir do .example)
├── requirements.txt  # Dependências Python
├── config.py         # Configurações centralizadas
├── audio_manager.py  # Captura e reprodução de áudio
├── ai_engine.py      # Integração OpenAI (Whisper + ChatGPT)
├── main.py           # Ponto de entrada principal
└── README.md         # Documentação
```

## 🚀 Instalação

### 1. Ativar o ambiente virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências
```powershell
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```powershell
copy .env.example .env
```
Edite o arquivo `.env` e insira sua chave da API OpenAI:
```
OPENAI_API_KEY=sk-sua-chave-real-aqui
```

## 🎮 Uso

### Modo Alexa (Loop Contínuo) - Padrão
```powershell
python main.py
```
- Diga **"Ana"** para ativar
- Faça sua pergunta
- A assistente responde por voz
- Diga **"sair"** ou **"desligar"** para encerrar
- Diga **"resetar"** para limpar o histórico

### Modo Comando Único
```powershell
python main.py --single
```
- Grava um único comando, processa e encerra

## ⚙️ Configurações Personalizáveis

| Variável | Padrão | Descrição |
|---|---|---|
| `WAKE_WORD` | `ana` | Palavra de ativação |
| `ASSISTANT_NAME` | `Ana` | Nome do assistente |
| `CHAT_MODEL` | `gpt-4o-mini` | Modelo do ChatGPT |
| `LISTEN_DURATION` | `3` | Segundos de escuta para wake word |
| `COMMAND_DURATION` | `7` | Segundos de escuta para comandos |
| `TTS_LANG` | `pt-br` | Idioma da síntese de voz |

## 🛠️ Tecnologias

- **Python 3.11+**
- **OpenAI Whisper** - Transcrição de áudio (Speech-to-Text)
- **ChatGPT (GPT-4o-mini)** - Processamento de linguagem natural
- **gTTS** - Síntese de voz (Text-to-Speech)
- **sounddevice** - Captura de áudio do microfone
- **scipy** - Gravação de arquivos WAV
