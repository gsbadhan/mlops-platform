import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { getApiErrorMessage } from '../../services/api-error';
import {
  ChangeModelVersionStageReq,
  CreateModelVersionReq,
  GetModelByIdRsp,
  GetModelVersionsByIdRsp,
  ModelService
} from '../../services/model';


@Component({
  selector: 'app-model-details',
  imports: [DatePipe],
  templateUrl: './model-details.html',
  styleUrl: './model-details.css',
})
export class ModelDetailsComponent {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private modelService = inject(ModelService);

  model = signal<GetModelByIdRsp | null>(null);
  loading = signal(true);
  error = signal('');

  versions = signal<GetModelVersionsByIdRsp[]>([]);
  versionsLoading = signal(true);
  versionsError = signal('');

  createVersionFormVisible = signal(false);
  creatingVersion = signal(false);
  createVersionError = signal('');
  newVersion = signal<CreateModelVersionReq>({
    version: '',
    artifact_uri: '',
    training_data_uri: '',
    tags: [],
  });
  newVersionTags = '';


  changeStageFormVisible = signal(false);
  changingStage = signal(false);
  changeStageError = signal('');
  selectedVersion = signal<GetModelVersionsByIdRsp | null>(null);
  selectedStage = signal('DRAFT');
  modelRegistryStages = [
    'DRAFT',
    'VALIDATED',
    'APPROVED',
    'STAGING',
    'PRODUCTION',
    'ARCHIVED',
  ];


  constructor() {
    const modelId = this.route.snapshot.paramMap.get('model_id');

    if (!modelId) {
      this.error.set('Model ID is missing.');
      this.loading.set(false);
      return;
    }

    this.loadModel(modelId);
    this.loadVersions(modelId);
  }

  goBack(): void {
    this.router.navigate(['/models']);
  }
  loadModel(modelId: string): void {
    this.modelService.getModelById(modelId).subscribe({
      next: (data) => {
        console.log('Model details:', data);

        this.model.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Model details error:', err);

        this.error.set('Unable to load model.');
        this.loading.set(false);
      },
    });
  }

  loadVersions(modelId: string): void {
    this.versionsLoading.set(true);
    this.versionsError.set('');

    this.modelService.getModelVersionsById(modelId).subscribe({
      next: (data) => {
        console.log('Model versions:', data);

        this.versions.set(data);
        this.versionsLoading.set(false);
      },

      error: (err: HttpErrorResponse) => {
        console.error('Model versions error:', err);
        this.versionsLoading.set(false);
        if (err.status === 404) {
          this.versions.set([]);
          return;
        }

        this.versionsError.set('Unable to load model versions.');
      },
    });
  }

  showCreateVersionForm(): void {
    this.createVersionFormVisible.set(true);
    this.createVersionError.set('');
  }

  hideCreateVersionForm(): void {
    this.createVersionFormVisible.set(false);
    this.createVersionError.set('');

    this.newVersion.set({
      version: '',
      artifact_uri: '',
      training_data_uri: '',
      tags: [],
    });

    this.newVersionTags = '';
  }

  updateVersion(event: Event): void {
    const value = (event.target as HTMLInputElement).value;

    this.newVersion.update(version => ({
      ...version,
      version: value,
    }));
  }

  updateArtifactUri(event: Event): void {
    const value = (event.target as HTMLInputElement).value;

    this.newVersion.update(version => ({
      ...version,
      artifact_uri: value,
    }));
  }

  updateTrainingDataUri(event: Event): void {
    const value = (event.target as HTMLInputElement).value;

    this.newVersion.update(version => ({
      ...version,
      training_data_uri: value,
    }));
  }

  updateTags(event: Event): void {
    this.newVersionTags = (
      event.target as HTMLInputElement
    ).value;
  }

  createVersion(event: Event): void {
    event.preventDefault();

    const modelId = this.route.snapshot.paramMap.get('model_id');

    if (!modelId) {
      this.createVersionError.set('Model ID is missing.');
      return;
    }

    const request: CreateModelVersionReq = {
      ...this.newVersion(),
      tags: this.newVersionTags
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0),
    };

    this.creatingVersion.set(true);
    this.createVersionError.set('');

    this.modelService
      .createModelVersion(modelId, request)
      .subscribe({
        next: (response) => {
          console.log('Model version created:', response);
          this.creatingVersion.set(false);
          this.hideCreateVersionForm();
          this.loadVersions(modelId);
        },

        error: (error: HttpErrorResponse) => {
          this.creatingVersion.set(false);
          this.createVersionError.set(
            getApiErrorMessage(
              error,
              'Unable to create model version.'
            )
          );
        },
      });
  }

  showChangeStageForm(
    version: GetModelVersionsByIdRsp
  ): void {
    console.log('Change stage clicked:', version);
    this.selectedVersion.set(version);
    this.selectedStage.set(version.stage);
    this.changeStageError.set('');
    this.changeStageFormVisible.set(true);
  }

  hideChangeStageForm(): void {
    this.changeStageFormVisible.set(false);
    this.selectedVersion.set(null);
    this.changeStageError.set('');
  }

  updateSelectedStage(event: Event): void {
    const value = (event.target as HTMLSelectElement).value;
    this.selectedStage.set(value);
  }

  changeStage(): void {
    const version = this.selectedVersion();
    if (!version) {
      this.changeStageError.set('Version is missing.');
      return;
    }

    const modelId = version.model_id;
    const request: ChangeModelVersionStageReq = {
      stage: this.selectedStage(),
    };

    this.changingStage.set(true);
    this.changeStageError.set('');

    this.modelService
      .changeModelVersionStage(
        modelId,
        version.id,
        request
      )
      .subscribe({
        next: (response) => {
          console.log('Stage changed:', response);
          this.changingStage.set(false);
          this.hideChangeStageForm();

          this.loadVersions(modelId);
        },
        error: (error: HttpErrorResponse) => {
          this.changingStage.set(false);
          this.changeStageError.set(
            getApiErrorMessage(
              error,
              'Unable to change model version stage.'
            )
          );
        },
      });
  }

}