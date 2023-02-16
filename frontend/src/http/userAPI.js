import {$host} from "./index";

export const registration = async (email, password1, password2) => {
    return await $host.post('/api/v1/users/', {email, password1, password2})
}

export const login = async (email, password) => {
    const loginFormData = new FormData();
    loginFormData.append('username', email)
    loginFormData.append('password', password)
    console.log(loginFormData)
    return await $host.post('/api/v1/token/', loginFormData)
}

export const check = async () => {
    return null
}
