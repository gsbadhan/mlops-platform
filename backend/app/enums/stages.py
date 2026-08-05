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


class MonitoringStatus(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"        