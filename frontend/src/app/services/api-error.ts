import { HttpErrorResponse } from '@angular/common/http';

export interface ApiErrorDetail {
    field: string;
    message: string;
    type: string;
}

export interface ApiError {
    status: number;
    message: string;
    errors: ApiErrorDetail[];
}

export function getApiErrorMessage(
    error: HttpErrorResponse,
    fallbackMessage = 'Something went wrong.'
): string {
    console.error('API error:', error);
    const apiError = error.error as ApiError;

    if (!apiError?.message) {
        return fallbackMessage;
    }

    if (apiError.errors?.length) {
        const details = apiError.errors
            .map(detail => `${detail.field}: ${detail.message}`)
            .join(', ');

        return `${apiError.message}: ${details}`;
    }
    return apiError.message;
}