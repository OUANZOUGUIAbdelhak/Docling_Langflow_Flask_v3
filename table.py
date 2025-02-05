from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import os
import subprocess
import requests
import pandas as pd
from io import BytesIO
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# Modèle de base de données
class GlassData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    reference = db.Column(db.String(200), nullable=False)
    first_author = db.Column(db.String(100), nullable=False)
    number_of_glass_types = db.Column(db.Integer, nullable=False)
    sio2 = db.Column(db.String(100), nullable=False)
    b2o3 = db.Column(db.String(100), nullable=False)
    na2o = db.Column(db.String(100), nullable=False)
    al2o3 = db.Column(db.String(100), nullable=False)
    fines = db.Column(db.String(100), nullable=False)
    density = db.Column(db.String(100), nullable=True)
    homogeneity = db.Column(db.String(100), nullable=True)
    b_iv_percent = db.Column(db.String(100), nullable=True)
    irradiated = db.Column(db.String(100), nullable=True)
    irradiated_characteristics = db.Column(db.String(100), nullable=True)
    temperature = db.Column(db.String(100), nullable=True)
    static_dynamic = db.Column(db.String(100), nullable=True)
    granular_range = db.Column(db.String(100), nullable=True)
    geometric_specific_surface = db.Column(db.String(100), nullable=True)
    bet_specific_surface = db.Column(db.String(100), nullable=True)
    polishing_quality = db.Column(db.String(100), nullable=True)
    glass_mass = db.Column(db.String(100), nullable=True)
    s_glass = db.Column(db.String(100), nullable=True)
    v_solution = db.Column(db.String(100), nullable=True)
    solution_flow_rate = db.Column(db.String(100), nullable=True)
    initial_ph = db.Column(db.String(100), nullable=True)
    final_ph = db.Column(db.String(100), nullable=True)
    solution_composition = db.Column(db.String(100), nullable=True)
    experiment_duration = db.Column(db.String(100), nullable=True)
    final_ph_amb = db.Column(db.String(100), nullable=True)
    final_ph_test = db.Column(db.String(100), nullable=True)
    normalization_rate = db.Column(db.String(100), nullable=True)
    v0_si = db.Column(db.String(100), nullable=True)
    r_squared_si = db.Column(db.String(100), nullable=True)
    y_intercept_si = db.Column(db.String(100), nullable=True)
    v0_b = db.Column(db.String(100), nullable=True)
    y_intercept_b = db.Column(db.String(100), nullable=True)
    v0_na = db.Column(db.String(100), nullable=True)
    r_squared_na = db.Column(db.String(100), nullable=True)
    y_intercept_na = db.Column(db.String(100), nullable=True)
    v0_dm = db.Column(db.String(100), nullable=True)
    congruence = db.Column(db.String(100), nullable=True)

# Créer la base de données si elle n'existe pas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    glass_data = GlassData.query.all()
    return render_template('index.html', glass_data=glass_data)

@app.route('/add_glass_data', methods=['POST'])
def add_glass_data():
    data = request.get_json()

    try:
        new_entry = GlassData(
            doc_type=data.get('type'),
            title=data.get('title'),
            reference=data.get('reference'),
            first_author=data.get('first_author'),
            number_of_glass_types=data.get('number_of_glass_types'),
            sio2=data.get('sio2'),
            b2o3=data.get('b2o3'),
            na2o=data.get('na2o'),
            al2o3=data.get('al2o3'),
            fines=data.get('fines'),
            density=data.get('density'),
            homogeneity=data.get('homogeneity'),
            b_iv_percent=data.get('b_iv_percent'),
            irradiated=data.get('irradiated'),
            irradiated_characteristics=data.get('irradiated_characteristics'),
            temperature=data.get('temperature'),
            static_dynamic=data.get('static_dynamic'),
            granular_range=data.get('granular_range'),
            geometric_specific_surface=data.get('geometric_specific_surface'),
            bet_specific_surface=data.get('bet_specific_surface'),
            polishing_quality=data.get('polishing_quality'),
            glass_mass=data.get('glass_mass'),
            s_glass=data.get('s_glass'),
            v_solution=data.get('v_solution'),
            solution_flow_rate=data.get('solution_flow_rate'),
            initial_ph=data.get('initial_ph'),
            final_ph=data.get('final_ph'),
            solution_composition=data.get('solution_composition'),
            experiment_duration=data.get('experiment_duration'),
            final_ph_amb=data.get('final_ph_amb'),
            final_ph_test=data.get('final_ph_test'),
            normalization_rate=data.get('normalization_rate'),
            v0_si=data.get('v0_si'),
            r_squared_si=data.get('r_squared_si'),
            y_intercept_si=data.get('y_intercept_si'),
            v0_b=data.get('v0_b'),
            y_intercept_b=data.get('y_intercept_b'),
            v0_na=data.get('v0_na'),
            r_squared_na=data.get('r_squared_na'),
            y_intercept_na=data.get('y_intercept_na'),
            v0_dm=data.get('v0_dm'),
            congruence=data.get('congruence')
        )

        db.session.add(new_entry)
        db.session.commit()
        return "Glass data added successfully!", 200

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/delete_document_reference/<int:id>', methods=['POST'])
def delete_document_reference(id):
    glass_data = GlassData.query.get(id)
    db.session.delete(glass_data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        docling_script_path = '/home/intra.cea.fr/ao280403/Bureau/Docling_Langflow_flask/DLF/docling_script.py'
        if not os.path.exists(docling_script_path):
            return f"Docling script not found at: {docling_script_path}", 500

        process = subprocess.Popen(
            ["python", docling_script_path, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        total_pages = 0
        for line in process.stdout:
            logging.info(line.strip())
            if "Page" in line and "/" in line:
                parts = line.split(" ")
                current_page = int(parts[1].split("/")[0])
                total_pages = int(parts[1].split("/")[1])
                percent_complete = (current_page / total_pages) * 100
                socketio.emit('progress', {'percent_complete': percent_complete})
            elif "Table" in line or "Picture" in line:
                socketio.emit('progress', {'message': line.strip()})

        process.wait()

        doc_filename = os.path.splitext(os.path.basename(filepath))[0]
        md_filepath = os.path.join('scratch', f"{doc_filename}-md", f"{doc_filename}-plain.md")

        if not os.path.exists(md_filepath):
            return f"Markdown file not found at: {md_filepath}", 500

        with open(md_filepath, 'r') as md_file:
            md_content = md_file.read()

        response = requests.post(
            "http://127.0.0.1:7860/api/v1/run/a7e4b6a1-d444-487c-bec7-a954e6d42725?stream=false",
            json={
                "input_value": md_content,
                "output_type": "chat",
                "input_type": "text",
                "tweaks": {
                    "File-3JBJ7": {},
                    "Prompt-F8PHW": {},
                    "ParseData-ggwft": {},
                    "ChatOutput-Uou7S": {},
                    "TextInput-Lc0yv": {},
                    "MistralModel-X63zd": {},
                    "CustomComponent-OsOFR": {}
                }
            }
        )

        return jsonify({"message": "File processed successfully", "data": response.json()})

@app.route('/download_excel', methods=['GET'])
def download_excel():
    glass_data = GlassData.query.all()
    data = []
    for entry in glass_data:
        data.append({
            "Type": entry.doc_type,
            "Titre": entry.title,
            "Référence": entry.reference,
            "Premier Auteur": entry.first_author,
            "Nombre de types de verres": entry.number_of_glass_types,
            "SiO₂": entry.sio2,
            "B₂O₃": entry.b2o3,
            "Na₂O": entry.na2o,
            "Al₂O₃": entry.al2o3,
            "Fines": entry.fines,
            "Densité": entry.density,
            "Homogénéité": entry.homogeneity,
            "% B(IV)": entry.b_iv_percent,
            "Irradié": entry.irradiated,
            "Caractéristiques si irradié": entry.irradiated_characteristics,
            "Température": entry.temperature,
            "Statique/dynamique": entry.static_dynamic,
            "Plage granulo si poudre": entry.granular_range,
            "Surface spécifique géométrique si poudre": entry.geometric_specific_surface,
            "Surface spécifique BET si poudre": entry.bet_specific_surface,
            "Qualité polissage si monolithe": entry.polishing_quality,
            "Masse verre": entry.glass_mass,
            "S(verre)": entry.s_glass,
            "V(solution)": entry.v_solution,
            "Débit solution": entry.solution_flow_rate,
            "pH initial (T amb)": entry.initial_ph,
            "pH final (T essai)": entry.final_ph,
            "Compo solution": entry.solution_composition,
            "Durée expérience": entry.experiment_duration,
            "pH final (T amb)": entry.final_ph_amb,
            "pH final (T essai)": entry.final_ph_test,
            "Normalisation vitesse (Spm ou SBET)": entry.normalization_rate,
            "V₀(Si)": entry.v0_si,
            "r²": entry.r_squared_si,
            "Ordonnée origine": entry.y_intercept_si,
            "V₀(B)": entry.v0_b,
            "Ordonnée origine": entry.y_intercept_b,
            "V₀(Na)": entry.v0_na,
            "r²": entry.r_squared_na,
            "Ordonnée origine": entry.y_intercept_na,
            "V₀(ΔM)": entry.v0_dm,
            "Congruence": entry.congruence
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Glass Data')
    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='glass_data.xlsx')

@socketio.on('connect')
def handle_connect():
    emit('status', {'msg': 'Connected'})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    socketio.run(app, debug=True, port=5001)
