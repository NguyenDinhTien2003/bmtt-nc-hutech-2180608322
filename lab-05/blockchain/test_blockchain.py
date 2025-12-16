from blockchain import Blockchain

# Khởi tạo Blockchain
my_blockchain = Blockchain()

# Thêm các giao dịch
print("Adding transactions...")
my_blockchain.add_transaction('Alice', 'Bob', 10)
my_blockchain.add_transaction('Bob', 'Charlie', 5)
my_blockchain.add_transaction('Charlie', 'Alice', 3)

# Đào một khối mới (Mining)
print("Mining a new block...")
previous_block = my_blockchain.get_previous_block()
previous_proof = previous_block.proof
proof = my_blockchain.proof_of_work(previous_proof)
previous_hash = previous_block.hash
my_blockchain.create_block(proof, previous_hash)

# Thêm thêm giao dịch và đào tiếp khối nữa
my_blockchain.add_transaction('Genesis', 'Miner', 1) # Phần thưởng đào
previous_block = my_blockchain.get_previous_block()
previous_proof = previous_block.proof
proof = my_blockchain.proof_of_work(previous_proof)
previous_hash = previous_block.hash
my_blockchain.create_block(proof, previous_hash)

# Hiển thị thông tin chuỗi
print("\n--- Blockchain Content ---")
for block in my_blockchain.chain:
    print(f"Block #{block.index}")
    print(f"  Timestamp: {block.timestamp}")
    print(f"  Transactions: {block.transactions}")
    print(f"  Proof: {block.proof}")
    print(f"  Previous Hash: {block.previous_hash}")
    print(f"  Hash: {block.hash}")
    print("-" * 30)

# Kiểm tra tính hợp lệ
print(f"Is Blockchain Valid?: {my_blockchain.is_chain_valid(my_blockchain.chain)}")