# SDN-Based Access Control System using POX

## 📌 Problem Statement
Design and implement an SDN-based access control system that allows only authorized hosts to communicate within a network. Unauthorized hosts must be blocked using controller-based flow rules.

---

## 🎯 Objectives
- Maintain access control using SDN principles
- Install allow/deny rules using OpenFlow
- Block unauthorized hosts
- Verify enforcement using network testing

---

## 🛠️ Setup Requirements

- Ubuntu (Virtual Machine recommended)
- Mininet
- POX Controller
- Python 3.9 (for POX compatibility)

---

## ⚙️ Execution Steps

### 1. Start POX Controller
    cd ~/pox
    ../pox-env/bin/python pox.py mac_blocker forwarding.l2_learning openflow.of_01 --port=6633

### 2. Start Mininet Topology
    sudo mn --topo single,3 --controller=remote,ip=127.0.0.1,port=6633 --mac

### 3. Test Connectivity
    pingall

---

## 📊 Expected Output

    *** Results: 66% dropped (2/6 received)

### Interpretation:
- h1 ↔ h2 → Allowed  
- h3 → Blocked  
- Access control successfully enforced  

---

## 🧠 Approach

- Implemented a custom POX controller module (mac_blocker.py)
- Used MAC-based filtering to block unauthorized host (h3)
- Installed high-priority OpenFlow rules to:
  - Drop packets from h3
  - Drop packets to h3
- Ensured rules override default learning switch behavior

---

## 📸 Output Screenshot

See `result.png`

---

## ✅ Conclusion

The SDN controller successfully enforces access control policies by dynamically installing flow rules. Unauthorized hosts are effectively isolated while authorized communication is preserved.
