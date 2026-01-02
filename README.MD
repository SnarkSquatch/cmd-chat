<div align="center">

# 🤐 CMD-CHAT: The "Ghost" Protocol

### The chat tool your ISP doesn't want you to have.

### Zero Logs. Zero Disk Writes. 100% Deniable.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NSA Approved](https://img.shields.io/badge/NSA-Hates_This-red.svg)](#)

</div>

---

> ⚠️ **WARNING:** This tool was designed for absolute privacy. Once you close the terminal, the conversation never existed. Not even forensics can recover what wasn't written. Use responsibly.

---

## 💀 Why does this exist?

Corporations sell your DMs. ISPs throttle your connections. "Encrypted" apps still store metadata on their servers.

**CMD-CHAT is different.**

It lives entirely in your RAM. It creates a secure tunnel between two terminals, encrypts every byte with military-grade algorithms, and then **self-destructs** the moment you type `/exit`.

### 🔥 The "Paranoid" Feature Set

- **Ghost Mode:** Nothing touches the hard drive. All data exists only in volatile memory (RAM).
- **Double-Blind Encryption:** RSA Handshake + AES Symmetric Session. Even if they intercept the traffic, it looks like white noise.
- **Kill Switch:** Closing the window wipes the keys instantly.
- **No Central Server:** You are the server. No logs for big tech to subpoena.

---

## 🕵️‍♂️ How the "Black Box" Works

1. **Handshake:** Client generates a disposable RSA key pair.
2. **Exchange:** Server mints a one-time symmetric key, encrypts it with your public key.
3. **Lock:** The tunnel is sealed.
4. **Vanish:** Communication happens. On exit, memory is overwritten. **Poof.**

---

## ⚡ Quick Start (Before it gets banned)

You don't need a PhD in cryptography. You just need Python.

### 1. Grab the Code

```bash
git clone https://github.com/emilycodestar/cmd-chat.git
cd cmd-chat
```

### 2. Lock & Load (Install)

```bash
# Linux / macOS
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Windows
python -m venv venv ; .\venv\Scripts\activate ; pip install -r requirements.txt
```

### 3. Go Dark (Usage)

#### Host the Bunker (Server)

```bash
python cmd_chat.py serve 0.0.0.0 3000 --password SUPER_SECRET_CODE
```

#### Join the Channel (Client)

```bash
python cmd_chat.py connect SERVER_IP 3000 Tyler SUPER_SECRET_CODE
```

(Replace SERVER_IP with localhost if testing locally)

### 👁️ Visual Proof

They can't read this, but you can.

![Example](example.gif)

<div align="center">

Built for the shadows.

If this repo disappears, you know why. 😉

⭐ Star it while it's still up

</div>
