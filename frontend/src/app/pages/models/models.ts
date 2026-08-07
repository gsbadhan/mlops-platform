import { Component, inject, signal } from '@angular/core';
import { CreateModelReq, GetModelsRsp, ModelService } from '../../services/model';
import { RouterLink } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { getApiErrorMessage } from '../../services/api-error';

@Component({
  selector: 'app-models',
  imports: [RouterLink],
  templateUrl: './models.html',
  styleUrl: './models.css',
})
export class ModelsComponent {
  private modelService = inject(ModelService);

  models = signal<GetModelsRsp[]>([]);
  loading = signal(true);
  error = signal('');

  createFormVisible = signal(false);
  creating = signal(false);
  createError = signal('');

  newModel = signal<CreateModelReq>({
    name: '',
    owner: '',
    description: '',
    framework: 'scikit-learn',
    algorithm: 'Random Forest',
  });

  frameworks = [
    'scikit-learn',
    'xgboost',
    'pytorch',
    'tensorflow',
    'lightgbm',
    'unknown',
  ];

  algorithms = [
    'Random Forest',
    'Gradient Boosting',
    'XGBoost',
    'LightGBM',
    'Logistic Regression',
    'Linear Regression',
    'Decision Tree',
    'Support Vector Machine',
    'K-Means',
    'Neural Network',
    'CNN',
    'RNN',
    'LSTM',
    'Transformer',
  ];


  constructor() {
    this.loadModels();
  }

  loadModels(): void {
    this.loading.set(true);
    this.error.set('');

    this.modelService.getModels().subscribe({
      next: (data) => {
        console.log('Models API response:', data);
        this.models.set(data);
        this.loading.set(false);
      },

      error: (err) => {
        console.error('Models API error:', err);
        this.error.set('Unable to load models.');
        this.loading.set(false);
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

    this.newModel.set({
      name: '',
      owner: '',
      description: '',
      framework: 'scikit-learn',
      algorithm: 'Random Forest',
    });
  }

  updateName(event: Event): void {
    const value = (event.target as HTMLInputElement).value;

    this.newModel.update(model => ({
      ...model,
      name: value,
    }));
  }

  updateOwner(event: Event): void {
    const value = (event.target as HTMLInputElement).value;

    this.newModel.update(model => ({
      ...model,
      owner: value,
    }));
  }

  updateDescription(event: Event): void {
    const value = (event.target as HTMLTextAreaElement).value;

    this.newModel.update(model => ({
      ...model,
      description: value,
    }));
  }

  updateFramework(event: Event): void {
    const value = (event.target as HTMLSelectElement).value;

    this.newModel.update(model => ({
      ...model,
      framework: value,
    }));
  }

  updateAlgorithm(event: Event): void {
    const value = (event.target as HTMLSelectElement).value;

    this.newModel.update(model => ({
      ...model,
      algorithm: value,
    }));
  }


  createModel(event: Event): void {
    event.preventDefault();
    const request = this.newModel();
    if (
      !request.name ||
      !request.owner ||
      !request.description ||
      !request.framework ||
      !request.algorithm
    ) {
      this.createError.set('Please fill in all fields.');
      return;
    }

    this.creating.set(true);
    this.createError.set('');

    this.modelService.createModel(request).subscribe({
      next: (response) => {
        console.log('Model created:', response);
        this.creating.set(false);
        this.hideCreateForm();
        this.loadModels();
      },

      error: (error: HttpErrorResponse) => {
        this.creating.set(false);
        this.createError.set(
          getApiErrorMessage(error, 'Unable to create model.')
        );
      },
    });
  }

}