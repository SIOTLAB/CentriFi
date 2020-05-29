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