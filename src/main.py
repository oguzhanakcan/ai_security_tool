from monitor import SystemMonitor
from ai_brain import AIBrain
import threading
import time
import os

class AutoSecurityTool:
    def __init__(self):
        self.monitor = SystemMonitor()
        self.brain = AIBrain()
        self.running = False
        self.brain_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'brain')
        print("AI Security Tool: Initializing advanced error detection and fixing system...")
    
    def start(self):
        print("\n=== AI Auto-Fix System v2.0 ===")
        print("Starting comprehensive monitoring system...")
        
        self.running = True
        self.monitor.start_background_monitoring()
        
        # Monitor all tools and systems
        self.start_complete_monitoring()
    
    def start_complete_monitoring(self):
        print("\nInitiating Complete Monitoring System:")
        
        # 1. Standard Python monitoring
        print("1. Starting Python error detection...")
        self.monitor_python_errors()
        
        # 2. Kali tools monitoring
        print("2. Starting Kali tools monitoring...")
        self.monitor_kali_tools()
        
        # 3. Custom tools monitoring
        print("3. Starting custom tools monitoring...")
        self.monitor_custom_tools()
        
        print("\nComplete monitoring system active!")
    
    def monitor_python_errors(self):
        test_file = self.create_test_file()
        self.brain.monitor_tool_execution(test_file)
    
    def monitor_kali_tools(self):
        kali_paths = [
            "/usr/share/",
            "/opt/",
            "/home/kali/custom_tools/"
        ]
        for path in kali_paths:
            self.brain.monitor_tool_execution(path)
    
    def monitor_custom_tools(self):
        custom_paths = [
            os.path.join(os.path.dirname(__file__), 'custom_tools'),
            os.path.join(self.brain_dir, 'tools')
        ]
        for path in custom_paths:
            os.makedirs(path, exist_ok=True)
            self.brain.monitor_tool_execution(path)
    
    def create_test_file(self):
        test_file = os.path.join(self.brain_dir, "test_tool.py")
        with open(test_file, 'w') as f:
            f.write("def test_function():\n")
            f.write("    x = 10\n")
            f.write("    if x > 5\n")  # Intentional syntax error
            f.write("        print('x is greater than 5')\n")
        return test_file

if __name__ == "__main__":
    tool = AutoSecurityTool()
    tool.start()
