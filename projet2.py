import tkinter as tk

def generer_palette():
    # Données source : Liste de tuples RGB
    couleurs = [
        (255, 87, 51),  # Orange Corail
        (51, 255, 87),  # Vert Printemps
        (51, 87, 255),  # Bleu Royal
        (255, 51, 161), # Rose Vif
        (241, 196, 15)  # Jaune Or
    ]

    root = tk.Tk()
    root.title("Color Palette Explorer")
    root.geometry("400x500")
    root.config(bg="#f0f0f0")

    # Zone d'affichage du code Hex (Défi Bonus)
    label_hex = tk.Label(root, text="Sélectionnez une couleur", 
                         font=("Helvetica", 14, "bold"), bg="#f0f0f0")
    label_hex.pack(pady=20)

    # Fonction pour changer le fond et mettre à jour le texte
    def changer_couleur(rgb_tuple):
        # Conversion RGB -> HEX
        hex_val = '#%02x%02x%02x' % rgb_tuple
        root.config(bg=hex_val)
        label_hex.config(text=f"Code HEX : {hex_val.upper()}", bg=hex_val)

    # Création dynamique des boutons
    for couleur in couleurs:
        hex_preview = '#%02x%02x%02x' % couleur
        
        btn = tk.Button(
            root, 
            text=f"RGB {couleur}",
            bg=hex_preview,
            fg="white" if sum(couleur) < 400 else "black", # Contraste auto
            font=("Arial", 10, "bold"),
            height=2,
            width=20,
            command=lambda c=couleur: changer_couleur(c)
        )
        btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    generer_palette()
