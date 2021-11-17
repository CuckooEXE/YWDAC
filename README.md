# You Wouldn't Download A Car

YWDAC is a (tiny) vulnerability and (tiny) exploit for the [Trading Paints](https://www.tradingpaints.com/) software. Trading Paints is "the custom car painting platform for iRacing". Basically, you can select custom paints/liveries to put on your car while racing, it makes it super fast and easy.

> This is actually incredibly similar to the vulnerability I found in [MouseTrap](https://axelp.io/MouseTrap), so I'll just breeze through this.

## Vulnerability

On a whim, I decided to look at the web traffic generated when Trading Paints launches. I opened up WireShark, and immediately saw that it used HTTP to check and fetch updates, rather than HTTPS. This makes it susceptible to [MITM](https://en.wikipedia.org/wiki/Man-in-the-middle_attack), which can allow an adversary to potentially serve malicious/false content and steal user data. 

The biggest hurdle is getting the domain for the system to re-route to your malicious webserver, however, that is out of scope for this particular exercise.

![Wireshark Overview](img/wireshark_overview.png)

Here, the Trading Paints software is visible, and behind it, you can see the communications to its update server. There are two "conversations":

1. Check the connection, then get the cars/collections for this user

![Check Connection and Get Cars](img/wireshark_stream1.png)

2. Check for updates (`/version.xml`)

![Check Updates](img/wireshark_stream2.png)

Here the XML shows multiple different DLLs and an EXE, along with its destination and file version. So I'm thinking all we have to do is create a lightweight webserver and serve a malicious payload.

The `downloaderurl` is set to `http://downloader.tradingpaints.com`.

![Downloader URL](img/downloader_url.png)

The logic to do the version checking is in the `Form1.checkUpdate` class, and it simply checks if the versions are equal, it doesn't care if they version you have is greater than the one hosted.

![Check Update Logic](img/checkUpdate.png)


## Testing

The malicious files are found in `YWDAC/`, they just pop up a message box with the current time. Let's change the `C:\Windows\System32\Drivers\etc\hosts` file, spin up the webserver in `webserver/`, and see if this works.

> Note: The `version.xml` needs all of the `<version></version>` to be: a) empty or b) nonsense that won't be matched by the current running version of Trading Paints.


```powershell
Add-Content C:\Windows\System32\Drivers\etc\hosts "`n127.0.0.1 dl.tradingpaints.com`n127.0.0.1 downloader.tradingpaints.com`n"
cp .\YWDAC\Debug\YWDAC.dll webserver\
cp .\YWDAC\Debug\YWDAC.exe webserver\
cd webserver\
python webserver.py
```

When we next launch `TP Updater.exe`, we see the Flask webserver respond with its requests for files, and it pops up with our malicious executable:

![Pwned](img/pwn.png)

And because TP Updater executes it from a trusted location, UAC pop-ups, and after accepting that, the process runs in a privileged state.

![Tokens](img/tokens.png)


## Extras

Because the the updater downloads whatever file from `version.xml`, we can actually have it download arbitrary files and placed anywhere on the system (`TP Updater.exe` launches UAC when it updates to write files to its directory in `C:\Program Files (x86)\Rhinode LLC\Trading Paints`).

Let's try placing this file on my Desktop. To do this, we'll add an additional entry into our `version.xml`:

```xml
   <File>
      <source>updates/YWDAC.exe</source>
      <name>YWDAC.exe</name>
      <dest>..\..\..\Users\John Smith\Deskotp\YWDAC.exe</dest>
      <filesize></filesize>
      <version></version>
   </File>
```

Nice! That worked:

![Pwned](img/arbitrary_write.png)


## Conclusion

Use HTTPS, __everywhere__.

