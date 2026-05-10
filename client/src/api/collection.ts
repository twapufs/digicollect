import { apiClient } from './client';
import type { CollectedCardResponse, CollectCardRequest } from './types';

export async function listCollection(): Promise<CollectedCardResponse[]> {
  const { data } = await apiClient.get<CollectedCardResponse[]>('/collection/');
  return data;
}

export async function collectCard(request: CollectCardRequest): Promise<CollectedCardResponse> {
  const { data } = await apiClient.post<CollectedCardResponse>('/collection/', request);
  return data;
}

export async function removeCollectedCard(collectedCardId: string): Promise<void> {
  await apiClient.delete(`/collection/${collectedCardId}`);
}
