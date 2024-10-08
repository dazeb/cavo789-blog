---
slug: move-wsl-to-another-location
title: Move WSL to another location
authors: [christophe]
tags: [docker, tips, wsl]
enableComments: true
image: /img/docker_tips_social_media.jpg
---
![Move WSL to another location](/img/docker_tips_banner.jpg)

> [https://dev.to/mefaba/installing-wsl-on-another-drive-in-windows-5c4a](https://dev.to/mefaba/installing-wsl-on-another-drive-in-windows-5c4a)

By default, the Linux distribution is installed on your C: drive. If, like me, you have a D: drive with almost nothing on it, it can be really interesting to move Linux on that second drive.

<!-- truncate -->

To do this, please:

* Run `wsl --list --verbose` from a **PowerShell** console; you'll get the name of your distribution (`Ubuntu` in my case),
* From a **PowerShell Admin** console,
  * Run `wsl --shutdown` to shutdown WSL,
  * On your second drive, create a temporary folder like `d:\wsl`,
  * Run `wsl --export Ubuntu d:\wsl\ubuntu.tar"`,
  * When finished, run `wsl --unregister Ubuntu` and, finally,
  * Run `wsl --import Ubuntu d:\wsl\ubuntu d:\wsl\ubuntu.tar --version 2`
  * Run `del d:\wsl\ubuntu.tar`

You will need to do this for every distribution you have installed and if you want to move it.

:::tip
If you have Docker, you can do the same i.e. move the Docker partition to your second disk.

```bash
wsl --export docker-desktop d:\wsl\docker-desktop.tar
wsl --export docker-desktop-data d:\wsl\docker-desktop-data.tar

wsl --unregister docker-desktop
wsl --unregister docker-desktop-data

wsl --import docker-desktop d:\wsl\docker-desktop d:\wsl\docker-desktop.tar --version 2
wsl --import docker-desktop-data d:\wsl\docker-desktop-data d:\wsl\docker-desktop-data.tar --version 2

del d:\wsl\docker-desktop.tar
del d:\wsl\docker-desktop-data.tar
```

:::

Once done, restart your computer to finalize the move.
