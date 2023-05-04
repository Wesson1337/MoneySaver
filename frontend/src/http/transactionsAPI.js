import {getUserIdFromJWT} from "./userAPI";
import {$authHost} from "./index";
import {SPENDING_CATEGORIES} from "../utils/consts";

const userId = getUserIdFromJWT()

export const getAllTransactions = async (currency, createdAtAfter, createdAtBefore) => {
    let response = await $authHost.get(`/api/v1/budget/users/${userId}/incomes/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const incomes_data = response["data"]
    response = await $authHost.get(`/api/v1/budget/users/${userId}/spendings/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const spendings_data = response["data"]
    return {incomes: incomes_data, spendings: spendings_data}
}

export const createTransaction = async (operationData) => {
    const {data} = await $authHost.post(`/api/v1/budget/${operationData.replenishment_account_id ? "incomes" : "spendings"}/`, operationData)
    return data
}

export const transferMoney = async (accountFrom, accountTo, amount) => {
    const operationData = {
        "user_id": userId,
        "category": SPENDING_CATEGORIES.TRANSFERS.nameForRequest,
        "amount": amount,
        "currency": accountFrom.currency,
        "comment": `Transfer from ${accountFrom.name} to ${accountTo.name}`
    }

    const spendingResponse = await createTransaction(Object.assign(operationData, {"receipt_account_id": accountFrom.id}))
    const incomeResponse = await createTransaction(Object.assign(operationData, {"replenishment_account_id": accountTo.id}))

    return {spendingResponse: spendingResponse, incomeResponse: incomeResponse}
}