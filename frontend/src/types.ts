import { HttpContext, HttpHeaders, HttpParams } from '@angular/common/http';

export interface Options {
  headers?:
    | HttpHeaders
    | {
        [header: string]: string | string[];
      };
  observe: 'body';
  context?: HttpContext;
  params?:
    | HttpParams
    | {
        [param: string]:
          | string
          | number
          | boolean
          | ReadonlyArray<string | number | boolean>;
      };
  reportProgress?: boolean;
  responseType?: 'json';
  withCredentials?: boolean;
  transferCache?:
    | {
        includeHeaders?: string[];
      }
    | boolean;
}

export interface Product {
  id: string;
  sku: string;
  name: string;
  qty_in_stock: number;
  price: number;
  image: string | null;
  created_at: string;
  updated_at: string;
  remark: string;
  reviews: any;
}

export interface Products {
  count: number;
  result: Product[];
  metadata: any;
}
