import { Routes } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard';
import { ModelsComponent } from './pages/models/models';
import { ModelDetailsComponent } from './pages/model-details/model-details';
import { DeploymentsComponent } from './pages/deployments/deployments';
import { DeploymentDetailsComponent } from './pages/deployment-details/deployment-details';
import { MonitoringComponent } from './pages/monitoring/monitoring';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full',
    },
    {
        path: 'dashboard',
        loadComponent: () =>
            import('./pages/dashboard/dashboard')
                .then(m => m.DashboardComponent),
    },
    {
        path: 'models',
        component: ModelsComponent,
    },
    {
        path: 'models/:model_id',
        component: ModelDetailsComponent,
    },
    {
        path: 'deployments',
        component: DeploymentsComponent,
    },
    {
        path: 'deployments/:deployment_id',
        component: DeploymentDetailsComponent,
    },
    {
        path: 'monitoring',
        loadComponent: () =>
            import('./pages/monitoring/monitoring')
                .then(m => m.MonitoringComponent),
    },
];