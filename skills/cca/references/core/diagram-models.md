# The Convergence Model

CCA composes several different layers. They are not all the same kind of standard.

```
flowchart TB
    subgraph HUMANS["Human knowledge-work methods"]
        BASB["BASB / CODE\nCapture · Organize\nDistill · Express"]
        PARA["PARA\nProjects · Areas\nResources · Archives"]
        ZK["ZETTELKASTEN\nAddressable Linked Ideas"]
    end

    subgraph AGENTS["Agent context methods"]
        WIKI["LLM WIKI\nPersistent Maintained Synthesis"]
        ICM["ICM / MWP\nStages · Routing · Handoffs"]
    end

    subgraph STANDARDS["Open Standards & Ecosystem Conventions"]
        AGENTSMD["AGENTS.md\nSSOT · Scoped \n Portable Instructions"]
        SKILLSMD["SKILL.md\nFocused Capabilities"]
    end

    subgraph FRAMEWORKS["Frameworks and Methodologies"]
        FAA["Enterprise scaling\nSAFe · LeSS · DA"]
        FAB["Team delivery methods\nScrum · Kanban · DSDM · FDD · ASD · XP"]
        FAC["SE approaches\nTDD · MDE · RAD · IID · Lean SD · RUP / UP"]
        FAD["Process discipline\nPSP · TSP"]
        FAE["Delivery lifecycle\nDevOps"]
        FAF["Method engineering\nSEMAT"]
    end
```

```
flowchart TB
    CCA["CCA\nComposition + interoperability semantics"]

    FRAMEWORKS --> CCA
    METHODOLOGIES --> CCA
    STANDARDS --> CCA
    PRINCIPLES --> CCA
    AGENTS --> CCA
    HUMANS --> CCA

    CCA --> BRAIN["PKM / Second brains"]
    CCA --> CODE["Coding projects"]
    CCA --> RESEARCH["Research systems"]
    CCA --> CLIENT["Client workspaces"]
    CCA --> HYBRID["Hybrid workspaces"]
```