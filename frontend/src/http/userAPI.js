import {$authHost, $host} from "./index";
import jwtDecode from "jwt-decode"
export const registration = async (email, password1, password2) => {
    const {data} = await $host.post('/api/v1/users/', {email: email, password1: password1, password2: password2})
    return await login(data.email, password1)
}

export const login = async (email, password) => {
    const loginFormData = new FormData();
    loginFormData.append('username', email)
    loginFormData.append('password', password)
    const {data} = await $host.post('/api/v1/token/', loginFormData)
    localStorage.setItem('token', data.access_token)
    return jwtDecode(data.access_token)
}

export const logout = () => {
    localStorage.setItem('token', null)
}

export const check = async () => {
    const {data} = await $authHost.get('/api/v1/users/me/')
    return data.email
}

export const getUserIdFromJWT = () => {
    const token = localStorage.getItem('token')
    return token ? jwtDecode(token).sub : null
}