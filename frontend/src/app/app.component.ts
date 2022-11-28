import { Component } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { AppService } from './app.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'CAMP_Project';
  burgerOpen: boolean = false;
  url: string = "";
  constructor(private route: ActivatedRoute, private router: Router , private service: AppService) { 
    this.router.events.subscribe((event: any) => {
      if (event instanceof NavigationEnd) {
          this.url = event.url;
      }
    });
  }
}
