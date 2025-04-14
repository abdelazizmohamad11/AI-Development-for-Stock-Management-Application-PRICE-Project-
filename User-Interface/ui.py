import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import datetime


def setup_ui(root, app):
    main_frame = tk.Frame(root, bg="#E3E3E3", padx=20, pady=20)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_rowconfigure(5, weight=1)  # Added row for update label
    main_frame.grid_columnconfigure(0, weight=1)

    # Processing panel (hidden by default)
    processing_label = tk.Label(main_frame, text="", font=("Arial", 12),
                              bg="#F5A623", fg="black", padx=10, pady=5)
    processing_label.grid(row=0, column=0, sticky="ew", pady=5)

    # Last update label
    last_update_label = tk.Label(main_frame, text="Dernière mise à jour: Chargement...",
                               font=("Arial", 10), bg="#E3E3E3", fg="#555555")
    last_update_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

    # Upload button
    upload_button = tk.Button(main_frame, text="Upload Dataset", bg="#3A7CA5", fg="white",
                            command=app.upload_dataset, padx=10, pady=5, font=("Arial", 12))
    upload_button.grid(row=2, column=0, pady=10)

    # EAN input
    ean_frame = tk.Frame(main_frame, bg="#E3E3E3")
    ean_frame.grid(row=3, column=0, pady=10)

    ean_label = tk.Label(ean_frame, text="Enter EAN:", font=("Arial", 12), bg="#E3E3E3")
    ean_label.pack(side=tk.LEFT, padx=5)

    ean_entry = tk.Entry(ean_frame, font=("Arial", 12), width=20)
    ean_entry.pack(side=tk.LEFT, padx=5)

    # Predict button
    predict_button = tk.Button(main_frame, text="Predict", command=app.predict,
                             bg="#F25C54", fg="white", padx=10, pady=5, font=("Arial", 12))
    predict_button.grid(row=4, column=0, pady=10)

    # Results frame (initially empty)
    result_frame = tk.Frame(main_frame, bg="#E3E3E3")
    result_frame.grid(row=5, column=0, sticky="nsew", pady=10)

    # Help button (question mark)
    help_button = tk.Button(main_frame, text="?", command=app.show_help,
                          bg="#FFFFFF", fg="#000000", font=("Arial", 14, "bold"),
                          width=3, height=1, bd=2, relief=tk.RAISED)
    help_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    return (processing_label, upload_button, ean_entry, predict_button,
            result_frame, help_button, last_update_label)


def show_processing_panel(processing_label, message):
    """Displays a processing message in the UI."""
    processing_label.config(text=message)
    processing_label.grid()  # Make sure it's visible


def hide_processing_panel(processing_label):
    """Hides the processing message in the UI."""
    processing_label.config(text="")
    processing_label.grid_remove()  # Hide it completely


def show_plot_window(ean_data, future_dates, future_predictions):
    """Shows the plot in a new window."""
    plot_window = tk.Toplevel()
    plot_window.title("Consumption Prediction Plot")
    plot_window.geometry("800x600")

    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)

    # Plot past data
    ax.plot(ean_data["Week_Start"], ean_data["Total_Weekly_Consumption"],
           marker='o', label="Past Consumption", color="blue")

    # Plot future predictions
    ax.plot(future_dates, future_predictions, marker='x', linestyle='dashed',
           label="Predicted Consumption", color="red")

    ax.set_title("Stock Consumption Prediction", fontsize=14)
    ax.set_xlabel("Week Start", fontsize=12)
    ax.set_ylabel("Consumption (units)", fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True)

    # Rotate x-axis labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def show_help_window():
    """Shows the help window with application guide."""
    help_window = tk.Toplevel()
    help_window.title("Guide d'utilisation - Aide")
    help_window.geometry("900x700")
    help_window.configure(bg="#f5f5f5")

    # Style configuration
    style = ttk.Style()
    style.configure("TNotebook", background="#f5f5f5")
    style.configure("TNotebook.Tab", font=('Arial', '11', 'bold'), padding=[10, 5])
    style.configure("TFrame", background="#f5f5f5")

    # Create notebook for multiple tabs
    notebook = ttk.Notebook(help_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_tab_content(parent, text):
        frame = tk.Frame(parent, bg="#ffffff", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12),
                            bg="#ffffff", fg="#333333", padx=15, pady=15,
                            relief=tk.FLAT, height=20)
        text_widget.insert(tk.END, text.strip())
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        return frame

    # Tab 1: Overview
    overview_text = """
    Bienvenue dans l'application de prédiction de consommation de stock !

    Cette application vous aide à mieux gérer votre inventaire en prédisant 
    la consommation future de vos produits (identifiés par leur code EAN) 
    sur la base des données historiques.

    Fonctionnalités principales :
    • Prédiction de la consommation pour les 4 prochaines semaines
    • Visualisation claire des tendances passées et futures
    • Gestion simplifiée de votre inventaire
    • Interface intuitive et facile à utiliser

    Comment commencer ?
    1. Chargez votre fichier de données (ce processus prend 7 à 8 minutes, selon les capacités de votre PC)
    2. Entrez le code EAN du produit
    3. Cliquez sur "Prédire" pour voir les résultats
    """
    overview_frame = create_tab_content(notebook, overview_text)
    notebook.add(overview_frame, text="Présentation")

    # Tab 2: Dataset Requirements
    dataset_text = """
    Configuration requise pour votre fichier de données :

    Votre fichier CSV doit contenir les colonnes suivantes :
    • 'EAN' : Identifiant unique du produit (nombre)
    • 'Quantite' : Consommation du stock (nombre positif)
    • 'Creation Date' : Date d'enregistrement (format MMM DD, YYYY hh:mm am/pm)

    Ce que fait l'application avec vos données :
    ✓ Transformation en consommation hebdomadaire
    ✓ Remplissage des semaines manquantes (consommation = 0)
    ✓ Nettoyage automatique des données
    ✓ Organisation chronologique

    Conseils :
    • Vérifiez que vos données sont complètes
    • Utilisez un format de date cohérent
    • Les valeurs négatives ne sont pas acceptées
    """
    dataset_frame = create_tab_content(notebook, dataset_text)
    notebook.add(dataset_frame, text="Configuration des données")

    # Tab 3: How It Works
    process_text = """
    Fonctionnement de l'application :

    1. PRÉTRAITEMENT DES DONNÉES
    • Transformation des dates en semaines
    • Calcul de la consommation hebdomadaire
    • Nettoyage des valeurs manquantes
    • Standardisation du format

    2. ENTRAÎNEMENT DES MODÈLES
    • Création d'un modèle spécifique pour chaque produit
    • Apprentissage basé sur l'historique
    • Validation des performances
    • Sauvegarde automatique

    3. PRÉDICTION
    • Prévision pour 4 semaines
    • Basée sur la dernière date disponible
    • Visualisation graphique

    Exemple :
    Si votre dernière date est le 31/03/2025, les prédictions seront :
    • Semaine 1 : 07/04/2025
    • Semaine 2 : 14/04/2025
    • Semaine 3 : 21/04/2025
    • Semaine 4 : 28/04/2025
    """
    process_frame = create_tab_content(notebook, process_text)
    notebook.add(process_frame, text="Comment ça marche ?")

    # Tab 4: Recommendations
    reco_text = """
    Recommandations pour une utilisation optimale :

    FRÉQUENCE DE MISE À JOUR :
    • Pour une gestion précise : mise à jour hebdomadaire
    • Pour une gestion standard : mise à jour mensuelle

    CONSEILS PRATIQUES :
    • Vérifiez régulièrement la qualité de vos données
    • Laissez l'application terminer tout le processus (4-8 min)
    • Consultez les graphiques pour comprendre les tendances

    CE QUE L'APPLICATION SAUVEGARDE :
    • Votre dataset de format jj_mm_yyyy (le jour de téléchargement)
    • Votre dataset prétraité
    • Les modèles entraînés

    """
    reco_frame = create_tab_content(notebook, reco_text)
    notebook.add(reco_frame, text="Bonnes pratiques")

    # Add some visual polish
    help_window.iconbitmap(default='')  # Add your icon here if available
    help_window.resizable(True, True)