import {getUserIdFromJWT} from "./userAPI";
import {$authHost} from "./index";

const userId = getUserIdFromJWT()

export const getAllOperations = async (currency, createdAtAfter, createdAtBefore) => {
    let response = await $authHost.get(`/api/v1/budget/users/${userId}/incomes/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const incomes_data = response["data"]
    response = await $authHost.get(`/api/v1/budget/users/${userId}/spendings/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const spendings_data = response["data"]
    return {incomes: incomes_data, spendings: spendings_data}
}

export const createOperation = async (operationData) => {
    const {data} = await $authHost.post(`/api/v1/budget/${operationData.replenishment_account_id ? "incomes" : "spendings"}/`, operationData)
    return data
}