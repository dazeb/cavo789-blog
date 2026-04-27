---
slug: accessing-ollama-accross-your-local-network
title: Accessing Ollama accross your local network
date: 2026-12-31
image: /img/v2/using_ollama_local_network.webp
mainTag: ai
tags: [ai, ollama]
language: en
draft: true
blueskyRecordKey:
---
![Accessing Ollama accross your local network](/img/v2/using_ollama_local_network.webp)

In a previous article (see <Link to="/blog/ollama-installation">Installing Ollama and get local AI</Link>), we've installed Ollama, one or more LLMs and a web interface called **Open WebUI**.

Now, let's take it a step further by connection this PC to a small local network so that we can access Ollama from another computer and, therefore, run AI locally.

<!-- truncate -->

## Create a local network

On my own, I'm using a D-Link DGS-108 to connect my computers on the same local network. I've bought it years ago and, I see the current price is around ~35 euros.

This switch has a 1000Mbps bandwith with almost no latency.

### The master computer side

On my most powerfull computer (i9 having 64GB of RAM), I've installed Ollama and Open WebUI so I can open `http://localhost:4000` and play with the AI.

To be able to connect that interface from my second computer, I need to discover the IP address of the master computer.

Because my OS is Windows 11 (even if I'm running under WSL2), in a Powershell session, I've started `ipconfig` and in the full log, pay attention to the `IPv4 Address. . . . . . . . . . . : 192.168.x.x` line. **For me, it's `192.168.0.218`.**

### The slave computer

On my second computer, I'll first check if I can access to my master computer by running `ping 192.168.0.218` and I got this:

```bash
Pinging 192.168.0.218 with 32 bytes of data:

Reply from 192.168.0.218: bytes=32 time<1ms TTL=128
Reply from 192.168.0.218: bytes=32 time<1ms TTL=128
Reply from 192.168.0.218: bytes=32 time=1ms TTL=128
Reply from 192.168.0.218: bytes=32 time=1ms TTL=128

Ping statistics for 192.168.0.218:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),

Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 1ms, Average = 0ms
```

This output means that our second computer can access to the master one with almost zero latency (`time<1ms`).

Make sure Ollama and **Open WebUI** are still running on the master computer and, on the slave one, open `http://192.168.0.218:4000` and you should see the login interface of Open WebUI.

## Configure VSCode

On the slave computer, install the <Link to="/blog/ollama-installation#using-a-vscode-extension">Continue extension</Link>.

In the `config.json` file, just replace `127.0.0.1` by `192.168.0.218` and that's it.  Keep the port number the same i.e. `11434`




