import asyncio
import platform
import tkinter as tk
from tkinter import messagebox
import threading
import json

# Import your modules (REAL LOGIC LIVES HERE)
from batterypercentage import get_battery
from list_devices import get_devices
from pairunpair import unpair_device

if platform.system() != "Windows":
    print("This app only works on Windows")
    exit()

FAVORITES_FILE = "favorites.json"


# ---------------- Favorites ----------------
def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_favorites(favs):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(list(favs), f)


# ---------------- GUI ----------------
class BluetoothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluetooth Manager")
        self.root.geometry("450x500")

        self.devices = []
        self.favorites = load_favorites()

        self.listbox = tk.Listbox(root, width=55)
        self.listbox.pack(pady=10)

        self.status = tk.Label(root, text="")
        self.status.pack()

        # Buttons
        tk.Button(root, text="Refresh", command=self.refresh).pack(pady=2)
        tk.Button(root, text="Battery", command=self.check_battery).pack(pady=2)
        tk.Button(root, text="Unpair", command=self.unpair).pack(pady=2)
        tk.Button(root, text="Toggle Favorite", command=self.toggle_favorite).pack(pady=2)

        self.refresh()
        self.auto_refresh()

    # ---------------- Async runner ----------------
    def run_async(self, coro, callback=None):
        def task():
            result = asyncio.run(coro)
            if callback:
                self.root.after(0, lambda: callback(result))

        threading.Thread(target=task).start()

    # ---------------- Refresh devices ----------------
    def refresh(self):
        def update(devs):
            self.devices = devs
            self.listbox.delete(0, tk.END)

            for d in devs:
                name = d.name
                if d.id in self.favorites:
                    name += " ⭐"
                self.listbox.insert(tk.END, name)

            self.status.config(text=f"{len(devs)} devices found")

        self.run_async(get_devices(), update)

    # ---------------- Auto refresh ----------------
    def auto_refresh(self):
        self.refresh()
        self.root.after(5000, self.auto_refresh)

    # ---------------- Helper ----------------
    def get_selected_device(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        return self.devices[idx[0]]

    # ---------------- Battery ----------------
    def check_battery(self):
        device = self.get_selected_device()
        if not device:
            messagebox.showwarning("Select device", "Pick a device first")
            return

        def task():
            return asyncio.run(get_battery(device))

        def show(result):
            if result is None:
                messagebox.showinfo("Battery", "Not available")
            else:
                messagebox.showinfo("Battery", f"{device.name}: {result}%")

        threading.Thread(target=lambda: show(task())).start()

    # ---------------- Unpair ----------------
    def unpair(self):
        device = self.get_selected_device()
        if not device:
            return

        def task():
            return asyncio.run(unpair_device(device))

        def show(result):
            messagebox.showinfo("Unpair", result)

        threading.Thread(target=lambda: show(task())).start()

    # ---------------- Favorites ----------------
    def toggle_favorite(self):
        device = self.get_selected_device()
        if not device:
            return

        if device.id in self.favorites:
            self.favorites.remove(device.id)
        else:
            self.favorites.add(device.id)

        save_favorites(self.favorites)
        self.refresh()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()