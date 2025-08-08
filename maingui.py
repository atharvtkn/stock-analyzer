import main
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt

class StockApp:
    def __init__(self):
        self.sa = main.StockAnalyzer()

        self.root = ctk.CTk()
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')
        self.root.geometry('900x650')
        self.root.title('Stock Price Analyzer')

        self.periods = ["5d", "1mo", "3mo", "6mo", "1y", "2y"]

        self.title_label = ctk.CTkLabel(
            self.root, text="📈 STOCK PRICE ANALYZER",
            font=('Segoe UI', 26, 'bold'), text_color='#0D47A1'
        )
        self.title_label.pack(pady=(10, 5))

        self.subtitle = ctk.CTkLabel(
            self.root, text="Analyze and visualize stock market trends",
            font=('Segoe UI', 14), text_color='#1565C0'
        )
        self.subtitle.pack(pady=(0, 20))

        self.ticker_label = ctk.CTkLabel(self.root, text="Enter Stock Symbol:", font=('Segoe UI', 14))
        self.ticker_label.pack()
        self.ticker_entry = ctk.CTkEntry(self.root, width=250, font=('Segoe UI', 14))
        self.ticker_entry.pack(pady=(0, 10))

        self.period_label = ctk.CTkLabel(self.root, text="Select Time Period:", font=('Segoe UI', 14))
        self.period_label.pack()
        self.period_choice = ctk.StringVar(value=self.periods[0])
        self.period_menu = ctk.CTkOptionMenu(self.root, variable=self.period_choice, values=self.periods, font=('Segoe UI', 14))
        self.period_menu.pack(pady=(0, 15))

        self.fetch_btn = ctk.CTkButton(self.root, text="Fetch Data", command=self.fetch_data, width=200)
        self.fetch_btn.pack(pady=5)
        self.summary_btn = ctk.CTkButton(self.root, text="Show Summary", command=self.show_summary, width=200)
        self.summary_btn.pack(pady=5)
        self.visualize_btn = ctk.CTkButton(self.root, text="Visualize Prices", command=self.visualize, width=200)
        self.visualize_btn.pack(pady=5)
        self.clear_btn = ctk.CTkButton(self.root, text="Clear Saved Data", command=self.clear_data, width=200)
        self.clear_btn.pack(pady=10)

        self.terminal_label = ctk.CTkLabel(self.root, text="Output Log:", font=('Segoe UI', 14, 'bold'))
        self.terminal_label.pack()
        self.terminal = ctk.CTkTextbox(self.root, width=700, height=180, font=('Consolas', 13))
        self.terminal.pack(pady=(0, 10))
        self.terminal.configure(state='disabled')

        self.df_cache = None
        self.root.mainloop()

    def update_terminal(self, message):
        self.terminal.configure(state='normal')
        self.terminal.delete('1.0', 'end')
        self.terminal.insert('end', message)
        self.terminal.configure(state='disabled')

    def fetch_data(self):
        symbol = self.ticker_entry.get().strip()
        period = self.period_choice.get()
        if not symbol:
            self.update_terminal("❌ Please enter a stock symbol.")
            return

        ok, result = self.sa.fetch_data(symbol, period)
        if not ok:
            self.update_terminal("❌ " + result)
        else:
            self.df_cache = result
            self.update_terminal(f"✅ Data fetched for {symbol.upper()} ({period}).")

    def show_summary(self):
        if self.df_cache is None:
            self.update_terminal("❌ Fetch data first.")
            return
        summary = self.sa.show_summary(self.df_cache)
        self.update_terminal(summary)

    def visualize(self):
        if self.df_cache is None:
            self.update_terminal("❌ Fetch data first.")
            return
        self.sa.visualize(self.df_cache)
        self.update_terminal("📊 Chart displayed.")

    def clear_data(self):
        confirm = CTkMessagebox(title="Clear Saved Data",
                                message="Are you sure you want to clear all saved stock data?",
                                icon="warning", option_1="No", option_2="Yes")
        if confirm.get() == "Yes":
            self.sa.clear_data()
            self.update_terminal("🗑️ All saved data cleared.")

if __name__ == "__main__":
    StockApp()
