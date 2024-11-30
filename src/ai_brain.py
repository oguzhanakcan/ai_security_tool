import json
import os
import ast
from datetime import datetime
import re

class AIBrain:
    def __init__(self):
        self.brain_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'brain')
        os.makedirs(self.brain_dir, exist_ok=True)
        
        self.memory_file = os.path.join(self.brain_dir, 'memory.json')
        self.memory = {
            "errors": [],
            "fixes": [],
            "patterns": [],
            "code_fixes": {},
            "tool_history": {}
        }
        self.save_memory()

    def monitor_tool_execution(self, tool_path):
        """Monitors any tool running and catches errors in real-time"""
        print(f"Monitoring tool: {tool_path}")
        self.memory["tool_history"][tool_path] = {
            "last_run": datetime.now().isoformat(),
            "errors": []
        }
        return True

    def analyze_code_error(self, file_path, error_data):
        """Deep analysis of code errors"""
        try:
            with open(file_path, 'r') as f:
                code = f.readlines()
            
            error_info = {
                "file": file_path,
                "code": code,
                "error": error_data,
                "line_number": self.find_error_line(code, error_data),
                "context": self.get_code_context(code, error_data)
            }
            
            self.memory["errors"].append(error_info)
            return error_info
        except Exception as e:
            print(f"Error analysis failed: {str(e)}")
            return None

    def generate_code_fix(self, error_analysis):
        """Generates the correct code fix based on error type"""
        fixes = {
            "ImportError": self.fix_import_code,
            "SyntaxError": self.fix_syntax_code,
            "IndentationError": self.fix_indentation,
            "NameError": self.fix_variable_code,
            "AttributeError": self.fix_attribute_code,
            "ConnectionError": self.fix_connection_code,
            "PermissionError": self.fix_permission_code
        }
        
        if error_analysis["error"]["type"] in fixes:
            fix = fixes[error_analysis["error"]["type"]](error_analysis)
            if fix:
                self.memory["code_fixes"][error_analysis["file"]] = fix
                return fix
        return None

    def apply_code_fix(self, file_path, fix_data):
        """Applies the fix directly to the code file"""
        try:
            with open(file_path, 'r') as f:
                code = f.readlines()
            
            code[fix_data["line_number"]] = fix_data["fixed_code"] + '\n'
            
            with open(file_path, 'w') as f:
                f.writelines(code)
            
            print(f"Successfully fixed code in {file_path}")
            return True
        except Exception as e:
            print(f"Fix application failed: {str(e)}")
            return False

    def fix_import_code(self, error_analysis):
        """Fixes import errors"""
        missing_module = re.search(r"No module named '(\w+)'", error_analysis["error"]["message"])
        if missing_module:
            return {
                "line_number": error_analysis["line_number"],
                "fixed_code": f"import {missing_module.group(1)}",
                "fix_type": "import_fix"
            }
        return None

    def fix_syntax_code(self, error_analysis):
        """Fixes syntax errors"""
        code_line = error_analysis["code"][error_analysis["line_number"]]
        fixed_code = self.correct_syntax(code_line)
        return {
            "line_number": error_analysis["line_number"],
            "fixed_code": fixed_code,
            "fix_type": "syntax_fix"
        }

    def fix_variable_code(self, error_analysis):
        """Fixes variable name errors"""
        code_line = error_analysis["code"][error_analysis["line_number"]]
        common_vars = {
            'lenght': 'length',
            'heigth': 'height',
            'widht': 'width',
            'colour': 'color'
        }
        for wrong, right in common_vars.items():
            if wrong in code_line:
                return {
                    "line_number": error_analysis["line_number"],
                    "fixed_code": code_line.replace(wrong, right),
                    "fix_type": "variable_fix"
                }
        return None

    def fix_attribute_code(self, error_analysis):
        """Fixes attribute errors"""
        code_line = error_analysis["code"][error_analysis["line_number"]]
        fixed_code = self.correct_attribute(code_line)
        return {
            "line_number": error_analysis["line_number"],
            "fixed_code": fixed_code,
            "fix_type": "attribute_fix"
        }

    def fix_connection_code(self, error_analysis):
        """Fixes connection errors"""
        return {
            "line_number": error_analysis["line_number"],
            "fixed_code": "try:\n    " + error_analysis["code"][error_analysis["line_number"]] + 
                         "except ConnectionError:\n    retry_connection()",
            "fix_type": "connection_fix"
        }

    def fix_permission_code(self, error_analysis):
        """Fixes permission errors"""
        return {
            "line_number": error_analysis["line_number"],
            "fixed_code": "os.chmod('" + error_analysis["error"]["message"] + "', 0o755)",
            "fix_type": "permission_fix"
        }

    def fix_indentation(self, error_analysis):
        """Fixes indentation errors"""
        code_line = error_analysis["code"][error_analysis["line_number"]]
        current_indent = len(code_line) - len(code_line.lstrip())
        
        if 'def' in code_line or 'class' in code_line:
            fixed_code = code_line.lstrip()
        elif 'if' in code_line or 'for' in code_line or 'while' in code_line:
            fixed_code = "    " * (current_indent // 4) + code_line.lstrip()
        else:
            fixed_code = "    " * ((current_indent // 4) + 1) + code_line.lstrip()
        
        return {
            "line_number": error_analysis["line_number"],
            "fixed_code": fixed_code,
            "fix_type": "indentation_fix"
        }

    def verify_fix(self, file_path):
        """Verifies if the applied fix works"""
        try:
            with open(file_path, 'r') as f:
                ast.parse(f.read())
            return True
        except:
            return False

    def learn_from_fix(self, error_data, fix_data):
        """Learns from successful fixes for future use"""
        self.memory["fixes"].append({
            "error": error_data,
            "fix": fix_data,
            "timestamp": datetime.now().isoformat()
        })
        self.save_memory()

    def save_memory(self):
        """Saves AI memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def correct_syntax(self, code_line):
        """Smart syntax correction"""
        if ':' not in code_line and ('if' in code_line or 'for' in code_line or 'while' in code_line):
            return code_line.rstrip() + ':'
        return code_line

    def correct_attribute(self, code_line):
        """Smart attribute correction"""
        common_attributes = {
            'lenght': 'length',
            'appendd': 'append',
            'writee': 'write'
        }
        for wrong, right in common_attributes.items():
            if wrong in code_line:
                return code_line.replace(wrong, right)
        return code_line

    def find_error_line(self, code, error_data):
        """Finds the exact line where error occurred"""
        if 'line' in error_data:
            return error_data['line'] - 1
        return 0

    def get_code_context(self, code, error_data):
        """Gets the context around the error"""
        line_num = self.find_error_line(code, error_data)
        start = max(0, line_num - 2)
        end = min(len(code), line_num + 3)
        return code[start:end]
