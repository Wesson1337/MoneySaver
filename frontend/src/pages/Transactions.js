import React, {useEffect, useState} from 'react';
import {Container, Spinner} from "react-bootstrap";
import MonthSelection from "../components/transactions/MonthSelection";
import {getAllTransactions} from "../http/transactionsAPI";
import Transaction from "../components/common/Transaction";
import {INCOME_CATEGORIES, SPENDING_CATEGORIES} from "../utils/consts";

const Transactions = () => {
    const [month, setMonth] = useState(new Date().getMonth())
    const [errorMsg, setErrorMsg] = useState("")
    const [transactions, setTransactions] = useState({})
    const [isLoading, setIsLoading] = useState(true)

    const getMonthTransactions = async () => {
        setIsLoading(true)
        const startDate = new Date()
        const endDate = new Date()
        startDate.setHours(0, 0, 0)
        endDate.setHours(23, 59, 59)
        startDate.setDate(1)
        startDate.setMonth(month)
        endDate.setMonth(month + 1)
        endDate.setDate(0)
        try {
            const {incomes, spendings} = await getAllTransactions(null, startDate, endDate)
            const operationsArray = incomes.concat(spendings)
            operationsArray.sort((a, b) => new Date(b["created_at"]) - new Date(a["created_at"]))
            return operationsArray
        } catch (e) {
            setErrorMsg(`${e?.response?.data?.detail || e}`)
        }
    }

    useEffect(() => {
        getMonthTransactions().then((t) => {
            if (t) {
                setTransactions(t)
                setIsLoading(false)
                console.log(t)
            }
        })
    }, [month])

    return (
        <Container>
            <MonthSelection
                month={month}
                setMonth={setMonth}
            />
            {
                isLoading ?
                    <Spinner animation="border"/>
                    :
                    <>
                        {transactions.map((t, index) =>
                            <Transaction
                                key={`operation-${index}`}
                                amount={t.amount}
                                amountInAccountCurrency={t["amount_in_account_currency_at_creation"]}
                                type={t["receipt_account"] ? "spending" : "income"}
                                category={t["receipt_account"] ? SPENDING_CATEGORIES[t["category"]].name : INCOME_CATEGORIES[t["category"]].name}
                                date={t["created_at"]}
                                icon={t["receipt_account"] ? SPENDING_CATEGORIES[t["category"]].icon : INCOME_CATEGORIES[t["category"]].icon}
                                account={t["receipt_account"] ? t["receipt_account"] : t["replenishment_account"]}
                            />)}
                    </>
            }
        </Container>
    );
};

export default Transactions;