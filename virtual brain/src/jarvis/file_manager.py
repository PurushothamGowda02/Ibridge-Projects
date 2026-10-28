"""JARVIS File Management System - Advanced file operations"""

import os
import shutil
import glob
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import mimetypes
import hashlib


class FileManager:
    """Advanced file management system like JARVIS"""
    
    def __init__(self):
        self.home_dir = Path.home()
        self.desktop_dir = self.home_dir / "Desktop"
        self.documents_dir = self.home_dir / "Documents"
        self.downloads_dir = self.home_dir / "Downloads"
    
    def organize_desktop(self) -> Dict[str, Any]:
        """Organize desktop files into folders by type"""
        try:
            organized_count = 0
            created_folders = []
            
            # Define file type categories
            categories = {
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
                'Presentations': ['.ppt', '.pptx', '.odp'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm']
            }
            
            if not self.desktop_dir.exists():
                return {'success': False, 'message': 'Desktop directory not found'}
            
            # Process each file on desktop
            for file_path in self.desktop_dir.iterdir():
                if file_path.is_file():
                    file_ext = file_path.suffix.lower()
                    
                    # Find appropriate category
                    target_folder = None
                    for category, extensions in categories.items():
                        if file_ext in extensions:
                            target_folder = category
                            break
                    
                    if target_folder:
                        # Create category folder if it doesn't exist
                        category_path = self.desktop_dir / target_folder
                        if not category_path.exists():
                            category_path.mkdir()
                            created_folders.append(target_folder)
                        
                        # Move file to category folder
                        target_path = category_path / file_path.name
                        if not target_path.exists():
                            shutil.move(str(file_path), str(target_path))
                            organized_count += 1
            
            return {
                'success': True,
                'message': f'Organized {organized_count} files into {len(created_folders)} folders',
                'organized_files': organized_count,
                'created_folders': created_folders
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to organize desktop: {str(e)}'
            }
    
    def find_files(self, pattern: str, directory: str = None, max_results: int = 50) -> Dict[str, Any]:
        """Find files matching pattern"""
        try:
            search_dir = Path(directory) if directory else self.home_dir
            if not search_dir.exists():
                return {'success': False, 'message': f'Directory not found: {directory}'}
            
            found_files = []
            
            # Search for files
            for file_path in search_dir.rglob(pattern):
                if len(found_files) >= max_results:
                    break
                
                if file_path.is_file():
                    stat = file_path.stat()
                    found_files.append({
                        'path': str(file_path),
                        'name': file_path.name,
                        'size_bytes': stat.st_size,
                        'size_mb': round(stat.st_size / (1024*1024), 2),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                    })
            
            return {
                'success': True,
                'message': f'Found {len(found_files)} files matching "{pattern}"',
                'files': found_files,
                'search_pattern': pattern,
                'search_directory': str(search_dir)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to find files: {str(e)}'
            }
    
    def find_large_files(self, min_size_mb: int = 100, directory: str = None) -> Dict[str, Any]:
        """Find large files consuming disk space"""
        try:
            search_dir = Path(directory) if directory else self.home_dir
            if not search_dir.exists():
                return {'success': False, 'message': f'Directory not found: {directory}'}
            
            large_files = []
            min_size_bytes = min_size_mb * 1024 * 1024
            
            for file_path in search_dir.rglob('*'):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size >= min_size_bytes:
                            large_files.append({
                                'path': str(file_path),
                                'name': file_path.name,
                                'size_mb': round(size / (1024*1024), 2),
                                'size_gb': round(size / (1024*1024*1024), 2),
                                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                            })
                    except (PermissionError, FileNotFoundError):
                        continue
            
            # Sort by size (largest first)
            large_files.sort(key=lambda x: x['size_mb'], reverse=True)
            
            total_size_gb = sum(f['size_gb'] for f in large_files)
            
            return {
                'success': True,
                'message': f'Found {len(large_files)} files larger than {min_size_mb}MB',
                'files': large_files[:50],  # Limit to top 50
                'total_files': len(large_files),
                'total_size_gb': round(total_size_gb, 2),
                'min_size_mb': min_size_mb
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to find large files: {str(e)}'
            }
    
    def find_duplicates(self, directory: str = None) -> Dict[str, Any]:
        """Find duplicate files by comparing file hashes"""
        try:
            search_dir = Path(directory) if directory else self.home_dir
            if not search_dir.exists():
                return {'success': False, 'message': f'Directory not found: {directory}'}
            
            file_hashes = {}
            duplicates = []
            
            for file_path in search_dir.rglob('*'):
                if file_path.is_file():
                    try:
                        # Calculate file hash
                        hash_md5 = hashlib.md5()
                        with open(file_path, "rb") as f:
                            for chunk in iter(lambda: f.read(4096), b""):
                                hash_md5.update(chunk)
                        file_hash = hash_md5.hexdigest()
                        
                        if file_hash in file_hashes:
                            # Found duplicate
                            duplicates.append({
                                'original': file_hashes[file_hash],
                                'duplicate': str(file_path),
                                'size_mb': round(file_path.stat().st_size / (1024*1024), 2),
                                'hash': file_hash
                            })
                        else:
                            file_hashes[file_hash] = str(file_path)
                    except (PermissionError, FileNotFoundError):
                        continue
            
            total_wasted_mb = sum(d['size_mb'] for d in duplicates)
            
            return {
                'success': True,
                'message': f'Found {len(duplicates)} duplicate files',
                'duplicates': duplicates,
                'total_wasted_mb': round(total_wasted_mb, 2),
                'total_wasted_gb': round(total_wasted_mb / 1024, 2)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to find duplicates: {str(e)}'
            }
    
    def clean_downloads(self, days_old: int = 30) -> Dict[str, Any]:
        """Clean old files from Downloads folder"""
        try:
            if not self.downloads_dir.exists():
                return {'success': False, 'message': 'Downloads directory not found'}
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            cleaned_files = []
            total_size_freed = 0
            
            for file_path in self.downloads_dir.iterdir():
                if file_path.is_file():
                    try:
                        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if modified_time < cutoff_date:
                            file_size = file_path.stat().st_size
                            file_path.unlink()  # Delete file
                            cleaned_files.append({
                                'name': file_path.name,
                                'size_mb': round(file_size / (1024*1024), 2),
                                'modified': modified_time.isoformat()
                            })
                            total_size_freed += file_size
                    except (PermissionError, FileNotFoundError):
                        continue
            
            return {
                'success': True,
                'message': f'Cleaned {len(cleaned_files)} old files from Downloads',
                'cleaned_files': cleaned_files,
                'total_files': len(cleaned_files),
                'size_freed_mb': round(total_size_freed / (1024*1024), 2),
                'size_freed_gb': round(total_size_freed / (1024*1024*1024), 2),
                'days_old': days_old
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to clean downloads: {str(e)}'
            }
    
    def create_backup(self, source_dir: str, backup_name: str = None) -> Dict[str, Any]:
        """Create backup of directory"""
        try:
            source_path = Path(source_dir)
            if not source_path.exists():
                return {'success': False, 'message': f'Source directory not found: {source_dir}'}
            
            # Create backup name with timestamp
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{source_path.name}_backup_{timestamp}"
            
            backup_path = self.documents_dir / "Backups" / backup_name
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy directory
            shutil.copytree(source_path, backup_path)
            
            # Calculate backup size
            total_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
            
            return {
                'success': True,
                'message': f'Created backup: {backup_name}',
                'backup_path': str(backup_path),
                'backup_name': backup_name,
                'size_mb': round(total_size / (1024*1024), 2),
                'size_gb': round(total_size / (1024*1024*1024), 2)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to create backup: {str(e)}'
            }
    
    def get_directory_size(self, directory: str) -> Dict[str, Any]:
        """Get total size of directory and its contents"""
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return {'success': False, 'message': f'Directory not found: {directory}'}
            
            total_size = 0
            file_count = 0
            folder_count = 0
            
            for item in dir_path.rglob('*'):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                        file_count += 1
                    except (PermissionError, FileNotFoundError):
                        continue
                elif item.is_dir():
                    folder_count += 1
            
            return {
                'success': True,
                'directory': directory,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024*1024), 2),
                'total_size_gb': round(total_size / (1024*1024*1024), 2),
                'file_count': file_count,
                'folder_count': folder_count
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to get directory size: {str(e)}'
            }