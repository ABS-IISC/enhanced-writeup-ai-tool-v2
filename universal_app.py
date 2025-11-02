"""
Universal Deployment App - Works on Localhost, Railway, Ngrok, and other platforms
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import threading
import time
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid
from collections import defaultdict
import sys

# Import with fallback
try:
    from docx import Document
except ImportError:
    print("Warning: python-docx not installed. Install with: pip install python-docx")
    Document = None

app = Flask(__name__)

# Universal configuration that works everywhere
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables (same as original)
current_session = None
analysis_progress = {"progress": 0, "message": "Ready", "current_section": ""}
analysis_status = "idle"
analysis_logs = []
chat_history = []
analysis_complete = False
functionalities_enabled = False

# Copy all your existing classes and functions here
class AnalysisSession:
    def __init__(self):
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.document_name = ""
        self.document_path = ""
        self.sections = {}
        self.analysis_results = {}
        self.user_feedback = defaultdict(list)
        self.accepted_feedback = defaultdict(list)
        self.rejected_feedback = defaultdict(list)
        self.current_section_index = 0
        self.analysis_thread = None
        self.stop_analysis_flag = False
        self.guidelines_document = None
        self.guidelines_content = None
        
    def get_section_names(self):
        return list(self.sections.keys())
    
    def get_current_section_name(self):
        section_names = self.get_section_names()
        if 0 <= self.current_section_index < len(section_names):
            return section_names[self.current_section_index]
        return None

def extract_document_sections_from_docx(doc):
    if not doc:
        return {"Sample Section": "Document processing not available"}
    
    sections = {}
    current_section = "Executive Summary"
    content = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            is_bold = any(run.bold for run in para.runs if run.bold)
            if is_bold and len(text) < 100 and any(keyword in text.lower() for keyword in ['summary', 'background', 'analysis', 'recommendation', 'conclusion', 'objective', 'scope', 'methodology']):
                if content:
                    sections[current_section] = '\n'.join(content)
                current_section = text.rstrip(':')
                content = []
            else:
                content.append(text)
    
    if content:
        sections[current_section] = '\n'.join(content)
    
    return sections

def analyze_section_with_ai(section_name, section_content, guidelines=None):
    time.sleep(2)  # Simulate AI processing
    import random
    
    feedback_items = []
    
    # Generate realistic feedback
    section_lower = section_name.lower()
    
    if 'summary' in section_lower:
        feedback_items.extend([
            {
                "id": f"ai_{uuid.uuid4().hex[:8]}",
                "type": "critical",
                "category": "completeness",
                "description": "Executive summary lacks key performance metrics and quantitative data",
                "suggestion": "Include specific numbers, percentages, and measurable outcomes to strengthen the summary",
                "risk_level": "High",
                "confidence": 0.92,
                "example": "Add metrics like '25% improvement in efficiency' or 'reduced processing time by 3 days'",
                "questions": ["Does this summary include quantifiable results?", "Are key stakeholders clearly identified?"]
            }
        ])
    
    # Add positive feedback
    if random.random() > 0.3:
        feedback_items.append({
            "id": f"ai_{uuid.uuid4().hex[:8]}",
            "type": "positive",
            "category": "strength",
            "description": f"Strong content structure and clear presentation in {section_name}",
            "suggestion": "Continue maintaining this level of clarity and organization",
            "risk_level": "Low",
            "confidence": 0.95,
            "example": "The logical flow and professional tone enhance readability",
            "questions": []
        })
    
    return {"feedback_items": feedback_items}

def process_chat_query(query, context):
    query_lower = query.lower()
    current_section = context.get('current_section', 'No section selected')
    doc_name = context.get('document_name', 'your document')
    functionalities_enabled = context.get('functionalities_enabled', False)
    
    if not functionalities_enabled:
        return f"**TARA AI - Analysis in Progress**\n\nI'm currently analyzing your document. Once complete, I'll have full access to provide detailed insights!"
    
    return f"**Hello! I'm TARA, your AI document analysis assistant.**\n\nI've completed analyzing {doc_name} and can help with analysis support and guidance.\n\nWhat would you like to explore?"

def log_activity(message, level="INFO", section=None):
    log_entry = {
        "id": f"log_{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
        "section": section
    }
    analysis_logs.append(log_entry)
    return log_entry

# Static files route for deployment
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# All your existing routes (copy from original app.py)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_document():
    global current_session, analysis_status
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.docx'):
        return jsonify({'success': False, 'error': 'Please upload a .docx file'}), 400
    
    try:
        current_session = AnalysisSession()
        analysis_status = "idle"
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        current_session.document_name = filename
        current_session.document_path = filepath
        
        if Document:
            doc = Document(filepath)
            sections = extract_document_sections_from_docx(doc)
        else:
            sections = {"Sample Section": "Document uploaded successfully. Full processing requires python-docx."}
        
        current_session.sections = sections
        
        log_activity(f"Document uploaded: {filename} ({len(sections)} sections)", "SUCCESS")
        
        return jsonify({
            'success': True,
            'session_id': current_session.session_id,
            'document_name': filename,
            'sections': list(sections.keys()),
            'total_sections': len(sections),
            'file_size': os.path.getsize(filepath)
        })
        
    except Exception as e:
        log_activity(f"Upload failed: {str(e)}", "ERROR")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start_analysis', methods=['POST'])
def start_analysis():
    global current_session, analysis_status, analysis_progress, analysis_complete, functionalities_enabled
    
    if not current_session:
        return jsonify({'success': False, 'error': 'No document uploaded'}), 400
    
    if analysis_status == "running":
        return jsonify({'success': False, 'error': 'Analysis already in progress'}), 400
    
    analysis_status = "running"
    analysis_progress = {"progress": 0, "message": "Initializing Analysis...", "current_section": ""}
    current_session.stop_analysis_flag = False
    analysis_complete = False
    functionalities_enabled = False
    
    def run_analysis():
        global analysis_status, analysis_progress, analysis_complete, functionalities_enabled
        
        try:
            section_names = current_session.get_section_names()
            total_sections = len(section_names)
            
            for i, section_name in enumerate(section_names):
                if current_session.stop_analysis_flag:
                    analysis_status = "stopped"
                    return
                
                progress_percent = int((i / total_sections) * 85)
                analysis_progress = {
                    "progress": progress_percent,
                    "message": f"Analyzing {section_name} ({i+1}/{total_sections})",
                    "current_section": section_name
                }
                
                section_content = current_session.sections[section_name]
                result = analyze_section_with_ai(section_name, section_content)
                current_session.analysis_results[section_name] = result
                
                time.sleep(1.5)
            
            analysis_progress = {"progress": 100, "message": "Analysis completed!", "current_section": ""}
            analysis_status = "completed"
            analysis_complete = True
            functionalities_enabled = True
            
        except Exception as e:
            analysis_status = "error"
            analysis_progress["message"] = f"Analysis failed: {str(e)}"
    
    current_session.analysis_thread = threading.Thread(target=run_analysis)
    current_session.analysis_thread.daemon = True
    current_session.analysis_thread.start()
    
    return jsonify({'success': True, 'message': 'Analysis started'})

@app.route('/api/status')
def get_status():
    global analysis_status, analysis_progress, analysis_logs, analysis_complete, functionalities_enabled
    
    if not current_session:
        return jsonify({
            'status': 'no_session',
            'progress': analysis_progress,
            'logs': analysis_logs[-10:],
            'analysis_complete': False,
            'functionalities_enabled': False,
            'statistics': {'total_sections': 0, 'analyzed_sections': 0, 'total_feedback': 0, 'high_risk': 0, 'medium_risk': 0, 'low_risk': 0}
        })
    
    # Calculate statistics
    total_feedback = high_risk = medium_risk = low_risk = 0
    for result in current_session.analysis_results.values():
        feedback_items = result.get('feedback_items', [])
        total_feedback += len(feedback_items)
        for item in feedback_items:
            risk_level = item.get('risk_level', 'Low')
            if risk_level == 'High': high_risk += 1
            elif risk_level == 'Medium': medium_risk += 1
            else: low_risk += 1
    
    return jsonify({
        'status': analysis_status,
        'progress': analysis_progress,
        'logs': analysis_logs[-20:],
        'analysis_complete': analysis_complete,
        'functionalities_enabled': functionalities_enabled,
        'statistics': {
            'total_sections': len(current_session.sections),
            'analyzed_sections': len(current_session.analysis_results),
            'total_feedback': total_feedback,
            'high_risk': high_risk,
            'medium_risk': medium_risk,
            'low_risk': low_risk
        }
    })

@app.route('/api/sections')
def get_sections():
    if not current_session:
        return jsonify({'sections': []})
    
    sections_info = []
    for section_name, content in current_session.sections.items():
        analysis_result = current_session.analysis_results.get(section_name, {})
        feedback_items = analysis_result.get('feedback_items', [])
        
        risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for item in feedback_items:
            risk_level = item.get('risk_level', 'Low')
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
        
        sections_info.append({
            'name': section_name,
            'word_count': len(content.split()),
            'analyzed': section_name in current_session.analysis_results,
            'feedback_count': len(feedback_items),
            'high_risk_count': risk_counts['High'],
            'medium_risk_count': risk_counts['Medium'],
            'low_risk_count': risk_counts['Low']
        })
    
    return jsonify({'sections': sections_info})

@app.route('/api/section/<section_name>')
def get_section_analysis(section_name):
    if not current_session or section_name not in current_session.sections:
        return jsonify({'success': False, 'error': 'Section not found'}), 404
    
    content = current_session.sections.get(section_name, "")
    analysis = current_session.analysis_results.get(section_name, {})
    
    return jsonify({
        'success': True,
        'section_name': section_name,
        'content': content,
        'analysis': analysis,
        'word_count': len(content.split()),
        'character_count': len(content)
    })

@app.route('/api/chat/basic', methods=['POST'])
def basic_chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        context = {
            'current_section': current_session.get_current_section_name() if current_session else None,
            'document_name': current_session.document_name if current_session else None,
            'functionalities_enabled': functionalities_enabled
        }
        
        response = process_chat_query(message, context)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Health check endpoint for deployment platforms
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("Universal Writeup Automation AI Tool")
    print("Compatible with: Localhost, Railway, Ngrok, Heroku, and more")
    print("=" * 50)
    
    # Universal port detection
    port = int(os.environ.get('PORT', os.environ.get('port', 5005)))
    host = '0.0.0.0'  # Works on all platforms
    
    print(f"Starting server on {host}:{port}")
    app.run(debug=False, host=host, port=port)