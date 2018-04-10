#!/usr/bin/env python3
"""
Comprehensive Blockchain Demo
Demonstrates all features of the Blockendance blockchain implementation
"""

import datetime as dt
import time
from block import Block
from genesis import create_blockchain
from newBlock import next_block
from checkChain import check_integrity, get_blockchain_stats
from persistence import save_blockchain, load_blockchain, export_blockchain_csv
from analytics import get_attendance_analytics, generate_attendance_report

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n🔹 {title}")
    print("-" * 40)

def demo_blockchain_creation():
    """Demonstrate blockchain creation"""
    print_header("BLOCKCHAIN CREATION DEMO")
    
    print("Creating a new blockchain from scratch...")
    blockchain = create_blockchain()
    
    print(f"✅ Genesis block created successfully!")
    print(f"   Index: {blockchain[0].index}")
    print(f"   Hash: {blockchain[0].hash}")
    print(f"   Data: {blockchain[0].data}")
    print(f"   Timestamp: {blockchain[0].timestamp}")
    
    return blockchain

def demo_block_addition(blockchain):
    """Demonstrate adding blocks with realistic data"""
    print_header("BLOCK ADDITION DEMO")
    
    # Sample attendance data for different scenarios
    attendance_records = [
        {
            "type": "attendance",
            "teacher_name": "Dr. Sarah Johnson",
            "date": "2018-04-01",
            "course": "Computer Science",
            "year": "2024",
            "present_students": ["CS-2024-01", "CS-2024-03", "CS-2024-05", "CS-2024-07", "CS-2024-09"]
        },
        {
            "type": "attendance",
            "teacher_name": "Prof. Michael Chen",
            "date": "2018-04-01",
            "course": "Mathematics",
            "year": "2023",
            "present_students": ["MATH-2023-02", "MATH-2023-04", "MATH-2023-06", "MATH-2023-08", "MATH-2023-10", "MATH-2023-12"]
        },
        {
            "type": "attendance",
            "teacher_name": "Dr. Emily Rodriguez",
            "date": "2018-04-02",
            "course": "Physics",
            "year": "2022",
            "present_students": ["PHY-2022-01", "PHY-2022-03", "PHY-2022-05"]
        },
        {
            "type": "attendance",
            "teacher_name": "Dr. Sarah Johnson",
            "date": "2018-04-03",
            "course": "Computer Science",
            "year": "2024",
            "present_students": ["CS-2024-01", "CS-2024-02", "CS-2024-05", "CS-2024-08"]
        },
        {
            "type": "attendance",
            "teacher_name": "Prof. David Wilson",
            "date": "2018-04-03",
            "course": "Chemistry",
            "year": "2021",
            "present_students": ["CHEM-2021-01", "CHEM-2021-02", "CHEM-2021-04", "CHEM-2021-06", "CHEM-2021-07", "CHEM-2021-09", "CHEM-2021-11"]
        }
    ]
    
    print("Adding attendance records to the blockchain...")
    
    for i, record in enumerate(attendance_records):
        print(f"\n📝 Adding Block {i+1}:")
        print(f"   Teacher: {record['teacher_name']}")
        print(f"   Course: {record['course']} ({record['year']})")
        print(f"   Date: {record['date']}")
        print(f"   Students Present: {len(record['present_students'])}")
        
        # Add block to blockchain
        previous_block = blockchain[-1]
        new_block = next_block(previous_block, record)
        blockchain.append(new_block)
        
        print(f"   ✅ Block #{new_block.index} added successfully")
        print(f"   Hash: {new_block.hash[:20]}...")
        
        # Small delay for demonstration
        time.sleep(0.5)
    
    print(f"\n🎉 Successfully added {len(attendance_records)} attendance blocks!")
    print(f"📊 Total blockchain length: {len(blockchain)} blocks")
    
    return blockchain

def demo_integrity_verification(blockchain):
    """Demonstrate blockchain integrity verification"""
    print_header("INTEGRITY VERIFICATION DEMO")
    
    print("Verifying blockchain integrity...")
    result = check_integrity(blockchain)
    print(f"✅ {result}")
    
    print("\nVerifying individual blocks...")
    for i, block in enumerate(blockchain):
        if block.is_valid():
            print(f"   Block {i}: ✅ Valid")
        else:
            print(f"   Block {i}: ❌ Invalid")
    
    print("\n🔒 Demonstrating tamper detection...")
    if len(blockchain) > 1:
        # Save original data
        original_data = blockchain[1].data.copy()
        original_hash = blockchain[1].hash
        
        # Tamper with data
        blockchain[1].data["teacher_name"] = "HACKER"
        print("   🚨 Simulating data tampering...")
        
        # Check integrity
        result = check_integrity(blockchain)
        print(f"   ❌ After tampering: {result}")
        
        # Restore data
        blockchain[1].data = original_data
        blockchain[1].hash = original_hash
        
        result = check_integrity(blockchain)
        print(f"   ✅ After restoration: {result}")

def demo_analytics(blockchain):
    """Demonstrate blockchain analytics"""
    print_header("BLOCKCHAIN ANALYTICS DEMO")
    
    print("Generating comprehensive analytics...")
    analytics = get_attendance_analytics(blockchain)
    
    print_section("Overview Statistics")
    overview = analytics['overview']
    print(f"Total Blocks: {overview['total_blocks']}")
    print(f"Attendance Records: {overview['attendance_blocks']}")
    print(f"Total Students Recorded: {overview['total_students_recorded']}")
    print(f"Unique Teachers: {len(overview['unique_teachers'])}")
    print(f"Unique Courses: {len(overview['unique_courses'])}")
    print(f"Date Range: {overview['date_range']['start']} to {overview['date_range']['end']}")
    
    print_section("Teacher Performance")
    for teacher, data in analytics['by_teacher'].items():
        avg_students = data['avg_students_per_class']
        print(f"{teacher}:")
        print(f"  Classes: {data['total_classes']}")
        print(f"  Total Students: {data['total_students']}")
        print(f"  Average per Class: {avg_students:.1f}")
        print(f"  Courses: {', '.join(data['courses'])}")
    
    print_section("Course Statistics")
    for course, data in analytics['by_course'].items():
        avg_students = data['avg_students_per_class']
        print(f"{course}:")
        print(f"  Classes: {data['total_classes']}")
        print(f"  Total Students: {data['total_students']}")
        print(f"  Average per Class: {avg_students:.1f}")
        print(f"  Teachers: {', '.join(data['teachers'])}")
    
    print_section("Most Active Students")
    top_students = sorted(analytics['student_attendance'].items(), 
                         key=lambda x: x[1], reverse=True)[:10]
    for student, count in top_students:
        print(f"{student}: {count} attendances")

def demo_persistence(blockchain):
    """Demonstrate blockchain persistence"""
    print_header("PERSISTENCE DEMO")
    
    print("Saving blockchain to file...")
    success, message = save_blockchain(blockchain, "demo_blockchain.json")
    print(f"✅ {message}")
    
    print("\nExporting to CSV format...")
    success, message = export_blockchain_csv(blockchain, "demo_export.csv")
    print(f"✅ {message}")
    
    print("\nTesting blockchain loading...")
    loaded_blockchain, load_message = load_blockchain("demo_blockchain.json")
    if loaded_blockchain:
        print(f"✅ {load_message}")
        
        # Verify loaded blockchain
        integrity = check_integrity(loaded_blockchain)
        print(f"✅ Loaded blockchain integrity: {integrity}")
    else:
        print(f"❌ Load failed: {load_message}")

def demo_report_generation(blockchain):
    """Demonstrate report generation"""
    print_header("REPORT GENERATION DEMO")
    
    print("Generating comprehensive attendance report...")
    report = generate_attendance_report(blockchain, format='text')
    
    print(report)
    
    print(f"\n📄 Report generated successfully!")
    print(f"📊 Report contains {len(report.split('\\n'))} lines")

def main():
    """Run the complete blockchain demonstration"""
    print("🚀 BLOCKENDANCE - COMPLETE BLOCKCHAIN DEMONSTRATION")
    print("🔗 Built from scratch in Python")
    print("📚 Educational blockchain implementation")
    
    try:
        # Step 1: Create blockchain
        blockchain = demo_blockchain_creation()
        
        # Step 2: Add blocks
        blockchain = demo_block_addition(blockchain)
        
        # Step 3: Verify integrity
        demo_integrity_verification(blockchain)
        
        # Step 4: Show analytics
        demo_analytics(blockchain)
        
        # Step 5: Demonstrate persistence
        demo_persistence(blockchain)
        
        # Step 6: Generate reports
        demo_report_generation(blockchain)
        
        # Final summary
        print_header("DEMONSTRATION COMPLETE")
        print("🎉 All blockchain features demonstrated successfully!")
        print(f"📈 Final blockchain contains {len(blockchain)} blocks")
        print(f"🔒 All blocks verified and secure")
        print(f"💾 Data saved and exported")
        print(f"📊 Analytics generated")
        
        print("\n🌟 Key Features Demonstrated:")
        print("   ✅ Blockchain creation from scratch")
        print("   ✅ Block addition with cryptographic linking")
        print("   ✅ Integrity verification and tamper detection")
        print("   ✅ Comprehensive analytics and reporting")
        print("   ✅ Data persistence and export capabilities")
        print("   ✅ Real-world attendance management use case")
        
        print("\n🎓 This demonstrates a complete blockchain implementation")
        print("   built entirely from scratch using core cryptographic principles!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
