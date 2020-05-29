import { Component, OnInit } from '@angular/core';
import { DataService } from '../../shared/data.service';
import { FormControl, FormGroup, Validators, FormArray } from '@angular/forms';
import { WifiSettings, APSettingInfo } from 'src/app/shared/wifi-settings';
import { newArray } from '@angular/compiler/src/util';
import { NetworkInfo } from 'src/app/shared/network-info';

@Component({
  selector: 'app-wifi-settings-page',
  templateUrl: './wifi-settings-page.component.html',
  styleUrls: ['./wifi-settings-page.component.css']
})
export class WifiSettingsPageComponent implements OnInit {

  readonly channelOptions: Array<number> = [1,2,3,4,5,6,7,8,9,10,11];
  readonly securityOptions: Array<string> = ["WPA2","WPA3"];

  // Raw Data
  wifiData: WifiSettings;
  networkInfo: NetworkInfo;

  // Form
  wifiForm: FormGroup;

  // Flags
  settingsRetrieved: boolean = true;
  networkInfoReceived: boolean = true;
  showPassword: boolean = false;
  saveFailed: boolean = false;
  saveSuccess: boolean = false;

  constructor(public dataService: DataService) { }

  
  //
  // On component creation, initial setup
  //
  
  ngOnInit(): void {
    this.requestNetworkInfo()
  }

  // Will make a network info request followed by a wifi settings request
  requestNetworkInfo(){
    this.dataService.getNetworkInfo().subscribe((response)=>{
      let data = response.body;
      
      this.networkInfoReceived = true;
      this.networkInfo = <NetworkInfo> data;
      this.requestWifiSettings();
    },
    error=>{
      this.networkInfoReceived = false;
      console.error("Cannot make request");
    });
  }

  requestWifiSettings(){
    this.wifiForm = new FormGroup({
      'networkName': new FormControl('', Validators.required),
      'password': new FormControl('', [Validators.required, Validators.pattern(this.dataService.illegalCharacters)]),
      'security': new FormControl('', Validators.required),
      'aps': new FormArray([])
    });

    this.dataService.getWifiSettings().subscribe((response)=>{
      let data = response.body;
      
      this.settingsRetrieved = true;
      this.wifiData = <WifiSettings>data;
      this.createFormControls();
      console.log(this.wifiForm)
    },
    error=>{
      this.settingsRetrieved = false;
      console.error("Cannot make request");
    });
  }


  //
  // Process initial data
  //

  createFormControls(){
    this.wifiForm.controls.networkName.setValue(this.wifiData.networkName);
    this.wifiForm.controls.password.setValue(this.wifiData.password);
    this.wifiForm.controls.security.setValue(this.wifiData.security);

    this.wifiData.aps.forEach(ap => {
      let formControl = new FormControl(ap.channel, Validators.required);
      this.apsFormArray.push(formControl);
    });
  }


  //
  // Getter functions
  //
  get apsFormArray(): FormArray {
    return this.wifiForm.get('aps') as FormArray
  }


  //
  // React to user input
  //

  onTogglePassword(){
    this.showPassword = !this.showPassword;
  }

  onSave(){
    if(this.wifiForm.valid){
      let settings:WifiSettings = {
        networkName: this.wifiForm.value.networkName,
        password: this.wifiForm.value.password,
        security: this.wifiForm.value.security,
        aps: new Array<APSettingInfo>()
      }

      for(let i = 0; i < this.apsFormArray.length; i++){
        let apSetting:APSettingInfo = { 
          apIP: this.wifiData.aps[i].apIP,
          channel: this.apsFormArray.at(i).value
        }
        settings.aps.push(apSetting);
      };

      this.dataService.saveWifiSettings(settings).subscribe((response)=>{
        let data = response.body;
        
        this.resetBannerFlags();
        this.saveSuccess = true;
        setTimeout(() => {this.saveSuccess = false},4000);

        console.log(this.wifiForm)
      },
      error=>{
        this.resetBannerFlags();
        this.saveFailed = true;
        setTimeout(() => {this.saveFailed = false},4000);
      });
    };
  }

  onBack(){
    this.dataService.goToHomePage();
  }

  //
  // Helper funcions
  //

  resetBannerFlags(){
    // this.settingsReceived and networkInfoReceived intentionally left out
    this.saveFailed = false;
    this.saveSuccess = false;
  }
}