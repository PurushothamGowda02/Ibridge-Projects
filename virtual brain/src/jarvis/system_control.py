"""JARVIS System Control Module - Advanced system monitoring and control"""

import psutil
import platform
import subprocess
import os
import shutil
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import json


class SystemController:
    """Advanced system control and monitoring like JARVIS"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': platform.node(),
            'python_version': platform.python_version()
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get real-time system status like JARVIS dashboard"""
        try:
            # CPU Information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory Information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk Information
            disk_usage = psutil.disk_usage('/')
            
            # Network Information
            network = psutil.net_io_counters()
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'usage_percent': cpu_percent,
                    'cores': cpu_count,
                    'frequency_mhz': cpu_freq.current if cpu_freq else None,
                    'temperature': self._get_cpu_temperature()
                },
                'memory': {
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_gb': round(memory.used / (1024**3), 2),
                    'usage_percent': memory.percent,
                    'swap_total_gb': round(swap.total / (1024**3), 2),
                    'swap_used_gb': round(swap.used / (1024**3), 2)
                },
                'disk': {
                    'total_gb': round(disk_usage.total / (1024**3), 2),
                    'used_gb': round(disk_usage.used / (1024**3), 2),
                    'free_gb': round(disk_usage.free / (1024**3), 2),
                    'usage_percent': round((disk_usage.used / disk_usage.total) * 100, 1)
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_received': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_received': network.packets_recv
                },
                'uptime': {
                    'boot_time': boot_time.isoformat(),
                    'uptime_hours': round(uptime.total_seconds() / 3600, 1)
                },
                'system': self.system_info
            }
        except Exception as e:
            return {'error': f'Failed to get system status: {str(e)}'}
    
    def _get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature (Windows specific)"""
        try:
            if platform.system() == "Windows":
                # Try to get temperature using WMI (requires wmi package)
                try:
                    import wmi
                    w = wmi.WMI(namespace="root\\wmi")
                    temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]
                    return round((temperature_info.CurrentTemperature / 10.0) - 273.15, 1)
                except:
                    return None
            else:
                # Linux/Mac temperature reading
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            for entry in entries:
                                if 'cpu' in name.lower() or 'core' in entry.label.lower():
                                    return entry.current
                except:
                    return None
        except:
            return None
    
    def get_running_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top running processes by CPU usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    proc_info = proc.info
                    proc_info['cpu_percent'] = proc.cpu_percent()
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:limit]
        except Exception as e:
            return [{'error': f'Failed to get processes: {str(e)}'}]
    
    def kill_process(self, process_name: str) -> Dict[str, Any]:
        """Terminate a process by name"""
        try:
            killed_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        proc.terminate()
                        killed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if killed_count > 0:
                return {
                    'success': True,
                    'message': f'Terminated {killed_count} instance(s) of {process_name}',
                    'killed_count': killed_count
                }
            else:
                return {
                    'success': False,
                    'message': f'No running process found with name: {process_name}'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to kill process: {str(e)}'
            }
    
    def clean_temp_files(self) -> Dict[str, Any]:
        """Clean temporary files like JARVIS maintenance"""
        try:
            cleaned_size = 0
            cleaned_files = 0
            
            temp_dirs = []
            if platform.system() == "Windows":
                temp_dirs = [
                    os.environ.get('TEMP', ''),
                    os.environ.get('TMP', ''),
                    os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
                ]
            else:
                temp_dirs = ['/tmp', '/var/tmp']
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                cleaned_size += file_size
                                cleaned_files += 1
                            except (PermissionError, FileNotFoundError):
                                continue
            
            return {
                'success': True,
                'message': f'Cleaned {cleaned_files} temporary files',
                'cleaned_files': cleaned_files,
                'cleaned_size_mb': round(cleaned_size / (1024*1024), 2)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to clean temp files: {str(e)}'
            }
    
    def schedule_shutdown(self, minutes: int) -> Dict[str, Any]:
        """Schedule system shutdown"""
        try:
            if platform.system() == "Windows":
                subprocess.run(['shutdown', '/s', '/t', str(minutes * 60)], check=True)
            else:
                subprocess.run(['sudo', 'shutdown', '-h', f'+{minutes}'], check=True)
            
            return {
                'success': True,
                'message': f'System will shutdown in {minutes} minutes'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to schedule shutdown: {str(e)}'
            }
    
    def cancel_shutdown(self) -> Dict[str, Any]:
        """Cancel scheduled shutdown"""
        try:
            if platform.system() == "Windows":
                subprocess.run(['shutdown', '/a'], check=True)
            else:
                subprocess.run(['sudo', 'shutdown', '-c'], check=True)
            
            return {
                'success': True,
                'message': 'Scheduled shutdown cancelled'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to cancel shutdown: {str(e)}'
            }
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network interface information"""
        try:
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {
                    'addresses': [],
                    'stats': None
                }
                
                for addr in addrs:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                
                # Get interface statistics
                try:
                    stats = psutil.net_if_stats()[interface]
                    interface_info['stats'] = {
                        'is_up': stats.isup,
                        'duplex': str(stats.duplex),
                        'speed': stats.speed,
                        'mtu': stats.mtu
                    }
                except KeyError:
                    pass
                
                interfaces[interface] = interface_info
            
            return {
                'success': True,
                'interfaces': interfaces,
                'io_counters': dict(psutil.net_io_counters()._asdict())
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to get network info: {str(e)}'
            }
    
    def get_disk_info(self) -> Dict[str, Any]:
        """Get detailed disk information"""
        try:
            disks = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'usage_percent': round((usage.used / usage.total) * 100, 1)
                    }
                except PermissionError:
                    continue
            
            return {
                'success': True,
                'disks': disks,
                'io_counters': dict(psutil.disk_io_counters()._asdict()) if psutil.disk_io_counters() else None
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to get disk info: {str(e)}'
            }