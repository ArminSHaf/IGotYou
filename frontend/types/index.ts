export interface DiscoveryQuery {
  searchQuery: string;
}

export interface Coordinates {
  lat: number;
  lng: number;
}

export interface Analysis {
  whySpecial: string;
  bestTime: string;
  insiderTip: string;
}

export interface HiddenGem {
  placeName: string;
  address: string;
  coordinates: Coordinates;
  rating: number;
  reviewCount: number;
  photos: string[];
  analysis: Analysis;
}

export interface DiscoveryResponse {
  gems: HiddenGem[];
  processingTime: number;
  query: string;
}
