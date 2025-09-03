import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QTabWidget, QWidget, QSizePolicy
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from metrics_monitoring import get_percent_data_from_db, get_cpu_time_distribution, get_ram_data_from_db, get_cpu_time_trend  # Import your DB function
# from PyQt5.QtWidgets import QSizePolicy
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=140):
        self.fig = Figure(dpi=dpi, constrained_layout=True)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1800, 1000)
        self.setWindowTitle("Live System Metrics Dashboard")

        # --- Create all 4 canvas blocks ---
        self.canvas_line_chart = MplCanvas(self, dpi=140)
        self.canvas_doughnut = MplCanvas(self, dpi=140)
        self.canvas_cpu_area_chart = MplCanvas(self, dpi=140)
        self.canvas_area_chart = MplCanvas(self, dpi=140)

        # --- For colorbar cleanup ---
        # self.canvas_scatter.cbar = None # no longer required

        # --- Layout setup ---
        tabs = QTabWidget()           # Create the QTabWidget
        # Add canvases (charts) as individual tabs
        tabs.addTab(self.canvas_line_chart, "System metrics Line Chart")
        tabs.addTab(self.canvas_doughnut, "CPU Time Distribution")
        tabs.addTab(self.canvas_cpu_area_chart, "CPU Time Area Chart")
        tabs.addTab(self.canvas_area_chart, "RAM Usage Area Chart")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # --- Timer Setup ---
        self.timer = QTimer()
        self.timer.setInterval(60 * 1000)  # 60 seconds
        self.timer.timeout.connect(self.update_charts)
        self.timer.start()

        # Initial chart load
        self.update_charts()

    def update_charts(self):
        self.update_line_chart()
        self.update_doughnut_chart()
        self.update_cpu_area_chart()
        self.update_area_chart()

    def update_line_chart(self):
        data = get_percent_data_from_db()
        if not data:
            return

        timestamps = [row[0] for row in data]
        cpu_percent = [row[1] for row in data]
        battery_percent = [row[2] for row in data]
        ram_percent = [row[3] for row in data]

        ax = self.canvas_line_chart.ax
        ax.clear()

        ax.plot(timestamps, cpu_percent, marker='o', color='blue', label='CPU %')
        ax.plot(timestamps, battery_percent, marker='x', color='green', label='Battery %')
        ax.plot(timestamps, ram_percent, marker='s', color='red', label='RAM %')

        ax.set_title("System Metrics Over Time")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Percentage")
        ax.tick_params(axis='x', rotation=45)

        # Fix the legend to top-right inside the plot
        # ax.legend(loc='upper right', frameon=True)

        # OR: To place legend outside the plot, use this instead:
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # self.canvas_line_chart.fig.tight_layout()
        self.canvas_line_chart.draw()

    def update_doughnut_chart(self):
        cpu_data = get_cpu_time_distribution()
        labels = list(cpu_data.keys())
        sizes_sec = list(cpu_data.values())
        sizes_min = [s / 60 for s in sizes_sec]  # ✅ Convert to minutes
        total = sum(sizes_min)
        colors = ['#66b3ff', '#ff9999', '#99ff99']  # Customize as needed

        ax = self.canvas_doughnut.ax
        ax.clear()

        wedges, _ = ax.pie(
            sizes_min,
            labels=None,
            colors=colors,
            startangle=90,
            autopct=None,
            wedgeprops={'width': 0.4}
        )

        ax.set_title("CPU Time Distribution (User / Kernel / Idle) in minutes")
        ax.axis('equal')

        # Create custom legend labels: "Label: XX.X% (Value)"
        legend_labels = [
            f"{label}: {size / total * 100:.1f}% ({size:.1f} min)"
            for label, size in zip(labels, sizes_min)
        ]

        # Add the legend with the same colors
        ax.legend(
            wedges,
            legend_labels,
            title="Legend",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        self.canvas_doughnut.draw()
    
    def update_cpu_area_chart(self):
        data = get_cpu_time_trend()
        if not data:
            return

        timestamps = [row[0] for row in data]
        user_times = [row[1] for row in data]
        system_times = [row[2] for row in data]
        idle_times = [row[3] for row in data]

        ax = self.canvas_cpu_area_chart.ax
        ax.clear()

        times_num = mdates.date2num(timestamps)

        # Plot stacked area chart
        ax.stackplot(
            times_num,
            user_times,
            system_times,
            idle_times,
            labels=['User Time', 'System Time', 'Idle Time'],
            colors=['#66b3ff', '#ffcc99', '#c2f0c2'],
            alpha=0.8
        )

        ax.set_title("CPU Utilization Breakdown Over Time")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("CPU Time (seconds)")
        ax.legend(loc='upper left')
        ax.grid(True)

        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
        ax.tick_params(axis='x', rotation=45)

        self.canvas_cpu_area_chart.draw()
    
    def update_area_chart(self):
        data = get_ram_data_from_db()  # New function to fetch RAM data
        if not data:
            return
        
        timestamps = [row[0] for row in data]

        # Convert all values from Bytes to GB
        to_gb = lambda x: x/ (1024 ** 3)

        total_ram = [to_gb(row[1]) for row in data]
        used_ram = [to_gb(row[2]) for row in data]
        available_ram = [to_gb(row[3]) for row in data]

        ax = self.canvas_area_chart.ax
        ax.clear()

        # Convert timestamps to matplotlib date format
        times_num = mdates.date2num(timestamps)

        # Plot stacked area chart of used + available RAM
        ax.stackplot(
            times_num,
            used_ram,
            available_ram,
            labels=['Used RAM', 'Available RAM'],
            colors=['#ff9999', '#99ff99'],
            alpha=0.8
        )

        # Add horizontal line for total RAM (optional)
        ax.axhline(y=total_ram[0] if total_ram else 0, color='blue', linestyle='--', label='Total RAM')

        ax.set_title("RAM Usage Over Time (Stacked Area)")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("RAM (GBs)")
        ax.legend(loc='upper left')
        ax.grid(True)
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
        ax.tick_params(axis='x', rotation=45)

        # Format RAM values with commas
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.1f}'))

        self.canvas_area_chart.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
