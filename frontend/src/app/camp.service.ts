import { Injectable } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from '../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class CampService {

  constructor(private route: ActivatedRoute) { }


  getInputFields() {
    return fetch(environment.url + '/inputfields', {
      headers: this.getHeaders(),
    });
  }

  setInputFields(data: any) {
    return fetch(environment.url + '/inputs', {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ 'data': data })
    });
  }


  getHeaders() : any {
    return {
      'Content-Type': 'application/json',
    }
  }

  generateOutput(){
    return fetch(environment.url + '/outputs', {
      headers: this.getHeaders(),
    });
    
  }


  displayChart(){
    return fetch(environment.url + '/chart', {
      headers: this.getHeaders(),
    });
    
  }

// // displays data

//   displayOutput(data: any){

//     return fetch(environment.url + '/outputs', {
//       method: 'POST',
//       headers: this.getHeaders(),
//       body: JSON.stringify({ 'data': data })
//     });
//   }

}
