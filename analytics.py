"""
Blockchain Analytics Module
Provides advanced analytics and reporting for the blockchain
"""

import datetime as dt
from collections import defaultdict, Counter
import json

def get_attendance_analytics(blockchain):
    """
    Generate comprehensive attendance analytics
    """
    analytics = {
        "overview": {
            "total_blocks": len(blockchain),
            "attendance_blocks": 0,
            "total_students_recorded": 0,
            "unique_teachers": set(),
            "unique_courses": set(),
            "date_range": {"start": None, "end": None}
        },
        "by_teacher": defaultdict(lambda: {
            "total_classes": 0,
            "total_students": 0,
            "courses": set(),
            "dates": []
        }),
        "by_course": defaultdict(lambda: {
            "total_classes": 0,
            "total_students": 0,
            "teachers": set(),
            "dates": []
        }),
        "by_date": defaultdict(lambda: {
            "classes": 0,
            "students": 0,
            "teachers": set(),
            "courses": set()
        }),
        "student_attendance": defaultdict(int),
        "trends": {
            "daily_attendance": [],
            "course_popularity": [],
            "teacher_activity": []
        }
    }
    
    dates = []
    
    for block in blockchain:
        if block.index == 0:  # Skip genesis block
            continue
            
        if block.data.get('type') == 'attendance':
            analytics["overview"]["attendance_blocks"] += 1
            
            teacher = block.data.get('teacher_name', 'Unknown')
            course = block.data.get('course', 'Unknown')
            date = block.data.get('date', '')
            students = block.data.get('present_students', [])
            
            # Update overview
            analytics["overview"]["total_students_recorded"] += len(students)
            analytics["overview"]["unique_teachers"].add(teacher)
            analytics["overview"]["unique_courses"].add(course)
            
            if date:
                dates.append(date)
            
            # Update teacher analytics
            analytics["by_teacher"][teacher]["total_classes"] += 1
            analytics["by_teacher"][teacher]["total_students"] += len(students)
            analytics["by_teacher"][teacher]["courses"].add(course)
            analytics["by_teacher"][teacher]["dates"].append(date)
            
            # Update course analytics
            analytics["by_course"][course]["total_classes"] += 1
            analytics["by_course"][course]["total_students"] += len(students)
            analytics["by_course"][course]["teachers"].add(teacher)
            analytics["by_course"][course]["dates"].append(date)
            
            # Update date analytics
            analytics["by_date"][date]["classes"] += 1
            analytics["by_date"][date]["students"] += len(students)
            analytics["by_date"][date]["teachers"].add(teacher)
            analytics["by_date"][date]["courses"].add(course)
            
            # Update student attendance count
            for student in students:
                analytics["student_attendance"][student] += 1
    
    # Convert sets to lists for JSON serialization
    analytics["overview"]["unique_teachers"] = list(analytics["overview"]["unique_teachers"])
    analytics["overview"]["unique_courses"] = list(analytics["overview"]["unique_courses"])
    
    # Set date range
    if dates:
        analytics["overview"]["date_range"]["start"] = min(dates)
        analytics["overview"]["date_range"]["end"] = max(dates)
    
    # Convert defaultdicts to regular dicts and sets to lists
    analytics["by_teacher"] = {k: {
        "total_classes": v["total_classes"],
        "total_students": v["total_students"],
        "courses": list(v["courses"]),
        "dates": v["dates"],
        "avg_students_per_class": v["total_students"] / v["total_classes"] if v["total_classes"] > 0 else 0
    } for k, v in analytics["by_teacher"].items()}
    
    analytics["by_course"] = {k: {
        "total_classes": v["total_classes"],
        "total_students": v["total_students"],
        "teachers": list(v["teachers"]),
        "dates": v["dates"],
        "avg_students_per_class": v["total_students"] / v["total_classes"] if v["total_classes"] > 0 else 0
    } for k, v in analytics["by_course"].items()}
    
    analytics["by_date"] = {k: {
        "classes": v["classes"],
        "students": v["students"],
        "teachers": list(v["teachers"]),
        "courses": list(v["courses"])
    } for k, v in analytics["by_date"].items()}
    
    # Generate trends
    analytics["trends"]["course_popularity"] = sorted(
        [(course, data["total_students"]) for course, data in analytics["by_course"].items()],
        key=lambda x: x[1], reverse=True
    )
    
    analytics["trends"]["teacher_activity"] = sorted(
        [(teacher, data["total_classes"]) for teacher, data in analytics["by_teacher"].items()],
        key=lambda x: x[1], reverse=True
    )
    
    analytics["trends"]["daily_attendance"] = sorted(
        [(date, data["students"]) for date, data in analytics["by_date"].items()]
    )
    
    return analytics

def get_blockchain_health(blockchain):
    """
    Analyze blockchain health and integrity metrics
    """
    health = {
        "integrity": {
            "valid_blocks": 0,
            "invalid_blocks": 0,
            "broken_links": 0,
            "hash_mismatches": 0
        },
        "performance": {
            "avg_block_size": 0,
            "total_data_size": 0,
            "block_creation_rate": 0
        },
        "security": {
            "unique_hashes": set(),
            "hash_distribution": {},
            "potential_issues": []
        }
    }
    
    total_size = 0
    timestamps = []
    
    for i, block in enumerate(blockchain):
        # Check block validity
        if block.is_valid():
            health["integrity"]["valid_blocks"] += 1
        else:
            health["integrity"]["invalid_blocks"] += 1
        
        # Check linkage
        if i > 0:
            if block.prev_hash != blockchain[i-1].hash:
                health["integrity"]["broken_links"] += 1
        
        # Calculate block size (approximate)
        block_size = len(json.dumps(block.to_dict(), default=str))
        total_size += block_size
        
        # Collect timestamps
        timestamps.append(block.timestamp)
        
        # Check hash uniqueness
        if block.hash in health["security"]["unique_hashes"]:
            health["security"]["potential_issues"].append(f"Duplicate hash found in block {i}")
        health["security"]["unique_hashes"].add(block.hash)
        
        # Analyze hash distribution
        hash_prefix = block.hash[:2]
        health["security"]["hash_distribution"][hash_prefix] = \
            health["security"]["hash_distribution"].get(hash_prefix, 0) + 1
    
    # Calculate performance metrics
    health["performance"]["total_data_size"] = total_size
    health["performance"]["avg_block_size"] = total_size / len(blockchain) if blockchain else 0
    
    # Calculate block creation rate (blocks per day)
    if len(timestamps) > 1:
        time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 86400  # days
        health["performance"]["block_creation_rate"] = len(blockchain) / time_span if time_span > 0 else 0
    
    # Convert set to count for JSON serialization
    health["security"]["unique_hashes"] = len(health["security"]["unique_hashes"])
    
    return health

def generate_attendance_report(blockchain, format="text"):
    """
    Generate a comprehensive attendance report
    """
    analytics = get_attendance_analytics(blockchain)
    
    if format == "json":
        return json.dumps(analytics, indent=2, default=str)
    
    # Text format report
    report = []
    report.append("=" * 60)
    report.append("BLOCKCHAIN ATTENDANCE REPORT")
    report.append("=" * 60)
    
    # Overview
    overview = analytics["overview"]
    report.append(f"\nOVERVIEW:")
    report.append(f"  Total Blocks: {overview['total_blocks']}")
    report.append(f"  Attendance Records: {overview['attendance_blocks']}")
    report.append(f"  Total Students Recorded: {overview['total_students_recorded']}")
    report.append(f"  Unique Teachers: {len(overview['unique_teachers'])}")
    report.append(f"  Unique Courses: {len(overview['unique_courses'])}")
    
    if overview['date_range']['start']:
        report.append(f"  Date Range: {overview['date_range']['start']} to {overview['date_range']['end']}")
    
    # Top teachers
    report.append(f"\nTOP TEACHERS BY ACTIVITY:")
    for teacher, classes in analytics["trends"]["teacher_activity"][:5]:
        avg_students = analytics["by_teacher"][teacher]["avg_students_per_class"]
        report.append(f"  {teacher}: {classes} classes, {avg_students:.1f} avg students")
    
    # Top courses
    report.append(f"\nTOP COURSES BY ATTENDANCE:")
    for course, total_students in analytics["trends"]["course_popularity"][:5]:
        classes = analytics["by_course"][course]["total_classes"]
        report.append(f"  {course}: {total_students} total students, {classes} classes")
    
    # Most active students
    report.append(f"\nMOST ACTIVE STUDENTS:")
    top_students = sorted(analytics["student_attendance"].items(), 
                         key=lambda x: x[1], reverse=True)[:10]
    for student, count in top_students:
        report.append(f"  {student}: {count} attendances")
    
    return "\n".join(report)

def export_analytics(blockchain, filename="blockchain_analytics.json"):
    """
    Export comprehensive analytics to file
    """
    try:
        analytics = get_attendance_analytics(blockchain)
        health = get_blockchain_health(blockchain)
        
        export_data = {
            "generated_at": str(dt.datetime.now()),
            "blockchain_stats": {
                "total_blocks": len(blockchain),
                "genesis_hash": blockchain[0].hash if blockchain else None,
                "latest_hash": blockchain[-1].hash if blockchain else None
            },
            "analytics": analytics,
            "health": health
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return True, f"Analytics exported to {filename}"
    
    except Exception as e:
        return False, f"Error exporting analytics: {str(e)}"
