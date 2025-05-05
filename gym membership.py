import streamlit as st
import hashlib
import time

# Define the Block class
class Block:
    def __init__(self, data, previous_hash=''):
        self.timestamp = time.ctime()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        info = self.timestamp + str(self.data) + self.previous_hash
        return hashlib.sha256(info.encode()).hexdigest()

# Define the GymLedger blockchain
class GymLedger:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = Block("Genesis Block", "0")
        self.chain.append(genesis)
    
    def add_entry(self, data):
        previous_hash = self.chain[-1].hash
        new_block = Block(data, previous_hash)
        self.chain.append(new_block)
    
    def get_chain(self):
        return self.chain

# Streamlit UI
st.title("🏋️‍♂️ Gym Membership Ledger (Blockchain)")

# Use Streamlit's session state to keep the blockchain persistent
if 'ledger' not in st.session_state:
    st.session_state.ledger = GymLedger()

st.subheader("➕ Add New Member Entry")

with st.form("entry_form"):
    member = st.text_input("Member Name")
    plan = st.selectbox("Membership Plan", ["Monthly", "Quarterly", "Annual"])
    amount = st.text_input("Amount Paid (e.g., $50)")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if member and amount:
            st.session_state.ledger.add_entry({
                "member": member,
                "plan": plan,
                "paid": amount
            })
            st.success("Entry added to ledger.")
        else:
            st.warning("Please fill in all fields.")

st.subheader("📜 Ledger Blocks")

for i, block in enumerate(st.session_state.ledger.get_chain()):
    with st.expander(f"Block {i}"):
        st.write(f"**Timestamp**: {block.timestamp}")
        st.write(f"**Data**: {block.data}")
        st.write(f"**Hash**: `{block.hash}`")
        st.write(f"**Previous Hash**: `{block.previous_hash}`")
