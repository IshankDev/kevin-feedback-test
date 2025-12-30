/** Error handling utilities. */

export interface ApiError {
  detail: string;
  type?: string;
}

export class ApiException extends Error {
  constructor(
    public status: number,
    public detail: string,
    public type?: string
  ) {
    super(detail);
    this.name = 'ApiException';
  }
}

export async function handleApiError(response: Response): Promise<never> {
  let errorDetail = 'An unexpected error occurred';
  let errorType: string | undefined;

  try {
    const errorData: ApiError = await response.json();
    errorDetail = errorData.detail || errorDetail;
    errorType = errorData.type;
  } catch {
    errorDetail = response.statusText || errorDetail;
  }

  throw new ApiException(response.status, errorDetail, errorType);
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof ApiException) {
    return error.detail;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected error occurred';
}

