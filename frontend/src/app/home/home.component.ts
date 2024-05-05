import { Component } from '@angular/core';
import { ProductsService } from '../services/products.service';
import { Products, Product } from '../../types';
import { ProductComponent } from '../components/product/product.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ProductComponent, CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  constructor(private productsService: ProductsService) {}

  products: Product[] = [];

  fetchProducts() {
    this.productsService
      .getProducts('http://localhost:8000/v1/products')
      .subscribe({
        next: (data: Products) => {
          this.products = data.result;
        },
        error: (error) => {
          console.log(error);
        },
      });
  }

  editProduct(product: Product, id: number) {
    this.productsService
      .editProduct(`http://localhost:8000/v1/products/${id}`, product)
      .subscribe({
        next: (data) => {
          console.log(data);
          this.fetchProducts();
        },
        error: (error) => {
          console.log(error);
        },
      });
  }
  deleteProduct(id: number) {
    this.productsService
      .deleteProduct(`http://localhost:8000/v1/products/${id}`)
      .subscribe({
        next: (data) => {
          console.log(data);
          this.fetchProducts();
        },
        error: (error) => {
          console.log(error);
        },
      });
  }
  addProduct(product: Product) {
    this.productsService
      .addProduct(`http://localhost:8000/v1/products`, product)
      .subscribe({
        next: (data) => {
          console.log(data);
          this.fetchProducts();
        },
        error: (error) => {
          console.log(error);
        },
      });
  }

  ngOnInit() {
    this.fetchProducts();
  }
}
