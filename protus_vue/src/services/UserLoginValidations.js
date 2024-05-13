import Validations from "@/services/Validations";

class UserLoginValidations {
    constructor(email, password) {
        this.email = email;
        this.password = password;
    }

    checkUserLoginValidations() {
        let errors = [];
        if (!Validations.checkEmail(this.email)) {
            errors['email'] = 'Некорректный email';
        }
        if (!Validations.checkUserEmail(this.email)) {
            errors['email'] = 'Недопустимый адрес электронной почты';
        }
        if (!Validations.minLength(this.password, 6)) {
            errors['password'] = 'Минимальная длина пароля 6 символов';
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

export default UserLoginValidations;