import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface GetModelVersionsByIdRsp {
  id: string;
  model_id: string;
  version: string;
  approved: boolean;
  stage: string;
  artifact_uri: string;
  training_data_uri: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface GetModelByIdRsp {
  id: string;
  name: string;
  owner: string;
  framework: string;
  versions: GetModelVersionsByIdRsp[];
}

export interface GetModelsRsp {
  id: string;
  name: string;
  owner: string;
  framework: string;
  versions: GetModelVersionsByIdRsp[];
}

export interface CreateModelReq {
  name: string;
  owner: string;
  description: string;
  framework: string;
  algorithm: string;
}

export interface CreateModelRsp {
  id: string;
  name: string;
  owner: string;
  description: string;
  framework: string;
  algorithm: string;
  created_at: string;
  updated_at: string;
}

export interface CreateModelVersionReq {
  version: string;
  artifact_uri: string;
  training_data_uri: string;
  tags: string[];
}

export interface CreateModelVersionRsp {
  id: string;
  model_id: string;
  version: string;
  approved: boolean;
  stage: string;
  artifact_uri: string;
  training_data_uri: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface ChangeModelVersionStageReq {
  stage: string;
}

export interface ChangeModelVersionStageRsp {
  id: string;
  model_id: string;
  version: string;
  approved: boolean;
  stage: string;
  artifact_uri: string;
  training_data_uri: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root',
})
export class ModelService {
  private http = inject(HttpClient);

  private apiUrl = 'http://localhost:8000/api/v1/models';

  getModels(): Observable<GetModelsRsp[]> {
    return this.http.get<GetModelsRsp[]>(this.apiUrl);
  }

  getModelById(modelId: string): Observable<GetModelByIdRsp> {
    return this.http.get<GetModelByIdRsp>(
      `${this.apiUrl}/${modelId}`
    );
  }

  getModelVersionsById(modelId: string): Observable<GetModelVersionsByIdRsp[]> {
    return this.http.get<GetModelVersionsByIdRsp[]>(
      `${this.apiUrl}/${modelId}/versions`
    );
  }

  createModel(
    request: CreateModelReq
  ): Observable<CreateModelRsp> {
    return this.http.post<CreateModelRsp>(
      this.apiUrl,
      request
    );
  }

  createModelVersion(
    modelId: string,
    request: CreateModelVersionReq
  ): Observable<CreateModelVersionRsp> {
    return this.http.post<CreateModelVersionRsp>(
      `${this.apiUrl}/${modelId}/versions`,
      request
    );
  }

  changeModelVersionStage(
    modelId: string,
    versionId: string,
    request: ChangeModelVersionStageReq
  ): Observable<ChangeModelVersionStageRsp> {
    return this.http.post<ChangeModelVersionStageRsp>(
      `${this.apiUrl}/${modelId}/versions/${versionId}/stage`,
      request
    );
  }


}