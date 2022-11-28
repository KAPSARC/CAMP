export class ScreenSize {
    xs : boolean = false; // (max-width: 576px)
    sm : boolean = false; // (min-width: 576px)
    md : boolean = false; // (min-width: 768px)
    lg : boolean = false; // (min-width: 992px)
    xl : boolean = false; // (min-width: 1200px)
    xxl: boolean = false; // (min-width: 1400px)

    isWeb() {
        return !this.md;
    }

    isTablet() {
        return !this.sm && this.md;
    }

    isHandset() {
        return this.sm;
    }


}
