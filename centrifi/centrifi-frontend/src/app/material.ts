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