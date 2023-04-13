import {getCurrencyRate} from "../http/currencyAPI";
import {SUPPORTED_CURRENCIES} from "./consts";

export const convertCurrency = async (amount, baseCurrency, desiredCurrency) => {
    if (!(baseCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Base currency is not supported in app")
    }
    if (!(desiredCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Desired currency is not supported in app")
    }
    if (baseCurrency === desiredCurrency || amount === 0) {
        return amount
    }
    let rate
    const cachedRate = JSON.parse(localStorage.getItem(`${baseCurrency}-${desiredCurrency}`))
    if (cachedRate && cachedRate["exp"] >= Math.floor(Date.now() / 1000)) {
        rate = cachedRate["rate"]
    } else {
        rate = await getCurrencyRate(baseCurrency, desiredCurrency)
        localStorage.setItem(`${baseCurrency}-${desiredCurrency}`, JSON.stringify(
            {
                rate: rate,
                exp: Math.floor(new Date(Date.now() + 60 * 60 * 1000).getTime() / 1000)
            }))
    }
    return amount * rate
}