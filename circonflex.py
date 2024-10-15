import plotly.graph_objects as go
import webbrowser

# Données de l'arbre avec les nouvelles sous-catégories et leurs valeurs
tree = {
    "Thèmes": {
        "Sociétal": {
            "Croyances populaires": 4,
            "Impact social": 4,
            "Psychologie collective": 3,
            "Éducation critique": 3
        },
        "Politique": {
            "Manipulation politique": 4,
            "Crise de confiance": 1,
            "Manque de transparence": 4
        },
        "Scientifique": {
            "Négation scientifique": 4,
            "Barrières à l’action": 1,
            "Communication scientifique": 3
        },
        "Théologique": {
            "Manipulation religieuse": 3,
            "Impact sur la foi": 3
        }
    }
}

# Préparation des données
labels = []
parents = []
values = []
colors = []

key_to_label = {}

# Mapping des couleurs pour les catégories principales
category_colors = {
    "Sociétal": "#1f77b4",    # Bleu
    "Politique": "#d62728",    # Rouge
    "Scientifique": "#2ca02c", # Vert
    "Théologique": "#9467bd"   # Violet
}

# Fonction pour éclaircir une couleur (hex) donnée
def lighten_color(color, amount=0.5):
    color = color.lstrip('#')
    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2 ,4))
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Fonction pour préparer les données pour Plotly
def prepare_data(tree, parent_label, parent_color):
    for key, value in tree.items():
        # Créer le label formaté
        label = f"<b>{key}</b>" if isinstance(value, dict) else key
        key_to_label[key] = label  # Associer la clé au label formaté

        labels.append(label)
        parents.append(parent_label)
        # Attribuer la couleur de la catégorie principale
        if key in category_colors:
            color = category_colors[key]
        else:
            color = parent_color

        colors.append(color)

        if isinstance(value, dict):
            # Calculer la somme des valeurs des enfants pour le nœud parent
            total_value = sum(value.values())
            values.append(total_value)
            prepare_data(value, label, color)
        else:
            # Ajouter la valeur du sous-thème
            values.append(value)
            # Éclaircir la couleur pour les sous-thèmes
            amount = 0.5  # Vous pouvez ajuster cet éclaircissement si nécessaire
            subtheme_color = lighten_color(color, amount)
            colors[-1] = subtheme_color  # Remplacer la couleur par la couleur éclaircie

# Ajouter le nœud racine
root_label = "<b>Thèmes</b>"
labels.append(root_label)
parents.append("")  # Le nœud racine n'a pas de parent
colors.append("#333333")  # Couleur pour le nœud racine
# Calculer la valeur totale pour le nœud racine
total_root_value = sum(
    sum(subtree.values()) if isinstance(subtree, dict) else subtree
    for subtree in tree["Thèmes"].values()
)
values.append(total_root_value)

# Construire les données à partir du nœud racine
prepare_data(tree["Thèmes"], root_label, "#333333")

# Création du diagramme Sunburst avec mode sombre
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues='total',
    insidetextorientation='radial',
    hoverinfo='label+percent entry',
    textinfo='label+percent parent',
    marker=dict(
        colors=colors,
        line=dict(color='#444', width=1)
    )
))

# Configuration du mode sombre et du style
fig.update_layout(
    paper_bgcolor='#1e1e1e',  # Fond de la page (sombre)
    plot_bgcolor='#1e1e1e',   # Fond du graphique (sombre)
    font=dict(color='#ffffff'),  # Couleur du texte (blanc)
    title={
        'text': 'Arbre des Thèmes',
        'font': {'size': 24, 'color': '#ffffff'},
        'x': 0.5
    },
    margin=dict(t=50, l=0, r=0, b=0)
)

# Ajuster le style du texte
fig.update_traces(
    textfont=dict(size=14, color='#ffffff'),  # Texte en blanc
    hoverlabel=dict(
        bgcolor='#333333',  # Fond des info-bulles
        font_size=14,
        font_family="Arial"
    )
)

# Enregistrer le graphique dans un fichier HTML
fig.write_html("arbre_des_themes.html")

# Ouvrir le fichier HTML dans le navigateur par défaut
webbrowser.open("arbre_des_themes.html")
