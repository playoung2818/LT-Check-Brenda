# LT-Check-Brenda

A Python-based tool for **lead time assignment** and **supply chain planning**.  
This project integrates data from QuickBooks, NAV, and Excel exports to automate the process of checking work orders (WO), purchase orders (PO), and vendor lead times.

---

## 📦 Requirements

- **Python**: 3.10 or later  
- **Package Manager**: `pip` (or `conda` if you prefer)

### Python Libraries

Install dependencies with:

```bash
pip install -r requirements.txt


## ⚙️ Installation
   Clone the repository and install the required packages:
   ```bash
   git clone https://github.com/your-repository/quickbook-inventory-log.git
   cd quickbook-inventory-log
   pip install -r requirements.txt

```
---

# SO Fulfillment Decision Tree

```mermaid
flowchart TD
    Q1["Q1: Does the SO have <br/> every item in stock?<br/> [By SO]"]
    Q2["Q2: Does the short <br/> item have a POD? [By Item]"]
    Q3["Q3: When will the <br/> short item arrive? [By Item]"]
    Q4["Q4: If sales want to <br/> pull in a SO,<br/>what is the earliest date <br/> we can give?"]

    Ready["✅ SO can be assigned LT"]
    NoCommit["❌ Taipei place POD"]
    Assign["📅 Assign ETA +7 as commitment date"]

    Q1 -->|Yes| Ready
    Q1 -->|No| Q2
    Q2 -->|Yes| Q3
    Q2 -->|No| NoCommit
    Q3 --> Q4
    Q4 --> Assign
    NoCommit --> Q3
