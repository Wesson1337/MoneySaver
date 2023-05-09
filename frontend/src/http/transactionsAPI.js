import {getUserIdFromJWT} from "./userAPI";
import {$authHost} from "./index";
import {SPENDING_CATEGORIES} from "../utils/consts";


export const getAllTransactions = async (currency, createdAtAfter, createdAtBefore) => {
    const userId = getUserIdFromJWT()
    let response = await $authHost.get(`/api/v1/budget/users/${userId}/incomes/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const incomes_data = response["data"]
    response = await $authHost.get(`/api/v1/budget/users/${userId}/spendings/`,
        {params: {currency: currency, created_at_ge: createdAtAfter, created_at_le: createdAtBefore}})
    const spendings_data = response["data"]
    return {incomes: incomes_data, spendings: spendings_data}
}

export const createTransaction = async (transactionData) => {
    const {data} = await $authHost.post(`/api/v1/budget/${transactionData.replenishment_account_id ? "incomes" : "spendings"}/`, transactionData)
    return data
}

export const transferMoney = async (accountFrom, accountTo, amount) => {
    const userId = getUserIdFromJWT()
    const transactionData = {
        "user_id": userId,
        "category": SPENDING_CATEGORIES.TRANSFERS.nameForRequest,
        "amount": amount,
        "currency": accountFrom.currency,
        "comment": `Transfer from ${accountFrom.name} to ${accountTo.name}`
    }

    const spendingResponse = await createTransaction(Object.assign(transactionData, {"receipt_account_id": accountFrom.id}))
    const incomeResponse = await createTransaction(Object.assign(transactionData, {"replenishment_account_id": accountTo.id}))

    return {spendingResponse: spendingResponse, incomeResponse: incomeResponse}
}

export const patchTransaction = async (transactionId, type, transactionData) => {
    const {data} = await $authHost.patch(`/api/v1/budget/${type === "income" ? "incomes" : "spendings"}/${transactionId}/`, transactionData)
    return data
}

export const deleteTransaction = async (transactionId, type) => {
    const {data} = await $authHost.delete(`/api/v1/budget/${type === "income" ? "incomes" : "spendings"}/${transactionId}/`)
    return data
}