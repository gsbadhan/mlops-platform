## Model Registry Workflow

```mermaid
graph LR
    DRAFT --> VALIDATED
    VALIDATED --> APPROVED
    APPROVED --> STAGING
    STAGING --> PRODUCTION
    PRODUCTION --> ARCHIVED
    
    style DRAFT fill:#e3f2fd, stroke-width:2px
    style VALIDATED fill:#fff3e0, stroke-width:2px
    style APPROVED fill:#f3e5f5, stroke-width:2px
    style STAGING fill:#e0f7fa, stroke-width:2px
    style PRODUCTION fill:#e8f5e9, stroke-width:2px
    style ARCHIVED fill:#efebe9, stroke-width:2px
```

## Deployment Workflow

```mermaid
graph TD
    REQUESTED --> VALIDATING
    VALIDATING --> DEPLOYING
    DEPLOYING --> SUCCEEDED
    DEPLOYING --> FAILED
    SUCCEEDED --> ROLLED_BACK
    FAILED --> REQUESTED
    
    style REQUESTED fill:#f9f,stroke:#333,stroke-width:2px
    style SUCCEEDED fill:#9f9,stroke:#333,stroke-width:2px
    style FAILED fill:#f99,stroke:#333,stroke-width:2px
    style ROLLED_BACK fill:#ff9,stroke:#333,stroke-width:2px
```    

## Model and Deployment Workflow
```mermaid
graph LR
    subgraph Model_Registry["Model Registry"]
        MR_Model[Model] --> MR_Version[Version] --> MR_Approval[Approval]
    end
    
    subgraph Deployment_Management["Deployment Management"]
        DM_Requested[Requested] --> DM_Validating[Validating]
        DM_Validating --> DM_Deploying[Deploying]
        DM_Deploying --> DM_Success[Succeeded]
        DM_Deploying --> DM_Fail[Failed]
        DM_Fail -->|Retry| DM_Requested
        DM_Success --> DM_Rollback[Rolled Back]
    end
    
    MR_Approval -->|Approved Version| DM_Requested
    
    style Model_Registry fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Deployment_Management fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    style MR_Model fill:#bbdefb
    style MR_Version fill:#bbdefb
    style MR_Approval fill:#bbdefb
    
    style DM_Requested fill:#fff3e0
    style DM_Validating fill:#fff3e0
    style DM_Deploying fill:#fff3e0
    style DM_Success fill:#c8e6c9
    style DM_Fail fill:#ffcdd2
    style DM_Rollback fill:#fff9c4
 ```   