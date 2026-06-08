import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import re
from collections import Counter

class ModernTextAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur de Texte Visuel Pro")
        self.root.geometry("750x650")
        
        # 1. Configuration du Style et des Couleurs
        self.colors = {
            'bg': '#2E3440',      # Fond sombre (style Nord)
            'fg': '#ECEFF4',      # Texte clair
            'accent': '#88C0D0',  # Bleu cyan
            'btn_bg': '#5E81AC',  # Bleu plus foncé
            'frame_bg': '#3B4252',# Fond de cadre légèrement plus clair
        }
        
        self.fonts = {
            'title': ('Helvetica Neue', 18, 'bold'),
            'text': ('Segoe UI', 10),
            'results': ('Consolas', 11),
        }

        self.style = ttk.Style()
        self.style.theme_use('clam') # Base propre
        
        # Configuration globale des styles ttk
        self.root.configure(bg=self.colors['bg'])
        
        # Style pour le bouton
        self.style.configure('Accent.TButton', 
                            background=self.colors['btn_bg'], 
                            foreground=self.colors['fg'], 
                            font=('Helvetica', 11, 'bold'),
                            padding=10)
        self.style.map('Accent.TButton', 
                       background=[('active', self.colors['accent'])])
        
        # Style pour les LabelFrames
        self.style.configure('Custom.TLabelframe', 
                            background=self.colors['bg'],
                            bordercolor=self.colors['accent'])
        self.style.configure('Custom.TLabelframe.Label', 
                            foreground=self.colors['accent'], 
                            background=self.colors['bg'],
                            font=('Helvetica', 10, 'bold'))

        self.create_widgets()

    def create_widgets(self):
        # -- TITRE --
        lbl_title = tk.Label(self.root, 
                             text="• TEXT ANALYZER •", 
                             font=self.fonts['title'], 
                             fg=self.colors['accent'], 
                             bg=self.colors['bg'])
        lbl_title.pack(pady=(25, 15))

        # -- CADRE SAISIE DE TEXTE --
        input_frame = ttk.LabelFrame(self.root, text=" Entrez votre texte ", style='Custom.TLabelframe')
        input_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        # Utilisation de tk.Text car scrolledtext est plus difficile à styliser profondément
        # On ajoute une bordure plate et du padding interne
        self.txt_input = tk.Text(input_frame, 
                                 height=12, 
                                 font=self.fonts['text'],
                                 wrap=tk.WORD,
                                 bg=self.colors['frame_bg'], 
                                 fg=self.colors['fg'],
                                 insertbackground=self.colors['fg'], # Couleur du curseur
                                 relief=tk.FLAT,
                                 padx=10, pady=10)
        
        # Ajout d'une barre de défilement stylisée
        scrollbar = ttk.Scrollbar(input_frame, command=self.txt_input.yview)
        self.txt_input['yscrollcommand'] = scrollbar.set
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)

        # -- BOUTON D'ACTION --
        self.btn_analyze = ttk.Button(self.root, 
                                      text="Lancer l'Analyse Visuelle", 
                                      style='Accent.TButton', 
                                      command=self.process_text)
        self.btn_analyze.pack(pady=20)

        # -- CADRE RÉSULTATS DÉTAILLÉS --
        results_frame = ttk.LabelFrame(self.root, text=" Tableau de bord des résultats ", style='Custom.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 25))

        # Sous-cadre pour organiser les labels
        results_inner = tk.Frame(results_frame, bg=self.colors['bg'])
        results_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Labels de résultats stylisés
        self.lbl_unique_words = self.create_result_label(results_inner, "Nombre de mots uniques :")
        self.lbl_top_words = self.create_result_label(results_inner, "Top 3 des mots fréquents :")
        
        # Le set de lettres nécessite plus d'espace
        self.lbl_unique_chars = self.create_result_label(results_inner, "Set de caractères utilisés :")
        # On remplace le label simple par une zone de texte pour les lettres (plus lisible si long)
        self.txt_chars_display = tk.Text(results_inner, height=2, font=self.fonts['results'],
                                          bg=self.colors['bg'], fg=self.colors['fg'], 
                                          relief=tk.FLAT, wrap=tk.CHAR, state=tk.DISABLED)
        self.txt_chars_display.pack(fill=tk.X, anchor="w", pady=(0, 5))

    def create_result_label(self, parent, text):
        """Fonction utilitaire pour créer des labels de résultats uniformes."""
        container = tk.Frame(parent, bg=self.colors['bg'])
        container.pack(fill=tk.X, anchor="w", pady=5)
        
        fixed_text = tk.Label(container, text=text, font=('Helvetica', 10, 'bold'),
                              fg=self.colors['accent'], bg=self.colors['bg'])
        fixed_text.pack(side=tk.LEFT)
        
        result_text = tk.Label(container, text=" -", font=self.fonts['results'],
                               fg=self.colors['fg'], bg=self.colors['bg'])
        result_text.pack(side=tk.LEFT, padx=(10, 0))
        
        return result_text

    def process_text(self):
        # 1. Récupération et Nettoyage
        raw_text = self.txt_input.get("1.0", tk.END).strip().lower()
        
        # Gestion du texte vide
        if not raw_text:
            self.lbl_unique_words.config(text="0")
            self.lbl_top_words.config(text="aucun mot")
            self.update_chars_display("")
            return

        # Regex pour ne garder que les mots (lettres et chiffres), ignore ponctuation
        words = re.findall(r'\b\w+\b', raw_text)
        
        if not words:
            # Cas où il n'y a que de la ponctuation
            self.lbl_unique_words.config(text="0")
            self.lbl_top_words.config(text="aucun mot valide")
            self.update_chars_display(set(raw_text)) # Affiche quand même les symboles
            return

        # --- CŒUR DE L'ANALYSE (Utilisation des SETS) ---
        
        # 2. Mots uniques (avec un set)
        unique_words_set = set(words)
        count_unique = len(unique_words_set)
        
        # 3. Lettres utilisées (set de caractères)
        # On filtre pour ne garder que les lettres de a-z
        letters_only = "".join(re.findall(r'[a-z]', raw_text))
        unique_letters_set = set(letters_only)
        # Tri des lettres pour un affichage joli {a, b, c...}
        sorted_letters = sorted(list(unique_letters_set))
        letters_display = "{" + ", ".join(sorted_letters) + "}"
        
        # 4. Mots les plus fréquents (Counter)
        most_common = Counter(words).most_common(3)
        top_words_str = " | ".join([f"'{w}' ({c})" for w, c in most_common])

        # --- MISE À JOUR DE L'AFFICHAGE ---
        self.lbl_unique_words.config(text=str(count_unique), fg='#A3BE8C') # Vert si succès
        self.lbl_top_words.config(text=top_words_str)
        self.update_chars_display(letters_display)

    def update_chars_display(self, text):
        """Met à jour la zone de texte contenant le set de caractères."""
        self.txt_chars_display.config(state=tk.NORMAL)
        self.txt_chars_display.delete("1.0", tk.END)
        self.txt_chars_display.insert("1.0", text)
        self.txt_chars_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTextAnalyzer(root)
    root.mainloop()
