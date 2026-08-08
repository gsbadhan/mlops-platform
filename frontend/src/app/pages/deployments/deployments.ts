import { Component, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { RouterLink } from '@angular/router';

import {
  DeploymentService,
  GetDeploymentsRsp,
  CreateDeploymentReq
} from '../../services/deployment';

import { getApiErrorMessage } from '../../services/api-error';

@Component({
  selector: 'app-deployments',
  imports: [DatePipe, RouterLink],
  templateUrl: './deployments.html',
  styleUrl: './deployments.css',
})
export class DeploymentsComponent {

  private deploymentService = inject(
    DeploymentService
  );

  deployments = signal<GetDeploymentsRsp[]>([]);
  loading = signal(false);
  error = signal('');

  // Create deployment
  createFormVisible = signal(false);
  creating = signal(false);
  createError = signal('');

  newDeployment = signal<CreateDeploymentReq>({
    model_version_id: '',
    environment: 'STAGING',
    idempotency_key: '',
  });

  deploymentEnvironments = [
    'STAGING',
    'PRODUCTION'
  ]

  ngOnInit(): void {
    this.loadDeployments();
  }

  loadDeployments(): void {
    this.loading.set(true);
    this.error.set('');

    this.deploymentService
      .getDeployments()
      .subscribe({
        next: (response) => {
          console.log(
            'Deployments:',
            response
          );

          this.deployments.set(response);
          this.loading.set(false);
        },

        error: (error: HttpErrorResponse) => {
          console.error(
            'Get deployments error:',
            error
          );

          this.loading.set(false);

          this.error.set(
            getApiErrorMessage(
              error,
              'Unable to load deployments.'
            )
          );
        },
      });
  }

  showCreateForm(): void {
    this.createFormVisible.set(true);
    this.createError.set('');
  }

  hideCreateForm(): void {
    this.createFormVisible.set(false);
    this.createError.set('');

    this.newDeployment.set({
      model_version_id: '',
      environment: 'STAGING',
      idempotency_key: '',
    });
  }

  updateModelVersionId(
    event: Event
  ): void {
    const value =
      (event.target as HTMLInputElement).value;

    this.newDeployment.update(
      deployment => ({
        ...deployment,
        model_version_id: value,
      })
    );
  }

  updateEnvironment(
    event: Event
  ): void {
    const value =
      (event.target as HTMLSelectElement).value;

    this.newDeployment.update(
      deployment => ({
        ...deployment,
        environment: value,
      })
    );
  }

  updateIdempotencyKey(
    event: Event
  ): void {
    const value =
      (event.target as HTMLInputElement).value;

    this.newDeployment.update(
      deployment => ({
        ...deployment,
        idempotency_key: value,
      })
    );
  }

  createDeployment(): void {
    const request =
      this.newDeployment();

    if (!request.model_version_id) {
      this.createError.set(
        'Model version ID is required.'
      );
      return;
    }

    if (!request.idempotency_key) {
      this.createError.set(
        'Idempotency key is required.'
      );
      return;
    }

    this.creating.set(true);
    this.createError.set('');

    this.deploymentService
      .createDeployment(request)
      .subscribe({
        next: (response) => {
          console.log(
            'Deployment created:',
            response
          );

          this.creating.set(false);
          this.hideCreateForm();
          this.loadDeployments();
        },

        error: (
          error: HttpErrorResponse
        ) => {
          console.error(
            'Create deployment error:',
            error
          );
          this.creating.set(false);
          this.createError.set(
            getApiErrorMessage(
              error,
              'Unable to create deployment.'
            )
          );
        },
      });
  }
}