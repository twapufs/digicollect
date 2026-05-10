import { apiClient } from './client';
import type { MasterCardResponse, CreateMasterCardRequest, UpdateMasterCardRequest } from './types';

export async function listMasterCards(): Promise<MasterCardResponse[]> {
  const { data } = await apiClient.get<MasterCardResponse[]>('/master-cards/');
  return data;
}

export async function getMasterCard(cardId: string): Promise<MasterCardResponse> {
  const { data } = await apiClient.get<MasterCardResponse>(`/master-cards/${cardId}`);
  return data;
}

export async function createMasterCard(request: CreateMasterCardRequest): Promise<MasterCardResponse> {
  const { data } = await apiClient.post<MasterCardResponse>('/master-cards/', request);
  return data;
}

export async function updateMasterCard(
  cardId: string,
  request: UpdateMasterCardRequest,
): Promise<MasterCardResponse> {
  const { data } = await apiClient.patch<MasterCardResponse>(`/master-cards/${cardId}`, request);
  return data;
}

export async function deleteMasterCard(cardId: string): Promise<void> {
  await apiClient.delete(`/master-cards/${cardId}`);
}
