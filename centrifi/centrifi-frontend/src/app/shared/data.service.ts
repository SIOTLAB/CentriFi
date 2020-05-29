import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { WifiSettings } from './wifi-settings';
import { NetworkInfo } from './network-info';
import { SetEndDeviceList } from './set-end-device-list';

const baseURL: string = "http://192.168.1.1:8000"

@Injectable({
  providedIn: 'root'
})
export class DataService {
  localTesting: boolean = false;

  // Page names
  readonly loginPage = "Login";
  readonly homePage = "Home Page";
  readonly cfPasswordPage = "Change Centrifi Password";
  readonly wifiSettingsPage = "WiFi Settings";
  readonly statsPage = "Network Statistics"
  readonly endDevicePage = "Connected Device Configuration"
  readonly illegalCharacters = '[a-zA-Z0-9!@#$%^&()_+-=`~:;,.<>/?{}\\[\\]\*]*';
  readonly passwordNotice = "Passwords can only have lowercase and uppercase letters, number, and the following special characters:  ?!@#$%^&*_+-=:;,.`~(){}[]<>"

  currentPage = this.loginPage;

  constructor(private http: HttpClient) { }


  //
  // HTTP request functions
  //
  login(typedPassword: string){
    return this.http.post(
      baseURL + '/api/login',
      {
        username: 'root',
        password: typedPassword
      },
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }

  getNetworkInfo(){
    return this.http.get(
      (this.localTesting ? '/assets/network-info.json': baseURL + '/api/list-network-info'),
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }

  getNetworkStatistics(){
    return this.http.get(
      (this.localTesting ? '/assets/network-stats.json': baseURL + '/api/network-statistics'),
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }


  changeCentriFiPassword(currPassword: string, newPassword: string){
    return this.http.post(
      baseURL + '/api/set-router-passwords',
      {
        currPassword: currPassword,
        newPassword: newPassword
      },
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }


  getWifiSettings(){
    
    return this.http.get(
      (this.localTesting ? '/assets/wifi-settings.json' : baseURL + '/api/get-wifi-settings'),
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }

  saveWifiSettings(settings:WifiSettings){
    return this.http.post(
      baseURL + '/api/set-wifi-settings',
      settings,
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }

  getEndDevices(){
    return this.http.get(
      (this.localTesting ? '/assets/end-device-list.json' : baseURL + '/api/list-end-devices'),
     {
       responseType: 'json',
       observe: 'response'
     }
   )
 }

  setEndDevices(deviceList: SetEndDeviceList){
    return this.http.post(
      baseURL + '/api/set-end-devices',
      deviceList,
      {
        responseType: 'json',
        observe: 'response'
      }
    )
  }


  //
  // Cross-component helper function
  //
  getRouterWholeName(networkInfo: NetworkInfo, ipAddress:string):string{
    console.log(networkInfo);
    let routerInfo = networkInfo.aps.find(element => element.apIP === ipAddress);
    
    // Should return something like "192.168.1.1 (Netgear)"
    return routerInfo.apIP + " (" + routerInfo.apType + ")";
  }

  public omit_special_char(e: any) {
    try {
        if (/[a-zA-Z0-9!@#$%^&*()_+-=`~{}[\]:;,.<>\/?]/.test(e.key)) {
            return true;
        }
        else {
            e.preventDefault();
            return false;
        }
    } catch (e) {
    }
  }

  
  //
  // Navigate to page
  //
  goToCFPasswordPage(){
    this.currentPage = this.cfPasswordPage;
  }

  goToWifiSettingsPage(){
    this.currentPage = this.wifiSettingsPage
  }

  goToHomePage(){
    this.currentPage = this.homePage;
  }

  goToStatsPage(){
    this.currentPage = this.statsPage;
  }

  goToEndDevicePage(){
    this.currentPage = this.endDevicePage;
  }
}
