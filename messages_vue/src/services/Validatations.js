export default class Validatations {
    static checkUsername(username) {
        return username !== 'Admin01';
    }

    static minUsernameLength(username) {
        return username.length >= 2;
    }

    static checkEmail(email) {
        return /\S+@\S+\.\S+/.test(email.toLowerCase());
    }

    static minLength(password, minLength) {
        return password.length >= minLength;
    }

    static checkCampaignStartDate(startAt, finishAt) {
        return finishAt > startAt;
    }

    static checkCampaignFinishDate(finishAt) {
        let now = new Date()
        return finishAt > now.toISOString();
    }

    static checkCustomerPhoneLength(phone) {
        return phone.length === 11;
    }

    static checkCustomerPhoneDigit(phone) {
        return /\d/.test(phone);
    }

    static checkCustomerTimeZone(timeZone) {
        return timeZone.length > 2;
    }
}
