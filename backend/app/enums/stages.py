from enum import Enum


class ModelRegistryStages(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"


class DeploymentState(str, Enum):
    REQUESTED = "REQUESTED"
    VALIDATING = "VALIDATING"
    DEPLOYING = "DEPLOYING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    NONE = "NONE"


class Framework(str, Enum):
    SCIKIT_LEARN = "scikit-learn"
    XGBOOST = "xgboost"
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    LIGHTGBM = "lightgbm"
    UNKNOWN = "unknown"


class DeploymentEnvironment(str, Enum):
    DEV = "DEV"
    TEST = "TEST"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class Algorithm(str, Enum):
    RANDOM_FOREST = "Random Forest"
    GRADIENT_BOOSTING = "Gradient Boosting"
    XGBOOST = "XGBoost"
    LIGHTGBM = "LightGBM"
    LOGISTIC_REGRESSION = "Logistic Regression"
    LINEAR_REGRESSION = "Linear Regression"
    DECISION_TREE = "Decision Tree"
    SVM = "Support Vector Machine"
    KMEANS = "K-Means"
    NEURAL_NETWORK = "Neural Network"
    CNN = "CNN"
    RNN = "RNN"
    LSTM = "LSTM"
    TRANSFORMER = "Transformer"


class DeploymentEvent(str, Enum):
    DEPLOYMENT_REQUESTED = "deployment_requested"
    VALIDATION_REQUESTED = "validation_requested"
    VALIDATION_STARTED = "validation_started"
    DEPLOYMENT_STARTED = "deployment_started"
    DEPLOYMENT_COMPLETED = "deployment_completed"
    DEPLOYMENT_FAILED = "deployment_failed"
    APPROVAL_VALIDATION_FAILED = "approval_validation_failed"
    RETRY_REQUESTED = "retry_requested"
    ROLLBACK_STARTED = "rollback_started"


MODEL_REGISTRY_STAGE_TRANSITIONS = {
    ModelRegistryStages.DRAFT: {
        ModelRegistryStages.VALIDATED,
    },
    ModelRegistryStages.VALIDATED: {
        ModelRegistryStages.APPROVED,
    },
    ModelRegistryStages.APPROVED: {
        ModelRegistryStages.STAGING,
    },
    ModelRegistryStages.STAGING: {
        ModelRegistryStages.PRODUCTION,
    },
    ModelRegistryStages.PRODUCTION: {
        ModelRegistryStages.ARCHIVED,
    },
    ModelRegistryStages.ARCHIVED: {},
}

DEPLOYMENT_STATE_TRANSITIONS = {
    DeploymentState.REQUESTED: {
        DeploymentState.VALIDATING,
    },
    DeploymentState.VALIDATING: {
        DeploymentState.DEPLOYING,
    },
    DeploymentState.DEPLOYING: {
        DeploymentState.SUCCEEDED,
        DeploymentState.FAILED,
    },
    DeploymentState.FAILED: {
        DeploymentState.REQUESTED,
    },
    DeploymentState.SUCCEEDED: {
        DeploymentState.ROLLED_BACK,
    },
    DeploymentState.ROLLED_BACK: {},
}


DEPLOYMENT_STATES_TO_EVENT: dict[
    tuple[DeploymentState, DeploymentState], DeploymentEvent
] = {
    (
        DeploymentState.NONE,
        DeploymentState.REQUESTED,
    ): DeploymentEvent.DEPLOYMENT_REQUESTED,
    (
        DeploymentState.REQUESTED,
        DeploymentState.VALIDATING,
    ): DeploymentEvent.VALIDATION_REQUESTED,
    (
        DeploymentState.VALIDATING,
        DeploymentState.DEPLOYING,
    ): DeploymentEvent.DEPLOYMENT_STARTED,
    (
        DeploymentState.DEPLOYING,
        DeploymentState.SUCCEEDED,
    ): DeploymentEvent.DEPLOYMENT_COMPLETED,
    (
        DeploymentState.DEPLOYING,
        DeploymentState.FAILED,
    ): DeploymentEvent.DEPLOYMENT_FAILED,
    (
        DeploymentState.SUCCEEDED,
        DeploymentState.ROLLED_BACK,
    ): DeploymentEvent.ROLLBACK_STARTED,
    (
        DeploymentState.FAILED,
        DeploymentState.REQUESTED,
    ): DeploymentEvent.RETRY_REQUESTED,
}
