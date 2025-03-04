import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from models.place import Place
from models.transition import Transition
from models.token_manager import TokenManager

class PetriNet:
    MAX_PLACES = 20  # Μέγιστος αριθμός θέσεων

    def __init__(self, name: str, gui=None):
        self.name = name
        self.places = {}
        self.transitions = {}
        self.gui = gui  # Αναφορά στο GUI για εμφάνιση μηνυμάτων

    def log_message(self, message):
        """Στέλνει μηνύματα στο GUI αντί για το terminal."""
        if self.gui:
            self.gui.update_status(message)
        else:
            print(message)

    def add_place(self, name: str, tokens: int = 0):
        """Προσθέτει έναν νέο κόμβο (Place) στο δίκτυο."""
        if len(self.places) >= self.MAX_PLACES:
            self.log_message("❌ Δεν μπορεί να προστεθεί άλλη θέση! Έχει επιτευχθεί το μέγιστο όριο των 20 θέσεων.")
            return
        self.places[name] = Place(name, tokens)
        self.log_message(f"✔ Προστέθηκε θέση: {name} με {tokens} tokens.")

    def add_transition(self, name: str, input_places: dict, output_places: dict):
        """
        Προσθέτει μια νέα μετάβαση στο Petri Net.
    
        :param name: Όνομα της μετάβασης
        :param input_places: Λεξικό {place_name: απαιτούμενα tokens}
        :param output_places: Λεξικό {place_name: tokens που προστίθενται}
        """
        for p, tokens in input_places.items():
            if tokens == 0:
                self.log_message(f"❌ Λάθος: Η θέση {p} έχει απαιτούμενα tokens = 0 στη μετάβαση {name}. Διορθώστε την τιμή!")
                return
    
        inputs = {self.places[p]: tokens for p, tokens in input_places.items()}
        outputs = {self.places[p]: tokens for p, tokens in output_places.items()}
        self.transitions[name] = Transition(name, inputs, outputs)
        self.log_message(f"✔ Προστέθηκε μετάβαση: {name}.")

    def fire_transition(self, name: str):
        """Χρησιμοποιεί το TokenManager για να εκτελέσει τη μετάβαση"""
        if name not in self.transitions:
            self.log_message(f"❌ Η μετάβαση {name} δεν υπάρχει στο Petri Net!")
            return False

        transition = self.transitions[name]
        if TokenManager.fire_transition(transition):
            self.log_message(f"✔ Η μετάβαση {name} εκτελέστηκε επιτυχώς.")
            return True
        else:
            self.log_message(f"❌ Η μετάβαση {name} δεν μπορεί να εκτελεστεί.")
            return False


    def show_state(self):
        """Εμφανίζει την τρέχουσα κατάσταση του Petri Net."""
        state_message = f"\n📌 Κατάσταση του Petri Net '{self.name}':\n"
        for place in self.places.values():
            state_message += str(place) + "\n"
        self.log_message(state_message)
