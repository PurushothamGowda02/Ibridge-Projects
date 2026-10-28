"""RAJIV Core - Complete System Administrator AI"""

import re
import os
import subprocess
import shutil
import winreg
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import socket
import platform

from .system_control import SystemController
from .file_manager import FileManager


class JARVISCore:
    """Complete RAJIV AI System - Every System Task Possible"""
    
    def __init__(self):
        self.system_controller = SystemController()
        self.file_manager = FileManager()
        self.personality = "professional"
        self.wake_words = ["rajiv", "computer", "hey rajiv"]
        
    def process_jarvis_command(self, command: str) -> Dict[str, Any]:
        """Process ANY system command - Complete System Control"""
        command_lower = command.lower().strip()
        
        # Remove wake words
        for wake_word in self.wake_words:
            if command_lower.startswith(wake_word):
                command_lower = command_lower[len(wake_word):].strip()
                if command_lower.startswith(','):
                    command_lower = command_lower[1:].strip()
                break
        
        # === SYSTEM CONTROL COMMANDS ===
        if any(phrase in command_lower for phrase in ['system status', 'system report', 'status report']):
            return self._handle_system_status()
        elif any(phrase in command_lower for phrase in ['show processes', 'running processes', 'task manager']):
            return self._handle_process_list()
        elif command_lower.startswith('kill process'):
            process_name = self._extract_process_name(command_lower)
            return self._handle_kill_process(process_name)
        elif any(phrase in command_lower for phrase in ['restart computer', 'reboot system', 'restart system']):
            return self._handle_restart_system()
        elif any(phrase in command_lower for phrase in ['shutdown computer', 'shutdown system']):
            minutes = self._extract_minutes(command_lower)
            return self._handle_shutdown(minutes)
        elif any(phrase in command_lower for phrase in ['cancel shutdown', 'abort shutdown']):
            return self._handle_cancel_shutdown()
        elif any(phrase in command_lower for phrase in ['lock computer', 'lock screen', 'lock system']):
            return self._handle_lock_screen()
        elif any(phrase in command_lower for phrase in ['sleep mode', 'hibernate', 'suspend']):
            return self._handle_sleep_mode()
        
        # === FILE & FOLDER OPERATIONS ===
        elif any(phrase in command_lower for phrase in ['organize desktop', 'clean desktop']):
            return self._handle_organize_desktop()
        elif command_lower.startswith('create folder'):
            folder_path = self._extract_path(command_lower, 'create folder')
            return self._handle_create_folder(folder_path)
        elif command_lower.startswith('delete folder'):
            folder_path = self._extract_path(command_lower, 'delete folder')
            return self._handle_delete_folder(folder_path)
        elif command_lower.startswith('copy file'):
            paths = self._extract_copy_paths(command_lower)
            return self._handle_copy_file(paths['source'], paths['destination'])
        elif command_lower.startswith('move file'):
            paths = self._extract_copy_paths(command_lower)
            return self._handle_move_file(paths['source'], paths['destination'])
        elif command_lower.startswith('delete file'):
            file_path = self._extract_path(command_lower, 'delete file')
            return self._handle_delete_file(file_path)
        elif command_lower.startswith('rename file'):
            paths = self._extract_rename_paths(command_lower)
            return self._handle_rename_file(paths['old'], paths['new'])
        elif command_lower.startswith('find files'):
            pattern = self._extract_file_pattern(command_lower)
            return self._handle_find_files(pattern)
        elif any(phrase in command_lower for phrase in ['find large files', 'large files']):
            size_mb = self._extract_file_size(command_lower)
            return self._handle_find_large_files(size_mb)
        elif any(phrase in command_lower for phrase in ['find duplicates', 'duplicate files']):
            return self._handle_find_duplicates()
        elif any(phrase in command_lower for phrase in ['clean downloads', 'clean download folder']):
            days = self._extract_days(command_lower)
            return self._handle_clean_downloads(days)
        elif any(phrase in command_lower for phrase in ['empty recycle bin', 'empty trash']):
            return self._handle_empty_recycle_bin()
        
        # === APPLICATION MANAGEMENT ===
        elif command_lower.startswith('open'):
            app_name = self._extract_app_name(command_lower)
            return self._handle_open_application(app_name)
        elif command_lower.startswith('close'):
            app_name = self._extract_app_name(command_lower)
            return self._handle_close_application(app_name)
        elif any(phrase in command_lower for phrase in ['install program', 'install software']):
            program = self._extract_program_name(command_lower)
            return self._handle_install_program(program)
        elif any(phrase in command_lower for phrase in ['uninstall program', 'remove program']):
            program = self._extract_program_name(command_lower)
            return self._handle_uninstall_program(program)
        elif any(phrase in command_lower for phrase in ['list programs', 'installed programs']):
            return self._handle_list_programs()
        
        # === NETWORK OPERATIONS ===
        elif any(phrase in command_lower for phrase in ['network status', 'network info']):
            return self._handle_network_info()
        elif any(phrase in command_lower for phrase in ['wifi status', 'wireless status']):
            return self._handle_wifi_status()
        elif any(phrase in command_lower for phrase in ['ping', 'test connection']):
            host = self._extract_host(command_lower)
            return self._handle_ping(host)
        elif any(phrase in command_lower for phrase in ['download file', 'download from']):
            url = self._extract_url(command_lower)
            return self._handle_download_file(url)
        elif any(phrase in command_lower for phrase in ['check internet', 'internet connection']):
            return self._handle_check_internet()
        
        # === SYSTEM MAINTENANCE ===
        elif any(phrase in command_lower for phrase in ['clean temp files', 'clean temporary files', 'system cleanup']):
            return self._handle_clean_temp()
        elif any(phrase in command_lower for phrase in ['disk cleanup', 'clean disk']):
            return self._handle_disk_cleanup()
        elif any(phrase in command_lower for phrase in ['defrag disk', 'defragment']):
            drive = self._extract_drive(command_lower)
            return self._handle_defrag_disk(drive)
        elif any(phrase in command_lower for phrase in ['check disk', 'scan disk']):
            drive = self._extract_drive(command_lower)
            return self._handle_check_disk(drive)
        elif any(phrase in command_lower for phrase in ['system scan', 'virus scan']):
            return self._handle_system_scan()
        elif any(phrase in command_lower for phrase in ['update system', 'windows update']):
            return self._handle_system_update()
        
        # === REGISTRY OPERATIONS ===
        elif any(phrase in command_lower for phrase in ['registry backup', 'backup registry']):
            return self._handle_registry_backup()
        elif any(phrase in command_lower for phrase in ['registry clean', 'clean registry']):
            return self._handle_registry_clean()
        
        # === SERVICES MANAGEMENT ===
        elif command_lower.startswith('start service'):
            service = self._extract_service_name(command_lower)
            return self._handle_start_service(service)
        elif command_lower.startswith('stop service'):
            service = self._extract_service_name(command_lower)
            return self._handle_stop_service(service)
        elif any(phrase in command_lower for phrase in ['list services', 'show services']):
            return self._handle_list_services()
        
        # === USER ACCOUNT MANAGEMENT ===
        elif command_lower.startswith('create user'):
            username = self._extract_username(command_lower)
            return self._handle_create_user(username)
        elif command_lower.startswith('delete user'):
            username = self._extract_username(command_lower)
            return self._handle_delete_user(username)
        elif any(phrase in command_lower for phrase in ['list users', 'show users']):
            return self._handle_list_users()
        elif any(phrase in command_lower for phrase in ['change password', 'reset password']):
            username = self._extract_username(command_lower)
            return self._handle_change_password(username)
        
        # === SCHEDULED TASKS ===
        elif command_lower.startswith('create task'):
            task_info = self._extract_task_info(command_lower)
            return self._handle_create_scheduled_task(task_info)
        elif command_lower.startswith('delete task'):
            task_name = self._extract_task_name(command_lower)
            return self._handle_delete_scheduled_task(task_name)
        elif any(phrase in command_lower for phrase in ['list tasks', 'scheduled tasks']):
            return self._handle_list_scheduled_tasks()
        
        # === ENVIRONMENT VARIABLES ===
        elif command_lower.startswith('set environment'):
            var_info = self._extract_env_var(command_lower)
            return self._handle_set_environment_variable(var_info)
        elif command_lower.startswith('get environment'):
            var_name = self._extract_env_var_name(command_lower)
            return self._handle_get_environment_variable(var_name)
        elif any(phrase in command_lower for phrase in ['list environment', 'environment variables']):
            return self._handle_list_environment_variables()
        
        # === SYSTEM INFORMATION ===
        elif any(phrase in command_lower for phrase in ['disk usage', 'disk space', 'storage info']):
            return self._handle_disk_info()
        elif any(phrase in command_lower for phrase in ['memory usage', 'ram usage']):
            return self._handle_memory_info()
        elif any(phrase in command_lower for phrase in ['cpu info', 'processor info']):
            return self._handle_cpu_info()
        elif any(phrase in command_lower for phrase in ['system info', 'computer info']):
            return self._handle_system_info()
        elif any(phrase in command_lower for phrase in ['hardware info', 'device info']):
            return self._handle_hardware_info()
        
        # === POWER MANAGEMENT ===
        elif any(phrase in command_lower for phrase in ['power plan', 'power scheme']):
            return self._handle_power_plan()
        elif any(phrase in command_lower for phrase in ['battery status', 'battery info']):
            return self._handle_battery_status()
        
        # === DISPLAY & AUDIO ===
        elif any(phrase in command_lower for phrase in ['screen resolution', 'display settings']):
            return self._handle_screen_resolution()
        elif any(phrase in command_lower for phrase in ['volume up', 'increase volume']):
            return self._handle_volume_up()
        elif any(phrase in command_lower for phrase in ['volume down', 'decrease volume']):
            return self._handle_volume_down()
        elif any(phrase in command_lower for phrase in ['mute', 'unmute']):
            return self._handle_mute_toggle()
        
        # === SECURITY OPERATIONS ===
        elif any(phrase in command_lower for phrase in ['firewall status', 'windows firewall']):
            return self._handle_firewall_status()
        elif any(phrase in command_lower for phrase in ['enable firewall', 'turn on firewall']):
            return self._handle_enable_firewall()
        elif any(phrase in command_lower for phrase in ['disable firewall', 'turn off firewall']):
            return self._handle_disable_firewall()
        elif any(phrase in command_lower for phrase in ['security scan', 'malware scan']):
            return self._handle_security_scan()
        
        # === TIME & DATE ===
        elif any(phrase in command_lower for phrase in ['set time', 'change time']):
            time_str = self._extract_time(command_lower)
            return self._handle_set_time(time_str)
        elif any(phrase in command_lower for phrase in ['set date', 'change date']):
            date_str = self._extract_date(command_lower)
            return self._handle_set_date(date_str)
        elif any(phrase in command_lower for phrase in ['time zone', 'timezone']):
            return self._handle_timezone_info()
        
        # === BACKUP & RESTORE ===
        elif any(phrase in command_lower for phrase in ['backup files', 'create backup']):
            backup_info = self._extract_backup_info(command_lower)
            return self._handle_backup_files(backup_info)
        elif any(phrase in command_lower for phrase in ['restore files', 'restore backup']):
            restore_info = self._extract_restore_info(command_lower)
            return self._handle_restore_files(restore_info)
        
        # === WEATHER & EXTERNAL INFO ===
        elif any(phrase in command_lower for phrase in ['weather', 'forecast']):
            location = self._extract_location(command_lower)
            return self._handle_weather(location)
        
        # === JARVIS PERSONALITY & GENERAL QUESTIONS ===
        elif any(phrase in command_lower for phrase in ['hello', 'hi', 'good morning', 'good evening']):
            return self._handle_greeting()
        elif any(phrase in command_lower for phrase in ['how are you', 'status']):
            return self._handle_status_inquiry()
        elif any(phrase in command_lower for phrase in ['thank you', 'thanks']):
            return self._handle_thanks()
        elif any(phrase in command_lower for phrase in ['help', 'what can you do', 'commands']):
            return self._handle_help()
        elif any(phrase in command_lower for phrase in ['who are you', 'what are you']):
            return self._handle_identity()
        elif any(phrase in command_lower for phrase in ['tell me about', 'what is', 'explain', 'define']):
            # For general knowledge questions, let AI core handle it
            return {
                'success': False,
                'message': "Let me search my knowledge base for that information...",
                'type': 'general_question'
            }
        elif any(phrase in command_lower for phrase in ['how to', 'how do i', 'tutorial']):
            # For how-to questions, let AI core handle it
            return {
                'success': False,
                'message': "Let me provide you with detailed instructions...",
                'type': 'general_question'
            }
        
        else:
            # For general questions, let the AI core handle it
            return {
                'success': False,
                'message': "Let me think about that...",
                'type': 'general_question'
            }
    
    def _handle_system_status(self) -> Dict[str, Any]:
        """Handle system status request"""
        status = self.system_controller.get_system_status()
        if 'error' in status:
            return {
                'success': False,
                'message': f"I encountered an issue retrieving system status: {status['error']}",
                'type': 'system_status'
            }
        
        # Format JARVIS-style response
        cpu_usage = status['cpu']['usage_percent']
        memory_usage = status['memory']['usage_percent']
        disk_usage = status['disk']['usage_percent']
        uptime_hours = status['uptime']['uptime_hours']
        
        response = f"System status report, sir:\\n\\n"
        response += f"• CPU Usage: {cpu_usage}%\\n"
        response += f"• Memory Usage: {memory_usage}% ({status['memory']['used_gb']}GB of {status['memory']['total_gb']}GB)\\n"
        response += f"• Disk Usage: {disk_usage}% ({status['disk']['used_gb']}GB of {status['disk']['total_gb']}GB)\\n"
        response += f"• System Uptime: {uptime_hours} hours\\n"
        
        if cpu_usage > 80:
            response += "\\n⚠️ CPU usage is high. Consider closing unnecessary applications."
        if memory_usage > 80:
            response += "\\n⚠️ Memory usage is high. System may benefit from a restart."
        if disk_usage > 90:
            response += "\\n⚠️ Disk space is critically low. Recommend cleanup operations."
        
        return {
            'success': True,
            'message': response,
            'type': 'system_status',
            'data': status
        }
    
    def _handle_process_list(self) -> Dict[str, Any]:
        """Handle process list request"""
        processes = self.system_controller.get_running_processes(10)
        
        response = "Top running processes by CPU usage:\\n\\n"
        for i, proc in enumerate(processes[:5], 1):
            if 'error' not in proc:
                response += f"{i}. {proc['name']} - CPU: {proc['cpu_percent']:.1f}%, Memory: {proc['memory_percent']:.1f}%\\n"
        
        return {
            'success': True,
            'message': response,
            'type': 'process_list',
            'data': processes
        }
    
    def _handle_kill_process(self, process_name: str) -> Dict[str, Any]:
        """Handle kill process request"""
        if not process_name:
            return {
                'success': False,
                'message': "Please specify which process to terminate.",
                'type': 'kill_process'
            }
        
        result = self.system_controller.kill_process(process_name)
        return {
            'success': result['success'],
            'message': result['message'],
            'type': 'kill_process',
            'data': result
        }
    
    def _handle_organize_desktop(self) -> Dict[str, Any]:
        """Handle desktop organization request"""
        result = self.file_manager.organize_desktop()
        
        if result['success']:
            message = f"Desktop organization complete. {result['message']}"
            if result['created_folders']:
                message += f"\\nCreated folders: {', '.join(result['created_folders'])}"
        else:
            message = f"Desktop organization failed: {result['message']}"
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'organize_desktop',
            'data': result
        }
    
    def _handle_find_files(self, pattern: str) -> Dict[str, Any]:
        """Handle find files request"""
        if not pattern:
            pattern = "*.*"
        
        result = self.file_manager.find_files(pattern)
        
        if result['success'] and result['files']:
            message = f"Found {len(result['files'])} files matching '{pattern}':\\n\\n"
            for file_info in result['files'][:5]:  # Show first 5
                message += f"• {file_info['name']} ({file_info['size_mb']} MB)\\n"
            
            if len(result['files']) > 5:
                message += f"\\n... and {len(result['files']) - 5} more files."
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'find_files',
            'data': result
        }
    
    def _handle_find_large_files(self, size_mb: int) -> Dict[str, Any]:
        """Handle find large files request"""
        result = self.file_manager.find_large_files(size_mb)
        
        if result['success'] and result['files']:
            message = f"Found {result['total_files']} files larger than {size_mb}MB:\\n\\n"
            for file_info in result['files'][:5]:  # Show first 5
                message += f"• {file_info['name']} ({file_info['size_gb']} GB)\\n"
            
            message += f"\\nTotal space used: {result['total_size_gb']} GB"
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'find_large_files',
            'data': result
        }
    
    def _handle_find_duplicates(self) -> Dict[str, Any]:
        """Handle find duplicates request"""
        result = self.file_manager.find_duplicates()
        
        if result['success'] and result['duplicates']:
            message = f"Found {len(result['duplicates'])} duplicate files wasting {result['total_wasted_gb']} GB of space.\\n\\n"
            for dup in result['duplicates'][:3]:  # Show first 3
                message += f"• Duplicate: {dup['duplicate']} ({dup['size_mb']} MB)\\n"
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'find_duplicates',
            'data': result
        }
    
    def _handle_clean_downloads(self, days: int) -> Dict[str, Any]:
        """Handle clean downloads request"""
        result = self.file_manager.clean_downloads(days)
        
        if result['success']:
            message = f"Downloads cleanup complete. {result['message']}\\n"
            message += f"Freed {result['size_freed_gb']} GB of space."
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'clean_downloads',
            'data': result
        }
    
    def _handle_clean_temp(self) -> Dict[str, Any]:
        """Handle clean temporary files request"""
        result = self.system_controller.clean_temp_files()
        
        if result['success']:
            message = f"Temporary files cleanup complete. {result['message']}\\n"
            message += f"Freed {result['cleaned_size_mb']} MB of space."
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'clean_temp',
            'data': result
        }
    
    def _handle_shutdown(self, minutes: int) -> Dict[str, Any]:
        """Handle shutdown request"""
        result = self.system_controller.schedule_shutdown(minutes)
        return {
            'success': result['success'],
            'message': result['message'],
            'type': 'shutdown',
            'data': result
        }
    
    def _handle_cancel_shutdown(self) -> Dict[str, Any]:
        """Handle cancel shutdown request"""
        result = self.system_controller.cancel_shutdown()
        return {
            'success': result['success'],
            'message': result['message'],
            'type': 'cancel_shutdown',
            'data': result
        }
    
    def _handle_network_info(self) -> Dict[str, Any]:
        """Handle network information request"""
        result = self.system_controller.get_network_info()
        
        if result['success']:
            message = "Network status report:\\n\\n"
            active_interfaces = [name for name, info in result['interfaces'].items() 
                               if info['stats'] and info['stats']['is_up']]
            message += f"Active interfaces: {', '.join(active_interfaces)}\\n"
            
            io = result['io_counters']
            message += f"Data sent: {round(io['bytes_sent'] / (1024*1024*1024), 2)} GB\\n"
            message += f"Data received: {round(io['bytes_recv'] / (1024*1024*1024), 2)} GB"
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'network_info',
            'data': result
        }
    
    def _handle_disk_info(self) -> Dict[str, Any]:
        """Handle disk information request"""
        result = self.system_controller.get_disk_info()
        
        if result['success']:
            message = "Storage status report:\\n\\n"
            for device, info in result['disks'].items():
                message += f"{device}: {info['used_gb']}GB / {info['total_gb']}GB ({info['usage_percent']}% used)\\n"
        else:
            message = result['message']
        
        return {
            'success': result['success'],
            'message': message,
            'type': 'disk_info',
            'data': result
        }
    
    def _handle_weather(self, location: str = "") -> Dict[str, Any]:
        """Handle weather request using wttr.in (no API key needed)"""
        if not location:
            location = "auto"

        try:
            # Use wttr.in free weather API - no key required
            url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
            req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

            current = data["current_condition"][0]
            area = data["nearest_area"][0]
            area_name = area["areaName"][0]["value"]
            country = area["country"][0]["value"]

            temp_c = current["temp_C"]
            feels_like = current["FeelsLikeC"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind_kmph = current["windspeedKmph"]

            message = (
                f"🌤 Weather in {area_name}, {country}:\n\n"
                f"• Condition: {desc}\n"
                f"• Temperature: {temp_c}°C (feels like {feels_like}°C)\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind Speed: {wind_kmph} km/h"
            )

            return {"success": True, "message": message, "type": "weather"}

        except Exception as e:
            return {
                "success": False,
                "message": f"Could not fetch weather for '{location}': {str(e)}",
                "type": "weather"
            }

    def _extract_location(self, command: str) -> str:
        """Extract location from weather command"""
        for phrase in ["weather in", "weather for", "forecast for", "forecast in", "weather"]:
            if phrase in command:
                location = command.split(phrase, 1)[-1].strip()
                if location:
                    return location
        return ""
    
    def _handle_greeting(self) -> Dict[str, Any]:
        """Handle greeting"""
        greetings = [
            "Good day, sir. How may I assist you?",
            "Hello. RAJIV at your service.",
            "Good to see you again. What can I do for you today?",
            "Welcome back. All systems are operational."
        ]
        import random
        return {
            'success': True,
            'message': random.choice(greetings),
            'type': 'greeting'
        }
    
    def _handle_status_inquiry(self) -> Dict[str, Any]:
        """Handle status inquiry"""
        return {
            'success': True,
            'message': "All systems are functioning within normal parameters. I am ready to assist you with any task.",
            'type': 'status_inquiry'
        }
    
    def _handle_thanks(self) -> Dict[str, Any]:
        """Handle thanks"""
        responses = [
            "You're welcome, sir.",
            "My pleasure.",
            "Always happy to help.",
            "At your service."
        ]
        import random
        return {
            'success': True,
            'message': random.choice(responses),
            'type': 'thanks'
        }
    
    def _handle_identity(self) -> Dict[str, Any]:
        """Handle identity inquiry"""
        return {
            'success': True,
            'message': "I am RAJIV - your intelligent virtual assistant. I can help you with system administration, answer questions on any topic, and assist with various tasks. I have access to your computer's systems and can also provide information on science, technology, history, and much more. How may I assist you today?",
            'type': 'identity'
        }
    
    # Helper methods for extracting parameters from commands
    def _extract_process_name(self, command: str) -> str:
        """Extract process name from kill command"""
        match = re.search(r'kill process (.+)', command)
        return match.group(1).strip() if match else ""
    
    def _extract_file_pattern(self, command: str) -> str:
        """Extract file pattern from find command"""
        match = re.search(r'find files (.+)', command)
        return match.group(1).strip() if match else "*.*"
    
    def _extract_file_size(self, command: str) -> int:
        """Extract file size from large files command"""
        match = re.search(r'(\d+)\s*mb', command)
        return int(match.group(1)) if match else 100
    
    def _extract_days(self, command: str) -> int:
        """Extract days from clean command"""
        match = re.search(r'(\d+)\s*days?', command)
        return int(match.group(1)) if match else 30
    
    def _extract_minutes(self, command: str) -> int:
        """Extract minutes from shutdown command"""
        match = re.search(r'(\d+)\s*minutes?', command)
        return int(match.group(1)) if match else 5
    
    def get_available_commands(self) -> Dict[str, Any]:
        """Get list of available RAJIV commands"""
        commands = {
            'System Control': [
                'system status - Get comprehensive system report',
                'show processes - Display running processes',
                'kill process [name] - Terminate a specific process',
                'clean temp files - Clean temporary files',
                'shutdown in [X] minutes - Schedule system shutdown',
                'cancel shutdown - Cancel scheduled shutdown'
            ],
            'File Management': [
                'organize desktop - Organize desktop files by type',
                'find files [pattern] - Search for files matching pattern',
                'find large files [size]mb - Find files larger than specified size',
                'find duplicates - Find duplicate files',
                'clean downloads [X] days - Clean old files from Downloads'
            ],
            'Information': [
                'network status - Display network information',
                'disk usage - Show storage information',
                'weather - Get weather forecast (requires API key)'
            ],
            'General': [
                'hello/hi - Greeting',
                'how are you - Status inquiry',
                'thank you - Acknowledgment'
            ]
        }
        
        return {
            'success': True,
            'message': 'Available RAJIV commands:',
            'type': 'help',
            'data': commands
        }
    
    # === COMPREHENSIVE SYSTEM HANDLERS ===
    
    def _handle_restart_system(self) -> Dict[str, Any]:
        """Handle system restart"""
        try:
            subprocess.run(['shutdown', '/r', '/t', '60'], check=True)
            return {
                'success': True,
                'message': "System restart scheduled in 60 seconds. Use 'cancel shutdown' to abort.",
                'type': 'restart_system'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to schedule restart: {str(e)}",
                'type': 'restart_system'
            }
    
    def _handle_lock_screen(self) -> Dict[str, Any]:
        """Handle screen lock"""
        try:
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=True)
            return {
                'success': True,
                'message': "Screen locked successfully.",
                'type': 'lock_screen'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to lock screen: {str(e)}",
                'type': 'lock_screen'
            }
    
    def _handle_sleep_mode(self) -> Dict[str, Any]:
        """Handle sleep mode"""
        try:
            subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'], check=True)
            return {
                'success': True,
                'message': "System entering sleep mode.",
                'type': 'sleep_mode'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to enter sleep mode: {str(e)}",
                'type': 'sleep_mode'
            }
    
    def _handle_create_folder(self, folder_path: str) -> Dict[str, Any]:
        """Handle folder creation"""
        if not folder_path:
            return {
                'success': False,
                'message': "Please specify folder path to create.",
                'type': 'create_folder'
            }
        
        try:
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            return {
                'success': True,
                'message': f"Folder created successfully: {folder_path}",
                'type': 'create_folder'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to create folder: {str(e)}",
                'type': 'create_folder'
            }
    
    def _handle_delete_folder(self, folder_path: str) -> Dict[str, Any]:
        """Handle folder deletion"""
        if not folder_path:
            return {
                'success': False,
                'message': "Please specify folder path to delete.",
                'type': 'delete_folder'
            }
        
        try:
            shutil.rmtree(folder_path)
            return {
                'success': True,
                'message': f"Folder deleted successfully: {folder_path}",
                'type': 'delete_folder'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to delete folder: {str(e)}",
                'type': 'delete_folder'
            }
    
    def _handle_copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Handle file copying"""
        if not source or not destination:
            return {
                'success': False,
                'message': "Please specify both source and destination paths.",
                'type': 'copy_file'
            }
        
        try:
            shutil.copy2(source, destination)
            return {
                'success': True,
                'message': f"File copied from {source} to {destination}",
                'type': 'copy_file'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to copy file: {str(e)}",
                'type': 'copy_file'
            }
    
    def _handle_move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Handle file moving"""
        if not source or not destination:
            return {
                'success': False,
                'message': "Please specify both source and destination paths.",
                'type': 'move_file'
            }
        
        try:
            shutil.move(source, destination)
            return {
                'success': True,
                'message': f"File moved from {source} to {destination}",
                'type': 'move_file'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to move file: {str(e)}",
                'type': 'move_file'
            }
    
    def _handle_delete_file(self, file_path: str) -> Dict[str, Any]:
        """Handle file deletion"""
        if not file_path:
            return {
                'success': False,
                'message': "Please specify file path to delete.",
                'type': 'delete_file'
            }
        
        try:
            os.remove(file_path)
            return {
                'success': True,
                'message': f"File deleted successfully: {file_path}",
                'type': 'delete_file'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to delete file: {str(e)}",
                'type': 'delete_file'
            }
    
    def _handle_rename_file(self, old_path: str, new_path: str) -> Dict[str, Any]:
        """Handle file renaming"""
        if not old_path or not new_path:
            return {
                'success': False,
                'message': "Please specify both old and new file paths.",
                'type': 'rename_file'
            }
        
        try:
            os.rename(old_path, new_path)
            return {
                'success': True,
                'message': f"File renamed from {old_path} to {new_path}",
                'type': 'rename_file'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to rename file: {str(e)}",
                'type': 'rename_file'
            }
    
    def _handle_empty_recycle_bin(self) -> Dict[str, Any]:
        """Handle emptying recycle bin"""
        try:
            subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], check=True)
            return {
                'success': True,
                'message': "Recycle bin emptied successfully.",
                'type': 'empty_recycle_bin'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to empty recycle bin: {str(e)}",
                'type': 'empty_recycle_bin'
            }
    
    def _handle_open_application(self, app_name: str) -> Dict[str, Any]:
        """Handle application opening"""
        if not app_name:
            return {
                'success': False,
                'message': "Please specify application name.",
                'type': 'open_application'
            }
        
        # Use the existing task executor
        from ..tasks.task_executor import TaskExecutor
        task_executor = TaskExecutor()
        result = task_executor.open_application(app_name)
        
        return {
            'success': result['success'],
            'message': result['message'],
            'type': 'open_application'
        }
    
    def _handle_close_application(self, app_name: str) -> Dict[str, Any]:
        """Handle application closing"""
        if not app_name:
            return {
                'success': False,
                'message': "Please specify application name to close.",
                'type': 'close_application'
            }
        
        return self._handle_kill_process(app_name)
    
    def _handle_install_program(self, program: str) -> Dict[str, Any]:
        """Handle program installation"""
        return {
            'success': True,
            'message': f"Program installation for '{program}' would require administrative privileges and package manager integration. This feature is planned for future updates.",
            'type': 'install_program'
        }
    
    def _handle_uninstall_program(self, program: str) -> Dict[str, Any]:
        """Handle program uninstallation"""
        try:
            # Open Programs and Features
            subprocess.run(['appwiz.cpl'], check=True)
            return {
                'success': True,
                'message': f"Programs and Features opened. Please manually uninstall '{program}' from the list.",
                'type': 'uninstall_program'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open Programs and Features: {str(e)}",
                'type': 'uninstall_program'
            }
    
    def _handle_list_programs(self) -> Dict[str, Any]:
        """Handle listing installed programs"""
        try:
            subprocess.run(['appwiz.cpl'], check=True)
            return {
                'success': True,
                'message': "Programs and Features opened showing all installed programs.",
                'type': 'list_programs'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open Programs and Features: {str(e)}",
                'type': 'list_programs'
            }
    
    def _handle_wifi_status(self) -> Dict[str, Any]:
        """Handle WiFi status check"""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, check=True)
            profiles = []
            for line in result.stdout.split('\n'):
                if 'All User Profile' in line:
                    profile = line.split(':')[1].strip()
                    profiles.append(profile)
            
            message = f"WiFi Status:\\n\\nAvailable profiles: {len(profiles)}\\n"
            for profile in profiles[:5]:  # Show first 5
                message += f"• {profile}\\n"
            
            return {
                'success': True,
                'message': message,
                'type': 'wifi_status',
                'data': {'profiles': profiles}
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to get WiFi status: {str(e)}",
                'type': 'wifi_status'
            }
    
    def _handle_ping(self, host: str) -> Dict[str, Any]:
        """Handle ping command"""
        if not host:
            host = "google.com"
        
        try:
            result = subprocess.run(['ping', '-n', '4', host], 
                                  capture_output=True, text=True, check=True)
            
            # Extract ping statistics
            lines = result.stdout.split('\n')
            stats_line = [line for line in lines if 'Average' in line]
            
            if stats_line:
                avg_time = stats_line[0].split('=')[-1].strip()
                message = f"Ping to {host} successful.\\nAverage response time: {avg_time}"
            else:
                message = f"Ping to {host} completed. Check detailed results."
            
            return {
                'success': True,
                'message': message,
                'type': 'ping',
                'data': {'output': result.stdout}
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Ping to {host} failed: {str(e)}",
                'type': 'ping'
            }
    
    def _handle_download_file(self, url: str) -> Dict[str, Any]:
        """Handle file download"""
        if not url:
            return {
                'success': False,
                'message': "Please specify URL to download.",
                'type': 'download_file'
            }
        
        try:
            # Extract filename from URL
            filename = url.split('/')[-1] or 'downloaded_file'
            download_path = Path.home() / 'Downloads' / filename
            
            urllib.request.urlretrieve(url, download_path)
            
            return {
                'success': True,
                'message': f"File downloaded successfully to {download_path}",
                'type': 'download_file',
                'data': {'path': str(download_path)}
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to download file: {str(e)}",
                'type': 'download_file'
            }
    
    def _handle_check_internet(self) -> Dict[str, Any]:
        """Handle internet connection check"""
        try:
            # Try to connect to Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return {
                'success': True,
                'message': "Internet connection is active and working properly.",
                'type': 'check_internet'
            }
        except OSError:
            return {
                'success': False,
                'message': "No internet connection detected.",
                'type': 'check_internet'
            }
    
    def _handle_disk_cleanup(self) -> Dict[str, Any]:
        """Handle disk cleanup"""
        try:
            subprocess.run(['cleanmgr'], check=True)
            return {
                'success': True,
                'message': "Disk Cleanup utility opened. Please select items to clean.",
                'type': 'disk_cleanup'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open Disk Cleanup: {str(e)}",
                'type': 'disk_cleanup'
            }
    
    def _handle_defrag_disk(self, drive: str) -> Dict[str, Any]:
        """Handle disk defragmentation"""
        if not drive:
            drive = "C:"
        
        try:
            subprocess.run(['defrag', drive, '/A'], check=True)
            return {
                'success': True,
                'message': f"Disk analysis started for drive {drive}. Full defragmentation requires administrative privileges.",
                'type': 'defrag_disk'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to analyze disk {drive}: {str(e)}",
                'type': 'defrag_disk'
            }
    
    def _handle_check_disk(self, drive: str) -> Dict[str, Any]:
        """Handle disk check"""
        if not drive:
            drive = "C:"
        
        try:
            result = subprocess.run(['chkdsk', drive], capture_output=True, text=True, check=True)
            return {
                'success': True,
                'message': f"Disk check completed for drive {drive}. Check results for any issues found.",
                'type': 'check_disk',
                'data': {'output': result.stdout}
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to check disk {drive}: {str(e)}",
                'type': 'check_disk'
            }
    
    def _handle_system_scan(self) -> Dict[str, Any]:
        """Handle system file scan"""
        try:
            subprocess.run(['sfc', '/scannow'], check=True)
            return {
                'success': True,
                'message': "System File Checker scan started. This may take several minutes to complete.",
                'type': 'system_scan'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to start system scan: {str(e)}",
                'type': 'system_scan'
            }
    
    def _handle_system_update(self) -> Dict[str, Any]:
        """Handle system update"""
        try:
            subprocess.run(['ms-settings:windowsupdate'], shell=True, check=True)
            return {
                'success': True,
                'message': "Windows Update settings opened. Please check for and install available updates.",
                'type': 'system_update'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to open Windows Update: {str(e)}",
                'type': 'system_update'
            }
    
    def _handle_memory_info(self) -> Dict[str, Any]:
        """Handle memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            message = f"Memory Status Report:\\n\\n"
            message += f"• Total RAM: {round(memory.total / (1024**3), 2)} GB\\n"
            message += f"• Available RAM: {round(memory.available / (1024**3), 2)} GB\\n"
            message += f"• Used RAM: {round(memory.used / (1024**3), 2)} GB ({memory.percent}%)\\n"
            message += f"• Swap Total: {round(swap.total / (1024**3), 2)} GB\\n"
            message += f"• Swap Used: {round(swap.used / (1024**3), 2)} GB ({swap.percent}%)"
            
            return {
                'success': True,
                'message': message,
                'type': 'memory_info',
                'data': {
                    'memory': memory._asdict(),
                    'swap': swap._asdict()
                }
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to get memory information: {str(e)}",
                'type': 'memory_info'
            }
    
    def _handle_cpu_info(self) -> Dict[str, Any]:
        """Handle CPU information"""
        try:
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            message = f"CPU Information:\\n\\n"
            message += f"• Processor: {platform.processor()}\\n"
            message += f"• Physical Cores: {psutil.cpu_count(logical=False)}\\n"
            message += f"• Logical Cores: {cpu_count}\\n"
            message += f"• Current Frequency: {cpu_freq.current:.2f} MHz\\n"
            message += f"• Max Frequency: {cpu_freq.max:.2f} MHz\\n"
            message += f"• Current Usage: {cpu_percent}%"
            
            return {
                'success': True,
                'message': message,
                'type': 'cpu_info',
                'data': {
                    'count': cpu_count,
                    'frequency': cpu_freq._asdict(),
                    'usage': cpu_percent
                }
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to get CPU information: {str(e)}",
                'type': 'cpu_info'
            }
    
    def _handle_system_info(self) -> Dict[str, Any]:
        """Handle comprehensive system information"""
        try:
            system_info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'hostname': socket.gethostname(),
                'username': os.getlogin()
            }
            
            message = f"System Information:\\n\\n"
            message += f"• Operating System: {system_info['system']} {system_info['release']}\\n"
            message += f"• Version: {system_info['version']}\\n"
            message += f"• Architecture: {system_info['machine']}\\n"
            message += f"• Processor: {system_info['processor']}\\n"
            message += f"• Computer Name: {system_info['hostname']}\\n"
            message += f"• Current User: {system_info['username']}"
            
            return {
                'success': True,
                'message': message,
                'type': 'system_info',
                'data': system_info
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to get system information: {str(e)}",
                'type': 'system_info'
            }
    
    def _handle_hardware_info(self) -> Dict[str, Any]:
        """Handle hardware information"""
        try:
            # Get basic hardware info
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            
            message = f"Hardware Information:\\n\\n"
            message += f"• System Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\\n"
            message += f"• CPU Cores: {psutil.cpu_count()} logical, {psutil.cpu_count(logical=False)} physical\\n"
            message += f"• Total RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\\n"
            
            # Get disk info
            disk_usage = psutil.disk_usage('/')
            message += f"• Primary Disk: {round(disk_usage.total / (1024**3), 2)} GB total"
            
            return {
                'success': True,
                'message': message,
                'type': 'hardware_info'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to get hardware information: {str(e)}",
                'type': 'hardware_info'
            }
    
    def _handle_volume_up(self) -> Dict[str, Any]:
        """Handle volume increase"""
        try:
            subprocess.run(['powershell', '-Command', 
                          '(New-Object -comObject WScript.Shell).SendKeys([char]175)'], 
                          check=True)
            return {
                'success': True,
                'message': "Volume increased.",
                'type': 'volume_up'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to increase volume: {str(e)}",
                'type': 'volume_up'
            }
    
    def _handle_volume_down(self) -> Dict[str, Any]:
        """Handle volume decrease"""
        try:
            subprocess.run(['powershell', '-Command', 
                          '(New-Object -comObject WScript.Shell).SendKeys([char]174)'], 
                          check=True)
            return {
                'success': True,
                'message': "Volume decreased.",
                'type': 'volume_down'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to decrease volume: {str(e)}",
                'type': 'volume_down'
            }
    
    def _handle_mute_toggle(self) -> Dict[str, Any]:
        """Handle mute toggle"""
        try:
            subprocess.run(['powershell', '-Command', 
                          '(New-Object -comObject WScript.Shell).SendKeys([char]173)'], 
                          check=True)
            return {
                'success': True,
                'message': "Audio mute toggled.",
                'type': 'mute_toggle'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to toggle mute: {str(e)}",
                'type': 'mute_toggle'
            }
    
    def _handle_help(self) -> Dict[str, Any]:
        """Handle help request"""
        help_text = """RAJIV Complete System Control - Available Commands:

🖥️ SYSTEM CONTROL:
• "system status" - Complete system report
• "restart computer" - Restart system
• "shutdown computer" - Shutdown system  
• "lock screen" - Lock workstation
• "sleep mode" - Enter sleep mode

📁 FILE OPERATIONS:
• "create folder [path]" - Create new folder
• "delete folder [path]" - Delete folder
• "copy file [source] to [dest]" - Copy file
• "move file [source] to [dest]" - Move file
• "delete file [path]" - Delete file
• "rename file [old] to [new]" - Rename file
• "organize desktop" - Sort desktop files
• "find large files" - Find files >100MB
• "empty recycle bin" - Empty trash

📱 APPLICATIONS:
• "open [app]" - Launch application
• "close [app]" - Close application
• "list programs" - Show installed programs

🌐 NETWORK:
• "network status" - Network information
• "wifi status" - WiFi profiles
• "ping [host]" - Test connection
• "check internet" - Test connectivity
• "download file [url]" - Download from URL

🔧 MAINTENANCE:
• "clean temp files" - System cleanup
• "disk cleanup" - Open disk cleanup
• "system scan" - Check system files
• "update system" - Windows updates

📊 INFORMATION:
• "memory usage" - RAM information
• "cpu info" - Processor details
• "disk usage" - Storage information
• "system info" - Complete system details

🔊 AUDIO/DISPLAY:
• "volume up/down" - Adjust volume
• "mute" - Toggle audio mute

And much more! Just ask RAJIV naturally."""

        return {
            'success': True,
            'message': help_text,
            'type': 'help'
        }
    
    def _handle_weather_duplicate_removed(self, location: str = None) -> Dict[str, Any]:
        """Removed duplicate - see _handle_weather above"""
        pass
    
    # === EXTRACTION HELPER METHODS ===
    
    def _extract_path(self, command: str, prefix: str) -> str:
        """Extract file/folder path from command"""
        try:
            return command.split(prefix)[1].strip()
        except:
            return ""
    
    def _extract_copy_paths(self, command: str) -> Dict[str, str]:
        """Extract source and destination paths from copy/move commands"""
        try:
            parts = command.split(' to ')
            if len(parts) == 2:
                source = parts[0].split(' ', 2)[2].strip()  # Remove "copy file" or "move file"
                destination = parts[1].strip()
                return {'source': source, 'destination': destination}
        except:
            pass
        return {'source': '', 'destination': ''}
    
    def _extract_rename_paths(self, command: str) -> Dict[str, str]:
        """Extract old and new paths from rename command"""
        try:
            parts = command.split(' to ')
            if len(parts) == 2:
                old = parts[0].split('rename file')[1].strip()
                new = parts[1].strip()
                return {'old': old, 'new': new}
        except:
            pass
        return {'old': '', 'new': ''}
    
    def _extract_app_name(self, command: str) -> str:
        """Extract application name from open/close commands"""
        try:
            if command.startswith('open '):
                return command[5:].strip()
            elif command.startswith('close '):
                return command[6:].strip()
        except:
            pass
        return ""
    
    def _extract_host(self, command: str) -> str:
        """Extract host from ping command"""
        try:
            if 'ping ' in command:
                return command.split('ping ')[1].strip()
        except:
            pass
        return "google.com"
    
    def _extract_url(self, command: str) -> str:
        """Extract URL from download command"""
        try:
            parts = command.split()
            for part in parts:
                if part.startswith('http'):
                    return part
        except:
            pass
        return ""
    
    def _extract_drive(self, command: str) -> str:
        """Extract drive letter from disk commands"""
        try:
            import re
            match = re.search(r'[A-Za-z]:', command)
            return match.group(0) if match else "C:"
        except:
            pass
        return "C:"