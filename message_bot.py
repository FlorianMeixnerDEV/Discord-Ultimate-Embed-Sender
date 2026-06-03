import sys
import subprocess
import os
from datetime import datetime
import json

# ==========================================
# --- AUTOMATISCHE IMPORT-PRÜFUNG ---
# ==========================================
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

import tkinter as tk
from tkinter import messagebox, colorchooser, ttk, filedialog

# ==========================================
# --- PYINSTALLER RESSOURCEN-PFAD ---
# ==========================================
def resource_path(relative_path):
    """Ermöglicht den Zugriff auf Ressourcen (wie das Icon) im PyInstaller-Onefile-Modus."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [base_dir, os.path.join(base_dir, "..")]
    for candidate in candidates:
        full_path = os.path.join(candidate, relative_path)
        if os.path.exists(full_path):
            return full_path
    return os.path.join(base_dir, relative_path)

def get_config_path():
    """Use the executable folder for the config in packaged builds, otherwise the project folder."""
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "webhook_config.json")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "webhook_config.json")

CONFIG_FILE = get_config_path()
DEFAULT_COLOR = "3498db"
selected_color_hex = DEFAULT_COLOR

# ==========================================
# --- SPRACH-DATENBANK (ÜBERSETZUNGEN) ---
# ==========================================
LANGUAGES = {
    "EN": {
        "title": "Discord Ultimate Embed Sender",
        "header_title": "Discord Embed Builder",
        "btn_debug": "🛠️ Debug Log",
        "btn_format": "ℹ️ Formatting",
        "btn_channels": "⚙️ Channels",
        "lbl_target": "Target Channel:",
        "no_channels": "No channels configured",
        "lbl_normal_msg": "NORMAL MESSAGE",
        "lbl_auth_name": "AUTHOR: NAME",
        "lbl_auth_link": "AUTHOR: LINK (URL)",
        "lbl_auth_icon": "AUTHOR: ICON (IMAGE URL)",
        "btn_local_icon": "📁 Choose Local Icon...",
        "lbl_embed_title": "EMBED TITLE",
        "lbl_title_link": "TITLE LINK (URL)",
        "lbl_desc": "DESCRIPTION / MESSAGE",
        "lbl_color": "BORDER COLOR",
        "btn_color": "Choose Color",
        "lbl_thumb": "THUMBNAIL IMAGE (URL)",
        "btn_local_thumb": "📁 Choose Local Thumbnail...",
        "lbl_main_img": "MAIN IMAGE (URL)",
        "btn_local_main": "📁 Choose Local Main Image...",
        "lbl_footer_text": "FOOTER TEXT",
        "lbl_footer_icon": "FOOTER ICON (IMAGE URL)",
        "btn_local_footer": "📁 Choose Local Footer Icon...",
        "btn_clear": "🗑️ Clear",
        "btn_send": "Send Embed to Discord",
        # Dialogs / Popups
        "clear_confirm_title": "Clear Form",
        "clear_confirm_msg": "Do you really want to clear all entered fields?",
        "log_cleared": "Log history cleared.",
        "pasted_safe": "Text securely pasted.",
        "paste_error": "Error pasting text: ",
        "json_load_error": "Error loading JSON: ",
        "json_save_error": "Could not save configuration: ",
        "channel_saved": "Channel '{name}' saved.",
        "channel_deleted": "Channel '{name}' was deleted.",
        "send_start": "Sending process started...",
        "err_no_channel_setup": "Please configure a channel using the gear icon ⚙️ first!",
        "local_file_detected": "Local file detected for [{key}]: {file}",
        "err_empty_payload": "Neither a normal message nor an embed has been filled out!",
        "send_success": "Message successfully sent!",
        "send_success_popup": "Message successfully sent to {channel}!",
        "discord_err": "Discord Error",
        "conn_err": "Connection failed",
        # Help Window
        "help_title": "Discord Formatting & Pings",
        "help_header": "Discord Text & Ping Formatting",
        "help_col_style": "Effect / Type",
        "help_col_syntax": "Code (Input)",
        "help_col_example": "Result / Note",
        "help_note": "Important: Real push pings only work in the 'NORMAL MESSAGE' field at the very top!",
        "help_roles_title": "Available roles (double-click to insert)",
        "help_roles_empty": "No roles could be loaded. Save a valid Bot Token in the settings first.",
        "help_role_col": "Role",
        "help_mention_col": "Mention",
        "main_role_label": "Role mention:",
        "main_role_placeholder": "No roles loaded",
        "h_italic": "Italic",
        "h_bold": "Bold",
        "h_underline": "Underlined",
        "h_spoiler": "Spoiler",
        "h_quote": "Quote",
        "h_ping_user": "Ping User",
        "h_ping_role": "Ping Role",
        "h_link_ch": "Link Channel",
        "h_mass_ping": "Mass Ping",
        "h_ex_italic": "Slanted text",
        "h_ex_bold": "Thick printed text",
        "h_ex_underline": "Line under the text",
        "h_ex_spoiler": "Blacks out text until clicked",
        "h_ex_quote": "Indents text as a quote",
        "h_ex_user": "Triggers a push notification",
        "h_ex_role": "Requires the '&' character",
        "h_ex_ch": "Creates a clickable link",
        "h_ex_mass": "Notifies everyone",
        # Settings Window
        "settings_title": "Manage Channels",
        "settings_header": "Add / Edit Channel",
        "settings_lbl_name": "Channel Name (e.g., #general):",
        "settings_lbl_url": "Webhook URL:",
        "settings_btn_save": "Save Channel",
        "settings_lbl_del": "Delete Channel Infrastructure:",
        "settings_btn_del": "Delete Selected Channel",
        "settings_btn_clear_all": "Delete All Channels",
        "settings_btn_reset_config": "Reset Configuration",
        "settings_err_fields": "Please fill out both fields!",
        "settings_clear_all_confirm_title": "Delete all channels",
        "settings_clear_all_confirm_msg": "Do you really want to delete all saved webhook and bot channels?",
        "settings_confirm_del_title": "Delete Channel",
        "settings_confirm_del_msg": "Do you really want to delete the channel '{name}'?",
        # Debug Window
        "debug_title": "Live Process Log & Debugger",
        "debug_header": "🛠️ System Log (Realtime)",
        "debug_btn_clear": "Clear",
        # Image Dialogs
        "img_title_auth": "Select local image for 'Author Icon'",
        "img_title_thumb": "Select local image for 'Thumbnail'",
        "img_title_main": "Select local image for 'Main Image'",
        "img_title_footer": "Select local image for 'Footer Icon'",
        "img_filetype": "Image files",
        "img_allfiles": "All files"
    },
    "DE": {
        "title": "Discord Ultimate Embed Sender",
        "header_title": "Discord Embed Builder",
        "btn_debug": "🛠️ Debug-Log",
        "btn_format": "ℹ️ Formatierung",
        "btn_channels": "⚙️ Kanäle",
        "lbl_target": "Zielkanal:",
        "no_channels": "Keine Kanäle eingerichtet",
        "lbl_normal_msg": "NORMALE NACHRICHT",
        "lbl_auth_name": "AUTOR: NAME",
        "lbl_auth_link": "AUTOR: LINK (URL)",
        "lbl_auth_icon": "AUTOR: ICON (BILD-URL)",
        "btn_local_icon": "📁 Lokales Icon wählen...",
        "lbl_embed_title": "EMBED TITEL",
        "lbl_title_link": "TITEL-LINK (URL)",
        "lbl_desc": "BESCHREIBUNG / NACHRICHT",
        "lbl_color": "RAHMENFARBE",
        "btn_color": "Farbe wählen",
        "lbl_thumb": "THUMBNAIL BILD (URL)",
        "btn_local_thumb": "📁 Lokales Thumbnail wählen...",
        "lbl_main_img": "HAUPTBILD (URL)",
        "btn_local_main": "📁 Lokales Hauptbild wählen...",
        "lbl_footer_text": "FOOTER TEXT",
        "lbl_footer_icon": "FOOTER ICON (BILD-URL)",
        "btn_local_footer": "📁 Lokales Footer-Icon wählen...",
        "btn_clear": "🗑️ Leeren",
        "btn_send": "Embed an Discord senden",
        # Dialoge / Popups
        "clear_confirm_title": "Formular leeren",
        "clear_confirm_msg": "Möchtest du wirklich alle eingegebenen Texte löschen?",
        "log_cleared": "Protokoll gelöscht.",
        "pasted_safe": "Text sicher eingefügt.",
        "paste_error": "Fehler beim Einfügen: ",
        "json_load_error": "Fehler beim Laden der JSON: ",
        "json_save_error": "Konnte Konfiguration nicht speichern: ",
        "channel_saved": "Kanal '{name}' gespeichert.",
        "channel_deleted": "Kanal '{name}' wurde gelöscht.",
        "send_start": "Sende-Vorgang gestartet...",
        "err_no_channel_setup": "Bitte richte zuerst einen Kanal über das Zahnrad ⚙️ ein!",
        "local_file_detected": "Lokale Datei für [{key}] erkannt: {file}",
        "err_empty_payload": "Es wurde weder eine normale Nachricht noch ein Embed ausgefüllt!",
        "send_success": "Nachricht erfolgreich gesendet!",
        "send_success_popup": "Nachricht erfolgreich an {channel} gesendet!",
        "discord_err": "Discord-Fehler",
        "conn_err": "Verbindung fehlgeschlagen",
        # Formatierungs-Hilfe
        "help_title": "Discord Formatierung & Pings",
        "help_header": "Discord Text- & Ping-Formatierung",
        "help_col_style": "Effekt / Typ",
        "help_col_syntax": "Code (Eingabe)",
        "help_col_example": "Ergebnis / Hinweis",
        "help_note": "Wichtig: Echte Push-Pings klappen nur im Feld 'NORMALE NACHRICHT' ganz oben!",
        "help_roles_title": "Verfügbare Rollen (Doppelklick zum Einfügen)",
        "help_roles_empty": "Es konnten keine Rollen geladen werden. Speichere zuerst einen gültigen Bot-Token in den Einstellungen.",
        "help_role_col": "Rolle",
        "help_mention_col": "Mention",
        "main_role_label": "Rollen-Mention:",
        "main_role_placeholder": "Keine Rollen geladen",
        "h_italic": "Kursiv",
        "h_bold": "Fett",
        "h_underline": "Unterstrichen",
        "h_spoiler": "Spoiler",
        "h_quote": "Zitat",
        "h_ping_user": "Benutzer pingen",
        "h_ping_role": "Rolle pingen",
        "h_link_ch": "Kanal verlinken",
        "h_mass_ping": "Massen-Ping",
        "h_ex_italic": "Abgeschrägter Text",
        "h_ex_bold": "Dick gedruckter Text",
        "h_ex_underline": "Linie unter dem Text",
        "h_ex_spoiler": "Schwärzt Text bis zum Klick",
        "h_ex_quote": "Rückt Text als Zitat ein",
        "h_ex_user": "Triggers Push-Meldung",
        "h_ex_role": "Erfordert das '&'-Zeichen",
        "h_ex_ch": "Erzeugt anklickbaren Link",
        "h_ex_mass": "Benachrichtigt alle",
        # Einstellungen
        "settings_title": "Kanäle verwalten",
        "settings_header": "Kanal hinzufügen / Bearbeiten",
        "settings_lbl_name": "Kanalname (z.B. #allgemein):",
        "settings_lbl_url": "Webhook URL:",
        "settings_btn_save": "Kanal Speichern",
        "settings_lbl_del": "Kanal löschen:",
        "settings_btn_del": "Ausgewählten Kanal löschen",
        "settings_btn_clear_all": "Alle Kanäle löschen",
        "settings_btn_reset_config": "Konfiguration zurücksetzen",
        "settings_err_fields": "Bitte beide Felder ausfüllen!",
        "settings_clear_all_confirm_title": "Alle Kanäle löschen",
        "settings_clear_all_confirm_msg": "Möchtest du wirklich alle gespeicherten Webhook- und Bot-Kanäle löschen?",
        "settings_confirm_del_title": "Kanal löschen",
        "settings_confirm_del_msg": "Möchtest du den Kanal '{name}' wirklich löschen?",
        # Debug Fenster
        "debug_title": "Live-Vorgangsprotokoll & Debugger",
        "debug_header": "🛠️ System-Protokoll (Echtzeit)",
        "debug_btn_clear": "Löschen",
        # Bild-Dialoge
        "img_title_auth": "Lokales Bild für 'Autor Icon' auswählen",
        "img_title_thumb": "Lokales Bild für 'Thumbnail' auswählen",
        "img_title_main": "Lokales Bild für 'Hauptbild' auswählen",
        "img_title_footer": "Lokales Bild für 'Footer Icon' auswählen",
        "img_filetype": "Bilddateien",
        "img_allfiles": "Alle Dateien"
    }
}

current_lang = "EN"
channel_menu = None
role_menu = None
role_var = None
role_lookup = {}

# Hauptfenster initialisieren
root = tk.Tk()
root.geometry("560x950")
root.minsize(500, 600)
root.configure(bg="#202225")

try:
    icon_path = resource_path("logo.ico")
    root.iconbitmap(icon_path)
except Exception:
    pass

log_history = []
debug_window = None
debug_text = None

# ==========================================
# --- LOGIK- UND HILFSFUNKTIONEN ---
# ==========================================

def get_txt(key):
    return LANGUAGES[current_lang].get(key, "")

def switch_language(lang):
    global current_lang
    current_lang = lang
    root.title(get_txt("title"))
    
    title_label.config(text=get_txt("header_title"))
    debug_btn.config(text=get_txt("btn_debug"))
    markdown_btn.config(text=get_txt("btn_format"))
    settings_btn.config(text=get_txt("btn_channels"))
    channel_lbl.config(text=get_txt("lbl_target"))
    
    lbl_normal.config(text=get_txt("lbl_normal_msg"))
    lbl_auth_n.config(text=get_txt("lbl_auth_name"))
    lbl_auth_l.config(text=get_txt("lbl_auth_link"))
    lbl_auth_i.config(text=get_txt("lbl_auth_icon"))
    
    lbl_emb_t.config(text=get_txt("lbl_embed_title"))
    lbl_title_l.config(text=get_txt("lbl_title_link"))
    lbl_desc_t.config(text=get_txt("lbl_desc"))
    lbl_col_t.config(text=get_txt("lbl_color"))
    
    lbl_thub_t.config(text=get_txt("lbl_thumb"))
    lbl_main_t.config(text=get_txt("lbl_main_img"))
    lbl_foot_t.config(text=get_txt("lbl_footer_text"))
    lbl_footi_t.config(text=get_txt("lbl_footer_icon"))
    
    clear_btn.config(text=get_txt("btn_clear"))
    send_btn.config(text=get_txt("btn_send"))
    
    author_icon_btn.config(text=get_txt("btn_local_icon"))
    thumb_btn.config(text=get_txt("btn_local_thumb"))
    main_img_btn.config(text=get_txt("btn_local_main"))
    footer_icon_btn.config(text=get_txt("btn_local_footer"))
    
    if selected_color_hex == DEFAULT_COLOR:
        color_button.config(text=get_txt("btn_color"))
    else:
        color_button.config(text=f"{get_txt('btn_color')}: #{selected_color_hex}")

    update_dropdown()
    update_role_dropdown()
    check_author_name()

def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] [{level}] {message}\n"
    log_history.append((formatted_msg, level))
    
    if debug_text and debug_text.winfo_exists():
        debug_text.config(state="normal")
        debug_text.insert(tk.END, formatted_msg)
        if level == "ERROR":
            debug_text.tag_add("error", "end -2 lines", "end -1 chars")
            debug_text.tag_config("error", foreground="#f04747")
        elif level == "SUCCESS":
            debug_text.tag_add("success", "end -2 lines", "end -1 chars")
            debug_text.tag_config("success", foreground="#43b581")
        elif level == "PAYLOAD":
            debug_text.tag_add("payload", "end -2 lines", "end -1 chars")
            debug_text.tag_config("payload", foreground="#faa61a")
        debug_text.config(state="disabled")
        debug_text.see(tk.END)

def toggle_debug_window():
    global debug_window, debug_text
    if debug_window and debug_window.winfo_exists():
        debug_window.lift()
        return
        
    debug_window = tk.Toplevel(root)
    debug_window.title(get_txt("debug_title"))
    debug_window.geometry("500x600")
    debug_window.configure(bg="#2f3136")
    debug_window.transient(root)
    
    try:
        debug_window.iconbitmap(resource_path("logo.ico"))
    except Exception:
        pass
    
    debug_title = tk.Frame(debug_window, bg="#202225", height=45)
    debug_title.pack(fill="x", side="top")
    debug_title.pack_propagate(False)
    
    debug_header_lbl = tk.Label(debug_title, text=get_txt("debug_header"), font=("Arial", 10, "bold"), fg="#faa61a", bg="#202225")
    debug_header_lbl.pack(side="left", padx=15)
    
    def clear_debug():
        global log_history
        log_history.clear()
        debug_text.config(state="normal")
        debug_text.delete("1.0", tk.END)
        debug_text.config(state="disabled")
        log_message(get_txt("log_cleared"), "INFO")

    tk.Button(debug_title, text=get_txt("debug_btn_clear"), font=("Arial", 8, "bold"), bg="#4f545c", fg="white", bd=0, cursor="hand2", padx=10, command=clear_debug).pack(side="right", padx=15, pady=10)
    
    debug_text = tk.Text(debug_window, bg="#18191c", fg="#b9bbbe", font=("Consolas", 9), insertbackground="white", bd=0, wrap="word", state="disabled")
    debug_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    debug_text.config(state="normal")
    for msg, level in log_history:
        debug_text.insert(tk.END, msg)
        if level == "ERROR":
            debug_text.tag_add("error", "end -2 lines", "end -1 chars")
            debug_text.tag_config("error", foreground="#f04747")
        elif level == "SUCCESS":
            debug_text.tag_add("success", "end -2 lines", "end -1 chars")
            debug_text.tag_config("success", foreground="#43b581")
        elif level == "PAYLOAD":
            debug_text.tag_add("payload", "end -2 lines", "end -1 chars")
            debug_text.tag_config("payload", foreground="#faa61a")
    debug_text.config(state="disabled")
    debug_text.see(tk.END)

def _on_mousewheel(event):
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")
    else:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def safe_paste(event):
    try:
        text = root.clipboard_get()
        clean_text = text.strip().replace("\n", "").replace("\r", "")
        widget = event.widget
        if isinstance(widget, tk.Entry):
            current_pos = widget.index(tk.INSERT)
            widget.insert(current_pos, clean_text)
            if widget == author_name_entry:
                root.after(10, check_author_name)
            log_message(get_txt("pasted_safe"), "INFO")
            return "break"
    except Exception as e:
        log_message(f"{get_txt('paste_error')}{e}", "ERROR")

def load_config():
    default_config = {"webhooks": {}, "bot_channels": {}, "bot_token": "", "last_selected": ""}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return default_config
                if "webhooks" not in data:
                    if "webhook_url" in data and data["webhook_url"]:
                        return {"webhooks": {"#standard": data["webhook_url"]}, "bot_channels": {}, "bot_token": "", "last_selected": "#standard"}
                    return default_config
                data.setdefault("bot_channels", {})
                data.setdefault("bot_token", "")
                return data
        except Exception as e:
            log_message(f"{get_txt('json_load_error')}{e}", "ERROR")
            return default_config
    return default_config

def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        return True
    except Exception as e:
        log_message(f"{get_txt('json_save_error')}{e}", "ERROR")
        return False


def build_bot_channel_label(guild_name, channel, category_map):
    channel_name = channel.get("name", "channel")
    category_name = category_map.get(channel.get("parent_id", ""), "")
    if category_name:
        return f"{guild_name} > {category_name} > #{channel_name}"
    return f"{guild_name} > #{channel_name}"


def update_dropdown():
    """Aktualisiert die Kanalauswahl im OptionMenu und erzwingt das Farbschema."""
    global channel_menu, channel_select_bar
    config = load_config()
    channels = list(config.get("webhooks", {}).keys()) + list(config.get("bot_channels", {}).keys())
    
    if channel_menu:
        channel_menu.destroy()
    
    if channels:
        last = config.get("last_selected", "")
        if last in channels:
            channel_var.set(last)
        else:
            channel_var.set(channels[0])
        channel_menu = tk.OptionMenu(channel_select_bar, channel_var, *channels)
    else:
        channel_var.set(get_txt("no_channels"))
        channel_menu = tk.OptionMenu(channel_select_bar, channel_var, get_txt("no_channels"))
        
    channel_menu.config(
        bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", 
        bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2"
    )
    channel_menu.pack(side="left", fill="x", expand=True, padx=(0, 20), pady=15)
    
    channel_menu["menu"].config(
        bg="#40444b", fg="white", activebackground="#7289da", activeforeground="white", bd=0, font=("Arial", 10)
    )

    if role_lbl is not None:
        role_lbl.config(text=get_txt("main_role_label"))


def update_role_dropdown():
    global role_menu, role_var, role_lookup

    try:
        if role_menu:
            role_menu.destroy()
    except Exception:
        pass

    role_lookup = {}
    config = load_config()
    token = config.get("bot_token", "").strip()

    if not token:
        role_var = tk.StringVar(root, value=get_txt("main_role_placeholder"))
        role_menu = tk.OptionMenu(role_select_frame, role_var, get_txt("main_role_placeholder"))
        role_menu.config(bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2", state="disabled")
        role_menu.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)
        return

    try:
        roles = fetch_bot_roles(token)
    except Exception:
        roles = []

    if not roles:
        role_var = tk.StringVar(root, value=get_txt("main_role_placeholder"))
        role_menu = tk.OptionMenu(role_select_frame, role_var, get_txt("main_role_placeholder"))
        role_menu.config(bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2", state="disabled")
        role_menu.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)
        return

    labels = [f"{item['guild']} · @{item['name']}" for item in roles]
    role_lookup = {label: item['mention'] for label, item in zip(labels, roles)}

    def insert_selected_role(*_args):
        label = role_var.get()
        mention = role_lookup.get(label, "")
        if mention:
            insert_role_mention(mention)

    role_var = tk.StringVar(root, value=labels[0])
    role_menu = tk.OptionMenu(role_select_frame, role_var, *labels, command=lambda *_: insert_selected_role())
    role_menu.config(bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2")
    role_menu.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)
    role_menu["menu"].config(bg="#40444b", fg="white", activebackground="#7289da", activeforeground="white", bd=0, font=("Arial", 10))


def pick_color():
    global selected_color_hex
    color_code = colorchooser.askcolor(title=get_txt("lbl_color"))
    if color_code[1]:
        selected_color_hex = color_code[1].replace("#", "")
        color_button.config(bg=color_code[1], text=f"{get_txt('btn_color')}: #{selected_color_hex}")

def clear_all_fields():
    if messagebox.askyesno(get_txt("clear_confirm_title"), get_txt("clear_confirm_msg")):
        content_text.delete("1.0", tk.END)
        author_name_entry.delete(0, tk.END)
        author_url_entry.delete(0, tk.END)
        author_icon_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        url_entry.delete(0, tk.END)
        desc_text.delete("1.0", tk.END)
        thumb_entry.delete(0, tk.END)
        image_entry.delete(0, tk.END)
        footer_text_entry.delete(0, tk.END)
        footer_icon_entry.delete(0, tk.END)
        
        global selected_color_hex
        selected_color_hex = DEFAULT_COLOR
        color_button.config(bg=f"#{DEFAULT_COLOR}", text=get_txt("btn_color"))
        
        check_author_name()
        log_message(get_txt("clear_confirm_title"), "INFO")

def choose_image_for_entry(entry_widget, translation_key):
    file_path = filedialog.askopenfilename(
        title=get_txt(translation_key),
        filetypes=[(get_txt("img_filetype"), "*.png *.jpg *.jpeg *.gif *.webp"), (get_txt("img_allfiles"), "*.*")]
    )
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)
        log_message(f"File chosen: {file_path}", "INFO")

def check_author_name(*args):
    if author_name_entry.get().strip():
        author_icon_btn.config(state="normal", bg="#4f545c", fg="white", cursor="hand2")
    else:
        author_icon_btn.config(state="disabled", bg="#2f3136", fg="#72767d", cursor="arrow")


def fetch_bot_roles(token):
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    guilds_response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=30)
    guilds_response.raise_for_status()
    guilds = guilds_response.json()
    if not isinstance(guilds, list):
        raise ValueError("Ungültige Antwort von Discord.")

    role_entries = []
    for guild in guilds:
        roles_response = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/roles", headers=headers, timeout=30)
        roles_response.raise_for_status()
        for role in roles_response.json():
            if role.get("id") and role.get("name") and role.get("name") != "@everyone" and not role.get("tags", {}).get("bot_id"):
                role_entries.append({
                    "guild": guild.get("name", "Guild"),
                    "name": role.get("name", "Role"),
                    "mention": f"<@&{role['id']}>",
                    "id": role.get("id"),
                })

    role_entries.sort(key=lambda item: (item["guild"].lower(), item["name"].lower()))
    return role_entries


def insert_role_mention(mention_text):
    try:
        content_text.insert(tk.INSERT, mention_text)
        content_text.focus_set()
        log_message(f"Inserted role mention: {mention_text}", "INFO")
    except Exception as e:
        log_message(f"Could not insert role mention: {e}", "ERROR")

# ==========================================
# --- MEHRFENSTER-SYSTEM ---
# ==========================================

def open_markdown_help():
    help_win = tk.Toplevel(root)
    help_win.title(get_txt("help_title"))
    help_win.geometry("560x480")
    help_win.configure(bg="#2f3136")
    help_win.transient(root)
    
    try: help_win.iconbitmap(resource_path("logo.ico"))
    except Exception: pass
    
    tk.Label(help_win, text=get_txt("help_header"), font=("Arial", 12, "bold"), fg="white", bg="#2f3136").pack(pady=12)
    
    style_tree = ttk.Style(help_win)
    style_tree.theme_use('clam')
    style_tree.configure("Markdown.Treeview", background="#40444b", foreground="white", fieldbackground="#40444b", rowheight=26, bd=0)
    style_tree.configure("Markdown.Treeview.Heading", background="#202225", foreground="white", font=("Arial", 9, "bold"), borderwidth=1)
    
    tree = ttk.Treeview(help_win, columns=("Stil", "Syntax", "Beispiel"), show="headings", style="Markdown.Treeview")
    tree.heading("Stil", text=get_txt("help_col_style"))
    tree.heading("Syntax", text=get_txt("help_col_syntax"))
    tree.heading("Beispiel", text=get_txt("help_col_example"))
    
    tree.column("Stil", width=130, minwidth=130, anchor="w")
    tree.column("Syntax", width=180, minwidth=180, anchor="center")
    tree.column("Beispiel", width=210, minwidth=210, anchor="w")
    
    rules = [
        (get_txt("h_italic"), "*Text* / _Text_", get_txt("h_ex_italic")),
        (get_txt("h_bold"), "**Text**", get_txt("h_ex_bold")),
        (get_txt("h_underline"), "__Text__", get_txt("h_ex_underline")),
        (get_txt("h_spoiler"), "||Text||", get_txt("h_ex_spoiler")),
        (get_txt("h_quote"), "> Text", get_txt("h_ex_quote")),
        (get_txt("h_ping_user"), "<@USER_ID>", get_txt("h_ex_user")),
        (get_txt("h_ping_role"), "<@&ROLLEN_ID>", get_txt("h_ex_role")),
        (get_txt("h_link_ch"), "<#KANAL_ID>", get_txt("h_ex_ch")),
        (get_txt("h_mass_ping"), "@everyone / @here", get_txt("h_ex_mass"))
    ]
    
    for rule in rules: tree.insert("", tk.END, values=rule)
    tree.pack(padx=15, pady=5, fill="both", expand=True)

    tk.Label(help_win, text=get_txt("help_note"), font=("Arial", 8, "bold", "italic"), fg="#faa61a", bg="#2f3136").pack(pady=(5, 10))

    role_frame = tk.Frame(help_win, bg="#2f3136")
    role_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
    tk.Label(role_frame, text=get_txt("help_roles_title"), font=("Arial", 10, "bold"), fg="white", bg="#2f3136").pack(anchor="w", pady=(0, 4))

    role_tree = ttk.Treeview(role_frame, columns=("role", "mention"), show="headings", style="Markdown.Treeview", height=8)
    role_tree.heading("role", text=get_txt("help_role_col"))
    role_tree.heading("mention", text=get_txt("help_mention_col"))
    role_tree.column("role", width=260, minwidth=260, anchor="w")
    role_tree.column("mention", width=140, minwidth=140, anchor="center")
    role_tree.pack(fill="both", expand=True)

    config = load_config()
    token = config.get("bot_token", "").strip()
    if token:
        try:
            roles = fetch_bot_roles(token)
            if roles:
                for entry in roles:
                    role_tree.insert("", tk.END, values=(f"{entry['guild']} · @{entry['name']}", entry['mention']))
            else:
                tk.Label(role_frame, text=get_txt("help_roles_empty"), fg="#b9bbbe", bg="#2f3136", justify="left").pack(anchor="w", pady=(6, 0))
        except Exception as e:
            tk.Label(role_frame, text=f"Fehler beim Laden der Rollen: {e}", fg="#f04747", bg="#2f3136", justify="left").pack(anchor="w", pady=(6, 0))
    else:
        tk.Label(role_frame, text=get_txt("help_roles_empty"), fg="#b9bbbe", bg="#2f3136", justify="left").pack(anchor="w", pady=(6, 0))

    def insert_selected_role(event=None):
        selected = role_tree.selection()
        if not selected:
            return
        mention = role_tree.item(selected[0], "values")[1]
        insert_role_mention(mention)

    role_tree.bind("<Double-1>", insert_selected_role)
    tk.Button(role_frame, text=get_txt("help_roles_title"), bg="#7289da", fg="white", bd=0, cursor="hand2", command=insert_selected_role).pack(anchor="e", pady=(6, 0))

def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title(get_txt("settings_title"))
    settings_win.geometry("650x820")
    settings_win.minsize(600, 720)
    settings_win.configure(bg="#2f3136")
    settings_win.transient(root)
    settings_win.grab_set()
    
    try: settings_win.iconbitmap(resource_path("logo.ico"))
    except Exception: pass

    config = load_config()
    tk.Label(settings_win, text=get_txt("settings_header"), font=("Arial", 11, "bold"), fg="white", bg="#2f3136").pack(pady=(15, 5))
    
    tk.Label(settings_win, text=get_txt("settings_lbl_name"), fg="#b9bbbe", bg="#2f3136", font=("Arial", 9)).pack(anchor="w", padx=20)
    name_entry = tk.Entry(settings_win, bg="#40444b", fg="white", insertbackground="white", bd=1, relief="solid")
    name_entry.pack(padx=20, pady=2, fill="x", ipady=3)
    name_entry.bind("<Control-v>", safe_paste)

    tk.Label(settings_win, text=get_txt("settings_lbl_url"), fg="#b9bbbe", bg="#2f3136", font=("Arial", 9)).pack(anchor="w", padx=20, pady=(5, 0))
    url_entry = tk.Entry(settings_win, bg="#40444b", fg="white", insertbackground="white", bd=1, relief="solid")
    url_entry.pack(padx=20, pady=2, fill="x", ipady=3)
    url_entry.bind("<Control-v>", safe_paste)

    tk.Label(settings_win, text="Bot Token:", fg="#b9bbbe", bg="#2f3136", font=("Arial", 9)).pack(anchor="w", padx=20, pady=(10, 0))
    bot_token_entry = tk.Entry(settings_win, bg="#40444b", fg="white", insertbackground="white", bd=1, relief="solid")
    bot_token_entry.insert(0, config.get("bot_token", ""))
    bot_token_entry.pack(padx=20, pady=2, fill="x", ipady=3)
    bot_token_entry.bind("<Control-v>", safe_paste)

    def load_bot_channels():
        nonlocal bot_menu

        token = bot_token_entry.get().strip()
        if not token:
            messagebox.showerror("Error", "Bitte zuerst einen Bot-Token eingeben.", parent=settings_win)
            return
        try:
            headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
            guilds_response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=30)
            guilds_response.raise_for_status()
            guilds = guilds_response.json()
            if not isinstance(guilds, list):
                raise ValueError("Ungültige Antwort von Discord.")

            loaded = 0
            config["bot_token"] = token
            config["bot_channels"] = {}
            channel_entries = []

            for guild in guilds:
                channels_response = requests.get(f"https://discord.com/api/v10/guilds/{guild['id']}/channels", headers=headers, timeout=30)
                channels_response.raise_for_status()
                guild_channels = channels_response.json()
                category_map = {item.get("id"): item.get("name", "") for item in guild_channels if item.get("type") == 4}

                for channel in guild_channels:
                    if channel.get("type") == 0:
                        channel_entries.append({
                            "label": build_bot_channel_label(guild.get("name", "Guild"), channel, category_map),
                            "data": {
                                "channel_id": channel.get("id"),
                                "guild_id": guild.get("id"),
                                "guild_name": guild.get("name", ""),
                                "channel_name": channel.get("name", ""),
                                "parent_id": channel.get("parent_id"),
                            },
                        })

            channel_entries.sort(key=lambda item: (item["label"].lower(), item["data"]["guild_name"].lower()))
            for entry in channel_entries:
                config["bot_channels"][entry["label"]] = entry["data"]
                loaded += 1

            save_config(config)
            update_dropdown()
            messagebox.showinfo("Bot-Kanäle", f"{loaded} Kanäle geladen. Wähle nun einen Eintrag aus der Liste aus.", parent=settings_win)

            if bot_menu is not None:
                bot_menu.destroy()

            bot_choice_var.set(list(config["bot_channels"].keys())[0] if config["bot_channels"] else "Keine Kanäle geladen")
            bot_menu = tk.OptionMenu(settings_win, bot_choice_var, *(list(config["bot_channels"].keys()) if config["bot_channels"] else ["Keine Kanäle geladen"]))
            bot_menu.config(bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2")
            bot_menu.pack(padx=20, pady=5, fill="x")
            bot_menu["menu"].config(bg="#40444b", fg="white", activebackground="#7289da", activeforeground="white", bd=0)
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) in (401, 403):
                messagebox.showerror("Bot-Fehler", "Der Bot-Token ist ungültig, abgelaufen oder der Bot hat keine Berechtigung für den Server. Bitte einen neuen Token in den Einstellungen speichern.", parent=settings_win)
            else:
                messagebox.showerror("Bot-Fehler", f"Kanal-Liste konnte nicht geladen werden:\n{e}", parent=settings_win)
        except Exception as e:
            messagebox.showerror("Bot-Fehler", f"Kanal-Liste konnte nicht geladen werden:\n{e}", parent=settings_win)

    tk.Button(settings_win, text="Bot-Kanäle laden", bg="#7289da", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2", command=load_bot_channels).pack(padx=20, pady=(5, 0), anchor="w")

    tk.Label(settings_win, text="Verfügbare Bot-Kanäle:", fg="#b9bbbe", bg="#2f3136", font=("Arial", 9)).pack(anchor="w", padx=20, pady=(10, 0))
    bot_menu = None
    bot_choice_var = tk.StringVar(settings_win)
    bot_choices = list(config.get("bot_channels", {}).keys())
    bot_choice_var.set(bot_choices[0] if bot_choices else "Keine Kanäle geladen")
    bot_menu = tk.OptionMenu(settings_win, bot_choice_var, *(bot_choices if bot_choices else ["Keine Kanäle geladen"]))
    bot_menu.config(bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2")
    bot_menu.pack(padx=20, pady=5, fill="x")
    bot_menu["menu"].config(bg="#40444b", fg="white", activebackground="#7289da", activeforeground="white", bd=0)

    def delete_bot_channel():
        selected = bot_choice_var.get()
        if selected and selected in config.get("bot_channels", {}):
            del config["bot_channels"][selected]
            save_config(config)
            update_dropdown()
            bot_choice_var.set(list(config["bot_channels"].keys())[0] if config["bot_channels"] else "Keine Kanäle geladen")
            messagebox.showinfo("Bot-Kanäle", "Ausgewählter Bot-Kanal entfernt.", parent=settings_win)

    tk.Button(settings_win, text="Ausgewählten Bot-Kanal löschen", bg="#f04747", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2", command=delete_bot_channel).pack(padx=20, pady=(4, 10), anchor="w")

    def save_channel():
        ch_name = name_entry.get().strip()
        ch_url = url_entry.get().strip()
        if not ch_name or not ch_url:
            messagebox.showerror("Error", get_txt("settings_err_fields"), parent=settings_win)
            return
        config["webhooks"][ch_name] = ch_url
        config["last_selected"] = ch_name
        if save_config(config):
            update_dropdown()
            log_message(get_txt("channel_saved").format(name=ch_name), "SUCCESS")
            settings_win.destroy()

    tk.Button(settings_win, text=get_txt("settings_btn_save"), bg="#43b581", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2", command=save_channel).pack(pady=10, ipady=4, ipadx=10)
    tk.Frame(settings_win, height=1, bg="#4f545c").pack(fill="x", padx=20, pady=10)
    tk.Label(settings_win, text=get_txt("settings_lbl_del"), fg="#b9bbbe", bg="#2f3136", font=("Arial", 9)).pack(anchor="w", padx=20)
    
    delete_var = tk.StringVar(settings_win)
    channels_list = list(config["webhooks"].keys())
    delete_var.set(channels_list[0] if channels_list else get_txt("no_channels"))
        
    delete_menu = tk.OptionMenu(settings_win, delete_var, *(channels_list if channels_list else [get_txt("no_channels")]))
    delete_menu.config(bg="#40444b", fg="white", activebackground="#4f545c", activeforeground="white", bd=1, relief="solid", highlightthickness=0, font=("Arial", 10), anchor="w", cursor="hand2")
    delete_menu.pack(padx=20, pady=5, fill="x")
    delete_menu["menu"].config(bg="#40444b", fg="white", activebackground="#7289da", activeforeground="white", bd=0)

    def delete_channel():
        to_delete = delete_var.get()
        if not to_delete or to_delete == get_txt("no_channels"): return
        if messagebox.askyesno(get_txt("settings_confirm_del_title"), get_txt("settings_confirm_del_msg").format(name=to_delete), parent=settings_win):
            del config["webhooks"][to_delete]
            if config.get("last_selected") == to_delete: config["last_selected"] = ""
            save_config(config)
            update_dropdown()
            log_message(get_txt("channel_deleted").format(name=to_delete), "SUCCESS")
            settings_win.destroy()

    tk.Button(settings_win, text=get_txt("settings_btn_del"), bg="#f04747", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2", command=delete_channel).pack(pady=10, ipady=4, ipadx=10)

    def clear_all_channels():
        if not messagebox.askyesno(get_txt("settings_clear_all_confirm_title"), get_txt("settings_clear_all_confirm_msg"), parent=settings_win):
            return
        config["webhooks"] = {}
        config["bot_channels"] = {}
        config["bot_token"] = ""
        config["last_selected"] = ""
        if save_config(config):
            update_dropdown()
            log_message("All saved channels deleted.", "SUCCESS")
            messagebox.showinfo("Kanäle", "Alle gespeicherten Kanäle wurden gelöscht.", parent=settings_win)
            settings_win.destroy()

    tk.Button(settings_win, text=get_txt("settings_btn_clear_all"), bg="#f04747", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2", command=clear_all_channels).pack(pady=(0, 6), ipady=4, ipadx=10)

    def reset_config():
        if not messagebox.askyesno("Reset Configuration", "Möchtest du wirklich alle gespeicherten Einstellungen und Kanäle zurücksetzen?", parent=settings_win):
            return
        try:
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            config.clear()
            config.update({"webhooks": {}, "bot_channels": {}, "bot_token": "", "last_selected": ""})
            save_config(config)
            update_dropdown()
            messagebox.showinfo("Reset", "Die Konfiguration wurde auf den Startzustand zurückgesetzt.", parent=settings_win)
            settings_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Konfiguration konnte nicht zurückgesetzt werden:\n{e}", parent=settings_win)

    tk.Button(settings_win, text=get_txt("settings_btn_reset_config"), bg="#7289da", fg="white", font=("Arial", 9, "bold"), bd=0, cursor="hand2", command=reset_config).pack(pady=(0, 10), ipady=4, ipadx=10)

# ==========================================
# --- SENDEN-LOGIK (API-SCHNITTSTELLE) ---
# ==========================================

def send_webhook():
    log_message(get_txt("send_start"), "INFO")
    config = load_config()
    selected_channel = channel_var.get()
    webhook_url = config.get("webhooks", {}).get(selected_channel)
    bot_channel = config.get("bot_channels", {}).get(selected_channel)
    bot_token = config.get("bot_token", "")

    if not webhook_url and not bot_channel:
        messagebox.showerror("Error", get_txt("err_no_channel_setup"))
        return

    if selected_channel == get_txt("no_channels"):
        messagebox.showerror("Error", get_txt("err_no_channel_setup"))
        return

    normal_content = content_text.get("1.0", tk.END).strip()
    title = title_entry.get().strip()
    description = desc_text.get("1.0", tk.END).strip()
    url = url_entry.get().strip()
    author_name = author_name_entry.get().strip()
    author_icon = author_icon_entry.get().strip()
    author_url = author_url_entry.get().strip()
    thumbnail_url = thumb_entry.get().strip()
    image_url = image_entry.get().strip()
    footer_text = footer_text_entry.get().strip()
    footer_icon = footer_icon_entry.get().strip()

    try: color_dec = int(selected_color_hex, 16)
    except ValueError: color_dec = 3447003

    payload = {"allowed_mentions": {"parse": ["users", "roles", "everyone"], "replied_user": True}}
    if normal_content: payload["content"] = normal_content

    embed = {}
    if title: embed["title"] = title
    if description: embed["description"] = description
    if url: embed["url"] = url
    embed["color"] = color_dec

    if author_name:
        embed["author"] = {"name": author_name}
        if author_url: embed["author"]["url"] = author_url

    files = {}
    file_counter = 1

    def process_image_field(field_value, target_dict, target_key):
        nonlocal file_counter
        if field_value:
            if os.path.exists(field_value) and os.path.isfile(field_value):
                filename = os.path.basename(field_value)
                target_dict[target_key] = f"attachment://{filename}"
                files[f"file_{file_counter}"] = (filename, open(field_value, "rb"))
                file_counter += 1
                log_message(get_txt("local_file_detected").format(key=target_key, file=filename), "INFO")
            else:
                target_dict[target_key] = field_value

    if author_name and author_icon: process_image_field(author_icon, embed["author"], "icon_url")
    if thumbnail_url:
        embed["thumbnail"] = {}
        process_image_field(thumbnail_url, embed["thumbnail"], "url")
    if image_url:
        embed["image"] = {}
        process_image_field(image_url, embed["image"], "url")
    if footer_text or footer_icon:
        embed["footer"] = {}
        if footer_text: embed["footer"]["text"] = footer_text
        if footer_icon: process_image_field(footer_icon, embed["footer"], "icon_url")

    has_embed = any([title, description, author_name, thumbnail_url, image_url, footer_text])
    if not normal_content and not has_embed:
        messagebox.showerror("Error", get_txt("err_empty_payload"))
        for f in files.values(): f[1].close()
        return

    if has_embed: payload["embeds"] = [embed]
    log_message(f"Payload:\n{json.dumps(payload, indent=2)}", "PAYLOAD")

    try:
        if bot_channel:
            endpoint = f"https://discord.com/api/v10/channels/{bot_channel['channel_id']}/messages"
            headers = {"Authorization": f"Bot {bot_token}"}
            if files:
                response = requests.post(endpoint, headers=headers, data={"payload_json": json.dumps(payload)}, files=files)
                for f in files.values(): f[1].close()
            else:
                response = requests.post(endpoint, headers=headers, json=payload)
        else:
            if files:
                response = requests.post(webhook_url, data={"payload_json": json.dumps(payload)}, files=files)
                for f in files.values(): f[1].close()
            else:
                response = requests.post(webhook_url, json=payload)

        if response.status_code in [200, 201, 204]:
            log_message(get_txt("send_success"), "SUCCESS")
            messagebox.showinfo("Success", get_txt("send_success_popup").format(channel=selected_channel))
        else:
            if response.status_code in (401, 403):
                messagebox.showerror("Error", "Der Bot-Token ist ungültig oder abgelaufen, oder der Bot hat keine Berechtigung für diesen Kanal. Bitte einen neuen Bot-Token in den Einstellungen speichern.")
            else:
                messagebox.showerror("Error", f"Discord Error (Status {response.status_code})\n{response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"{get_txt('conn_err')}:\n{e}")

def on_frame_configure(event): canvas.configure(scrollregion=canvas.bbox("all"))
def on_canvas_configure(event): canvas.itemconfig(canvas_window, width=event.width)

# ==========================================
# --- INTERFACE SETUP (GUI) ---
# ==========================================

root.bind_class("Entry", "<Control-v>", safe_paste)

# --- TOP BAR INTERFACE (Responsive Grid-Layout) ---
top_bar = tk.Frame(root, bg="#2f3136", height=50)
top_bar.pack(fill="x", side="top")
top_bar.pack_propagate(False)

top_bar.grid_columnconfigure(0, weight=1)

title_label = tk.Label(top_bar, font=("Arial", 12, "bold"), fg="#ffffff", bg="#2f3136", anchor="w")
title_label.grid(row=0, column=0, sticky="w", padx=15, pady=10)

debug_btn = tk.Button(top_bar, font=("Arial", 9, "bold"), bg="#faa61a", fg="black", bd=0, cursor="hand2", padx=8, command=toggle_debug_window)
debug_btn.grid(row=0, column=1, padx=4, pady=10)

markdown_btn = tk.Button(top_bar, font=("Arial", 9, "bold"), bg="#4f545c", fg="white", bd=0, cursor="hand2", padx=8, command=open_markdown_help)
markdown_btn.grid(row=0, column=2, padx=4, pady=10)

settings_btn = tk.Button(top_bar, font=("Arial", 9, "bold"), bg="#4f545c", fg="white", bd=0, cursor="hand2", padx=8, command=open_settings)
settings_btn.grid(row=0, column=3, padx=4, pady=10)

lang_var = tk.StringVar(root, value="EN")
lang_menu = tk.OptionMenu(top_bar, lang_var, "EN", "DE", command=switch_language)
lang_menu.config(bg="#4f545c", fg="white", activebackground="#7289da", activeforeground="white", bd=0, highlightthickness=0, font=("Arial", 9, "bold"), padx=5, cursor="hand2")
lang_menu.grid(row=0, column=4, padx=15, pady=10)
lang_menu["menu"].config(bg="#40444b", fg="white", activebackground="#7289da", activeforeground="white", bd=0)

# --- CHANNEL SELECT BAR ---
channel_select_bar = tk.Frame(root, bg="#2f3136", height=60)
channel_select_bar.pack(fill="x", side="top", padx=0, pady=(1, 0))
channel_select_bar.pack_propagate(False)

channel_lbl = tk.Label(channel_select_bar, font=("Arial", 10, "bold"), fg="#b9bbbe", bg="#2f3136")
channel_lbl.pack(side="left", padx=(20, 10))

channel_var = tk.StringVar(root)

role_select_frame = tk.Frame(root, bg="#2f3136", height=60)
role_select_frame.pack(fill="x", side="top", padx=0, pady=(0, 1))
role_select_frame.pack_propagate(False)

role_lbl = tk.Label(role_select_frame, font=("Arial", 10, "bold"), fg="#b9bbbe", bg="#2f3136")
role_lbl.pack(side="left", padx=(20, 10), pady=10)

refresh_roles_btn = tk.Button(role_select_frame, text="↻", bg="#4f545c", fg="white", font=("Arial", 10, "bold"), bd=0, cursor="hand2", command=update_role_dropdown)
refresh_roles_btn.pack(side="left", padx=(0, 8), pady=10)

# --- SCROLLBAR SYSTEM ---
canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0, bg="#36393f")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#36393f")

scrollable_frame.bind("<Configure>", on_frame_configure)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.bind("<Configure>", on_canvas_configure)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", _on_mousewheel)
canvas.bind_all("<Button-5>", _on_mousewheel)

def create_styled_field_refs(parent):
    frame = tk.Frame(parent, bg="#36393f")
    frame.pack(fill="x", padx=20, pady=5)
    lbl = tk.Label(frame, font=("Arial", 9, "bold"), fg="#b9bbbe", bg="#36393f")
    lbl.pack(anchor="w", pady=(2, 2))
    entry = tk.Entry(frame, bg="#40444b", fg="#dcddde", insertbackground="white", bd=1, relief="solid", font=("Arial", 10))
    entry.pack(fill="x", ipady=4)
    return lbl, entry

content_frame = tk.Frame(scrollable_frame, bg="#36393f")
content_frame.pack(fill="x", padx=20, pady=(15, 5))
lbl_normal = tk.Label(content_frame, font=("Arial", 9, "bold"), fg="#7289da", bg="#36393f")
lbl_normal.pack(anchor="w", pady=2)
content_text = tk.Text(content_frame, height=4, bg="#40444b", fg="#dcddde", insertbackground="white", bd=1, relief="solid", font=("Arial", 10), wrap="word")
content_text.pack(fill="x")

tk.Frame(scrollable_frame, height=2, bg="#7289da").pack(fill="x", padx=20, pady=15)

lbl_auth_n, author_name_entry = create_styled_field_refs(scrollable_frame)
author_name_entry.bind("<KeyRelease>", check_author_name)
lbl_auth_l, author_url_entry = create_styled_field_refs(scrollable_frame)

lbl_auth_i, author_icon_entry = create_styled_field_refs(scrollable_frame)
author_icon_btn = tk.Button(scrollable_frame, font=("Arial", 8), bd=0, command=lambda: choose_image_for_entry(author_icon_entry, "img_title_auth"))
author_icon_btn.pack(padx=20, pady=(2, 5), anchor="e")

tk.Frame(scrollable_frame, height=1, bg="#2f3136").pack(fill="x", padx=20, pady=10)

lbl_emb_t, title_entry = create_styled_field_refs(scrollable_frame)
lbl_title_l, url_entry = create_styled_field_refs(scrollable_frame)

desc_frame = tk.Frame(scrollable_frame, bg="#36393f")
desc_frame.pack(fill="x", padx=20, pady=5)
lbl_desc_t = tk.Label(desc_frame, font=("Arial", 9, "bold"), fg="#b9bbbe", bg="#36393f")
lbl_desc_t.pack(anchor="w", pady=2)
desc_text = tk.Text(desc_frame, height=6, bg="#40444b", fg="#dcddde", insertbackground="white", bd=1, relief="solid", font=("Arial", 10), wrap="word")
desc_text.pack(fill="x")

tk.Frame(scrollable_frame, height=1, bg="#2f3136").pack(fill="x", padx=20, pady=10)

color_frame = tk.Frame(scrollable_frame, bg="#36393f")
color_frame.pack(fill="x", padx=20, pady=5)
lbl_col_t = tk.Label(color_frame, font=("Arial", 9, "bold"), fg="#b9bbbe", bg="#36393f")
lbl_col_t.pack(anchor="w", pady=2)
color_button = tk.Button(color_frame, bg=f"#{DEFAULT_COLOR}", fg="white", font=("Arial", 10, "bold"), bd=0, height=2, cursor="hand2", command=pick_color)
color_button.pack(fill="x", pady=2)

tk.Frame(scrollable_frame, height=1, bg="#2f3136").pack(fill="x", padx=20, pady=10)

lbl_thub_t, thumb_entry = create_styled_field_refs(scrollable_frame)
thumb_btn = tk.Button(scrollable_frame, bg="#4f545c", fg="white", font=("Arial", 8), bd=0, cursor="hand2", command=lambda: choose_image_for_entry(thumb_entry, "img_title_thumb"))
thumb_btn.pack(padx=20, pady=(2, 5), anchor="e")

lbl_main_t, image_entry = create_styled_field_refs(scrollable_frame)
main_img_btn = tk.Button(scrollable_frame, bg="#4f545c", fg="white", font=("Arial", 8), bd=0, cursor="hand2", command=lambda: choose_image_for_entry(image_entry, "img_title_main"))
main_img_btn.pack(padx=20, pady=(2, 5), anchor="e")

tk.Frame(scrollable_frame, height=1, bg="#2f3136").pack(fill="x", padx=20, pady=10)

lbl_foot_t, footer_text_entry = create_styled_field_refs(scrollable_frame)

lbl_footi_t, footer_icon_entry = create_styled_field_refs(scrollable_frame)
footer_icon_btn = tk.Button(scrollable_frame, bg="#4f545c", fg="white", font=("Arial", 8), bd=0, cursor="hand2", command=lambda: choose_image_for_entry(footer_icon_entry, "img_title_footer"))
footer_icon_btn.pack(padx=20, pady=(2, 5), anchor="e")

# --- BOTTOM BAR ---
bottom_bar = tk.Frame(root, bg="#2f3136", height=70)
bottom_bar.pack(fill="x", side="bottom")
bottom_bar.pack_propagate(False)

clear_btn = tk.Button(bottom_bar, bg="#f04747", fg="white", font=("Arial", 11, "bold"), bd=0, cursor="hand2", command=clear_all_fields)
clear_btn.pack(side="left", fill="y", padx=(20, 10), pady=12, ipadx=15)

send_btn = tk.Button(bottom_bar, bg="#43b581", fg="white", font=("Arial", 12, "bold"), bd=0, cursor="hand2", command=send_webhook)
send_btn.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=12)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

log_message("System initialized. Environment loading.", "INFO")
switch_language("EN")

root.mainloop()