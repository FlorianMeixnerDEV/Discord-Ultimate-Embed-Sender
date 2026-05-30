
# Discord Ultimate Embed Sender



The **Discord Ultimate Embed Sender** is a structured and user-friendly tool that allows you to design professional, highly customizable embed messages and send them instantly to Discord channels via webhooks.




## Installation

**Option 1: Standalone (.exe)**

For Windows users, a pre-compiled, self-executable .exe file is available. It can be launched directly by double-clicking, without requiring any prerequisites or Python installations.

**Option 2: Python Script**

If you prefer running the source code manually, make sure Python is installed:

```bash
  pip install requests
  python message.py
```
    
## Manage Channels

Clicking the **Channels** button in the top right of the menu bar opens the management window for your Discord connections. Here you can easily organize your target channels:

**Add / Edit Channel:** Enter a custom name for your channel (e.g., #announcement) along with the corresponding Discord Webhook URL and click Save Channel.

**Delete Channel Infrastructure:** Select an existing profile from the dropdown menu to permanently remove it by clicking _Delete Selected Channel._

<img width="482" height="392" alt="settings" src="https://github.com/user-attachments/assets/12683b47-5bc1-44c9-82fb-411386fc2781" />

## Designing the Embed on the Main Screen

In the main menu, choose your desired target channel from the dropdown under Target Channel. Afterward, you can define the exact visual appearance of your message:

**Text Elements**

Set the Embed Title and optionally add a Title Link (URL) to make the heading clickable. Use the large Description / Message field to write your primary message body.

**Colors & Media**

Click the Choose Color button to set the accent color on the side (Border Color). You can also include a Thumbnail Image and a large Main Image directly via URLs or local files.

<img width="1920" height="1030" alt="hauptbildschirm" src="https://github.com/user-attachments/assets/31a12dcd-be98-44ba-a573-af611b572364" />


## Utilities & Real-Time Error Diagnosis

To make your workflow smoother, the software includes two integrated utility windows that can also be accessed via the top-right menu bar:

**Formatting & Pings**
A compact cheat sheet for Discord Markdown (Bold, Italic, Underline, Spoiler) and the exact syntax guidelines for mentioning User IDs, Role IDs, or Channels.

<img width="702" height="640" alt="discord_formatting" src="https://github.com/user-attachments/assets/baa7f61f-c137-4d76-9053-eff54648ad17" />



**Live Process Log & Debugger**

The built-in logger tracks all background activities in real time. If a webhook fails or a URL is unreachable, the error becomes immediately visible here.

<img width="502" height="632" alt="debug_log" src="https://github.com/user-attachments/assets/ec05f0c9-d3d7-461a-a1e8-94a7f07ec7eb" />



