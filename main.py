import time
import tkinter as tk
from tkinter import ttk, font
from telethon import TelegramClient
import asyncio
import threading
from datetime import datetime, timedelta
import random
import json

api_id = your-api-id
api_hash = 'your-api-hash'
phone_number = 'your-number-with+'

client = TelegramClient(phone_number, api_id, api_hash)

# Global variables to manage messaging tasks and state
messaging_task = None
is_paused = False
pause_event = asyncio.Event()
loop = asyncio.get_event_loop()


def start_messaging(groups_input, message_entry, time_interval_entry, time_left_var, resume=False):
    global messaging_task, is_paused, pause_event
    if not resume:
        user_message = message_entry.get()
        groups = [group.strip() for group in groups_input.get().split(',')]
        if not user_message.strip():
            time_left_var.set("Введите сообщение.")
            return
        if not groups:
            time_left_var.set("Пожалуйста, введите хотя бы один ID группы.")
            return
        try:
            interval = float(time_interval_entry.get()) * 60
            if interval <= 0:
                raise ValueError("Интервал времени должен быть положительным числом.")
        except ValueError as e:
            time_left_var.set(f"Неверный интервал времени: {e}")
            return
        message_to_send = f"{user_message}\nдля полной информации о работе <a href='https://t.me/All_Jobs_in_Israel'>пишите</a> 👈"

    def update_gui(text):
        time_left_var.set(text)

    async def periodic_messaging(groups, message_to_send, interval_seconds, update_callback, parse_mode='html'):
        await client.start()
        while True:
            if is_paused:
                await pause_event.wait()
            for group in groups:
                try:
                    await client.send_message(group, message_to_send, parse_mode=parse_mode)
                    update_callback(f"Сообщение успешно отправлено в {group}!")
                except Exception as e:
                    update_callback(f"Произошла ошибка: {e}")
                # update_callback("Подготовка к отсчету...")
                await asyncio.sleep(random.randint(6, 10))  # Simulating sending time
            # Countdown logic after sending the message to all groups
            next_send_time = datetime.now() + timedelta(seconds=interval_seconds)
            while datetime.now() < next_send_time:
                if is_paused:
                    await pause_event.wait()
                remaining_seconds = int((next_send_time - datetime.now()).total_seconds())
                next_time_str = next_send_time.strftime('%Y-%m-%d %H:%M:%S')
                update_callback(f"Следующее сообщение через {remaining_seconds} секунд в {next_time_str}")
                await asyncio.sleep(1)

    if not resume:
        if messaging_task:
            messaging_task.cancel()
        messaging_task = asyncio.run_coroutine_threadsafe(
            periodic_messaging(groups, user_message, interval, update_gui, 'html'), loop)


def stop_messaging():
    global is_paused, pause_event
    print("Останавливаю")
    is_paused = True
    pause_event.clear()


def resume_messaging(groups_input, message_entry, time_interval_entry, time_left_var):
    global is_paused, pause_event, messaging_task
    if messaging_task and messaging_task.done():
        print("Task is completed, restarting...")
        start_messaging(groups_input, message_entry, time_interval_entry, time_left_var, resume=True)
    elif is_paused:
        print("Resuming messaging...")
        is_paused = False
        pause_event.set()
    else:
        print("Messaging is not paused; no action taken.")


root = tk.Tk()
root.title("Бот v1 от @ali_codz")
root.geometry("1920x1080")

loop = asyncio.get_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()

LABEL_FONT = ("Verdana", 8)
LARGE_FONT = ("Verdana", 10)
BUTTON_FONT = ("Verdana", 8, 'bold')

# Define frame width and height
frame_width = 200  # Example width
frame_height = 100  # Example height

top_section = ttk.Frame(root)
top_section.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

left_frame = ttk.Frame(top_section, width=frame_width, height=frame_height)
left_frame.grid_propagate(False)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 2.5), pady=2.5)

middle_frame = ttk.Frame(top_section, width=frame_width, height=frame_height)
middle_frame.grid_propagate(False)
middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2.5, pady=2.5)

right_frame = ttk.Frame(top_section, width=frame_width, height=frame_height)
right_frame.grid_propagate(False)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2.5, 5), pady=2.5)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill=tk.X, padx=5, pady=5)  # Reduced padding for the separator

lower_section = ttk.Frame(root)
lower_section.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=6)  # Reduced padding to bring sections closer

lower_left_frame = ttk.Frame(lower_section, width=frame_width, height=frame_height)
lower_left_frame.grid_propagate(False)
lower_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 2.5), pady=2.5)

lower_middle_frame = ttk.Frame(lower_section, width=frame_width, height=frame_height)
lower_middle_frame.grid_propagate(False)
lower_middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2.5, pady=2.5)

lower_right_frame = ttk.Frame(lower_section, width=frame_width, height=frame_height)
lower_right_frame.grid_propagate(False)
lower_right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2.5, 5), pady=2.5)

middle_separator = ttk.Separator(root, orient='horizontal')
middle_separator.pack(fill=tk.X, padx=5, pady=5)

bottom_section = ttk.Frame(root)
bottom_section.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=5)  # Reduced padding to bring sections closer

bottom_left_frame = ttk.Frame(bottom_section, width=frame_width, height=frame_height)
bottom_left_frame.grid_propagate(False)
bottom_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 2.5), pady=2.5)

bottom_middle_frame = ttk.Frame(bottom_section, width=frame_width, height=frame_height)
bottom_middle_frame.grid_propagate(False)
bottom_middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2.5, pady=2.5)

bottom_right_frame = ttk.Frame(bottom_section, width=frame_width, height=frame_height)
bottom_right_frame.grid_propagate(False)
bottom_right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2.5, 5), pady=2.5)


def save_data(groups_data):
    with open("groups_dataa.json", "w") as f:
        json.dump(groups_data, f)


def load_data():
    try:
        with open("groups_dataa.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def create_group_ui(frame, group_number):
    saved_data = load_data()

    message_key = f"group_{group_number}_message"
    groups_key = f"group_{group_number}_groups"
    interval_key = f"group_{group_number}_interval"

    ttk.Label(frame, text=f"Сообщение для группы {group_number}:", font=LABEL_FONT).pack(pady=(10, 0))
    message_entry = ttk.Entry(frame, font=LARGE_FONT, width=35)
    message_entry.insert(0, saved_data.get(message_key, ""))  # Use saved data if available
    message_entry.pack(pady=5)

    ttk.Label(frame, text=f"ID групп(ы) для группы {group_number} (через запятую):", font=LABEL_FONT).pack(pady=(5, 0))
    groups_input = ttk.Entry(frame, font=LARGE_FONT, width=35)
    groups_input.insert(0, saved_data.get(groups_key, ""))  # Use saved data if available
    groups_input.pack(pady=5)

    ttk.Label(frame, text=f"Интервал времени для группы {group_number} (в минутах):", font=LABEL_FONT).pack(pady=(5, 0))
    time_interval_entry = ttk.Entry(frame, font=LARGE_FONT, width=35)
    time_interval_entry.insert(0, saved_data.get(interval_key, ""))  # Use saved data if available
    time_interval_entry.pack(pady=5)

    button_frame = ttk.Frame(frame)  # Frame to hold buttons for layout purposes
    button_frame.pack(fill=tk.X, expand=False, pady=(5, 0))

    time_left_var = tk.StringVar(value="Напишите сообщение")
    ttk.Button(button_frame, text=f"Отправить сообщение в группу{group_number}", style='TButton', width=35,
               command=lambda: start_messaging(groups_input, message_entry, time_interval_entry, time_left_var)).pack(
        side=tk.TOP, expand=False)

    button_style = ttk.Style()
    button_style.configure('Small.TButton', font=("Verdana", 8, 'bold'))

    stop_button = ttk.Button(button_frame, text=f"Остановить сообщения в {group_number}", style='Small.TButton',
                             command=stop_messaging)
    stop_button.pack(side=tk.LEFT, padx=5, pady=(2, 5), expand=True)

    resume_button = ttk.Button(button_frame, text=f"Возобновить сообщения в {group_number}", style='Small.TButton',
                               command=lambda: resume_messaging(groups_input, message_entry, time_interval_entry,
                                                                time_left_var))
    resume_button.pack(side=tk.RIGHT, padx=5, pady=(2, 5), expand=True)

    ttk.Label(frame, textvariable=time_left_var, font=LABEL_FONT).pack(pady=5)

    return {
        'message_entry': message_entry,
        'groups_input': groups_input,
        'time_interval_entry': time_interval_entry
    }

group_widgets = {}

group_widgets[1] = create_group_ui(left_frame, 1)
group_widgets[2] = create_group_ui(middle_frame, 2)
group_widgets[3] = create_group_ui(right_frame, 3)
group_widgets[4] = create_group_ui(bottom_left_frame, 4)
group_widgets[5] = create_group_ui(bottom_middle_frame, 5)
group_widgets[6] = create_group_ui(bottom_right_frame, 6)
group_widgets[7] = create_group_ui(lower_left_frame, 7)
group_widgets[8] = create_group_ui(lower_middle_frame, 8)
group_widgets[9] = create_group_ui(lower_right_frame, 9)


def on_close():
    groups_data = {}
    for i in range(1, 10):  # Assuming you have 9 groups
        group_widget = group_widgets[i]
        groups_data[f"group_{i}_message"] = group_widget['message_entry'].get()
        groups_data[f"group_{i}_groups"] = group_widget['groups_input'].get()
        groups_data[f"group_{i}_interval"] = group_widget['time_interval_entry'].get()
    save_data(groups_data)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

style = ttk.Style()
style.configure('TButton', font=BUTTON_FONT, padding=6)
style.configure('TEntry', padding=6)
root.mainloop()
