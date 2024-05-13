import Validations from './Validatations';

class SignupValidations {
    constructor(username, email, password) {
        this.username = username;
        this.email = email;
        this.password = password;
    }

    checkRegisterValidations() {
        let errors = [];
        if (!Validations.checkUsername(this.username)) {
            errors['username'] = 'Недопустимое имя пользователя';
        }
        if (!Validations.minUsernameLength(this.username)) {
            errors['username'] = 'Минимальная длина имени 2 символа';
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
        for (let key in detail) {
            errorMsg.push(`${key} - ${detail[key]}`)
        }
        return errorMsg.length > 1 ? errorMsg.join(' ') : errorMsg[0];
    }
}

export default SignupValidations;