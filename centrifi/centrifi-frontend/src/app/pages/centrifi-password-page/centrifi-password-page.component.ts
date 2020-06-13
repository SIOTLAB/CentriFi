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
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ConfirmPasswordValidator } from 'src/app/shared/confirm-password.directive';

@Component({
  selector: 'app-centrifi-password-page',
  templateUrl: './centrifi-password-page.component.html',
  styleUrls: ['./centrifi-password-page.component.css']
})
export class CentrifiPasswordPageComponent implements OnInit {
  
  // Forms
  passwordForm: FormGroup;

  // Flags
  saveSuccess: Boolean = false;
  saveFailed: Boolean = false;


  //
  // On component creation, initial setup
  //
 
  constructor(public dataService: DataService) { }

  ngOnInit(): void {
    this.passwordForm = new FormGroup({
      'currPassword': new FormControl('', Validators.required), 
      'password': new FormControl('', [Validators.required, Validators.pattern(this.dataService.illegalCharacters)]), 
      'confirmPassword': new FormControl('',  [Validators.required, Validators.pattern(this.dataService.illegalCharacters)]), 
    }, {validators: ConfirmPasswordValidator});
  }

  //
  // React to user input
  //
  onPasswordFinish(){
    if(this.passwordForm.valid){
      this.dataService.changeCentriFiPassword(this.passwordForm.value.currPassword, this.passwordForm.value.password).subscribe((response)=>{
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
  // Helper functions
  // 

  resetBannerFlags(){
    this.saveFailed = false;
    this.saveSuccess = false;
  }

}