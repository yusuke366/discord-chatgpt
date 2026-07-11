# Discord ChatGPT Bot

Discord上でChatGPTと会話できるボットです。

## 機能

- ChatGPTとの会話
- Slash Commandによる人格切り替え
- 人格定義の外部ファイル化
- チャンネルごとの人格設定
- OpenAI APIエラーのハンドリング
- `.env` によるシークレット管理

---

## 使用技術

- Python 3.12
- discord.py
- OpenAI API
- python-dotenv

---

## ディレクトリ構成

```text
discord-chatgpt/
├── .env
├── chatbot.py
├── personas/
│   ├── assistant.txt
│   ├── engineer.txt
│   └── girl_friend.txt
└── requirements.txt
```

---

## セットアップ

### 仮想環境作成

```bash
python3 -m venv ~/.venv
source ~/.venv/bin/activate
```

### ライブラリインストール

```bash
pip install -U pip
pip install discord.py openai python-dotenv
```

### requirements.txt作成

```bash
pip freeze > requirements.txt
```

---

## Discord Bot作成

### 1. Developer Portal

https://discord.com/developers/applications

でアプリケーションを作成する。

### 2. Bot作成

```text
Bot
↓
Add Bot
```

### 3. Token取得

```text
Bot
↓
Reset Token
```

取得したトークンを控える。

### 4. Message Content Intent有効化

```text
Bot
↓
Privileged Gateway Intents
↓
MESSAGE CONTENT INTENT
```

をONにする。

---

## Bot招待

### OAuth2

```text
OAuth2
↓
URL Generator
```

### Scopes

```text
✅ bot
✅ applications.commands
```

### Bot Permissions

```text
✅ View Channels
✅ Send Messages
✅ Read Message History
✅ Add Reactions
✅ Use Slash Commands
```

生成されたURLをブラウザで開き、サーバーへ招待する。

---

## OpenAI API

### APIキー取得

https://platform.openai.com/api-keys

### 課金設定

https://platform.openai.com/settings/organization/billing

APIはChatGPT Plusとは別契約。

---

## 環境変数

`.env`

```env
DISCORD_TOKEN=xxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

---

## 人格ファイル

### 女友達

`personas/girl_friend.txt`

```text
あなたはDiscordサーバーの女の子の住人です。

特徴:
- 20代前半くらいの自然な女性口調
- タメ口
- 親しみやすい
- 返信は1〜3文程度
- AIであることは普段言わない
```

### アシスタント

`personas/assistant.txt`

```text
あなたは知識が豊富で親切なアシスタントです。
...
```

### ソフトウェアエンジニア

`personas/engineer.txt`

```text
あなたは経験豊富なソフトウェアエンジニアです。
...
```

---

## 起動

```bash
python chatbot.py
```

成功すると

```text
ログイン成功: chatgptbot#XXXX
1 個のコマンドを同期しました
```

と表示される。

---

## Slash Command

### 人格変更

```text
/persona
```

選択可能な人格

- 女友達
- アシスタント
- ソフトウェアエンジニア

人格設定はチャンネルごとに管理される。

例:

```text
#雑談
→ 女友達

#質問
→ アシスタント

#開発
→ ソフトウェアエンジニア
```

---

## systemdによる常駐化

### サービス作成

```bash
sudo vi /etc/systemd/system/chatgptbot.service
```

```ini
[Unit]
Description=Discord ChatGPT Bot
After=network.target

[Service]
User=yusuke
WorkingDirectory=/home/yusuke/git/denki/discord-chatgpt
ExecStart=/home/yusuke/.venv/bin/python3 -m app.chatbot
Restart=always

[Install]
WantedBy=multi-user.target
```

### 起動

```bash
sudo systemctl daemon-reload

sudo systemctl enable chatgptbot

sudo systemctl start chatgptbot
```

### 状態確認

```bash
sudo systemctl status chatgptbot
```

### ログ確認

```bash
journalctl -u chatgptbot -f
```

---

## トラブルシューティング

### API利用枠エラー

```text
openai.RateLimitError
insufficient_quota
```

原因:

- 課金設定未実施
- API残高不足

確認:

```text
Billing
↓
Payment Methods
```

---

### Slash Commandが表示されない

確認事項:

- `applications.commands` スコープで招待済み
- `await bot.tree.sync()` 実行済み
- Discordクライアント再起動済み
- Bot再招待済み

---

## ライセンス

Personal Use
