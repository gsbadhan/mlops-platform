import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface GetDeploymentsRsp {
  deployment_id: string;
  model_id: string;
  version: string;
  environment: string;
  status: string;
  event: string;
  timestamp: string;
}

export interface GetDeploymentByIdRsp {
  deployment_id: string;
  model_id: string;
  version: string;
  environment: string;
  status: string;
  event: string;
  timestamp: string;
}

export interface CreateDeploymentReq {
  model_version_id: string;
  environment: string;
  idempotency_key: string;
}

export interface CreateDeploymentRsp {
  deployment_id: string;
  model_id: string;
  version: string;
  environment: string;
  status: string;
  event: string;
  timestamp: string;
}

export interface ChangeDeploymentStateReq {
  state: string;
}

export interface ChangeDeploymentStateRsp {
  deployment_id: string;
  model_id: string;
  version: string;
  environment: string;
  status: string;
  event: string;
  timestamp: string;
}

@Injectable({
  providedIn: 'root',
})
export class DeploymentService {
  private http = inject(HttpClient);

  private apiUrl = 'http://localhost:8000/api/v1/deployments';

  getDeployments(): Observable<GetDeploymentsRsp[]> {
    return this.http.get<GetDeploymentsRsp[]>(this.apiUrl);
  }

  getDeploymentById(
    deploymentId: string
  ): Observable<GetDeploymentByIdRsp> {
    return this.http.get<GetDeploymentByIdRsp>(
      `${this.apiUrl}/${deploymentId}`
    );
  }

  createDeployment(
    request: CreateDeploymentReq
  ): Observable<CreateDeploymentRsp> {
    return this.http.post<CreateDeploymentRsp>(
      this.apiUrl,
      request
    );
  }

  changeDeploymentState(
    deploymentId: string,
    request: ChangeDeploymentStateReq
  ): Observable<ChangeDeploymentStateRsp> {
    return this.http.post<ChangeDeploymentStateRsp>(
      `${this.apiUrl}/${deploymentId}/state`,
      request
    );
  }
}