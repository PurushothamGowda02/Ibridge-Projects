"""Task Executor - Executes system-level tasks like time retrieval, calculations, and app launching"""

import subprocess
import platform
from datetime import datetime
from typing import Dict, Any


class TaskExecutor:
    """Executes various system-level tasks for the Virtual Brain Assistant"""
    
    def get_current_time(self) -> str:
        """
        Get the current system time in HH:MM format.
        
        Returns:
            str: Current time formatted as HH:MM (24-hour format)
        """
        try:
            now = datetime.now()
            return now.strftime("%H:%M")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve current time: {str(e)}")
    
    def get_current_date(self) -> str:
        """
        Get the current system date in a readable format.
        
        Returns:
            str: Current date formatted as YYYY-MM-DD
        """
        try:
            now = datetime.now()
            return now.strftime("%Y-%m-%d")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve current date: {str(e)}")
    
    def calculate(self, expression: str) -> float:  
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression string (e.g., "2 + 2", "10 * 5")
        
        Returns:
            float: Result of the calculation
        
        Raises:
            ValueError: If the expression is invalid or contains unsafe operations
        """
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string")
        
        # Remove whitespace
        expression = expression.strip()
        
        if not expression:
            raise ValueError("Expression cannot be empty")
        
        # Define allowed characters for safety (including 'e' and 'E' for scientific notation)
        allowed_chars = set("0123456789+-*/().%**eE ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Additional safety checks
        dangerous_patterns = ["__", "import", "exec", "eval", "open", "file"]
        expression_lower = expression.lower()
        if any(pattern in expression_lower for pattern in dangerous_patterns):
            raise ValueError("Expression contains forbidden operations")
        
        try:
            # Use eval with restricted namespace for safety
            result = eval(expression, {"__builtins__": {}}, {})
            
            # Ensure result is numeric
            if not isinstance(result, (int, float)):
                raise ValueError("Expression did not evaluate to a number")
            
            return float(result)
        except SyntaxError:
            raise ValueError(f"Invalid mathematical expression: {expression}")
        except ZeroDivisionError:
            raise ValueError("Division by zero")
        except Exception as e:
            raise ValueError(f"Failed to evaluate expression: {str(e)}")
    
    def open_application(self, app_name: str) -> Dict[str, Any]:
        """
        Open an application on the system.
        
        Args:
            app_name: Name of the application to open
        
        Returns:
            dict: Result dictionary with 'success' (bool) and 'message' (str)
        """
        if not app_name or not isinstance(app_name, str):
            return {
                "success": False,
                "message": "Application name must be a non-empty string"
            }
        
        app_name = app_name.strip()
        
        if not app_name:
            return {
                "success": False,
                "message": "Application name cannot be empty"
            }
        
        try:
            system = platform.system()
            
            # Map common app names to Windows executables
            windows_app_map = {
                # System Apps
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "calc": "calc.exe",
                "explorer": "explorer.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "command prompt": "cmd.exe",
                "powershell": "powershell.exe",
                "task manager": "taskmgr.exe",
                "taskmgr": "taskmgr.exe",
                "control panel": "control.exe",
                "control": "control.exe",
                "settings": "ms-settings:",
                "snipping tool": "SnippingTool.exe",
                "screenshot": "SnippingTool.exe",
                "wordpad": "wordpad.exe",
                "character map": "charmap.exe",
                "registry editor": "regedit.exe",
                "regedit": "regedit.exe",
                
                # Browsers
                "chrome": "chrome.exe",
                "google chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
                "microsoft edge": "msedge.exe",
                "brave": "brave.exe",
                "opera": "opera.exe",
                "opera gx": "opera.exe",
                
                # Microsoft Office
                "word": "winword.exe",
                "microsoft word": "winword.exe",
                "excel": "excel.exe",
                "microsoft excel": "excel.exe",
                "powerpoint": "powerpnt.exe",
                "microsoft powerpoint": "powerpnt.exe",
                "outlook": "outlook.exe",
                "microsoft outlook": "outlook.exe",
                "onenote": "onenote.exe",
                "microsoft onenote": "onenote.exe",
                "access": "msaccess.exe",
                "microsoft access": "msaccess.exe",
                "publisher": "mspub.exe",
                "microsoft publisher": "mspub.exe",
                
                # Development Tools
                "code": "code.cmd",
                "vscode": "code.cmd",
                "visual studio code": "code.cmd",
                "visual studio": "devenv.exe",
                "pycharm": "pycharm64.exe",
                "intellij": "idea64.exe",
                "android studio": "studio64.exe",
                "sublime": "sublime_text.exe",
                "sublime text": "sublime_text.exe",
                "atom": "atom.exe",
                "notepad++": "notepad++.exe",
                "git bash": "git-bash.exe",
                "github desktop": "GitHubDesktop.exe",
                "postman": "Postman.exe",
                
                # Communication Apps
                "whatsapp": "WhatsApp.exe",
                "telegram": "Telegram.exe",
                "discord": "Discord.exe",
                "slack": "slack.exe",
                "teams": "Teams.exe",
                "microsoft teams": "Teams.exe",
                "zoom": "Zoom.exe",
                "skype": "Skype.exe",
                "messenger": "Messenger.exe",
                "signal": "Signal.exe",
                
                # Media & Entertainment
                "spotify": "Spotify.exe",
                "vlc": "vlc.exe",
                "vlc media player": "vlc.exe",
                "windows media player": "wmplayer.exe",
                "media player": "wmplayer.exe",
                "itunes": "iTunes.exe",
                "netflix": "Netflix.exe",
                "youtube music": "YouTube Music.exe",
                "audacity": "audacity.exe",
                "obs": "obs64.exe",
                "obs studio": "obs64.exe",
                
                # Graphics & Design
                "photoshop": "Photoshop.exe",
                "adobe photoshop": "Photoshop.exe",
                "illustrator": "Illustrator.exe",
                "adobe illustrator": "Illustrator.exe",
                "premiere": "Adobe Premiere Pro.exe",
                "premiere pro": "Adobe Premiere Pro.exe",
                "after effects": "AfterFX.exe",
                "gimp": "gimp-2.10.exe",
                "inkscape": "inkscape.exe",
                "blender": "blender.exe",
                "figma": "Figma.exe",
                "canva": "Canva.exe",
                
                # Productivity
                "notion": "Notion.exe",
                "evernote": "Evernote.exe",
                "trello": "Trello.exe",
                "todoist": "Todoist.exe",
                "obsidian": "Obsidian.exe",
                "anki": "anki.exe",
                
                # File Management
                "7zip": "7zFM.exe",
                "7-zip": "7zFM.exe",
                "winrar": "WinRAR.exe",
                "total commander": "TOTALCMD64.EXE",
                "filezilla": "filezilla.exe",
                
                # Gaming
                "steam": "steam.exe",
                "epic games": "EpicGamesLauncher.exe",
                "epic": "EpicGamesLauncher.exe",
                "origin": "Origin.exe",
                "uplay": "upc.exe",
                "battle.net": "Battle.net.exe",
                "battlenet": "Battle.net.exe",
                "xbox": "XboxApp.exe",
                "minecraft": "Minecraft.exe",
                
                # Utilities
                "ccleaner": "CCleaner64.exe",
                "malwarebytes": "mbam.exe",
                "teamviewer": "TeamViewer.exe",
                "anydesk": "AnyDesk.exe",
                "virtualbox": "VirtualBox.exe",
                "vmware": "vmware.exe",
                "docker": "Docker Desktop.exe",
                "putty": "putty.exe",
                "winscp": "WinSCP.exe",
                
                # Browsers (Additional)
                "tor": "firefox.exe",
                "tor browser": "firefox.exe",
                "vivaldi": "vivaldi.exe",
                
                # Social Media
                "twitter": "Twitter.exe",
                "instagram": "Instagram.exe",
                "facebook": "Facebook.exe",
                "tiktok": "TikTok.exe",
                
                # Reading & Documents
                "adobe reader": "AcroRd32.exe",
                "acrobat": "Acrobat.exe",
                "kindle": "Kindle.exe",
                "calibre": "calibre.exe",
                
                # Database
                "mysql workbench": "MySQLWorkbench.exe",
                "mongodb compass": "MongoDBCompass.exe",
                "pgadmin": "pgAdmin4.exe",
            }
            
            if system == "Windows":
                # Map app name to executable if available
                app_to_launch = windows_app_map.get(app_name.lower(), app_name)
                
                # Try to start the application on Windows
                # Use shell=True and proper command format
                subprocess.Popen(f'start "" "{app_to_launch}"', shell=True)
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            elif system == "Linux":
                subprocess.Popen([app_name])
            else:
                return {
                    "success": False,
                    "message": f"Unsupported operating system: {system}"
                }
            
            return {
                "success": True,
                "message": f"Successfully launched {app_name}"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "message": f"Application '{app_name}' not found on the system"
            }
        except PermissionError:
            return {
                "success": False,
                "message": f"Permission denied to launch '{app_name}'"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to launch application: {str(e)}"
            }
    
    def execute_task(self, task_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task based on type and parameters.
        
        Args:
            task_type: Type of task to execute (time, date, calculate, open_app)
            parameters: Dictionary of parameters for the task
        
        Returns:
            dict: Result dictionary with 'success' (bool), 'result' (Any), and optional 'error' (str)
        """
        try:
            if task_type == "time":
                result = self.get_current_time()
                return {"success": True, "result": result}
            
            elif task_type == "date":
                result = self.get_current_date()
                return {"success": True, "result": result}
            
            elif task_type == "calculate":
                expression = parameters.get("expression")
                if not expression:
                    return {"success": False, "error": "Missing expression parameter"}
                result = self.calculate(expression)
                return {"success": True, "result": result}
            
            elif task_type == "open_app":
                app_name = parameters.get("app_name")
                if not app_name:
                    return {"success": False, "error": "Missing app_name parameter"}
                result = self.open_application(app_name)
                return result
            
            else:
                return {"success": False, "error": f"Unknown task type: {task_type}"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
