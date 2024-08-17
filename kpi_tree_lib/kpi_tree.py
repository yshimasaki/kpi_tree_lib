import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from anytree import Node, RenderTree

class KPICard:
    def __init__(self, name, value, yoy_or_mom=None, bgcolor="lightgray"):
        self.name = name
        self.value = value
        self.yoy_or_mom = yoy_or_mom
        self.bgcolor = bgcolor

class KPITree:
    def __init__(self, tree_structure_text):
        self.root = None
        self.nodes = {}
        self.parse_tree_structure(tree_structure_text)

    def parse_tree_structure(self, tree_structure_text):
        lines = tree_structure_text.split("\n")
        for line in lines:
            if line.strip():
                level = line.count("    ")
                kpi_name = line.strip()
                if level == 0:
                    self.root = Node(kpi_name)
                    self.nodes[kpi_name] = self.root
                else:
                    parent = self.get_parent_node(level)
                    node = Node(kpi_name, parent=parent)
                    self.nodes[kpi_name] = node

    def get_parent_node(self, level):
        parent_node = self.root
        for node in self.nodes.values():
            if node.depth == level - 1:
                parent_node = node
        return parent_node

    def display_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print(f"{pre}{node.name}")

    def visualize_tree(self, kpi_cards, save_as_png=False, filename="kpi_tree.png", figsize=(15, 8)):
        fig, ax = plt.subplots(figsize=figsize)

        dx = 0.11 # 幅
        dy = 0.1 # 高さ
        fixed_gap = dx * 0.6
        
        def get_tree_width(node):
            if node.is_leaf:
                return 1
            return max(sum(get_tree_width(child) for child in node.children), 1)
        
        total_width = get_tree_width(self.root) # LeafNodeの合計数
        width_adjustment = 0.9  # 全体の幅を調整する係数
        tree_width = total_width * dx * width_adjustment

        def plot_node(node, x, y):
            kpi = kpi_cards[node.name]
            rect = Rectangle((x, y), dx, dy, fc=kpi.bgcolor,ec='black', lw=1, ls='-')
            ax.add_patch(rect)

            ax.text(x + dx / 2, y + dy * 0.7, kpi.name,
                    ha="center", va="center", fontsize=10, fontweight="bold", color="black")
            ax.text(x + dx / 2, y + dy * 0.45, f"{kpi.value}",
                    ha="center", va="center", fontsize=10, fontweight="normal", color="black")
            if kpi.yoy_or_mom:
                ax.text(x + dx / 2, y + dy * 0.25, kpi.yoy_or_mom,
                        ha="center", va="center", fontsize=10, fontweight="normal", color="black")

            return x + dx / 2, y + dy / 2

        def draw_tree(node, x, y, level, available_width):
            x_mid, y_mid = plot_node(node, x - dx / 2, y)
            if not node.is_leaf:
                children_widths = [get_tree_width(child) for child in node.children]
                total_width = sum(children_widths)
                
                total_gap_width = fixed_gap * (len(node.children) - 1)
                available_child_width = (available_width - total_gap_width) *1.05 #available_width = tree_width
                
                scale = available_child_width / total_width if total_width > 0 else 1

                child_x = x - (available_width / 2)
                for i, child in enumerate(node.children):
                    child_width = children_widths[i] * scale
                    logging.warning(f"{child}: {child_width} = {children_widths[i]}*{scale}")
                    child_y = y - (dy * 2 + level * 0.05)
                    ax.plot([x_mid, child_x + child_width / 2], [y_mid - dy / 2, child_y + dy], 'k-')
                    draw_tree(child, child_x + child_width / 2, child_y, level + 1, child_width) #recursive
                    child_x += child_width + fixed_gap
        
        draw_tree(self.root, 0.5, 0.9, 0, tree_width)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()

        plt.tight_layout()
        if save_as_png:
            plt.savefig(filename, bbox_inches="tight", pad_inches=0.1, dpi=300)
        else:
            plt.show()
