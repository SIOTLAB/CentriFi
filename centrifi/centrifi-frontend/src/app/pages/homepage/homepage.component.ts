import { Component, OnInit } from '@angular/core';
import { DataService } from '../../shared/data.service';
import { NetworkInfo, APInfo } from 'src/app/shared/network-info';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {

  // Flags
  infoRecieved = true;
  
  // Raw data
  networkInfo: NetworkInfo;


  //
  // On component creation, initial setup
  //
  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.getNetworkInfo().subscribe((response)=>{
      let data = response.body;
      
      this.networkInfo = <NetworkInfo> data;
    },
    error=>{
      this.infoRecieved = false;
      console.error("Cannot make request");
    });
  }


  //
  // React to user input
  //

  clickCFPassword(){
    this.dataService.goToCFPasswordPage();
  }
  
  clickWifiSettings(){
    this.dataService.goToWifiSettingsPage();
  }

  clickNetworkStatistics(){
    this.dataService.goToStatsPage();
  }
  clickEndDevice(){
    this.dataService.goToEndDevicePage();
  }
}
