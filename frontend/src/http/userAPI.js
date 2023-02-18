import {$host} from "./index";

export const registration = async (email, password1, password2) => {
    const response = await $host.post('/api/v1/users/', {email: email, password1: password1, password2: password2})
    await login(response.data.email, password1)
    return response
}

export const login = async (email, password) => {
    const loginFormData = new FormData();
    loginFormData.append('username', email)
    loginFormData.append('password', password)
    return await $host.post('/api/v1/token/', loginFormData)
}

export const check = async () => {
    return null
}
