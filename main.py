from shift_manager_oop import ShiftManager

# Define Italy's holiday dates
ITALIAN_HOLIDAYS = [
            "2017-01-01",  # Capodanno
            "2017-01-06",  # Epifania
            "2017-04-16",  # Pasqua
            "2017-04-17",  # Lunedì dell'Angelo
            "2017-04-25",  # Festa della Liberazione
            "2017-05-01",  # Festa dei Lavoratori
            "2017-06-02",  # Festa della Repubblica
            "2017-08-15",  # Ferragosto
            "2017-11-01",  # Ognissanti
            "2017-12-08",  # Immacolata Concezione
            "2017-12-25",  # Natale
            "2017-12-26",  # Santo Stefano
        ]

if __name__ == "__main__":
    shift_manager = ShiftManager(input_data_file_path=r"C:\Users\denis\OneDrive\Documenti\GitHub\ruby-challenge"
                                                      r"\level1\data.json",
                                 italian_holidays=ITALIAN_HOLIDAYS)
    shift_manager.fill_availabilities()
