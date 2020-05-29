import { MatButtonModule } from '@angular/material/button';
import { MatRadioModule } from '@angular/material/radio';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { NgModule } from '@angular/core';


@NgModule({
  imports: [
    MatButtonModule,
    MatRadioModule,
    MatInputModule,
    MatListModule,
    MatIconModule
  ],  
  exports: [
    MatButtonModule,
    MatRadioModule,
    MatInputModule,
    MatListModule,
    MatSelectModule,
    MatIconModule
  ]
})

export class MaterialModule {

}