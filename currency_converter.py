import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Function to fetch currency list from API
def get_currencies():
    url = "https://api.exchangerate.host/symbols"
    try:
        response = requests.get(url)
        data = response.json()

        if "symbols" in data:
            return sorted(data["symbols"].keys())
        else:
            messagebox.showerror("API Error", "Failed to fetch currency list. Using fallback.")
            return ["USD", "INR", "EUR", "GBP"]
    except Exception as e:
        messagebox.showerror("Network Error", f"Could not reach the currency API.\n{e}")
        return ["USD", "INR", "EUR", "GBP"]

# Function to perform currency conversion
def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combo.get()
        to_currency = to_currency_combo.get()

        if not from_currency or not to_currency:
            messagebox.showerror("Input Error", "Please select both currencies.")
            return

        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        response = requests.get(url)
        data = response.json()

        if "result" in data:
            converted_amount = data["result"]
            result_label.config(
                text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
            )
        else:
            messagebox.showerror("Conversion Error", "Invalid conversion result from API.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")

# GUI setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x260")
root.resizable(False, False)

currency_list = get_currencies()

tk.Label(root, text="Amount:").pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

tk.Label(root, text="From Currency:").pack(pady=5)
from_currency_combo = ttk.Combobox(root, values=currency_list, state="readonly")
from_currency_combo.set("USD")
from_currency_combo.pack(pady=5)

tk.Label(root, text="To Currency:").pack(pady=5)
to_currency_combo = ttk.Combobox(root, values=currency_list, state="readonly")
to_currency_combo.set("INR")
to_currency_combo.pack(pady=5)

tk.Button(root, text="Convert", command=convert_currency).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
