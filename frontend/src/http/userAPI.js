import {$host} from "./index";

export const registration = async (email, password1, password2) => {
    return await $host.post('/api/v1/users/', {email, password1, password2})
}

export const login = async (email, password) => {
    return await $host.post('/api/v1/token/', {email, password})
}

export const check = async () => {
    return null
}
