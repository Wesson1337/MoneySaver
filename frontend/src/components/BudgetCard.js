import React, {useEffect, useState} from 'react';
import {Card, Spinner} from "react-bootstrap";
import {convertCurrency} from "../utils/currency";
import {prettifyFloat} from "../utils/prettifyFloat";
import {useNavigate} from "react-router-dom";
import {ACCOUNTS_ROUTE} from "../utils/consts";

const BudgetCard = (props) => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)
    const [isActive, setIsActive] = useState(false)
    const navigate = useNavigate()

    const getTotalBalance = async () => {
        let totalBalance = 0;
        let a
        let accountBalance
        for (let i = 0; i < props.data.accounts.length; i++) {
            a = props.data.accounts[i]
            if (a.is_active) {
                if (a.balance && a.currency !== "USD") {
                    try {
                        accountBalance = await convertCurrency(a.balance, a.currency, "USD")
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
        <Card
            className="w-25 p-3"
            onMouseEnter={() => setIsActive(true)}
            onMouseLeave={() => setIsActive(false)}
            onClick={() => navigate(ACCOUNTS_ROUTE)}
            style={{
                filter: isActive ? "drop-shadow(1px 1px 2px rgba(2, 2, 2, 0.14))" : null,
                transition: "0.25s"
            }}
        >
            <h4>Total balance:</h4>
            {isLoading ? <Spinner variant="border" size="sm" className="m-auto"/> : <h3 style={{color: "rgb(66 131 69)"}}>{`${totalBalance} $`}</h3>}
        </Card>
    );
};

export default BudgetCard;