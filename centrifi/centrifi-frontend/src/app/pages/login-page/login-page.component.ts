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

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  password = null;
  loggedIn = false;
  unreachedServer = false;
  incorrectPassword = false;


  //
  // On component creation, initial setup
  //
  constructor(public dataService: DataService) { }

  ngOnInit(): void {
    
  }


  //
  // React to user input
  //

  onLogin(){
    // Bypasses login for local testing 
    if(this.dataService.localTesting){
      this.dataService.currentPage = this.dataService.homePage;
    }
    else{
      this.dataService.login(this.password).subscribe((response)=>{
        
        this.resetBannerFlags();
        this.loggedIn = true;

        setTimeout(() =>{
          this.dataService.currentPage = this.dataService.homePage;
        },1000);
      },
      error=>{
        console.log(error)
        if(error.status === 403){
          this.resetBannerFlags();
          this.incorrectPassword = true;
        }
        else{
          console.error("Cannot make request");
          this.resetBannerFlags();
          this.unreachedServer = true;  
        }
      });
    }

  }

  //
  // Helper functions
  //

  resetBannerFlags(){
    this.incorrectPassword = false;
    this.unreachedServer = false;
    this.loggedIn = false;
  }

}
