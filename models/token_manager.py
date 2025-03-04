class TokenManager:
    @staticmethod
    def can_fire(transition):
        """Ελέγχει αν μια μετάβαση μπορεί να εκτελεστεί"""
        print(f"🔍 Έλεγχος αν μπορεί να εκτελεστεί η μετάβαση {transition.name}")

        if not transition.inputs:  # Αν δεν υπάρχουν input places, μπορεί να εκτελεστεί άμεσα
            print(f"✅ Η μετάβαση {transition.name} μπορεί να εκτελεστεί γιατί δεν έχει inputs.")
            return True

        for place, tokens in transition.inputs.items():
            print(f"📍 Έλεγχος θέσης {place.name}: έχει {place.tokens} tokens, απαιτούνται {tokens}.")

        # 🔥 Εδώ διασφαλίζουμε ότι η μετάβαση εκτελείται ΜΟΝΟ αν όλα τα places έχουν tokens!
            if tokens == 0:  
                print(f"⚠ Προειδοποίηση: Το {place.name} απαιτεί 0 tokens. Είναι σωστό;")
            elif place.tokens < tokens:
                print(f"❌ Η θέση {place.name} δεν έχει αρκετά tokens!")
                return False

        print(f"✔ Όλες οι θέσεις έχουν αρκετά tokens για τη μετάβαση {transition.name}.")
        return True


    @staticmethod
    def fire_transition(transition):
        """Εκτελεί μια μετάβαση αν είναι εφικτό και μεταφέρει τα tokens."""
        print(f"\n🚀 Προσπάθεια εκτέλεσης της μετάβασης {transition.name}...")

        if not TokenManager.can_fire(transition):
            print(f"❌ Η μετάβαση {transition.name} ΔΕΝ μπορεί να εκτελεστεί λόγω έλλειψης tokens.")
            return False

        print(f"🔄 Αφαίρεση tokens από τις θέσεις εισόδου...")
        for place, tokens in transition.inputs.items():
            print(f" - Από τη θέση {place.name}: {place.tokens} ➝ {place.tokens - tokens}")
            place.tokens -= tokens

        if not transition.outputs:
            print(f"🔥 Η μετάβαση {transition.name} εκτελέστηκε και κατανάλωσε tokens χωρίς έξοδο.")
            return True

        print(f"📥 Προσθήκη tokens στις θέσεις εξόδου...")
        for place, tokens in transition.outputs.items():
            print(f" - Στη θέση {place.name}: {place.tokens} ➝ {place.tokens + tokens}")
            place.tokens += tokens

        print(f"✔ Η μετάβαση {transition.name} εκτελέστηκε επιτυχώς.")
        return True
