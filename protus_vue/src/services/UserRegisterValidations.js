import Validations from './Validations';

class UserRegisterValidations {
    constructor(email, password) {
        this.email = email;
        this.password = password;
    }

    checkUserRegisterValidations() {
        let errors = [];
        if (!Validations.checkUserEmail(this.email)) {
            errors['email'] = 'Недопустимый адрес электронной почты';
        }
        if (!Validations.checkEmail(this.email)) {
            errors['email'] = 'Некорректный email';
        }
        if (!Validations.minLength(this.password, 6)) {
            errors['password'] = 'Минимальная длина пароля 6 символов'
        }
        return errors;
    }

    static getErrorMessageDetail(detail) {
        let errorMsg = [];
        if (typeof detail == "object") {
            for (let key in detail) {
                errorMsg.push(`${detail[key]}`)
            }
        } else if (typeof detail == "string") {
            errorMsg.push(detail)
        }
        return errorMsg.length > 1 ? errorMsg.join(' ') : errorMsg[0];
    }
}

export default UserRegisterValidations;