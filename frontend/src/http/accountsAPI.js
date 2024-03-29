import {$authHost} from "./index";
import {getUserIdFromJWT} from "./userAPI";


export const getAllAccounts = async () => {
    const userId = getUserIdFromJWT()
    const {data} = await $authHost.get(`/api/v1/budget/users/${userId}/accounts/`)
    return data
}

export const getAccount = async (accountId) => {
    const {data} = await $authHost.get(`/api/v1/budget/accounts/${accountId}/`)
    return data
}

export const patchAccount = async (accountId, dataToUpdate) => {
    const {data} = await $authHost.patch(`/api/v1/budget/accounts/${accountId}/`, dataToUpdate)
    return data
}

export const createAccount = async (accountData) => {
    const {data} = await $authHost.post(`/api/v1/budget/accounts/`, accountData)
    return data
}