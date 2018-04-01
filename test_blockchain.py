#!/usr/bin/env python3
"""
Test script to verify blockchain functionality
Demonstrates core blockchain operations without the web interface
"""

import datetime as dt
from block import Block
from genesis import create_blockchain
from newBlock import next_block, add_block
from checkChain import check_integrity, get_blockchain_stats

def test_blockchain_creation():
    """Test blockchain initialization"""
    print("🔗 Testing Blockchain Creation...")
    blockchain = create_blockchain()
    
    print(f"✅ Genesis block created: {blockchain[0]}")
    print(f"✅ Genesis block hash: {blockchain[0].hash}")
    print(f"✅ Blockchain length: {len(blockchain)}")
    return blockchain

def test_block_addition(blockchain):
    """Test adding new blocks to the blockchain"""
    print("\n📝 Testing Block Addition...")
    
    # Simulate attendance data
    attendance_data = {
        "type": "attendance",
        "teacher_name": "Dr. Smith",
        "date": "2018-03-16",
        "course": "Computer Science",
        "year": "2024",
        "present_students": ["CS-2024-01", "CS-2024-03", "CS-2024-05"]
    }
    
    # Add block
    previous_block = blockchain[-1]
    new_block = next_block(previous_block, attendance_data)
    blockchain.append(new_block)
    
    print(f"✅ New block added: {new_block}")
    print(f"✅ Block data: {new_block.data['teacher_name']} - {len(new_block.data['present_students'])} students")
    print(f"✅ Blockchain length: {len(blockchain)}")
    
    return blockchain

def test_multiple_blocks(blockchain):
    """Test adding multiple blocks"""
    print("\n📚 Testing Multiple Block Addition...")
    
    test_data = [
        {
            "type": "attendance",
            "teacher_name": "Prof. Johnson",
            "date": "2018-03-17",
            "course": "Mathematics",
            "year": "2023",
            "present_students": ["MATH-2023-02", "MATH-2023-04", "MATH-2023-06", "MATH-2023-08"]
        },
        {
            "type": "attendance", 
            "teacher_name": "Dr. Wilson",
            "date": "2018-03-18",
            "course": "Physics",
            "year": "2022",
            "present_students": ["PHY-2022-01", "PHY-2022-02"]
        }
    ]
    
    for i, data in enumerate(test_data):
        previous_block = blockchain[-1]
        new_block = next_block(previous_block, data)
        blockchain.append(new_block)
        print(f"✅ Block {i+2} added: {data['teacher_name']} - {data['course']}")
    
    print(f"✅ Total blocks in chain: {len(blockchain)}")
    return blockchain

def test_chain_integrity(blockchain):
    """Test blockchain integrity verification"""
    print("\n🔒 Testing Chain Integrity...")
    
    result = check_integrity(blockchain)
    print(f"✅ Integrity check result: {result}")
    
    # Test individual block validation
    for i, block in enumerate(blockchain):
        if block.is_valid():
            print(f"✅ Block {i} is valid")
        else:
            print(f"❌ Block {i} is invalid")
    
    return result

def test_tamper_detection(blockchain):
    """Test tamper detection by modifying a block"""
    print("\n🚨 Testing Tamper Detection...")
    
    if len(blockchain) > 1:
        # Save original data
        original_data = blockchain[1].data.copy()
        original_hash = blockchain[1].hash
        
        # Tamper with block data
        blockchain[1].data["teacher_name"] = "TAMPERED"
        
        # Check integrity (should fail)
        result = check_integrity(blockchain)
        print(f"❌ After tampering: {result}")
        
        # Restore original data
        blockchain[1].data = original_data
        blockchain[1].hash = original_hash
        
        # Check integrity again (should pass)
        result = check_integrity(blockchain)
        print(f"✅ After restoration: {result}")

def test_blockchain_stats(blockchain):
    """Test blockchain statistics"""
    print("\n📊 Testing Blockchain Statistics...")
    
    stats = get_blockchain_stats(blockchain)
    print(f"✅ Total blocks: {stats['total_blocks']}")
    print(f"✅ Attendance blocks: {stats['attendance_blocks']}")
    print(f"✅ Total attendance records: {stats['total_attendance_records']}")
    
    if stats['latest_block']:
        latest = stats['latest_block']
        print(f"✅ Latest block index: {latest['index']}")
        print(f"✅ Latest block hash: {latest['hash'][:20]}...")

def main():
    """Run all blockchain tests"""
    print("🚀 Starting Blockchain Functionality Tests")
    print("=" * 50)
    
    try:
        # Test blockchain creation
        blockchain = test_blockchain_creation()
        
        # Test block addition
        blockchain = test_block_addition(blockchain)
        
        # Test multiple blocks
        blockchain = test_multiple_blocks(blockchain)
        
        # Test chain integrity
        test_chain_integrity(blockchain)
        
        # Test tamper detection
        test_tamper_detection(blockchain)
        
        # Test statistics
        test_blockchain_stats(blockchain)
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print(f"📈 Final blockchain contains {len(blockchain)} blocks")
        
        # Display final chain summary
        print("\n📋 Blockchain Summary:")
        for i, block in enumerate(blockchain):
            if block.data.get('type') == 'genesis':
                print(f"  Block {i}: Genesis Block")
            else:
                teacher = block.data.get('teacher_name', 'Unknown')
                course = block.data.get('course', 'Unknown')
                students = len(block.data.get('present_students', []))
                print(f"  Block {i}: {teacher} - {course} ({students} students)")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
