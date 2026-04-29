#Copyright © 2026 Anas Boutaghroucht
#Sous license CC BY-NC 4.0
#Voir LICENCE pour plus d'info
#Utilise www.api-football.com
import tkinter as tk
from tkinter import ttk, messagebox
import requests

class FootballFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Dashboard Pro")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a")

        self.api_key = "ENTRER_API_ICI"
        self.headers = {'x-apisports-key': self.api_key}
        
        # On stocke les matchs ici pour pouvoir les filtrer sans relancer l'API
        self.all_fixtures = []

        self.setup_ui()
        self.load_live()

    def setup_ui(self):
        # --- BARRE DE RECHERCHE ET BOUTONS ---
        top_frame = tk.Frame(self.root, bg="#1e293b", pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Rechercher équipe :", fg="white", bg="#1e293b").pack(side=tk.LEFT, padx=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_matches) # Filtre en temps réel quand on tape
        tk.Entry(top_frame, textvariable=self.search_var, width=25).pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="ACTUALISER", command=self.load_live, bg="#22c55e", fg="white").pack(side=tk.RIGHT, padx=20)

        # --- TABLEAU ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", rowheight=35)
        style.configure("Treeview.Heading", background="#0f172a", foreground="white", font=("Arial", 10, "bold"))

        self.tree = ttk.Treeview(self.root, columns=("L", "M", "S", "T"), show='headings')
        self.tree.heading("L", text="LIGUE")
        self.tree.heading("M", text="MATCH")
        self.tree.heading("S", text="SCORE")
        self.tree.heading("T", text="TEMPS")
        self.tree.column("L", width=150)
        self.tree.column("M", width=350)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def load_live(self):
        try:
            url = "https://v3.football.api-sports.io/fixtures"
            r = requests.get(url, headers=self.headers, params={'live': 'all'}, timeout=10)
            self.all_fixtures = r.json().get("response", [])
            self.filter_matches() # Affichage initial
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def filter_matches(self, *args):
        # On vide le tableau
        for i in self.tree.get_children(): self.tree.delete(i)
        
        search_query = self.search_var.get().lower()

        for f in self.all_fixtures:
            home = f['teams']['home']['name']
            away = f['teams']['away']['name']
            league = f['league']['name']
            
            # Filtre : on n'affiche que si ça correspond à la recherche
            if search_query in home.lower() or search_query in away.lower() or search_query in league.lower():
                score = f"{f['goals']['home']} - {f['goals']['away']}"
                time = f"{f['fixture']['status']['elapsed']}'"
                self.tree.insert("", tk.END, values=(league, f"{home} vs {away}", score, time))

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballFinal(root)
    root.mainloop()
