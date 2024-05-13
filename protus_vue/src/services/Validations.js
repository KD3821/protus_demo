export default class Validations {
    static checkUserEmail(email) {
        return email !== 'user@example.com';
    }

    static checkEmail(email) {
        return /\S+@\S+\.\S+/.test(email.toLowerCase());
    }

    static minLength(password, minLength) {
        return password.length >= minLength;
    }

    static minClientNameLength(username) {
        return username.length >= 2;
    }
}