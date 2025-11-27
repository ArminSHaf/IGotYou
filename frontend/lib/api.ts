import axios from 'axios';
import type { DiscoveryResponse } from '@/types';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '/api',
  timeout: 30000,
});

export const discoverGems = async (query: string): Promise<DiscoveryResponse> => {
  const { data } = await apiClient.post<DiscoveryResponse>('/discover', {
    searchQuery: query,
  });
  return data;
};
