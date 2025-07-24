import tkinter as tk
import threading
import serial_connection  # Handles serial communication

octave = 4

def make_piano_gui():
    root = tk.Tk()
    root.title("Piano GUI")

    canvas = tk.Canvas(root, width=700, height=200)
    canvas.pack()

    white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    black_keys = ['c', 'd', '', 'f', 'g', 'a', '']  # Lowercase to distinguish from white keys if needed

    key_width = 100
    key_height = 200
    black_key_width = 60
    black_key_height = 120

    key_map = {}
    key_colors = {}
    pressed_color = "#bbbbbb"
    pressed_black = "#333333"
    current_pressed_key = None
    send_loop_id = None
    held_note = None

    def press_key_visual(item):
        original_color = key_colors[item]
        color = pressed_color if original_color == 'white' else pressed_black
        canvas.itemconfig(item, fill=color)
        return original_color

    def release_key_visual(item, original_color):
        canvas.itemconfig(item, fill=original_color)

    def send_note_continuously(note):
        nonlocal send_loop_id, held_note
        held_note = note
        note_byte = note.encode('ascii')  # one-byte
        octave_byte = bytes([octave])     # single-byte integer
        serial_connection.send_to_arduino(note_byte + octave_byte)
        send_loop_id = canvas.after(100, lambda: send_note_continuously(note))


    def stop_sending_note():
        nonlocal send_loop_id, held_note
        if send_loop_id:
            canvas.after_cancel(send_loop_id)
            send_loop_id = None
            held_note = None
        serial_connection.send_to_arduino(b"XX")  # signal to stop

    def on_mouse_down(event):
        nonlocal current_pressed_key
        item = canvas.find_closest(event.x, event.y)[0]
        note = key_map.get(item)
        if note:
            original_color = press_key_visual(item)
            current_pressed_key = (item, original_color)
            send_note_continuously(note)

    def on_mouse_up(event):
        nonlocal current_pressed_key
        if current_pressed_key:
            item, original_color = current_pressed_key
            release_key_visual(item, original_color)
            current_pressed_key = None
            stop_sending_note()

    # Draw white keys
    for i, note in enumerate(white_keys):
        x = i * key_width
        rect = canvas.create_rectangle(x, 0, x + key_width, key_height, fill='white', outline='black')
        canvas.create_text(x + key_width // 2, key_height - 20, text=note)
        key_map[rect] = note
        key_colors[rect] = 'white'

    # Draw black keys
    for i, note in enumerate(black_keys):
        if note:
            x = (i + 1) * key_width - black_key_width // 2
            rect = canvas.create_rectangle(x, 0, x + black_key_width, black_key_height, fill='black', outline='black')
            canvas.create_text(x + black_key_width // 2, black_key_height - 20, text=note.upper(), fill='white')
            key_map[rect] = note
            key_colors[rect] = 'black'

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

if __name__ == "__main__":
    threading.Thread(target=serial_connection.start_serial, daemon=True).start()
    make_piano_gui()
