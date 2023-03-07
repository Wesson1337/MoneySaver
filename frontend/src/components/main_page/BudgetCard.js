import React, {useEffect, useState} from 'react';
import {Spinner} from "react-bootstrap";
import {convertCurrency} from "../../utils/currency";
import {prettifyFloat} from "../../utils/prettifyFloat";
import MainPageCard from "./MainPageCard";
import {ACCOUNTS_ROUTE, SUPPORTED_CURRENCIES} from "../../utils/consts";

const BudgetCard = (props) => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)

    const getTotalBalance = async () => {
        let totalBalance = 0;
        let a
        let accountBalance
        for (let i = 0; i < props.data.accounts.length; i++) {
            a = props.data.accounts[i]
            if (a.is_active) {
                if (a.balance && a.currency !== "USD") {
                    try {
                        accountBalance = await convertCurrency(a.balance, a.currency, SUPPORTED_CURRENCIES.USD, props.data.latestExchangeRates)
                    } catch (e) {
                        props.setErrorMsg(`${e}`)
                    }
                } else {
                    accountBalance = a.balance
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
        <MainPageCard navigateTo={ACCOUNTS_ROUTE}>
            <h4>Total balance:</h4>
            {isLoading
                ?
                <Spinner variant="border" size="sm" className="m-auto"/>
                :
                <h3 style={{color: "rgb(66 131 69)"}}>{`${totalBalance} $`}</h3>}
        </MainPageCard>
    );
};

export default BudgetCard;