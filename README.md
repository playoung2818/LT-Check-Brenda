flowchart TD
    Q1["Does the SO have every item in stock?<br/>(Available, ATP, Counted in Warehouse) [By SO]"]
    Ready["✅ SO is Ready to Ship"]
    Q2["Does the short item have a POD? [By Item]"]
    NoCommit["❌ Cannot commit date (no POD)"]
    Q3["When will the short item arrive? [By Item]"]
    Q4["If sales want to pull in a SO,<br/>what is the earliest date we can give?"]
    Assign["📅 Assign ETA / Latest arrival date"]

    Q1 -->|Yes| Ready
    Q1 -->|No| Q2
    Q2 -->|Yes| Q3
    Q2 -->|No| NoCommit
    Q3 --> Q4
    Q4 --> Assign
