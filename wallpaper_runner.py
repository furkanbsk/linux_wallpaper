import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush

class LifeCalendar(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.setGeometry(screen_geometry)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Life Calendar Wallpaper")

        # Colors
        self.bg_color = QColor(0, 0, 0)
        self.text_color = QColor(255, 255, 255)
        self.highlight_color = QColor(255, 69, 0) # Red Orange
        self.dot_filled = QColor(255, 255, 255)
        self.dot_empty = QColor(50, 50, 50)
        self.dot_current = QColor(255, 69, 0)

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 * 60) # Update every minute

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw Background
        painter.fillRect(self.rect(), self.bg_color)

        # Calculate Data
        now = datetime.datetime.now()
        year = now.year
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        total_days = 366 if is_leap else 365
        current_day_of_year = now.timetuple().tm_yday
        days_left = total_days - current_day_of_year
        progress = (current_day_of_year / total_days) * 100

        # Layout Determination
        w = self.width()
        h = self.height()
        is_landscape = w > h

        margin = 60 # Increased margin
        
        # --- Draw Clock ---
        painter.setPen(self.text_color)
        
        # Time string
        time_str = now.strftime("%H:%M")
        
        # Date string
        date_str = now.strftime("%a, %b %-d")

        if not is_landscape:
            # --- PORTRAIT MODE: CLOCK & DATE ONLY ---
            # Clock Font (Minimalist size)
            font_size = int(w * 0.12) # Was 0.20
            font = QFont("Inter", font_size, QFont.Bold)
            painter.setFont(font)
            time_rect = painter.fontMetrics().boundingRect(time_str)
            
            # Date Font
            date_font_size = int(font_size * 0.35) # Slightly larger relative to clock for balance
            date_font = QFont("Inter", date_font_size)
            painter.setFont(date_font)
            date_rect = painter.fontMetrics().boundingRect(date_str)
            
            # Spacing
            spacing = 20
            total_h = time_rect.height() + date_rect.height() + spacing
            
            start_y = (h - total_h) // 2
            
            # Draw Clock
            painter.setFont(font)
            clock_rect = QRect(0, start_y, w, time_rect.height())
            painter.drawText(clock_rect, Qt.AlignCenter, time_str)
            
            # Draw Date
            painter.setFont(date_font)
            painter.setPen(QColor(150, 150, 150))
            date_y = start_y + time_rect.height() + spacing
            date_draw_rect = QRect(0, date_y, w, date_rect.height() + 20)
            painter.drawText(date_draw_rect, Qt.AlignCenter, date_str)
            
            return

        # --- LANDSCAPE MODE: FULL DASHBOARD ---
        
        # Split: Left (30%) = Info, Right (70%) = Grid
        split_x = int(w * 0.3)
        
        # 1. First, Calculate Right Panel (Grid) Geometry to get alignment reference
        panel_x = split_x
        panel_y = 0
        panel_w = w - split_x
        panel_h = h
        
        # Scaling factor for grid
        scale_factor = 0.70 
        
        grid_w = int(panel_w * scale_factor)
        grid_h = int(panel_h * scale_factor)
        
        # Center the grid within the right panel
        grid_x = panel_x + (panel_w - grid_w) // 2
        grid_y = (panel_h - grid_h) // 2
        
        # --- Left Panel: Info ---
        
        # 1. Clock (Aligned to Grid Top)
        clock_font_size = int(h * 0.12)
        clock_font = QFont("Inter", clock_font_size, QFont.Bold)
        painter.setFont(clock_font)
        painter.setPen(self.text_color)
        
        # Calculate offset to align TOP of text with TOP of grid
        fm = painter.fontMetrics()
        ascent = fm.ascent()
        
        # "Pulled a little bit right" -> Increase margin
        clock_x = margin + 40 
        
        # Align Top: baseline = grid_y + ascent
        clock_y = grid_y + ascent
        
        painter.drawText(int(clock_x), int(clock_y), time_str)
        
        # 2. Date
        date_font_size = int(clock_font_size * 0.35)
        date_font = QFont("Inter", date_font_size)
        painter.setFont(date_font)
        painter.setPen(QColor(150, 150, 150))
        date_rect = painter.fontMetrics().boundingRect(date_str)
        
        date_y = clock_y + date_rect.height() + 15
        painter.drawText(int(clock_x + 2), int(date_y), date_str)
        
        # 3. Stats (Aligned to bottom left, Horizontal Layout, Smaller)
        # Smaller sizes as requested
        stats_val_size = int(h * 0.035) # Reduced from 0.05
        stats_lbl_size = int(stats_val_size * 0.7) # Simpler look
        
        lbl_font = QFont("Inter", stats_lbl_size)
        val_font = QFont("Inter", stats_val_size, QFont.Bold)
        
        # Metrics for spacing
        painter.setFont(val_font)
        val_height = painter.fontMetrics().height()
        
        # Calculate offsets
        block_spacing = 10 
        label_val_gap = 15
        
        # Position from bottom up - Align bottom block with Grid Bottom? 
        # Or just margin. Let's stick to margin but maybe match grid bottom if close?
        # User asked for "pulled below", let's stick to bottom margin but push it slightly down if needed.
        # Actually "clock pulled below" was the request.
        # Let's align stats bottom roughly with grid bottom relative area
        
        bottom_y = grid_y + grid_h # Align bottom of stats with bottom of grid
        
        # --- Row 1: Progress (Bottom) ---
        # Label: "Progress"
        painter.setFont(lbl_font)
        painter.setPen(QColor(150, 150, 150))
        lbl_text = "Progress"
        lbl_width = painter.fontMetrics().width(lbl_text)
        painter.drawText(int(clock_x), int(bottom_y), lbl_text)
        
        # Value: "9.3%"
        painter.setFont(val_font)
        painter.setPen(self.highlight_color)
        val_text = f"{progress:.1f}%"
        painter.drawText(int(clock_x + lbl_width + label_val_gap), int(bottom_y), val_text)
        
        # --- Row 2: Days Left (Above Progress) ---
        row2_y = bottom_y - val_height - block_spacing
        
        # Label: "Days Left"
        painter.setFont(lbl_font)
        painter.setPen(QColor(150, 150, 150))
        lbl_text = "Days Left"
        lbl_width = painter.fontMetrics().width(lbl_text)
        painter.drawText(int(clock_x), int(row2_y), lbl_text)
        
        # Value: "331"
        painter.setFont(val_font)
        painter.setPen(self.highlight_color)
        val_text = str(days_left)
        painter.drawText(int(clock_x + lbl_width + label_val_gap), int(row2_y), val_text)
        
        # Grid Logic
        cols = 32 # Increased columns for horizontal look (approx 3:1 aspect ratio)
        rows = (total_days // cols) + 1
        
        # Cell calculation
        cell_size = min(grid_w / cols, grid_h / rows)
        dot_size = int(cell_size * 0.75) # Larger dots (75% fill)
        gap = int(cell_size * 0.25)
        
        # Re-center actual grid block
        actual_w = cols * (dot_size + gap) - gap
        actual_h = rows * (dot_size + gap) - gap
        
        start_x = grid_x + (grid_w - actual_w) // 2
        start_y = grid_y + (grid_h - actual_h) // 2
        
        painter.setPen(Qt.NoPen)
        
        for i in range(total_days):
            day_num = i + 1
            col = i % cols
            row = i // cols
            
            x = start_x + col * (dot_size + gap)
            y = start_y + row * (dot_size + gap)
            
            if day_num < current_day_of_year:
                painter.setBrush(QBrush(self.dot_filled))
            elif day_num == current_day_of_year:
                painter.setBrush(QBrush(self.dot_current))
            else:
                painter.setBrush(QBrush(self.dot_empty))
                
            painter.drawEllipse(int(x), int(y), int(dot_size), int(dot_size))


def main():
    app = QApplication(sys.argv)
    
    # Get all screens
    screens = app.screens()
    windows = []
    
    for screen in screens:
        geom = screen.geometry()
        # Create a window for each screen
        w = LifeCalendar(geom)
        w.show()
        windows.append(w)
        
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
