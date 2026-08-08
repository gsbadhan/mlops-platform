import { Component, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { RouterLink } from '@angular/router';

import {
  GetModelMetricsRsp,
  ModelService,
  GetModelsRsp,
} from '../../services/model';

import { getApiErrorMessage } from '../../services/api-error';

@Component({
  selector: 'app-monitoring',
  templateUrl: './monitoring.html',
  styleUrl: './monitoring.css',
  imports: [RouterLink],
})
export class MonitoringComponent {
  private modelService = inject(ModelService);

  models = signal<GetModelsRsp[]>([]);
  selectedModelId = signal('');
  loadingModels = signal(false);
  modelsError = signal('');
  //
  metrics = signal<GetModelMetricsRsp[]>([]);
  loadingMetrics = signal(false);
  metricsError = signal('');

  constructor() {
    this.loadModels();
  }

  loadModels(): void {
    this.loadingModels.set(true);
    this.modelsError.set('');

    this.modelService.getModels().subscribe({
      next: (response) => {
        this.models.set(response);
        this.loadingModels.set(false);
      },

      error: (error: HttpErrorResponse) => {
        console.error(
          'Get models error:',
          error
        );

        this.loadingModels.set(false);

        this.modelsError.set(
          getApiErrorMessage(
            error,
            'Unable to load models.'
          )
        );
      },
    });
  }

  updateSelectedModel(event: Event): void {
    const modelId =
      (event.target as HTMLSelectElement).value;

    this.selectedModelId.set(modelId);
    this.loadModelMetrics(modelId);
  }

  //
  loadModelMetrics(modelId: string): void {
    if (!modelId) {
      this.metrics.set([]);
      return;
    }

    this.loadingMetrics.set(true);
    this.metricsError.set('');
    this.metrics.set([]);

    this.modelService
      .getModelMetrics(modelId)
      .subscribe({
        next: (response) => {
          console.log(
            'Model metrics:',
            response
          );

          this.metrics.set(response);
          this.loadingMetrics.set(false);
        },

        error: (error: HttpErrorResponse) => {
          console.error(
            'Get model metrics error:',
            error
          );

          this.loadingMetrics.set(false);

          this.metricsError.set(
            getApiErrorMessage(
              error,
              'Unable to load model metrics.'
            )
          );
        },
      });
  }
}