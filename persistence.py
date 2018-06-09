"""
Blockchain Persistence Module
Handles saving and loading blockchain data to/from JSON files
"""

import json
import os
import datetime as dt
from block import Block

BLOCKCHAIN_FILE = "blockchain_data.json"
BACKUP_DIR = "blockchain_backups"

def save_blockchain(blockchain, filename=None):
    """
    Save blockchain to JSON file
    """
    if filename is None:
        filename = BLOCKCHAIN_FILE
    
    try:
        # Convert blockchain to serializable format
        blockchain_data = {
            "metadata": {
                "created": str(dt.datetime.now()),
                "total_blocks": len(blockchain),
                "version": "1.0"
            },
            "blocks": [block.to_dict() for block in blockchain]
        }
        
        # Ensure backup directory exists
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(blockchain_data, f, indent=2, default=str)
        
        # Create backup with timestamp
        timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(BACKUP_DIR, f"blockchain_backup_{timestamp}.json")
        with open(backup_filename, 'w') as f:
            json.dump(blockchain_data, f, indent=2, default=str)
        
        return True, f"Blockchain saved to {filename} and backed up to {backup_filename}"
    
    except Exception as e:
        return False, f"Error saving blockchain: {str(e)}"

def load_blockchain(filename=None):
    """
    Load blockchain from JSON file
    """
    if filename is None:
        filename = BLOCKCHAIN_FILE
    
    try:
        if not os.path.exists(filename):
            return None, f"Blockchain file {filename} not found"
        
        with open(filename, 'r') as f:
            blockchain_data = json.load(f)
        
        # Reconstruct blockchain from data
        blockchain = []
        for block_data in blockchain_data["blocks"]:
            # Convert timestamp string back to datetime
            timestamp = dt.datetime.fromisoformat(block_data["timestamp"].replace('Z', '+00:00'))
            
            # Create block object
            block = Block(
                index=block_data["index"],
                timestamp=timestamp,
                data=block_data["data"],
                prev_hash=block_data["prev_hash"]
            )
            
            # Verify the hash matches
            if block.hash != block_data["hash"]:
                return None, f"Hash mismatch in block {block_data['index']}"
            
            blockchain.append(block)
        
        metadata = blockchain_data.get("metadata", {})
        return blockchain, f"Blockchain loaded successfully: {metadata.get('total_blocks', 0)} blocks"
    
    except Exception as e:
        return None, f"Error loading blockchain: {str(e)}"

def export_blockchain_csv(blockchain, filename="blockchain_export.csv"):
    """
    Export blockchain data to CSV format
    """
    try:
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['block_index', 'timestamp', 'type', 'teacher_name', 'course', 
                         'year', 'date', 'students_present', 'prev_hash', 'hash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for block in blockchain:
                if block.data.get('type') == 'genesis':
                    writer.writerow({
                        'block_index': block.index,
                        'timestamp': block.timestamp,
                        'type': 'genesis',
                        'teacher_name': '',
                        'course': '',
                        'year': '',
                        'date': '',
                        'students_present': '',
                        'prev_hash': block.prev_hash,
                        'hash': block.hash
                    })
                elif block.data.get('type') == 'attendance':
                    writer.writerow({
                        'block_index': block.index,
                        'timestamp': block.timestamp,
                        'type': 'attendance',
                        'teacher_name': block.data.get('teacher_name', ''),
                        'course': block.data.get('course', ''),
                        'year': block.data.get('year', ''),
                        'date': block.data.get('date', ''),
                        'students_present': ';'.join(block.data.get('present_students', [])),
                        'prev_hash': block.prev_hash,
                        'hash': block.hash
                    })
        
        return True, f"Blockchain exported to {filename}"
    
    except Exception as e:
        return False, f"Error exporting blockchain: {str(e)}"

def get_blockchain_backups():
    """
    Get list of available blockchain backups
    """
    try:
        if not os.path.exists(BACKUP_DIR):
            return []
        
        backups = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("blockchain_backup_") and filename.endswith(".json"):
                filepath = os.path.join(BACKUP_DIR, filename)
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': stat.st_size,
                    'created': dt.datetime.fromtimestamp(stat.st_mtime)
                })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    except Exception as e:
        print(f"Error getting backups: {e}")
        return []

def restore_from_backup(backup_filename):
    """
    Restore blockchain from a backup file
    """
    try:
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        blockchain, message = load_blockchain(backup_path)
        
        if blockchain:
            # Save as current blockchain
            success, save_message = save_blockchain(blockchain)
            if success:
                return blockchain, f"Restored from backup: {backup_filename}"
            else:
                return None, f"Failed to save restored blockchain: {save_message}"
        else:
            return None, f"Failed to load backup: {message}"
    
    except Exception as e:
        return None, f"Error restoring from backup: {str(e)}"

def cleanup_old_backups(keep_count=10):
    """
    Clean up old backup files, keeping only the most recent ones
    """
    try:
        backups = get_blockchain_backups()
        
        if len(backups) <= keep_count:
            return True, f"No cleanup needed. {len(backups)} backups found."
        
        # Remove old backups
        removed_count = 0
        for backup in backups[keep_count:]:
            os.remove(backup['filepath'])
            removed_count += 1
        
        return True, f"Cleaned up {removed_count} old backups. Kept {keep_count} most recent."
    
    except Exception as e:
        return False, f"Error cleaning up backups: {str(e)}"
