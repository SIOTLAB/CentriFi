import { Component, OnInit } from '@angular/core';
import { DataService } from '../../shared/data.service';
import { FormControl, FormGroup, FormArray, Validators } from '@angular/forms';
import { NetworkInfo } from 'src/app/shared/network-info';
import { GetEndDeviceList } from 'src/app/shared/get-end-device-list';
import { SetEndDeviceList, Device} from 'src/app/shared/set-end-device-list';

interface NetworkAreaOption{
  formControlValue: string;
  jsonValue: string;
}

@Component({
  selector: 'app-end-device-page',
  templateUrl: './end-device-page.component.html',
  styleUrls: ['./end-device-page.component.css']
})
export class EndDevicePageComponent implements OnInit {

  networkAreaOptions: Array<NetworkAreaOption> = new Array({
    formControlValue: "Whole Network",
    jsonValue: "no"
  });

  // Raw Data and Froms
  networkInfo: NetworkInfo;
  endDeviceList: GetEndDeviceList;
  endDeviceForm: FormGroup;

  // Flags
  formPrepared: boolean = false;
  networkInfoReceived: boolean = true;
  endDeviceInfoReceived: boolean = true;
  saveFailed: boolean = false;
  saveSuccess: boolean = false;

  //
  // On component creation, initial setup
  //
  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.endDeviceForm = new FormGroup({
      'devices': new FormArray([]),
    });
    this.requestNetworkInfo();
  }

  requestNetworkInfo(){
    this.dataService.getNetworkInfo().subscribe((response)=>{
      let data = response.body;
      
      this.networkInfoReceived = true;
      this.networkInfo = <NetworkInfo> data;
      this.createNetworkAreaOptions();
      this.requestEndDevices();
    },
    error=>{
      this.networkInfoReceived = false;
      console.error("Cannot make request");
    });
  }

  createNetworkAreaOptions(){
    this.networkInfo.aps.forEach(ap => {
      this.networkAreaOptions.push({
        formControlValue: this.dataService.getRouterWholeName(this.networkInfo, ap.apIP),
        jsonValue: ap.apIP
      });
    })
  }

  requestEndDevices(){
    this.dataService.getEndDevices().subscribe((response)=>{
      let data = response.body;
      
      this.endDeviceInfoReceived = true;
      this.endDeviceList = <GetEndDeviceList> data;
      this.createFormControls();
      this.formPrepared = true;
    },
    error=>{
      this.endDeviceInfoReceived = false;
      console.error("Cannot make request");
    });
  }

  get devicesFormArray(): FormArray {
    return this.endDeviceForm.get('devices') as FormArray
  }

  createFormControls(){
    this.endDeviceList.devices.forEach(endDevice => {
      let formControl = new FormControl(this.formControlFromJson(endDevice.roamingRestricted), Validators.required);
      this.devicesFormArray.push(formControl);
    });
  }

  jsonFromFormControl(formControlValue: string):string{
    return this.networkAreaOptions.find(option =>
      option.formControlValue === formControlValue
    ).jsonValue;
  }

  formControlFromJson(jsonValue: string):string{
    return this.networkAreaOptions.find(option =>
      option.jsonValue === jsonValue
    ).formControlValue;
  }
  
  
  //
  // React to user input data
  //

  onSave(){
    if(this.endDeviceForm.valid){
      let settings:SetEndDeviceList = {devices: []}

      for(let i = 0; i < this.devicesFormArray.length; i++){
        let device:Device = { 
          deviceMAC: this.endDeviceList.devices[i].deviceMAC,
          roamingRestricted: this.jsonFromFormControl(this.devicesFormArray.at(i).value)
        }
        settings.devices.push(device);
      };
      
      this.dataService.setEndDevices(settings).subscribe((response)=>{
        let data = response.body;
        
        this.resetBannerFlags();
        this.saveSuccess = true;
        setTimeout(() => {this.saveSuccess = false},4000);
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
    // this.endDeviceInfoReceived and networkInfoReceived intentionally left out
    this.saveFailed = false;
    this.saveSuccess = false;
  }

}