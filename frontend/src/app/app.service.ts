import { Injectable } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ScreenSize } from './screen-size';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  // Screen size detector
  screenSizeSubject = new Subject<ScreenSize>();

  constructor(private http: HttpClient, private route: ActivatedRoute, private breakpointObserver: BreakpointObserver) {
    this.breakpointObserver.observe('[(max-width: 576px),(max-width: 768px),(max-width: 992px),(max-width: 1200px),(max-width: 1400px),(min-width: 1400px)]').subscribe((result) => {
      var screen = new ScreenSize();
      if (result.breakpoints['(max-width: 576px)']) {
        screen.xs = true;
      }
      if (result.breakpoints['(max-width: 768px)']) {
        screen.sm = true;
      }
      if (result.breakpoints['(max-width: 992px)']) {
        screen.md = true;
      }
      if (result.breakpoints['(max-width: 1200px)']) {
        screen.lg = true;
      }
      if (result.breakpoints['(max-width: 1400px)']) {
        screen.xl = true;
      }
      if (result.breakpoints['(min-width: 1400px)']) {
        screen.xxl = true;
      }
      this.screenSizeSubject.next(screen);
    });
  }

  getCurrentScreenSize() {
    var screen = new ScreenSize();
    screen.xs = this.breakpointObserver.isMatched('(max-width: 576px)');
    screen.sm = this.breakpointObserver.isMatched('(max-width: 768px)');
    screen.md = this.breakpointObserver.isMatched('(max-width: 992px)');
    screen.lg = this.breakpointObserver.isMatched('(max-width: 1200px)');
    screen.xl = this.breakpointObserver.isMatched('(max-width: 1400px)');
    screen.xxl = this.breakpointObserver.isMatched('(min-width: 1400px)');
    return screen;
  }

  debounce(func: any, cond: any, timeout: any) {
    if (!cond()) {
      setTimeout(() => {
        this.debounce(func, cond, timeout);
      }, 250);
    } else {
      func();
    }
  }

}