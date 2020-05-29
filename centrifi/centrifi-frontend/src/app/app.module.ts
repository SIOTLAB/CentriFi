import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
// import { CookieService } from "ngx-cookie-service";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { HomepageComponent } from './pages/homepage/homepage.component';
import { MaterialModule } from './material';
import { PageContainerComponent } from './pages/page-container/page-container.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { DataService } from './shared/data.service';
import { CentrifiPasswordPageComponent } from './pages/centrifi-password-page/centrifi-password-page.component';
import { ConfirmPasswordValidatorDirective } from './shared/confirm-password.directive';
import { WifiSettingsPageComponent } from './pages/wifi-settings-page/wifi-settings-page.component';
import { StatisticsPageComponent } from './pages/statistics-page/statistics-page.component';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { DatePipe } from '@angular/common';
import { EndDevicePageComponent } from './pages/end-device-page/end-device-page.component';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    PageContainerComponent,
    LoginPageComponent,
    CentrifiPasswordPageComponent,
    ConfirmPasswordValidatorDirective,
    WifiSettingsPageComponent,
    StatisticsPageComponent,
    EndDevicePageComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    NgxChartsModule
  ],
  providers: [
    DataService,
    DatePipe
    // CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
