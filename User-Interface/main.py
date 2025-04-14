import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import pandas as pd
import os
import shutil
import subprocess
import datetime
from ui import setup_ui, show_processing_panel, hide_processing_panel, show_plot_window, show_help_window
from prediction import predict_consumption
from utils import load_models, load_dataset

# Load models and scaler
models, scaler = load_models()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Consumption Predictor")
        self.root.geometry("800x600")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Setup UI components (panels, buttons, entry fields)
        (self.processing_label, self.upload_button, self.ean_entry,
         self.predict_button, self.result_frame, self.help_button,
         self.last_update_label) = setup_ui(root, self)

        # Initialize last update display
        self.update_last_update_display()

        # Hide the processing panel at the beginning
        hide_processing_panel(self.processing_label)

    def update_last_update_display(self):
        """Update the last update label with current dataset info"""
        dataset_folder = "../Dataset"
        update_text = "Dernière mise à jour: Aucun dataset chargé"

        if os.path.exists(dataset_folder):
            files = [f for f in os.listdir(dataset_folder) if f.endswith('.csv')]
            date_files = [f for f in files if f.count('_') == 2 and f.replace('.csv', '').replace('_', '').isdigit()]

            if date_files:
                latest_file = max(date_files,
                                  key=lambda x: datetime.datetime.strptime(x.replace('.csv', ''), "%d_%m_%Y"))
                update_date = latest_file.replace('.csv', '').replace('_', ' / ')
                update_text = f"Dernière mise à jour: {update_date}"

                self.last_update_label.config(text=update_text)

    def show_help(self):
        show_help_window()

    def upload_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        new_dataset_name = os.path.basename(file_path)
        confirm = messagebox.askyesno("Confirm Selection", f"You selected {new_dataset_name}. Proceed?")
        if not confirm:
            return

        ready = messagebox.askyesno("Preprocessing Notice", "This process may take some time. Continue?")
        if not ready:
            return

        dataset_folder = "../Dataset"
        for filename in os.listdir(dataset_folder):
            os.remove(os.path.join(dataset_folder, filename))

        # Save with current date format
        today = datetime.datetime.now().strftime("%d_%m_%Y")
        new_filename = f"{today}.csv"
        shutil.copy(file_path, os.path.join(dataset_folder, new_filename))

        # Also keep the original for preprocessing
        shutil.copy(file_path, os.path.join(dataset_folder, new_dataset_name))

        show_processing_panel(self.processing_label, "Preprocessing dataset...")

        def run_preprocessing_and_training():
            try:
                # Run preprocessing
                subprocess.run(["python", "preprocessing.py", new_dataset_name], check=True)

                # After preprocessing, train models
                show_processing_panel(self.processing_label, "Training models...")
                subprocess.run(["python", "model_training.py"], check=True)

                # Reload the new models
                global models, scaler
                models, scaler = load_models()

                # Update last update display
                self.update_last_update_display()

                hide_processing_panel(self.processing_label)
                messagebox.showinfo("Success", "Dataset processed and models retrained successfully!")

                # Clean up - remove the temporary original file
                os.remove(os.path.join(dataset_folder, new_dataset_name))
            except subprocess.CalledProcessError as e:
                hide_processing_panel(self.processing_label)
                messagebox.showerror("Error", f"Processing failed: {str(e)}")

        threading.Thread(target=run_preprocessing_and_training, daemon=True).start()

    def predict(self):
        try:
            ean = float(self.ean_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid EAN!")
            return

        df = load_dataset()
        future_dates, future_predictions, ean_data = predict_consumption(ean, df, models, scaler)

        if future_dates is None:
            messagebox.showerror("Error", "EAN not found!")
            return

        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Add title for results
        results_title = tk.Label(self.result_frame, text="Prediction Results", font=("Arial", 14, "bold"))
        results_title.pack(pady=5)

        # Display results in a better format
        for i, (date, pred) in enumerate(zip(future_dates, future_predictions)):
            week_label = tk.Label(self.result_frame,
                                  text=f"Week {i + 1} ({date.date()}): {int(pred)} units",
                                  font=("Arial", 12))
            week_label.pack(pady=2)

        # Show plot in a new window
        show_plot_window(ean_data, future_dates, future_predictions)


# Run the application
root = tk.Tk()
app = App(root)
root.mainloop()