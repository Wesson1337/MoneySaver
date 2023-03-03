import React, {useEffect, useState} from 'react';
import {Card, Col, Container, Placeholder, Row, Spinner} from "react-bootstrap";
import {convertCurrency} from "../utils/currency";
import {CURRENCIES_AND_SYMBOLS} from "../utils/consts";

const BudgetCard = (props) => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)

    const getTotalBalance = async () => {
        let totalBalance = 0;
        for (let i = 0; i < props.data.accounts.length; i++) {
            let a = null
            a = props.data.accounts[i]
            let accountBalance = 0
            if (a.balance && a.currency !== "USD") {
                try {
                    accountBalance = await convertCurrency(a.balance, a.currency, "USD")
                }
                catch (e) {
                    props.setErrorMsg(`${e}`)
                }
            } else {
                accountBalance = a.balance
            }
            totalBalance += accountBalance
        }
        return totalBalance.toFixed(2)
    }
    
    const prettifyFloat = (num) => {
        let parts = num.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
        return parts.join(".");
    }

    useEffect(() => {
        getTotalBalance().then(totalBalance => setTotalBalance(totalBalance)).finally(() => setIsLoading(false))
    }, [])

    return (
        <>
        {!props.data.accounts
        ?
        <Card><h1>There's not active accounts yet</h1></Card>
        :
        <Card className="w-50">
            {props.data.accounts.map((a) => (
                <Container className="d-flex justify-content-between">
                    <div>{a.name ? a.name : "Unnamed account"}</div>
                    <div>{prettifyFloat(a.balance)} {CURRENCIES_AND_SYMBOLS[a.currency]}</div>
                </Container>)
            )}
            <Container className="d-flex justify-content-between">
                <div>Total balance:</div>
                <div>{isLoading ? <Spinner variant="border" size="sm"/> : `${prettifyFloat(totalBalance)} $`}</div>
            </Container>
        </Card>
        }
        </>
    );
};

export default BudgetCard;