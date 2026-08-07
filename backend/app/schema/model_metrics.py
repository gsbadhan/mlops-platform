from pydantic import BaseModel, ConfigDict


class ModelMetricsResponse(BaseModel):
    version: str
    accuracy: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1_score: float | None = None

    model_config = ConfigDict(from_attributes=True)
