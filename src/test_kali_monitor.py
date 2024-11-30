from monitor import SystemMonitor
from ai_brain import AIBrain
import os
import sys
import threading
import time

class KaliToolMonitor:
    def __init__(self):
        self.monitor = SystemMonitor()
        self.brain = AIBrain()
        self.tool_history = {}
        print("Kali Tool Monitor: Initializing...")

    def start_monitoring(self, tool_path):
        print(f"\n=== Kali Tool Monitor v2.0 ===")
        print(f"Starting advanced monitoring for: {tool_path}")
        
        # Initialize monitoring
        self.monitor.start_background_monitoring()
        self.brain.monitor_tool_execution(tool_path)
        
        # Track tool execution
        self.tool_history[tool_path] = {
            "start_time": time.time(),
            "errors_fixed": 0,
            "status": "active"
        }
        
        # Start real-time monitoring
        self.monitor_tool_execution(tool_path)

    def monitor_tool_execution(self, tool_path):
        try:
            # Monitor tool process
            while True:
                if os.path.exists(tool_path):
                    # Check for runtime errors
                    self.check_tool_errors(tool_path)
                    # Monitor tool output
                    self.monitor_tool_output(tool_path)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            self.cleanup()

    def check_tool_errors(self, tool_path):
        try:
            with open(tool_path, 'r') as f:
                content = f.read()
                # Analyze tool code for errors
                if error := self.brain.analyze_code_error(tool_path, {"type": "CodeCheck", "message": "Routine check"}):
                    print(f"\nDetected potential issue in {tool_path}")
                    self.handle_tool_error(tool_path, error)
        except Exception as e:
            self.handle_tool_error(tool_path, {"type": str(type(e).__name__), "message": str(e)})

    def handle_tool_error(self, tool_path, error):
        print(f"Fixing error in {tool_path}")
        # Generate and apply fix
        if fix := self.brain.generate_code_fix({"file": tool_path, "error": error}):
            self.brain.apply_code_fix(tool_path, fix)
            self.tool_history[tool_path]["errors_fixed"] += 1
            print("Fix applied successfully!")

    def monitor_tool_output(self, tool_path):
        # Monitor tool's output for runtime issues
        tool_dir = os.path.dirname(tool_path)
        if os.path.exists(os.path.join(tool_dir, 'output.log')):
            self.analyze_tool_output(tool_path)

    def analyze_tool_output(self, tool_path):
        # Analyze tool output for potential issues
        pass

    def cleanup(self):
        print("\nSaving monitoring data...")
        self.brain.save_memory()
        print("Monitoring system shutdown complete")

def main():
    monitor = KaliToolMonitor()
    
    if len(sys.argv) < 2:
        print("Usage: python test_kali_monitor.py <path_to_your_tool>")
        sys.exit(1)
    
    tool_path = sys.argv[1]
    if not os.path.exists(tool_path):
        print(f"Error: Tool not found at {tool_path}")
        sys.exit(1)
    
    monitor.start_monitoring(tool_path)

if __name__ == "__main__":
    main()
