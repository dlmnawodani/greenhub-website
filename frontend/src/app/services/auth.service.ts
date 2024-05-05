import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private loginUrl = 'http://localhost:8000/v1/login';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<boolean> {
    console.log('Attempting to login with username:', username);
    console.log('Attempting to login with password:', password);
    console.log('Login URL:', this.loginUrl);
    const body = { username, password };
    return this.http.post<any>(this.loginUrl, body).pipe(
      map((response) => {
        // handle successful login, e.g. set token in local storage or session storage
        localStorage.setItem('token', response.token);
        console.log('Login Successful');
        return true;
      }),
      catchError((error) => {
        // handle login error, e.g. display error message or redirect to error page
        console.error('Login failed:', error);
        return of(false);
      })
    );
  }

  logout() {
    // handle logout, e.g. remove token from local storage or session storage
    localStorage.removeItem('token');
  }

  isLoggedIn(): boolean {
    // check if user is logged in, e.g. check if token exists in local storage or session storage
    return !!localStorage.getItem('token');
  }
}
