from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from routes.vendedores import process_excel_file

app = Flask(__name__, static_folder='./static')
CORS(app)

DATA_FILE = './src/data/all_vendors_data.json'
EXCEL_FILE = './src/data/TestecampanhasVBA3.0MACRO-JULHO.xlsm'

def load_initial_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Tentar processar a planilha na inicializacao se ela existir
try:
    if os.path.exists(EXCEL_FILE):
        processed_data = process_excel_file(EXCEL_FILE)
        save_data(processed_data)
except Exception as e:
    print(f"Erro ao processar a planilha na inicializacao: {e}")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/status')
def status():
    data = load_initial_data()
    return jsonify({
        'status': 'ok',
        'data_loaded': len(data) > 0,
        'vendedores_count': len(data)
    })

@app.route('/api/vendedores')
def get_vendedores():
    data = load_initial_data()
    vendedores_resumidos = [{'codigo': k, 'nome': v['nome_vendedor']} for k, v in data.items()]
    return jsonify(vendedores_resumidos)

@app.route('/api/vendedores/<int:codigo>')
def vendedor_detail(codigo):
    data = load_initial_data()
    vendedor = data.get(str(codigo))
    if vendedor:
        return jsonify(vendedor)
    return jsonify({'error': 'Vendedor nao encontrado'}), 404

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xlsm')):
        os.makedirs('./src/data', exist_ok=True)
        filepath = os.path.join('./src/data', file.filename)
        file.save(filepath)
        try:
            processed_data = process_excel_file(filepath)
            save_data(processed_data)
            return jsonify({'message': 'Planilha processada com sucesso', 'vendedores_count': len(processed_data)}), 200
        except Exception as e:
            return jsonify({'error': f'Erro ao processar a planilha: {str(e)}'}), 500
    return jsonify({'error': 'Formato de arquivo nao suportado. Use .xlsx ou .xlsm'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
