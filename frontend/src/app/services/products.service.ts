import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';
import { Products } from '../../types';

@Injectable({
  providedIn: 'root',
})
export class ProductsService {
  constructor(private apiService: ApiService) {}

  getProducts = (url: string, params?: any): Observable<Products> => {
    return this.apiService.get(url, params);
  };
  addProduct = (url: string, body: any): Observable<any> => {
    return this.apiService.post(url, body, { observe: 'body' });
  };
  editProduct = (url: string, body: any): Observable<any> => {
    return this.apiService.put(url, body, { observe: 'body' });
  };
  deleteProduct = (url: string): Observable<any> => {
    return this.apiService.delete(url, { observe: 'body' });
  };
}
