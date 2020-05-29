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
