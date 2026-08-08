import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { getApiErrorMessage } from '../../services/api-error';
import {
  ChangeDeploymentStateReq,
  DeploymentService,
  GetDeploymentByIdRsp,
} from '../../services/deployment';

@Component({
  selector: 'app-deployment-details',
  imports: [DatePipe],
  templateUrl: './deployment-details.html',
  styleUrl: './deployment-details.css',
})
export class DeploymentDetailsComponent {
  private deploymentService = inject(DeploymentService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  deployment = signal<GetDeploymentByIdRsp | null>(null);
  loading = signal(false);
  error = signal('');
  //
  changeStateFormVisible = signal(false);
  changingState = signal(false);
  changeStateError = signal('');
  selectedState = signal('VALIDATING');


  deploymentStates = [
    'VALIDATING',
    'DEPLOYING',
    'SUCCEEDED',
    'FAILED'
  ];

  ngOnInit(): void {
    const deploymentId =
      this.route.snapshot.paramMap.get('deployment_id');

    if (!deploymentId) {
      this.error.set('Deployment ID is missing.');
      return;
    }

    this.loadDeployment(deploymentId);
  }

  loadDeployment(deploymentId: string): void {
    this.loading.set(true);
    this.error.set('');

    this.deploymentService
      .getDeploymentById(deploymentId)
      .subscribe({
        next: (response) => {
          console.log('Deployment:', response);

          this.deployment.set(response);
          this.loading.set(false);
        },

        error: (error) => {
          console.error('Get deployment error:', error);

          this.loading.set(false);
          this.error.set('Unable to load deployment.');
        },
      });
  }

  goBack(): void {
    this.router.navigate(['/deployments']);
  }

  showChangeStateForm(): void {
    this.changeStateFormVisible.set(true);
    this.changeStateError.set('');
    this.selectedState.set('VALIDATING');
  }

  hideChangeStateForm(): void {
    this.changeStateFormVisible.set(false);
    this.changeStateError.set('');
  }

  updateSelectedState(event: Event): void {
    const value =
      (event.target as HTMLSelectElement).value;
    this.selectedState.set(value);
  }

  changeDeploymentState(): void {
    const deployment =
      this.deployment();

    if (!deployment) {
      return;
    }

    const request: ChangeDeploymentStateReq = {
      state: this.selectedState(),
    };

    this.changingState.set(true);
    this.changeStateError.set('');

    this.deploymentService
      .changeDeploymentState(
        deployment.deployment_id,
        request
      )
      .subscribe({
        next: (response) => {
          console.log(
            'Deployment state changed:',
            response
          );
          this.deployment.set(response);
          this.changingState.set(false);
          this.hideChangeStateForm();
        },

        error: (error: HttpErrorResponse) => {
          console.error(
            'Change deployment state error:',
            error
          );
          this.changingState.set(false);
          this.changeStateError.set(
            getApiErrorMessage(
              error,
              'Unable to change deployment state.'
            )
          );
        },
      });
  }
}