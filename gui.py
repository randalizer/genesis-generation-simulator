"""
Graphical interface for the Genesis Generation Simulator.
"""

import random
import tkinter as tk
from tkinter import ttk

from genesis.config import load_config
from genesis.person import Person
from genesis.simulation import Simulation

from main import load_seed_people


class SimulatorGUI:
    """Graphical interface for the simulator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Genesis Generation Simulator")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)

        self.config = load_config("config.json")

        self.people: dict[str, Person] = load_seed_people(
            "seed_people.json",
            self.config,
        )

        random.seed(self.config.random_seed)

        self.simulation = Simulation(
            self.config,
            self.people,
        )

        self.current_year = 0
        self.running = False
        self.run_after_id: str | None = None

        self._build_interface()

    def _build_interface(self) -> None:
        """Build the main application window."""

        # ------------------------------------------------------------
        # Main window grid
        # ------------------------------------------------------------

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        title = ttk.Label(
            self.root,
            text="Genesis Generation Simulator",
            font=("TkDefaultFont", 18, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            pady=(10, 5),
        )

        # Main two-column area.
        main_frame = ttk.Frame(self.root)
        main_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=5,
        )

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # ============================================================
        # LEFT COLUMN — CURRENT YEAR
        # ============================================================

        current_column = ttk.LabelFrame(
            main_frame,
            text="Current Year",
        )
        current_column.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7),
        )

        current_column.columnconfigure(0, weight=1)
        current_column.rowconfigure(1, weight=1)
        current_column.rowconfigure(2, weight=1)

        # Current-year summary.
        current_summary = ttk.Frame(current_column)
        current_summary.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=8,
        )

        self.year_label = ttk.Label(
            current_summary,
            text="Year: Not Started",
        )
        self.year_label.pack(
            anchor="w",
            pady=2,
        )

        self.birth_count_label = ttk.Label(
            current_summary,
            text="Births: 0",
        )
        self.birth_count_label.pack(
            anchor="w",
            pady=2,
        )

        self.marriage_count_label = ttk.Label(
            current_summary,
            text="Marriages: 0",
        )
        self.marriage_count_label.pack(
            anchor="w",
            pady=2,
        )

        # ------------------------------------------------------------
        # Births this year
        # ------------------------------------------------------------

        births_frame = ttk.LabelFrame(
            current_column,
            text="Births This Year",
        )
        births_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 5),
        )

        births_frame.columnconfigure(0, weight=1)
        births_frame.rowconfigure(0, weight=1)

        self.birth_list = tk.Listbox(
            births_frame,
            height=6,
        )
        self.birth_list.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(5, 0),
            pady=5,
        )

        birth_scrollbar = ttk.Scrollbar(
            births_frame,
            orient="vertical",
            command=self.birth_list.yview,
        )
        birth_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 5),
            pady=5,
        )

        self.birth_list.configure(
            yscrollcommand=birth_scrollbar.set,
        )

        self.birth_list.bind(
            "<Double-Button-1>",
            self.show_person_details,
        )

        # ------------------------------------------------------------
        # Families created this year
        # ------------------------------------------------------------

        families_frame = ttk.LabelFrame(
            current_column,
            text="Families Created This Year",
        )
        families_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(5, 10),
        )

        families_frame.columnconfigure(0, weight=1)
        families_frame.rowconfigure(0, weight=1)

        self.family_list = tk.Listbox(
            families_frame,
            height=6,
        )
        self.family_list.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(5, 0),
            pady=5,
        )

        family_scrollbar = ttk.Scrollbar(
            families_frame,
            orient="vertical",
            command=self.family_list.yview,
        )
        family_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 5),
            pady=5,
        )

        self.family_list.configure(
            yscrollcommand=family_scrollbar.set,
        )

        self.family_list.bind(
            "<Double-Button-1>",
            self.show_family_details,
        )

        # ============================================================
        # RIGHT COLUMN — TOTAL
        # ============================================================

        total_column = ttk.LabelFrame(
            main_frame,
            text="Total",
        )
        total_column.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0),
        )

        total_column.columnconfigure(0, weight=1)
        total_column.rowconfigure(1, weight=1)
        total_column.rowconfigure(2, weight=1)

        # Total summary.
        total_summary = ttk.Frame(total_column)
        total_summary.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=8,
        )

        self.population_label = ttk.Label(
            total_summary,
            text=f"Population: {self.simulation.population_count}",
        )
        self.population_label.pack(
            anchor="w",
            pady=2,
        )

        self.family_count_label = ttk.Label(
            total_summary,
            text=f"Families: {len(self.simulation.families)}",
        )
        self.family_count_label.pack(
            anchor="w",
            pady=2,
        )

        # ------------------------------------------------------------
        # All people
        # ------------------------------------------------------------

        all_people_frame = ttk.LabelFrame(
            total_column,
            text="All People",
        )
        all_people_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 5),
        )

        all_people_frame.columnconfigure(0, weight=1)
        all_people_frame.rowconfigure(0, weight=1)

        self.all_people_list = tk.Listbox(
            all_people_frame,
            height=6,
        )
        self.all_people_list.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(5, 0),
            pady=5,
        )

        all_people_scrollbar = ttk.Scrollbar(
            all_people_frame,
            orient="vertical",
            command=self.all_people_list.yview,
        )
        all_people_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 5),
            pady=5,
        )

        self.all_people_list.configure(
            yscrollcommand=all_people_scrollbar.set,
        )

        self.all_people_list.bind(
            "<Double-Button-1>",
            self.show_person_details,
        )

        # ------------------------------------------------------------
        # All families
        # ------------------------------------------------------------

        all_families_frame = ttk.LabelFrame(
            total_column,
            text="All Families",
        )
        all_families_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(5, 10),
        )

        all_families_frame.columnconfigure(0, weight=1)
        all_families_frame.rowconfigure(0, weight=1)

        self.all_families_list = tk.Listbox(
            all_families_frame,
            height=6,
        )
        self.all_families_list.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(5, 0),
            pady=5,
        )

        all_families_scrollbar = ttk.Scrollbar(
            all_families_frame,
            orient="vertical",
            command=self.all_families_list.yview,
        )
        all_families_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 5),
            pady=5,
        )

        self.all_families_list.configure(
            yscrollcommand=all_families_scrollbar.set,
        )

        self.all_families_list.bind(
            "<Double-Button-1>",
            self.show_family_details,
        )

        # ============================================================
        # CONTROLS
        # ============================================================

        controls_frame = ttk.Frame(self.root)
        controls_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=(5, 10),
        )

        ttk.Label(
            controls_frame,
            text="Run Delay (seconds):",
        ).pack(
            side="left",
            padx=(0, 5),
        )

        self.delay_var = tk.DoubleVar(value=2.0)

        self.delay_spinbox = ttk.Spinbox(
            controls_frame,
            from_=0.5,
            to=10.0,
            increment=0.5,
            textvariable=self.delay_var,
            width=6,
        )
        self.delay_spinbox.pack(
            side="left",
            padx=(0, 20),
        )

        self.pause_button = ttk.Button(
            controls_frame,
            text="Pause",
            command=self.pause_simulation,
            state="disabled",
        )
        self.pause_button.pack(
            side="right",
            padx=(5, 0),
        )

        self.run_button = ttk.Button(
            controls_frame,
            text="Run",
            command=self.start_simulation,
        )
        self.run_button.pack(
            side="right",
            padx=5,
        )

        self.next_button = ttk.Button(
            controls_frame,
            text="Next Year",
            command=self.next_year,
        )
        self.next_button.pack(
            side="right",
            padx=5,
        )

        # Populate permanent lists.
        self.refresh_all_people_list()
        self.refresh_all_families_list()

    # ================================================================
    # SIMULATION CONTROLS
    # ================================================================

    def start_simulation(self) -> None:
        """Automatically advance the simulation."""

        if self.running:
            return

        if self.current_year >= self.config.simulation_end_year:
            return

        self.running = True

        self.run_button.configure(state="disabled")
        self.next_button.configure(state="disabled")
        self.pause_button.configure(state="normal")

        self._run_next_year()

    def _run_next_year(self) -> None:
        """Advance one year and schedule the next automatic year."""

        if not self.running:
            return

        self.next_year()

        if self.current_year >= self.config.simulation_end_year:
            self.running = False
            self.run_after_id = None
            return

        try:
            delay_seconds = float(self.delay_var.get())
        except (tk.TclError, ValueError):
            delay_seconds = 2.0
            self.delay_var.set(delay_seconds)

        delay_seconds = max(
            0.5,
            min(delay_seconds, 10.0),
        )

        self.run_after_id = self.root.after(
            int(delay_seconds * 1000),
            self._run_next_year,
        )

    def pause_simulation(self) -> None:
        """Pause automatic simulation."""

        self.running = False

        if self.run_after_id is not None:
            self.root.after_cancel(self.run_after_id)
            self.run_after_id = None

        if self.current_year < self.config.simulation_end_year:
            self.run_button.configure(state="normal")
            self.next_button.configure(state="normal")

        self.pause_button.configure(state="disabled")

    def next_year(self) -> None:
        """Advance the simulation by one year."""

        next_year = self.current_year + 1

        if next_year > self.config.simulation_end_year:
            self.next_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")
            return

        result = self.simulation.run_year(next_year)

        self.current_year = next_year

        # Refresh permanent lists.
        self.refresh_all_people_list()
        self.refresh_all_families_list()

        # Update summaries.
        self.year_label.configure(
            text=f"Year: {result.year}",
        )

        self.birth_count_label.configure(
            text=f"Births: {result.birth_count}",
        )

        self.marriage_count_label.configure(
            text=f"Marriages: {result.marriage_count}",
        )

        self.population_label.configure(
            text=f"Population: {result.population_count}",
        )

        self.family_count_label.configure(
            text=f"Families: {result.family_count}",
        )

        # Clear previous year's event lists.
        self.birth_list.delete(0, tk.END)
        self.family_list.delete(0, tk.END)

        # Births this year.
        for child, family in result.births:
            sex = "Male" if child.sex == "M" else "Female"

            self.birth_list.insert(
                tk.END,
                f"{child.name} - {sex} - {family.id}",
            )

        # Families created this year.
        for family in result.families_created:
            husband = self.simulation.population[
                family.husband_id
            ]

            wife = self.simulation.population[
                family.wife_id
            ]

            self.family_list.insert(
                tk.END,
                f"{family.id} - "
                f"{husband.name} + {wife.name}",
            )

        if self.current_year >= self.config.simulation_end_year:
            self.running = False

            if self.run_after_id is not None:
                self.root.after_cancel(self.run_after_id)
                self.run_after_id = None

            self.next_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")

    # ================================================================
    # PERMANENT LISTS
    # ================================================================

    def refresh_all_people_list(self) -> None:
        """Refresh the list of all people in the simulation."""

        self.all_people_list.delete(0, tk.END)

        for person in self.simulation.population.values():
            sex = "Male" if person.sex == "M" else "Female"

            self.all_people_list.insert(
                tk.END,
                f"{person.name} - {sex}",
            )

    def refresh_all_families_list(self) -> None:
        """Refresh the list of all families in the simulation."""

        self.all_families_list.delete(0, tk.END)

        for family in self.simulation.families.values():
            husband = self.simulation.population.get(
                family.husband_id
            )

            wife = self.simulation.population.get(
                family.wife_id
            )

            husband_name = (
                husband.name if husband else "Unknown"
            )

            wife_name = (
                wife.name if wife else "Unknown"
            )

            self.all_families_list.insert(
                tk.END,
                f"{family.id} - "
                f"{husband_name} + {wife_name}",
            )

    # ================================================================
    # PERSON DETAILS
    # ================================================================

    def show_person_details(self, event: tk.Event) -> None:
        """Open a detail window for the selected person."""

        person_list = event.widget

        selection = person_list.curselection()

        if not selection:
            return

        index = selection[0]

        person_name = person_list.get(index).split(" - ")[0]

        person = next(
            (
                person
                for person in self.simulation.population.values()
                if person.name == person_name
            ),
            None,
        )

        if person is None:
            return

        father = self.simulation.population.get(
            person.father_id
        )

        mother = self.simulation.population.get(
            person.mother_id
        )

        display_year = max(self.current_year, 0)

        window = tk.Toplevel(self.root)
        window.title(person.name)
        window.geometry("400x350")

        ttk.Label(
            window,
            text=person.name,
            font=("TkDefaultFont", 16, "bold"),
        ).pack(pady=10)

        details = [
            f"ID: {person.id}",
            f"Sex: {'Male' if person.sex == 'M' else 'Female'}",
            f"Birth Year: {person.birth_year}",
            f"Current Age: {person.age(display_year)}",
            "",
            f"Father: {father.name if father else 'Unknown'}",
            f"Mother: {mother.name if mother else 'Unknown'}",
            "",
            (
                f"Hair: {person.hair_color} "
                f"(Tone {person.hair_tone})"
            ),
            (
                f"Eyes: {person.eye_color} "
                f"(Shade {person.eye_shade})"
            ),
            f"Desire for Children: {person.desire_for_children}",
        ]

        ttk.Label(
            window,
            text="\n".join(details),
            justify="left",
        ).pack(
            anchor="w",
            padx=20,
            pady=10,
        )

    # ================================================================
    # FAMILY DETAILS
    # ================================================================

    def show_family_details(self, event: tk.Event) -> None:
        """Open a detail window for the selected family."""

        family_list = event.widget

        selection = family_list.curselection()

        if not selection:
            return

        index = selection[0]

        family_id = family_list.get(index).split(" - ")[0]

        family = self.simulation.families.get(family_id)

        if family is None:
            return

        husband = self.simulation.population.get(
            family.husband_id
        )

        wife = self.simulation.population.get(
            family.wife_id
        )

        display_year = max(self.current_year, 0)

        window = tk.Toplevel(self.root)
        window.title(family.id)
        window.geometry("450x500")

        ttk.Label(
            window,
            text=f"Family {family.id}",
            font=("TkDefaultFont", 16, "bold"),
        ).pack(pady=10)

        details = [
            f"Marriage Year: {family.marriage_year}",
            (
                f"Years Married: "
                f"{family.marriage_duration(display_year)}"
            ),
            "",
            (
                f"Husband: "
                f"{husband.name if husband else 'Unknown'}"
            ),
            (
                f"Wife: "
                f"{wife.name if wife else 'Unknown'}"
            ),
            "",
            f"Children: {family.child_count}",
        ]

        ttk.Label(
            window,
            text="\n".join(details),
            justify="left",
        ).pack(
            anchor="w",
            padx=20,
            pady=10,
        )

        ttk.Label(
            window,
            text="Children",
            font=("TkDefaultFont", 11, "bold"),
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5),
        )

        child_list = tk.Listbox(
            window,
            height=10,
        )

        for child_id in family.children:
            child = self.simulation.population.get(child_id)

            if child is not None:
                sex = "Male" if child.sex == "M" else "Female"

                child_list.insert(
                    tk.END,
                    f"{child.name} - {sex} - Born Year {child.birth_year}",
                )

        child_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15),
        )

def main() -> None:
    root = tk.Tk()
    SimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()