def find_records(form, blockchain):
    """
    Find attendance records in the blockchain based on form criteria
    """
    try:
        # Extract search criteria from form
        search_name = form.get("name", "").strip()
        search_date = form.get("date", "").strip()
        search_course = form.get("course", "").strip()
        search_year = form.get("year", "").strip()
        expected_count = int(form.get("number", 0))

        # Search through blockchain
        for block in blockchain:
            # Skip genesis block
            if block.index == 0:
                continue

            # Check if block contains attendance data
            if not isinstance(block.data, dict) or block.data.get("type") != "attendance":
                continue

            # Extract block data
            block_data = block.data

            # Check if all criteria match
            conditions = [
                block_data.get("teacher_name", "") == search_name,
                block_data.get("date", "") == search_date,
                block_data.get("course", "") == search_course,
                block_data.get("year", "") == search_year,
                len(block_data.get("present_students", [])) == expected_count
            ]

            if all(conditions):
                return block_data.get("present_students", [])

        return -1  # Not found

    except (ValueError, TypeError) as e:
        print(f"Error in find_records: {e}")
        return -1

def get_all_attendance_records(blockchain):
    """
    Get all attendance records from the blockchain
    """
    records = []
    for block in blockchain:
        if (block.index > 0 and
            isinstance(block.data, dict) and
            block.data.get("type") == "attendance"):
            records.append({
                "block_index": block.index,
                "timestamp": block.timestamp,
                "teacher_name": block.data.get("teacher_name", ""),
                "date": block.data.get("date", ""),
                "course": block.data.get("course", ""),
                "year": block.data.get("year", ""),
                "present_students": block.data.get("present_students", []),
                "student_count": len(block.data.get("present_students", []))
            })
    return records

def search_by_student(blockchain, roll_no):
    """
    Find all attendance records for a specific student
    """
    student_records = []
    for block in blockchain:
        if (block.index > 0 and
            isinstance(block.data, dict) and
            block.data.get("type") == "attendance"):

            if roll_no in block.data.get("present_students", []):
                student_records.append({
                    "date": block.data.get("date", ""),
                    "course": block.data.get("course", ""),
                    "year": block.data.get("year", ""),
                    "teacher_name": block.data.get("teacher_name", "")
                })
    return student_records
