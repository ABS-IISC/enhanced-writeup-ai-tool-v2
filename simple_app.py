from flask import Flask, render_template, request, jsonify
import os
import json
import time
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads' if os.environ.get('RAILWAY_ENVIRONMENT') else 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

# Simple global storage
sessions = {}
current_session_id = None

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('simple.html')

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

@app.route('/api/upload', methods=['POST'])
def upload():
    global current_session_id
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file'}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.docx'):
        return jsonify({'success': False, 'error': 'Only .docx files'}), 400
    
    session_id = str(uuid.uuid4())[:8]
    current_session_id = session_id
    
    sessions[session_id] = {
        'filename': file.filename,
        'sections': {
            'Executive Summary': 'This is the executive summary section with key findings and recommendations.',
            'Background': 'Background information and context for the analysis.',
            'Analysis': 'Detailed analysis of the data and findings.',
            'Recommendations': 'Key recommendations based on the analysis.'
        },
        'analysis': {},
        'status': 'uploaded'
    }
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'document_name': file.filename,
        'sections': list(sessions[session_id]['sections'].keys())
    })

@app.route('/api/start_analysis', methods=['POST'])
def start_analysis():
    if not current_session_id:
        return jsonify({'success': False, 'error': 'No document'}), 400
    
    session = sessions[current_session_id]
    
    # Generate simple analysis
    for section_name in session['sections']:
        session['analysis'][section_name] = {
            'feedback_items': [
                {
                    'id': str(uuid.uuid4())[:8],
                    'type': 'improvement',
                    'description': f'Consider adding more detail to {section_name}',
                    'suggestion': 'Include specific examples and data',
                    'risk_level': 'Medium'
                },
                {
                    'id': str(uuid.uuid4())[:8],
                    'type': 'positive',
                    'description': f'Good structure in {section_name}',
                    'suggestion': 'Continue this approach',
                    'risk_level': 'Low'
                }
            ]
        }
    
    session['status'] = 'analyzed'
    return jsonify({'success': True})

@app.route('/api/status')
def status():
    if not current_session_id:
        return jsonify({'status': 'no_session', 'progress': {'progress': 0}})
    
    session = sessions[current_session_id]
    
    # Count risks
    high_risk = medium_risk = low_risk = 0
    for analysis in session['analysis'].values():
        for item in analysis.get('feedback_items', []):
            risk = item.get('risk_level', 'Low')
            if risk == 'High': high_risk += 1
            elif risk == 'Medium': medium_risk += 1
            else: low_risk += 1
    
    return jsonify({
        'status': session['status'],
        'progress': {'progress': 100 if session['status'] == 'analyzed' else 0},
        'statistics': {
            'total_sections': len(session['sections']),
            'high_risk': high_risk,
            'medium_risk': medium_risk,
            'low_risk': low_risk
        },
        'analysis_complete': session['status'] == 'analyzed',
        'functionalities_enabled': True
    })

@app.route('/api/sections')
def sections():
    if not current_session_id:
        return jsonify({'sections': []})
    
    session = sessions[current_session_id]
    sections_info = []
    
    for name, content in session['sections'].items():
        analysis = session['analysis'].get(name, {})
        feedback_items = analysis.get('feedback_items', [])
        
        sections_info.append({
            'name': name,
            'word_count': len(content.split()),
            'analyzed': name in session['analysis'],
            'feedback_count': len(feedback_items),
            'high_risk_count': sum(1 for item in feedback_items if item.get('risk_level') == 'High'),
            'medium_risk_count': sum(1 for item in feedback_items if item.get('risk_level') == 'Medium'),
            'low_risk_count': sum(1 for item in feedback_items if item.get('risk_level') == 'Low')
        })
    
    return jsonify({'sections': sections_info})

@app.route('/api/section/<section_name>')
def section_detail(section_name):
    if not current_session_id:
        return jsonify({'success': False}), 404
    
    session = sessions[current_session_id]
    
    if section_name not in session['sections']:
        return jsonify({'success': False}), 404
    
    return jsonify({
        'success': True,
        'section_name': section_name,
        'content': session['sections'][section_name],
        'analysis': session['analysis'].get(section_name, {}),
        'word_count': len(session['sections'][section_name].split())
    })

@app.route('/api/chat/basic', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    # Simple responses
    if 'risk' in message.lower():
        response = "I can see risk items in your document. High-risk items need immediate attention, medium-risk should be addressed, and low-risk are minor improvements."
    elif 'section' in message.lower():
        response = "Select a section from the sidebar to see detailed analysis and recommendations."
    elif 'help' in message.lower():
        response = "I can help you analyze your document. Upload a file, start analysis, then ask me about sections, risks, or improvements."
    else:
        response = "Hello! I'm your AI assistant. I can help analyze your document sections and provide recommendations. What would you like to know?"
    
    return jsonify({
        'success': True,
        'response': response
    })

@app.route('/api/feedback/accept', methods=['POST'])
def accept_feedback():
    return jsonify({'success': True, 'message': 'Feedback accepted'})

@app.route('/api/feedback/reject', methods=['POST'])
def reject_feedback():
    return jsonify({'success': True, 'message': 'Feedback rejected'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=False)