import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import tkinter as tk

# ===== HELPER FUNCTIONS =====
def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def make_distance_matrix(cities):
    n = len(cities)
    D = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = euclidean(cities[i], cities[j])
            D[i][j] = D[j][i] = d
    return D

def route_distance(route, D):
    return sum(D[route[i]][route[(i+1) % len(route)]] for i in range(len(route)))

# ===== GENETIC OPERATORS =====
def create_individual(n, start_city):
    route = [i for i in range(n) if i != start_city]
    random.shuffle(route)
    return [start_city] + route

def initial_population(pop_size, n, start_city):
    return [create_individual(n, start_city) for _ in range(pop_size)]

def tournament_selection(pop, fitnesses, k=3):
    selected = random.sample(range(len(pop)), k)
    best = min(selected, key=lambda idx: fitnesses[idx])
    return pop[best][:]

def ordered_crossover(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(1, n), 2))
    child = [-1]*n
    child[a:b+1] = p1[a:b+1]
    p2_idx = 0
    for i in range(n):
        if child[i] == -1:
            while p2[p2_idx] in child:
                p2_idx += 1
            child[i] = p2[p2_idx]
    return child

def swap_mutation(ind, rate=0.02):
    for i in range(1, len(ind)):
        if random.random() < rate:
            j = random.randrange(1, len(ind))
            ind[i], ind[j] = ind[j], ind[i]

# ===== GENETIC ALGORITHM =====
def genetic_algorithm_tsp(cities, start_city, pop_size=200, generations=400):
    n = len(cities)
    D = make_distance_matrix(cities)
    pop = initial_population(pop_size, n, start_city)

    best_route, best_dist = None, float('inf')
    history_best, history_avg, best_routes = [], [], []

    for gen in range(generations):
        fitnesses = [route_distance(ind, D) for ind in pop]
        gen_best_idx = np.argmin(fitnesses)
        gen_best_dist = fitnesses[gen_best_idx]
        gen_avg = np.mean(fitnesses)

        history_best.append(gen_best_dist)
        history_avg.append(gen_avg)

        if gen_best_dist < best_dist:
            best_dist = gen_best_dist
            best_route = pop[gen_best_idx][:]

        best_routes.append(best_route[:])

        new_pop = [best_route[:]]
        while len(new_pop) < pop_size:
            p1 = tournament_selection(pop, fitnesses)
            p2 = tournament_selection(pop, fitnesses)
            child = ordered_crossover(p1, p2)
            swap_mutation(child)
            new_pop.append(child)
        pop = new_pop[:pop_size]

    return best_route, best_dist, history_best, history_avg, best_routes, D

# ===== GUI INPUT WINDOW =====
def get_parameters():
    def center_window(win):
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"+{x}+{y}")

    def submit():
        try:
            params["num_cities"] = int(entry_cities.get())
            params["pop_size"] = int(entry_pop.get())
            params["generations"] = int(entry_gen.get())
            params["start_city"] = int(entry_start.get())
            window.destroy()
        except ValueError:
            label_status.config(text="❌ Please enter valid integers.", fg="red")

    window = tk.Tk()
    window.title("GA_TSP - Input Configuration")
    window.geometry("350x300")
    window.resizable(False, False)
    window.configure(bg="#f5f5f5")
    center_window(window)

    tk.Label(window, text="Genetic Algorithm Parameters", font=("Arial", 13, "bold"), bg="#f5f5f5").pack(pady=10)
    frm = tk.Frame(window, bg="#f5f5f5")
    frm.pack(pady=10)

    tk.Label(frm, text="Number of cities:", bg="#f5f5f5").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_cities = tk.Entry(frm, width=10)
    entry_cities.insert(0, "20")
    entry_cities.grid(row=0, column=1)

    tk.Label(frm, text="Population size:", bg="#f5f5f5").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_pop = tk.Entry(frm, width=10)
    entry_pop.insert(0, "200")
    entry_pop.grid(row=1, column=1)

    tk.Label(frm, text="Generations:", bg="#f5f5f5").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_gen = tk.Entry(frm, width=10)
    entry_gen.insert(0, "100")
    entry_gen.grid(row=2, column=1)

    tk.Label(frm, text="Start city (index):", bg="#f5f5f5").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_start = tk.Entry(frm, width=10)
    entry_start.insert(0, "0")
    entry_start.grid(row=3, column=1)

    label_status = tk.Label(window, text="", bg="#f5f5f5", fg="green")
    label_status.pack(pady=5)

    tk.Button(window, text="Start Simulation", command=submit, bg="#007acc", fg="white",
              width=15, height=1, font=("Arial", 11, "bold")).pack(pady=10)

    params = {}
    window.mainloop()
    return params

# ===== MAIN VISUALIZATION =====
def animate_ga_tsp(last_params=None):
    params = last_params or get_parameters()
    if not params:
        print("Cancelled.")
        return

    num_cities = params["num_cities"]
    pop_size = params["pop_size"]
    generations = params["generations"]
    start_city = params["start_city"]

    cities = np.array([(random.random()*100, random.random()*100) for _ in range(num_cities)])
    best_route, best_distance, history_best, history_avg, best_routes, D = genetic_algorithm_tsp(
        cities, start_city, pop_size, generations
    )

    # === Create only one figure (fix: remove empty Figure(1)) ===
    fig, (ax_route, ax_prog) = plt.subplots(1, 2, figsize=(12, 6))
    fig.canvas.manager.set_window_title("GA_TSP")

    try:
        mngr = plt.get_current_fig_manager()
        mngr.window.wm_geometry("+{}+{}".format(
            int((mngr.window.winfo_screenwidth() - 900)/2),
            int((mngr.window.winfo_screenheight() - 600)/2)
        ))
    except Exception:
        pass

    fig.suptitle("TRAVELING SALESMAN PROBLEM - Genetic Algorithm",
                 fontsize=13, fontweight='bold', color='#003366')

    (best_line,) = ax_prog.plot([], [], label="Best", color='blue')
    (avg_line,) = ax_prog.plot([], [], label="Average", color='orange')
    ax_prog.set_xlim(0, generations)
    ax_prog.set_ylim(min(history_best)*0.9, max(history_avg)*1.1)
    ax_prog.set_xlabel("Generation")
    ax_prog.set_ylabel("Route length")
    ax_prog.set_title("Convergence graph", fontsize=12, fontweight="bold", color="#003366")
    ax_prog.legend()

    # === Information Display ===
    ax_info = fig.add_axes([0.08, 0.0, 0.7, 0.12])
    ax_info.axis("off")
    ax_info.set_facecolor("#f0f8ff")
    info_text = ax_info.text(0.02, 0.5, "", fontsize=10.5, family="monospace", va="center", color="#003366")

    # === Styled Buttons ===
    def styled_button(ax, label, color):
        ax.set_facecolor(color)
        btn = Button(ax, label, color=color, hovercolor="#005f99")
        btn.label.set_color("white")
        btn.label.set_fontsize(10)
        btn.label.set_fontweight("bold")
        btn.label.set_bbox(dict(boxstyle="round,pad=0.3", facecolor=color, edgecolor="none"))
        return btn

    ax_prev = plt.axes([0.68, 0.04, 0.08, 0.05])
    ax_next = plt.axes([0.87, 0.04, 0.08, 0.05])
    ax_box = plt.axes([0.58, 0.04, 0.09, 0.05])
    ax_go = plt.axes([0.77, 0.04, 0.08, 0.05])
    ax_auto = plt.axes([0.85, 0.13, 0.12, 0.05])
    ax_restart = plt.axes([0.68, 0.13, 0.15, 0.05])

    btn_prev = styled_button(ax_prev, "← Prev", "#007acc")
    btn_next = styled_button(ax_next, "Next →", "#007acc")
    txt_gen = TextBox(ax_box, "Go to: ", initial="1")
    btn_go = styled_button(ax_go, "Go", "#28a745")
    btn_auto = styled_button(ax_auto, "Auto Play", "#ff8c00")
    btn_restart = styled_button(ax_restart, "Restart","#ff8c00")

    current_gen = [0]
    auto_play = [False]

    def draw_generation(g):
        ax_route.cla()
        route = best_routes[g]
        ordered = cities[route + [route[0]]]
        ax_route.plot(ordered[:, 0], ordered[:, 1], color="dodgerblue", lw=2)
        ax_route.scatter(cities[:, 0], cities[:, 1], color="gray", s=30)
        ax_route.scatter(cities[start_city, 0], cities[start_city, 1], color="green", s=80, label="Start")
        ax_route.scatter(cities[route[-1], 0], cities[route[-1], 1], color="red", s=80, label="End")

        for i, (x, y) in enumerate(cities):
            ax_route.text(x+1, y+1, str(i), fontsize=7)

        ax_route.set_xlim(0, 100)
        ax_route.set_ylim(0, 100)
        ax_route.set_title(f"Optimized route at generation {g+1}",
                           fontsize=12, fontweight="bold", color="#003366")
        ax_route.legend(fontsize=8, loc="upper right")

        best_line.set_data(range(g+1), history_best[:g+1])
        avg_line.set_data(range(g+1), history_avg[:g+1])

        info = (
            f"Cities: {num_cities} | Population: {pop_size} | Generations: {generations}\n"
            f"Current generation: {g+1}/{generations} | Best Distance: {history_best[g]:.4f}"
        )
        info_text.set_text(info)
        fig.canvas.draw_idle()

    def next_gen(event=None):
        if current_gen[0] < generations - 1:
            current_gen[0] += 1
            draw_generation(current_gen[0])

    def prev_gen(event=None):
        if current_gen[0] > 0:
            current_gen[0] -= 1
            draw_generation(current_gen[0])

    def goto_gen(event=None):
        try:
            g = int(txt_gen.text) - 1
            if 0 <= g < generations:
                current_gen[0] = g
                draw_generation(g)
        except ValueError:
            pass

    def toggle_auto(event=None):
        auto_play[0] = not auto_play[0]
        btn_auto.label.set_text("Pause" if auto_play[0] else "Auto Play")
        if auto_play[0]:
            run_auto()

    def run_auto():
        if auto_play[0] and current_gen[0] < generations - 1:
            current_gen[0] += 1
            draw_generation(current_gen[0])
            fig.canvas.flush_events()
            fig.canvas.start_event_loop(0.3)
            run_auto()
        else:
            auto_play[0] = False
            btn_auto.label.set_text("Auto Play")

    def restart(event=None):
        plt.close('all')      # đóng mọi figure đang mở
        animate_ga_tsp()      # chạy lại toàn bộ, mở lại cửa sổ nhập từ đầu

    # === Bind Buttons ===
    btn_next.on_clicked(next_gen)
    btn_prev.on_clicked(prev_gen)
    btn_go.on_clicked(goto_gen)
    btn_auto.on_clicked(toggle_auto)
    btn_restart.on_clicked(restart)

    draw_generation(0)
    plt.tight_layout(rect=[0, 0.14, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    animate_ga_tsp()
