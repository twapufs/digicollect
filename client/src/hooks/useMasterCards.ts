import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  listMasterCards,
  getMasterCard,
  createMasterCard,
  updateMasterCard,
  deleteMasterCard,
} from '../api/masterCards';
import type { CreateMasterCardRequest, UpdateMasterCardRequest } from '../api/types';

const MASTER_CARDS_KEY = ['master-cards'] as const;
const masterCardKey = (id: string) => [...MASTER_CARDS_KEY, id] as const;

export function useMasterCards() {
  return useQuery({ queryKey: MASTER_CARDS_KEY, queryFn: listMasterCards });
}

export function useMasterCard(cardId: string) {
  return useQuery({
    queryKey: masterCardKey(cardId),
    queryFn: () => getMasterCard(cardId),
    enabled: !!cardId,
  });
}

export function useCreateMasterCard() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: CreateMasterCardRequest) => createMasterCard(request),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: MASTER_CARDS_KEY }),
  });
}

export function useUpdateMasterCard(cardId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: UpdateMasterCardRequest) => updateMasterCard(cardId, request),
    onSuccess: (updated) => {
      queryClient.setQueryData(masterCardKey(cardId), updated);
      queryClient.invalidateQueries({ queryKey: MASTER_CARDS_KEY });
    },
  });
}

export function useDeleteMasterCard() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (cardId: string) => deleteMasterCard(cardId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: MASTER_CARDS_KEY }),
  });
}
