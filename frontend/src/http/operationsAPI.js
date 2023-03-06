import {getUserIdFromJWT} from "./userAPI";
import {$authHost} from "./index";

export const getAllOperations = async (currency, createdAtAfter, createdAtBefore) => {
    const userId = getUserIdFromJWT()
    let response = await $authHost.get(`/api/v1/budget/users/${userId}/incomes/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const incomes_data = response["data"]
    response = await $authHost.get(`/api/v1/budget/users/${userId}/spendings/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const spendings_data = response["data"]
    return {incomes: incomes_data, spendings: spendings_data}
}