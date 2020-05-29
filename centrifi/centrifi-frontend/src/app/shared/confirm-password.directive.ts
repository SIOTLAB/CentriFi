import { Directive } from '@angular/core';
import { FormGroup, Validator, ValidationErrors, NG_VALIDATORS, AbstractControl, ValidatorFn } from '@angular/forms';

@Directive({
  selector: '[appConfirmPassword]',
  providers: [{
    provide: NG_VALIDATORS,
    useExisting: ConfirmPasswordValidatorDirective,
    multi: true
  }]
})
export class ConfirmPasswordValidatorDirective implements Validator {
  validate(control: AbstractControl): ValidationErrors {
    return ConfirmPasswordValidator(control)
  }
}

export const ConfirmPasswordValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
  const password = control.get('password');
  const confirmPassword = control.get('confirmPassword');

  return password && confirmPassword && password.value === confirmPassword.value ?
    null :  // Form is valid
    { 'mismatch': true }; // ValidationError
};