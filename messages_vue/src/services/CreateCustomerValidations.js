import Validations from "@/services/Validatations";

class CreateCustomerValidations {
    constructor(phone, carrier, tag, tz_name) {
        this.phone = phone;
        this.carrier = carrier;
        this.tag = tag;
        this.timeZone = tz_name;
    }

    checkCreateCustomerValidations() {
        let errors = [];
        if (!Validations.checkCustomerPhoneDigit(this.phone)) {
            errors['phone'] = 'Номер телефона должен содержать только цифры';
        }
        if (!Validations.checkCustomerPhoneLength(this.phone)) {
            errors['phone'] = 'Номер телефона должен содержать 11 цифр';
        }
        if (!Validations.checkCustomerTimeZone(this.timeZone)) {
            errors['timezone'] = 'Часовой пояс должен содержать минимум 3 символа';
        }
        if (!!!this.carrier) {
            errors['carrier'] = 'Выберите мобильного оператора';
        }
        return errors;
    }

    static getErrorMessageDetail(detail) {
        let errorMsg = [];
        for (let key in detail) {
            errorMsg.push(`${key} - ${detail[key]}`);
        }
        return errorMsg.length > 1 ? errorMsg.join(' ') : errorMsg[0];
    }
}

export default CreateCustomerValidations;
