---
slug: wsl-powershell
title: Starting the default associated Windows program on WSL
authors: [christophe]
image: /img/wsl_tips_social_media.jpg
tags: [powershell, tips, wsl]
enableComments: true
---
![Starting the default associated Windows program on WSL](/img/wsl_tips_banner.jpg)

Very often, I'm in my Linux console and I'd like to open a pdf file that I've just generated or, more simply, to open an html file. But how can I do this?

Without knowing the tip that is the subject of this article, at the moment I launch [Windows Explorer](/blog/wsl-windows-explorer) from my console, I get then the well-known file explorer interface and there I double-click on the file I want to open and leave it to Windows, which knows which program to launch to open this or that extension.

In fact, it's much simpler...

<!-- truncate -->

The tip: start `powershell.exe` followed by the filename to open like `powershell.exe guide.pdf` or `powershell.exe index.html`.

:::note Not available in Bash
`powershell.exe` only works in the console. You can't use it in a Bash script (`.sh`), it won't be recognized there.
:::

:::tip `xdg-open`
You can also use `xdg-open` to start your default browser so `xdg-open index.html` will open the file in your Windows browser.
:::

If you get the error below, you'll find a solution in the article [Windows Explorer](/blog/wsl-windows-explorer#wsl-localhost-is-not-accessible)

```bash
Start : This command cannot be run due to the error: The system cannot find the file specified.
At line:1 char:1
+ Start "readme.html"
+ ~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [Start-Process], InvalidOperationException
    + FullyQualifiedErrorId : InvalidOperationException,Microsoft.PowerShell.Commands.StartProcessCommand
```
