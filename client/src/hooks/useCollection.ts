import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listCollection, collectCard, removeCollectedCard } from '../api/collection';
import type { CollectCardRequest } from '../api/types';

const COLLECTION_KEY = ['collection'] as const;

export function useCollection() {
  return useQuery({ queryKey: COLLECTION_KEY, queryFn: listCollection });
}

export function useCollectCard() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: CollectCardRequest) => collectCard(request),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: COLLECTION_KEY }),
  });
}

export function useRemoveCollectedCard() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (collectedCardId: string) => removeCollectedCard(collectedCardId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: COLLECTION_KEY }),
  });
}
