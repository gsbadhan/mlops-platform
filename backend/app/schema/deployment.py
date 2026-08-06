from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from app.enums.stages import DeploymentEnvironment
from app.enums.stages import DeploymentState, DeploymentEvent


class CreateDeploymentRequest(BaseModel):
    model_version_id: str = Field(min_length=3, max_length=36)
    environment: DeploymentEnvironment
    idempotency_key: str = Field(min_length=3, max_length=100)


class DeploymentResponse(BaseModel):
    deployment_id: str
    model_id: str
    version: str
    environment: DeploymentEnvironment
    status: DeploymentState
    event: DeploymentEvent
    timestamp: datetime
