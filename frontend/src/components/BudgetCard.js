import React, {useEffect, useState} from 'react';
import {Spinner} from "react-bootstrap";
import {convertCurrency} from "../utils/currency";
import {prettifyFloat} from "../utils/prettifyFloat";
import MainPageCard from "./MainPageCard";
import {ACCOUNTS_ROUTE, INTERFACE_COLORS, SUPPORTED_CURRENCIES} from "../utils/consts";

const BudgetCard = (props) => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)

    const getTotalBalance = async () => {
        let totalBalance = 0;
        let a
        let accountBalance
        for (let i = 0; i < props.data.accounts.length; i++) {
            a = props.data.accounts[i]
            if (a["is_active"]) {
                if (a["balance"] && a.currency !== "USD") {
                    try {
                        accountBalance = await convertCurrency(a["balance"], a.currency, SUPPORTED_CURRENCIES.USD, props.data.latestExchangeRates)
                    } catch (e) {
                        props.setErrorMsg(`${e}`)
                    }
                } else {
                    accountBalance = a["balance"]
                }
                totalBalance += accountBalance
            }
        }
        return totalBalance.toFixed(2)
    }


    useEffect(() => {
        getTotalBalance().then(totalBalance => setTotalBalance(prettifyFloat(totalBalance))).finally(() => setIsLoading(false))
    }, [])

    return (
        <MainPageCard navigateto={ACCOUNTS_ROUTE} className="d-flex justify-content-around" id="budget-card">
            <h4 className="m-0 text-nowrap">Total balance:</h4>
            {isLoading
                ?
                <Spinner variant="border" size="sm" className="m-auto"/>
                :
                <h2 className="m-0 mt-1 text-nowrap" style={{color: INTERFACE_COLORS.GREEN}}>{`${totalBalance} $`}</h2>}
        </MainPageCard>
    );
};

export default BudgetCard;