# SO Fulfillment Decision Tree

```mermaid
flowchart TD
    Q1["Q1: Does the SO have every item in stock?<br/>(Available, ATP, Counted in Warehouse) [By SO]"]
    Q2["Q2: Does the short item have a POD? [By Item]"]
    Q3["Q3: When will the short item arrive? [By Item]"]
    Q4["Q4: If sales want to pull in a SO,<br/>what is the earliest date we can give?"]

    Ready["✅ SO is Ready to Ship"]
    NoCommit["❌ Cannot commit date (no POD)"]
    Assign["📅 Assign ETA +7 as commitment date"]

    Q1 -->|Yes| Ready
    Q1 -->|No| Q2
    Q2 -->|Yes| Q3
    Q2 -->|No| NoCommit
    Q3 --> Q4
    Q4 --> Assign
