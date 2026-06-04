import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import urllib.request
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Meteorological Analysis Dashboard (FastAPI Powered)")
        self.root.geometry("1200x750")
        self.root.configure(bg="#1E1E24") 
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('.', background='#1E1E24', foreground='#FFFFFF')
        self.style.configure('TFrame', background='#1E1E24')
        self.style.configure('TLabelframe', background='#2A2A35', bordercolor='#3A3A4A')
        self.style.configure('TLabelframe.Label', background='#2A2A35', foreground='#A0A0B0', font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('TLabel', background='#1E1E24', foreground='#E0E0E0', font=('Segoe UI', 10))
        self.style.configure('KPI.TLabel', background='#2A2A35', foreground='#FFFFFF', font=('Segoe UI', 12))
        self.style.configure('KPITitle.TLabel', background='#2A2A35', foreground='#A0A0B0', font=('Segoe UI', 9, 'bold'))
        
        self.style.configure('Accent.TButton', background='#007ACC', foreground='#FFFFFF', font=('Segoe UI', 10, 'bold'), borderwidth=0)
        self.style.map('Accent.TButton', background=[('active', '#0098FF'), ('disabled', '#3A3A4A')])
        
        self.create_widgets()
        
    def create_widgets(self):
        top_container = ttk.Frame(self.root, padding=15)
        top_container.pack(side=tk.TOP, fill=tk.X)
        
        input_card = tk.Frame(top_container, bg='#2A2A35', padx=15, pady=12, bd=0)
        input_card.pack(fill=tk.X)
        
        lbl_location = tk.Label(input_card, text="Search Location:", bg='#2A2A35', fg='#FFFFFF', font=('Segoe UI', 10, 'bold'))
        lbl_location.pack(side=tk.LEFT, padx=(0, 5))
        
        self.location_entry = tk.Entry(input_card, width=25, font=('Segoe UI', 10), bg='#1E1E24', fg='#FFFFFF', insertbackground='white', bd=1, relief='flat')
        self.location_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=3)
        self.location_entry.insert(0, "Vancouver, Canada")
        
        lbl_start = tk.Label(input_card, text="Start Date:", bg='#2A2A35', fg='#CCCCCC', font=('Segoe UI', 10))
        lbl_start.pack(side=tk.LEFT, padx=(0, 5))
        self.start_date_entry = tk.Entry(input_card, width=12, font=('Segoe UI', 10), bg='#1E1E24', fg='#FFFFFF', insertbackground='white', bd=1, relief='flat')
        self.start_date_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=3)
        self.start_date_entry.insert(0, "2025-01-01")
        
        lbl_end = tk.Label(input_card, text="End Date:", bg='#2A2A35', fg='#CCCCCC', font=('Segoe UI', 10))
        lbl_end.pack(side=tk.LEFT, padx=(0, 5))
        self.end_date_entry = tk.Entry(input_card, width=12, font=('Segoe UI', 10), bg='#1E1E24', fg='#FFFFFF', insertbackground='white', bd=1, relief='flat')
        self.end_date_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=3)
        self.end_date_entry.insert(0, "2025-01-20")
        
        self.search_btn = ttk.Button(input_card, text="Analyze Weather", style='Accent.TButton', command=self.start_analysis_thread)
        self.search_btn.pack(side=tk.LEFT, padx=(10, 10))
        
        self.progress_bar = ttk.Progressbar(input_card, mode='indeterminate', length=120)
        
        sidebar_container = ttk.Frame(self.root, padding=(15, 0, 10, 15))
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y)
        
        temp_card = tk.Frame(sidebar_container, bg='#2A2A35', width=220, height=120, bd=0)
        temp_card.pack_propagate(False)
        temp_card.pack(side=tk.TOP, pady=(0, 15))
        ttk.Label(temp_card, text="MEAN TEMP HIGH", style='KPITitle.TLabel').pack(anchor=tk.W, padx=15, pady=(15, 5))
        self.temp_stat_lbl = ttk.Label(temp_card, text="-- °C", font=('Segoe UI', 20, 'bold'), background='#2A2A35', foreground='#FF5C5C')
        self.temp_stat_lbl.pack(anchor=tk.W, padx=15)

        rain_card = tk.Frame(sidebar_container, bg='#2A2A35', width=220, height=120, bd=0)
        rain_card.pack_propagate(False)
        rain_card.pack(side=tk.TOP)
        ttk.Label(rain_card, text="TOTAL PRECIPITATION", style='KPITitle.TLabel').pack(anchor=tk.W, padx=15, pady=(15, 5))
        self.rain_stat_lbl = ttk.Label(rain_card, text="-- mm", font=('Segoe UI', 20, 'bold'), background='#2A2A35', foreground='#3CAEA3')
        self.rain_stat_lbl.pack(anchor=tk.W, padx=15)

        self.chart_frame = ttk.Frame(self.root, padding=(5, 0, 15, 15))
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.fig, self.ax1 = plt.subplots(figsize=(8, 5))
        self.fig.patch.set_facecolor('#1E1E24') 
        self.ax1.set_facecolor('#2A2A35')      
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_analysis_thread(self):
        self.search_btn.config(state=tk.DISABLED)
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        self.progress_bar.start(10)
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def run_analysis(self):
        query = self.location_entry.get().strip()
        start = self.start_date_entry.get().strip()
        end = self.end_date_entry.get().strip()
        
        payload = {
            "location": query,
            "start_date": start,
            "end_date": end
        }
        
        try:
            data_bytes = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                "http://127.0.0.1:8000/api/weather", 
                data=data_bytes, 
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                api_response = json.loads(response.read().decode())
                
            self.root.after(0, self.update_ui_success, api_response, start, end)
            
        except Exception as e:
            self.root.after(0, self.update_ui_failure, str(e))

    def update_ui_success(self, api_data, start, end):
        self.fig.clear()
        self.fig.patch.set_facecolor('#1E1E24')
        
        ax1 = self.fig.add_subplot(111)
        ax1.set_facecolor('#2A2A35')
        
        chart_info = api_data["chart_data"]
        dates = pd.to_datetime(chart_info["dates"])
        temps = chart_info["max_temps"]
        rainfall = chart_info["rainfall"]
        
        color_temp = '#FF5C5C'
        ax1.set_xlabel('Date', fontweight='bold', labelpad=10, color='#A0A0B0')
        ax1.set_ylabel('Max Temperature (°C)', color=color_temp, fontweight='bold')
        
        line1 = ax1.plot(dates, temps, color=color_temp, marker='o', linewidth=2.5, label='Temp High', zorder=3)
        ax1.tick_params(axis='y', labelcolor=color_temp, colors='#A0A0B0')
        ax1.tick_params(axis='x', colors='#A0A0B0')
        ax1.grid(True, alpha=0.1, linestyle='-', color='#FFFFFF')
        
        ax2 = ax1.twinx()
        color_rain = '#3CAEA3'
        ax2.set_ylabel('Daily Precipitation (mm)', color=color_rain, fontweight='bold')
        
        bar1 = ax2.bar(dates, rainfall, color=color_rain, alpha=0.4, width=0.5, label='Rainfall', zorder=2)
        ax2.tick_params(axis='y', labelcolor=color_rain, colors='#A0A0B0')
        
        for ax in [ax1, ax2]:
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_color('#3A3A4A')
            ax.spines['left'].set_color('#3A3A4A')
            ax.spines['right'].set_color('#3A3A4A')

        self.fig.autofmt_xdate()
        ax1.set_title(f"FastAPI Powered Analysis: {api_data['full_name']}\n({start} to {end})", 
                      fontsize=12, fontweight='bold', pad=15, color='#FFFFFF')
        
        lns = line1 + [bar1]
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left', frameon=True, facecolor='#2A2A35', edgecolor='#3A3A4A')
        plt.setp(ax1.get_legend().get_texts(), color='#E0E0E0')
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        self.temp_stat_lbl.config(text=f"{api_data['mean_max_temp']:.1f} °C")
        self.rain_stat_lbl.config(text=f"{api_data['total_precipitation']:.1f} mm")
        
        self.stop_progress_animation()

    def update_ui_failure(self, error_msg):
        self.stop_progress_animation()
        messagebox.showerror("FastAPI Router Error", f"Sunucudan analiz verileri çekilemedi:\n\n{error_msg}")

    def stop_progress_animation(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.search_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()