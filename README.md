# kpi_tree_lib
A library to generate a KPI trees (decomposition trees)

## Insatall
```pip install git+https://github.com/yshimasaki/kpi_tree_lib.git```

## Usage

1. Define KPI structure with tabbed text
```Python
tree_structure = """
Root
    Child1
        Grandchild1
        Grandchild2
    Child2
        Grandchild3
"""
```

2. Generate KPI Tree
```Python
kpi_tree = KPITree(tree_structure)
```

3. Define values of each KPI Card
For each card, you can define name, value, MoM or YoY value (opt), and background color.
```Python
kpi_cards = {
    "Root": KPICard("Root", 100, "10% YoY", "lightblue"),
    "Child1": KPICard("Child1", 50, "5% YoY", "lightgreen"),
    "Child2": KPICard("Child2", 50, "15% YoY", "lightpink"),
    "Grandchild1": KPICard("Grandchild1", 25, "2% YoY", "lightyellow"),
    "Grandchild2": KPICard("Grandchild2", 25, "8% YoY", "lightcyan"),
    "Grandchild3": KPICard("Grandchild3", 50, "20% YoY", "lightcoral")
}
```

4. Visualize KPI trees
```Python
kpi_tree.visualize_tree(kpi_cards, save_as_png=True, filename="kpi_tree_example.png")
```