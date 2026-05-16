import {
  HealthCheckResponse,
  ApiError,
  BackendStatus,
  RepositoryIntelligence,
  AnalyzeRepositoryRequest,
  RepositoryAnalysisError
} from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });

    if (!response.ok) {
      // Try to parse error response
      try {
        const errorData = await response.json();
        throw new Error(JSON.stringify(errorData));
      } catch {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`API request failed: ${error.message}`);
    }
    throw new Error('API request failed: Unknown error');
  }
}

/**
 * Check root endpoint (GET /)
 */
export async function checkRootEndpoint(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/`, {
      method: 'GET',
    });
    return response.ok;
  } catch (error) {
    console.error('Root endpoint check failed:', error);
    return false;
  }
}

/**
 * Check docs endpoint (GET /docs)
 */
export async function checkDocsEndpoint(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/docs`, {
      method: 'GET',
    });
    return response.ok;
  } catch (error) {
    console.error('Docs endpoint check failed:', error);
    return false;
  }
}

/**
 * Check health endpoint (GET /api/health)
 */
export async function checkHealthEndpoint(): Promise<HealthCheckResponse | null> {
  try {
    return await fetchAPI<HealthCheckResponse>('/health');
  } catch (error) {
    console.error('Health endpoint check failed:', error);
    return null;
  }
}

/**
 * Comprehensive backend status check
 */
export async function checkBackendStatus(): Promise<BackendStatus> {
  try {
    const [rootOk, docsOk, healthData] = await Promise.all([
      checkRootEndpoint(),
      checkDocsEndpoint(),
      checkHealthEndpoint(),
    ]);

    const isHealthy = rootOk && docsOk && healthData !== null;

    return {
      isHealthy,
      rootEndpoint: rootOk,
      docsEndpoint: docsOk,
      healthEndpoint: healthData !== null,
      error: isHealthy ? undefined : 'One or more endpoints are not responding',
    };
  } catch (error) {
    return {
      isHealthy: false,
      rootEndpoint: false,
      docsEndpoint: false,
      healthEndpoint: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}

/**
 * Get API base URL
 */
export function getApiUrl(): string {
  return API_URL;
}

// Made with Bob

/**
 * Validate GitHub repository URL
 */
export function validateGitHubUrl(url: string): boolean {
  const githubUrlPattern = /^https?:\/\/(www\.)?github\.com\/[\w-]+\/[\w.-]+\/?$/;
  return githubUrlPattern.test(url.trim());
}

/**
 * Analyze repository and get intelligence
 */
export async function analyzeRepository(
  request: AnalyzeRepositoryRequest
): Promise<RepositoryIntelligence> {
  try {
    const response = await fetchAPI<RepositoryIntelligence>(
      '/api/frontend/repository-intelligence',
      {
        method: 'POST',
        body: JSON.stringify(request),
      }
    );
    return response;
  } catch (error) {
    if (error instanceof Error) {
      // Try to parse structured error
      try {
        const errorData = JSON.parse(error.message.replace('API request failed: ', ''));
        throw errorData;
      } catch {
        throw new Error(error.message);
      }
    }
    throw new Error('Failed to analyze repository');
  }
}
