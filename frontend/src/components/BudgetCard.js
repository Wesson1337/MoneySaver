import React, {useEffect, useState} from 'react';
import {Card, Placeholder, Row, Spinner} from "react-bootstrap";
import {convertCurrency} from "../utils/currency";

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
                accountBalance = await convertCurrency(a.balance, a.currency, "USD")
            } else {
                accountBalance = a.balance
            }
            totalBalance += accountBalance
        }
        return totalBalance
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
        <Card>
            {props.data.accounts.map((a) => (
                <Row>
                    <div>{a.name ? a.name : "unnamed"}</div>
                    <div>{a.balance}{a.currency}</div>
                </Row>)
            )}
            <Row>
                <div>Total:</div>
                <div>{isLoading ? <Spinner variant="border" size="sm"/> : `${totalBalance}$`}</div>
            </Row>
        </Card>
        }
        </>
    );
};

export default BudgetCard;