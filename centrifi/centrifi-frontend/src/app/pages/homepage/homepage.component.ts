/*
  This file is part of CentriFi.

  CentriFi is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  CentriFi is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with CentriFi.  If not, see <https://www.gnu.org/licenses/>.
*/

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
