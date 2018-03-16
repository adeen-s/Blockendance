from block import Block
import datetime as dt
import copy

def next_block(last_block, data):
    """
    Create the next block in the blockchain
    """
    if not last_block:
        raise ValueError("Previous block cannot be None")

    this_index = last_block.index + 1
    this_timestamp = dt.datetime.now()
    # Deep copy to prevent modification of original data
    this_data = copy.deepcopy(data)
    this_prev_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_prev_hash)

def add_block(form, data, blockchain):
    """
    Add a new attendance block to the blockchain
    """
    try:
        # Create attendance data structure
        attendance_data = {
            "type": "attendance",
            "teacher_name": data[0] if len(data) > 0 else "",
            "date": data[1] if len(data) > 1 else "",
            "course": data[2] if len(data) > 2 else "",
            "year": data[3] if len(data) > 3 else "",
            "present_students": []
        }

        # Collect present students from form
        i = 1
        while form.get("roll_no{}".format(i)):
            roll_no = form.get("roll_no{}".format(i))
            if roll_no:  # Only add non-empty roll numbers
                attendance_data["present_students"].append(roll_no)
            i += 1

        # Validate that we have some data
        if not attendance_data["present_students"]:
            return "Error: No students marked present!"

        # Get the last block and create new block
        previous_block = blockchain[-1]
        block_to_add = next_block(previous_block, attendance_data)

        # Validate the new block
        if not block_to_add.is_valid():
            return "Error: Invalid block created!"

        # Add to blockchain
        blockchain.append(block_to_add)

        return "Block #{} has been added to the blockchain! {} students marked present.".format(
            block_to_add.index, len(attendance_data["present_students"]))

    except Exception as e:
        return f"Error adding block: {str(e)}"
