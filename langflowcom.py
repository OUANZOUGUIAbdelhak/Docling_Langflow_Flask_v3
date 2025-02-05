from langflow.custom import Component
from langflow.io import Output, MessageTextInput
from langflow.schema import Data
import requests

class SendGlassDataToTableComponent(Component):
    display_name = "Send Glass Data to Table"
    description = "Send detailed glass composition and document reference information to the Flask server."
    icon = "table"

    inputs = [
        MessageTextInput(
            name="extracted_text",
            display_name="Extracted Text",
            info=(
                "Extracted text containing document reference and glass composition information."
            ),
            value=(
                "1. Type du document : Example Type\n"
                "2. Titre du document : Example Title\n"
                "3. Référence : Example Reference\n"
                "4. Premier Auteur : Example Author\n"
                "5. Nombre de types de verres : 1\n"
                "6. SiO₂ : 50\n"
                "7. B₂O₃ : 10\n"
                "8. Na₂O : 20\n"
                "9. Al₂O₃ : 15\n"
                "10. Fines : 5\n"
                "11. Densité : 2.50\n"
                "12. Homogénéité : Homogène\n"
                "13. % B(IV) : 60.00\n"
                "14. Irradié : O\n"
                "15. Caractéristiques si irradié : Commentaire\n"
                "16. Température : 25\n"
                "17. Statique/dynamique : Commentaire\n"
                "18. Plage granulo si poudre : 100\n"
                "19. Surface spécifique géométrique si poudre : 50\n"
                "20. Surface spécifique BET si poudre : 60\n"
                "21. Qualité polissage si monolithe : Commentaire\n"
                "22. Masse verre : 100\n"
                "23. S(verre) : 50\n"
                "24. V(solution) : 1000\n"
                "25. Débit solution : 50\n"
                "26. pH initial (T amb) : 6-7\n"
                "27. pH final (T essai) : 6-7\n"
                "28. Compo solution : Eau pure\n"
                "29. Durée expérience : 28\n"
                "30. pH final (T amb) : 6-7\n"
                "31. pH final (T essai) : 6-7\n"
                "32. Normalisation vitesse (Spm ou SBET) : 2.4\n"
                "33. V₀(Si) : 2.4\n"
                "34. r² : 0.959\n"
                "35. Ordonnée origine : 0.00\n"
                "36. V₀(B) : 2.4\n"
                "37. Ordonnée origine : 0.00\n"
                "38. V₀(Na) : 2.4\n"
                "39. r² : 0.959\n"
                "40. Ordonnée origine : 0.00\n"
                "41. V₀(ΔM) : 2.4\n"
                "42. Congruence : Congruente\n"
            ),
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Response", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        extracted_text = self.extracted_text
        print(f"Extracted Text: {extracted_text}")

        try:
            # Nettoyer et analyser le texte
            lines = [line.strip() for line in extracted_text.split("\n") if line.strip()]

            # Extraction des données
            doc_type = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("1. Type du document :")), None)
            title = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("2. Titre du document :")), None)
            reference = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("3. Référence :")), None)
            first_author = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("4. Premier Auteur :")), None)
            number_of_glass_types = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("5. Nombre de types de verres :")), None)
            sio2 = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("6. SiO₂ :")), None)
            b2o3 = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("7. B₂O₃ :")), None)
            na2o = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("8. Na₂O :")), None)
            al2o3 = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("9. Al₂O₃ :")), None)
            fines = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("10. Fines :")), None)
            density = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("11. Densité :")), None)
            homogeneity = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("12. Homogénéité :")), None)
            b_iv_percent = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("13. % B(IV) :")), None)
            irradiated = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("14. Irradié :")), None)
            irradiated_characteristics = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("15. Caractéristiques si irradié :")), None)
            temperature = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("16. Température :")), None)
            static_dynamic = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("17. Statique/dynamique :")), None)
            granular_range = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("18. Plage granulo si poudre :")), None)
            geometric_specific_surface = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("19. Surface spécifique géométrique si poudre :")), None)
            bet_specific_surface = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("20. Surface spécifique BET si poudre :")), None)
            polishing_quality = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("21. Qualité polissage si monolithe :")), None)
            glass_mass = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("22. Masse verre :")), None)
            s_glass = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("23. S(verre) :")), None)
            v_solution = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("24. V(solution) :")), None)
            solution_flow_rate = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("25. Débit solution :")), None)
            initial_ph = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("26. pH initial (T amb) :")), None)
            final_ph = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("27. pH final (T essai) :")), None)
            solution_composition = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("28. Compo solution :")), None)
            experiment_duration = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("29. Durée expérience :")), None)
            final_ph_amb = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("30. pH final (T amb) :")), None)
            final_ph_test = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("31. pH final (T essai) :")), None)
            normalization_rate = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("32. Normalisation vitesse (Spm ou SBET) :")), None)
            v0_si = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("33. V₀(Si) :")), None)
            r_squared_si = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("34. r² :")), None)
            y_intercept_si = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("35. Ordonnée origine :")), None)
            v0_b = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("36. V₀(B) :")), None)
            y_intercept_b = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("37. Ordonnée origine :")), None)
            v0_na = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("38. V₀(Na) :")), None)
            r_squared_na = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("39. r² :")), None)
            y_intercept_na = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("40. Ordonnée origine :")), None)
            v0_dm = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("41. V₀(ΔM) :")), None)
            congruence = next((line.split(":", 1)[1].strip() for line in lines if line.startswith("42. Congruence :")), None)

            if not all([doc_type, title, reference, first_author, number_of_glass_types, sio2, b2o3, na2o, al2o3, fines, density, homogeneity, b_iv_percent, irradiated, irradiated_characteristics, temperature, static_dynamic, granular_range, geometric_specific_surface, bet_specific_surface, polishing_quality, glass_mass, s_glass, v_solution, solution_flow_rate, initial_ph, final_ph, solution_composition, experiment_duration, final_ph_amb, final_ph_test, normalization_rate, v0_si, r_squared_si, y_intercept_si, v0_b, y_intercept_b, v0_na, r_squared_na, y_intercept_na, v0_dm, congruence]):
                raise ValueError("Some fields are missing.")

            # Préparer les données
            url = 'http://127.0.0.1:5001/add_glass_data'
            data = {
                "type": doc_type,
                "title": title,
                "reference": reference,
                "first_author": first_author,
                "number_of_glass_types": number_of_glass_types,
                "sio2": sio2,
                "b2o3": b2o3,
                "na2o": na2o,
                "al2o3": al2o3,
                "fines": fines,
                "density": density,
                "homogeneity": homogeneity,
                "b_iv_percent": b_iv_percent,
                "irradiated": irradiated,
                "irradiated_characteristics": irradiated_characteristics,
                "temperature": temperature,
                "static_dynamic": static_dynamic,
                "granular_range": granular_range,
                "geometric_specific_surface": geometric_specific_surface,
                "bet_specific_surface": bet_specific_surface,
                "polishing_quality": polishing_quality,
                "glass_mass": glass_mass,
                "s_glass": s_glass,
                "v_solution": v_solution,
                "solution_flow_rate": solution_flow_rate,
                "initial_ph": initial_ph,
                "final_ph": final_ph,
                "solution_composition": solution_composition,
                "experiment_duration": experiment_duration,
                "final_ph_amb": final_ph_amb,
                "final_ph_test": final_ph_test,
                "normalization_rate": normalization_rate,
                "v0_si": v0_si,
                "r_squared_si": r_squared_si,
                "y_intercept_si": y_intercept_si,
                "v0_b": v0_b,
                "y_intercept_b": y_intercept_b,
                "v0_na": v0_na,
                "r_squared_na": r_squared_na,
                "y_intercept_na": y_intercept_na,
                "v0_dm": v0_dm,
                "congruence": congruence
            }
            print(f"Sending data: {data}")

            response = requests.post(url, json=data)

            if response.status_code == 200:
                return Data(value="Glass data added successfully!")
            else:
                return Data(value=f"Error adding glass data. Status Code: {response.status_code} - {response.text}")

        except Exception as e:
            return Data(value=f"Exception occurred: {str(e)}")
