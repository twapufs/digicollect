export type Rarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
export type Role = 'admin' | 'collector';

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: string;
  username: string;
  role: Role;
}

export interface RegisterRequest {
  username: string;
  password: string;
  role?: Role;
  admin_key?: string | null;
}

export interface MasterCardResponse {
  id: string;
  title: string;
  symbol: string;
  rarity: Rarity;
  description: string;
  quantity: number;
  available_quantity: number;
}

export interface CreateMasterCardRequest {
  title: string;
  symbol: string;
  rarity: Rarity;
  description: string;
  quantity: number;
}

export interface UpdateMasterCardRequest {
  title?: string | null;
  symbol?: string | null;
  rarity?: Rarity | null;
  description?: string | null;
  quantity?: number | null;
}

export interface CollectedCardResponse {
  id: string;
  master_card: MasterCardResponse;
  collected_at: string;
}

export interface CollectCardRequest {
  master_card_id: string;
}
