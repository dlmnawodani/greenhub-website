import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  // constructor(private authService: AuthService) {}

  // login(username: string, password: string) {
  //   this.authService.login(username, password).subscribe((success) => {
  //     if (success) {
  //       // login successful, navigate to another page or show success message
  //       console.log("success")
  //     } else {
  //       // login failed, show error message
  //       console.log("fkd")
  //     }
  //   });
  // }

  loginObj: Login;
  constructor(private http: HttpClient) {
    this.loginObj = new Login();
  }

  onLogin() {
    console.log('uname', this.loginObj.username, 'pw', this.loginObj.password);
    // Check if both username and password are provided
    if (!this.loginObj.username || !this.loginObj.password) {
      console.error('Username and password are required.');
      return;
    }

    this.http
      .post('http://localhost:8000/v1/login/', this.loginObj)
      .subscribe((res: any) => {
        if (res.result) {
          console.log('Login Success');
        } else {
          console.log(res.message);
        }
      });
  }
}

export class Login {
  username: string;
  password: string;
  constructor() {
    this.username = '';
    this.password = '';
  }
}
