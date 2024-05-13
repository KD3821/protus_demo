import Validations from './Validatations';

class CreateCampaignValidations {
    constructor(start_at, finish_at, text, carrier) {
        this.startAt = start_at;
        this.finishAt = finish_at;
        this.text = text;
        this.carrier = carrier;
    }

    checkCreateCampaignValidations() {
        let errors = [];
        if (!Validations.checkCampaignStartDate(this.startAt, this.finishAt)) {
            errors['start'] = 'Дата начала рассылки не может быть позднее даты ее завершения.';
        }
        if (!Validations.checkCampaignFinishDate(this.finishAt)) {
            errors['finish'] = 'Дата завершения рассылки не может быть в прошлом.';
        }
        if (this.text.length < 10) {
            errors['text'] = 'Минимальная длина сообщения - 10 символов.';
        }
        if (!!!this.carrier) {
            errors['carrier'] = 'Выберите мобильного оператора.';
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

export default CreateCampaignValidations;