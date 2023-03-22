import axios from "axios";
import {SUPPORTED_CURRENCIES} from "../utils/consts";
import {$authHost} from "./index";

export const getCurrencyRate = async (baseCurrency, desiredCurrency) => {
    if (!(baseCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Base currency is not supported in app")
    }
    if (!(desiredCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Desired currency is not supported in app")
    }
    const {data} = await $authHost.get(`/api/v1/currency/`, {params: {base_currency: baseCurrency, desired_currency: desiredCurrency}})
    return data
}