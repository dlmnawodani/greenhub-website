import { Component } from '@angular/core';
import { ProductsService } from '../services/products.service';
import { Products } from '../../types';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  constructor(
    private productsService: ProductsService
  ) {}

  ngOnInit() {
    this.productsService.getProducts('http://localhost:8000/v1/products').subscribe((products: Products) => {
      console.log(products);
    })
  }
}
