import tkinter as tk
from tkinter import messagebox

# Constants for annual radiation dose limits (in Sievert)
ANNUAL_DOSE_LIMIT_OCCUPATIONAL = 50 / 1000  # 50 mSv for occupational exposure (converted to Sv)
ANNUAL_DOSE_LIMIT_PUBLIC = 1 / 1000  # 1 mSv for the public (converted to Sv)

def convert_to_sievert(value, unit, radiation_type):
    """
    Converts different radiation units (Roentgen, Curie, Gray) to Sievert, adjusted for radiation type.
    """
    if unit == "R":
        if radiation_type == "Gamma":
            return value * 0.01  # 1 Roentgen ≈ 0.01 Sievert for Gamma radiation
        elif radiation_type == "Alpha":
            return value * 0.02  # 1 Roentgen ≈ 0.02 Sievert for Alpha radiation
        elif radiation_type == "Beta":
            return value * 0.015  # 1 Roentgen ≈ 0.015 Sievert for Beta radiation
    elif unit == "Ci":
        if radiation_type == "Gamma":
            return value * 37  # 1 Curie ≈ 37 Sievert for Gamma radiation
        elif radiation_type == "Alpha":
            return value * 74  # Alpha radiation is more harmful
        elif radiation_type == "Beta":
            return value * 45  # Beta radiation is intermediate
    elif unit == "Gy":
        return value  # 1 Gray = 1 Sievert (assuming it’s gamma radiation, for simplicity)
    elif unit == "Sv":
        return value  # No conversion needed if already in Sievert
    else:
        raise ValueError("Unknown unit. Please use R (Roentgen), Ci (Curie), Gy (Gray), or Sv (Sievert).")


def get_radiation_health_effects(dose):
    """
    Returns health effects based on the radiation dose in Sievert (Sv).
    """
    if dose < 0.1:
        return ("No immediate health effects. Long-term exposure may slightly increase the risk of cancer.",
                "Limit exposure and monitor over time. Regular check-ups advised.")
    elif 0.1 <= dose < 1:
        return ("Increased risk of cancer with long-term exposure. Acute symptoms unlikely.",
                "Minimize exposure, wear protective clothing, and stay indoors during high radiation events.")
    elif 1 <= dose < 2:
        return ("Mild radiation sickness possible, including nausea and fatigue. Higher cancer risk.",
                "Seek medical attention for any symptoms. Use shielding and reduce exposure duration.")
    elif 2 <= dose < 6:
        return ("Moderate to severe radiation sickness. Potential damage to internal organs, bone marrow damage.",
                "Immediate medical treatment required. Stay indoors, avoid contaminated areas, and use protective gear.")
    elif 6 <= dose < 10:
        return ("Severe radiation sickness. Death is likely without medical intervention.",
                "Emergency medical attention required. Full protection and decontamination necessary.")
    else:
        return ("Extremely high radiation dose. Death is almost certain within days or weeks.",
                "Immediate evacuation and emergency medical intervention required. Avoid exposure at all costs.")


def radiation_protection_solutions():
    """
    Returns general protection solutions for radiation exposure.
    """
    solutions = {
        "Time": "Minimize the time spent in radiation-exposed areas.",
        "Distance": "Increase distance from the radiation source to reduce exposure.",
        "Shielding": "Use protective barriers (lead, concrete, or water) to block radiation.",
        "Monitoring": "Regularly monitor radiation levels in areas where exposure is possible.",
        "Medical Check-ups": "Schedule frequent medical check-ups if exposed to ionizing radiation over time."
    }
    return solutions

def calculate_effective_dose(dose, radiation_type):
    """
    Calculates the effective dose for human health based on radiation type.
    """
    # Adjust the effective dose based on radiation type (Gamma, Alpha, Beta)
    if radiation_type == "Gamma":
        effective_dose = dose * 1.0  # Effective dose for gamma radiation
    elif radiation_type == "Alpha":
        effective_dose = dose * 20  # Alpha radiation is much more harmful internally
    elif radiation_type == "Beta":
        effective_dose = dose * 10  # Beta radiation is intermediate in its effects
    else:
        effective_dose = dose  # Default to no adjustment

    return effective_dose

# Tkinter GUI setup
class RadiationWarningApp:
    def __init__(self, aziz):
        self.root = aziz
        self.root.title("Radiation Health Effect Warning System")
        self.root.geometry("600x650")

        self.title_label = tk.Label(aziz, text="Radiation Health Effect Warning System", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=5)

        # Input Fields
        self.value_label = tk.Label(aziz, text="Enter the radiation exposure value:")
        self.value_label.pack()

        self.value_entry = tk.Entry(aziz)
        self.value_entry.pack(pady=5)

        self.radiation_type_label = tk.Label(aziz, text="Select Radiation Type (Gamma, Alpha, Beta):")
        self.radiation_type_label.pack()

        self.radiation_type = tk.StringVar()
        self.radiation_type.set("Gamma")  # Default to Gamma

        self.radiation_type_menu = tk.OptionMenu(aziz, self.radiation_type, "Gamma", "Alpha", "Beta")
        self.radiation_type_menu.pack(pady=5)

        # Frame for Radio Buttons (Unit Selection)
        self.unit_frame = tk.Frame(aziz)
        self.unit_frame.pack(pady=5)

        self.selected_unit = tk.StringVar()
        self.selected_unit.set("R")  # Default to Roentgen

        # Unit Selection Buttons (in one line)
        self.roentgen_button = tk.Radiobutton(self.unit_frame, text="Roentgen (R)", variable=self.selected_unit,
                                              value="R")
        self.roentgen_button.pack(side=tk.LEFT, padx=5)

        self.curie_button = tk.Radiobutton(self.unit_frame, text="Curie (Ci)", variable=self.selected_unit, value="Ci")
        self.curie_button.pack(side=tk.LEFT, padx=5)

        self.gray_button = tk.Radiobutton(self.unit_frame, text="Gray (Gy)", variable=self.selected_unit, value="Gy")
        self.gray_button.pack(side=tk.LEFT, padx=5)

        self.sievert_button = tk.Radiobutton(self.unit_frame, text="Sievert (Sv)", variable=self.selected_unit,
                                             value="Sv")
        self.sievert_button.pack(side=tk.LEFT, padx=5)

        # Submit Button (Green Color)
        self.submit_button = tk.Button(aziz, text="Submit", command=self.display_results, bg="green", fg="white",
                                       font=("Arial", 12, "bold"))
        self.submit_button.pack(pady=5)

        # Output Labels
        self.output_label = tk.Label(aziz, text="Results will be displayed here.", justify="left")
        self.output_label.pack(pady=5)

        # Health Warning Section
        self.health_warning_frame = tk.Frame(aziz, bd=2, relief="solid", padx=5, pady=5)
        self.health_warning_frame.pack(pady=5, fill="both")

        self.health_warning_label = tk.Label(self.health_warning_frame, text=" Health Warning ",
                                             font=("Arial", 15, "bold"), fg="red", anchor="center")
        self.health_warning_label.pack(fill="both")

        self.health_warning_output = tk.Label(self.health_warning_frame, text="", justify="left", anchor="center")
        self.health_warning_output.pack()

        # Recommended Action Section
        self.recommended_action_frame = tk.Frame(aziz, bd=2, relief="solid", padx=5, pady=5)
        self.recommended_action_frame.pack(pady=5, fill="both")

        self.recommended_action_label = tk.Label(self.recommended_action_frame, text=" Recommended Action ",
                                                 font=("Arial", 15, "bold"), anchor="center")
        self.recommended_action_label.pack(fill="both")

        self.recommended_action_output = tk.Label(self.recommended_action_frame, text="", justify="left",
                                                  anchor="center")
        self.recommended_action_output.pack()

        # General Protection Section
        self.protection_solutions_frame = tk.Frame(aziz, bd=2, relief="solid", padx=5, pady=5)
        self.protection_solutions_frame.pack(pady=5, fill="both")

        self.protection_solutions_label = tk.Label(self.protection_solutions_frame,
                                                   text=" General Protection Solutions ",
                                                   font=("Arial", 15, "bold"), fg="green", anchor="center")
        self.protection_solutions_label.pack(fill="both")

        self.protection_solutions_output = tk.Label(self.protection_solutions_frame, text="",
                                                    anchor="center")
        self.protection_solutions_output.pack()

        # Annual Dose Limit Information
        self.annual_dose_frame = tk.Frame(aziz, bd=2, relief="solid", padx=5, pady=5)
        self.annual_dose_frame.pack(pady=5, fill="both")

        self.annual_dose_label = tk.Label(self.annual_dose_frame, text=" Annual Dose Limit ",
                                          font=("Arial", 12, "bold"), anchor="center")
        self.annual_dose_label.pack(fill="both")

        self.annual_dose_output = tk.Label(self.annual_dose_frame, text="", justify="left", anchor="center")
        self.annual_dose_output.pack()

        # sign Labels
        self.output_label = tk.Label(aziz, text="@Aziz", justify="left", fg="blue")
        self.output_label.pack(padx=15,anchor="ne",side="top")

    def display_results(self):
        try:
            value = float(self.value_entry.get())
            unit = self.selected_unit.get()
            radiation_type = self.radiation_type.get()

            # Convert the input value to Sievert based on selected radiation type and unit
            dose_in_sievert = convert_to_sievert(value, unit, radiation_type)

            # Get health effects and recommendations based on the dose
            health_warning, health_solution = get_radiation_health_effects(dose_in_sievert)

            # Display health warning, action, and solutions
            self.health_warning_output.config(text=health_warning)
            self.recommended_action_output.config(text=health_solution)
            self.protection_solutions_output.config(
                text="\n".join([f"{key}: {value}" for key, value in radiation_protection_solutions().items()]))

            # Compare with annual dose limit
            if dose_in_sievert > ANNUAL_DOSE_LIMIT_OCCUPATIONAL:
                self.annual_dose_output.config(
                    text=f"Warning: Your dose exceeds the occupational annual dose limit ({ANNUAL_DOSE_LIMIT_OCCUPATIONAL * 1000} mSv).")
            elif dose_in_sievert > ANNUAL_DOSE_LIMIT_PUBLIC:
                self.annual_dose_output.config(
                    text=f"Warning: Your dose exceeds the public annual dose limit ({ANNUAL_DOSE_LIMIT_PUBLIC * 1000} mSv).")
            else:
                self.annual_dose_output.config(text="Your dose is within safe limits.")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the radiation dose.")

# Create the Tkinter window
root = tk.Tk()
app = RadiationWarningApp(root)
root.mainloop()