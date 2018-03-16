def check_integrity(chain):
    """
    Check the integrity of the entire blockchain
    """
    if not chain:
        return "Error: Empty blockchain"

    if len(chain) == 1:
        # Only genesis block
        genesis = chain[0]
        if genesis.is_valid() and genesis.index == 0:
            return "Blockchain integrity verified: Only genesis block present"
        else:
            return "Error: Invalid genesis block"

    # Check each block
    for i, block in enumerate(chain):
        # Validate current block's hash
        if not block.is_valid():
            return f"Error: Block #{i} has invalid hash"

        # Check linkage to previous block (except genesis)
        if i > 0:
            previous_block = chain[i-1]
            if block.prev_hash != previous_block.hash:
                return f"Error: Block #{i} is not properly linked to previous block #{i-1}"

            # Check index sequence
            if block.index != previous_block.index + 1:
                return f"Error: Block #{i} has incorrect index. Expected {previous_block.index + 1}, got {block.index}"

    return f"Blockchain integrity verified: All {len(chain)} blocks are valid and properly linked"

def validate_block(block, previous_block=None):
    """
    Validate a single block
    """
    if not block:
        return False, "Block is None"

    # Check if block hash is valid
    if not block.is_valid():
        return False, "Block hash is invalid"

    # Check if it's properly linked to previous block
    if previous_block:
        if block.prev_hash != previous_block.hash:
            return False, "Block is not properly linked to previous block"
        if block.index != previous_block.index + 1:
            return False, "Block index is incorrect"

    return True, "Block is valid"

def get_blockchain_stats(chain):
    """
    Get statistics about the blockchain
    """
    if not chain:
        return {"error": "Empty blockchain"}

    stats = {
        "total_blocks": len(chain),
        "genesis_block": chain[0].to_dict() if chain else None,
        "latest_block": chain[-1].to_dict() if chain else None,
        "attendance_blocks": 0,
        "total_attendance_records": 0
    }

    for block in chain:
        if (block.index > 0 and
            isinstance(block.data, dict) and
            block.data.get("type") == "attendance"):
            stats["attendance_blocks"] += 1
            stats["total_attendance_records"] += len(block.data.get("present_students", []))

    return stats
