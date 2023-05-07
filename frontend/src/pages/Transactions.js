import React, {useEffect, useState} from 'react';
import {Card, Container, Spinner} from "react-bootstrap";
import MonthSelection from "../components/transactions_page/MonthSelection";
import {getAllTransactions} from "../http/transactionsAPI";
import Transaction from "../components/common/Transaction";
import {INCOME_CATEGORIES, SPENDING_CATEGORIES} from "../utils/consts";
import AddTransactionButtons from "../components/common/AddTransactionButtons";
import {getAllAccounts} from "../http/accountsAPI";
import {ErrorComponent} from "../components/common/ErrorComponent";

const Transactions = () => {
    const [month, setMonth] = useState(new Date().getMonth())
    const [errorMsg, setErrorMsg] = useState("")
    const [transactions, setTransactions] = useState({})
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState({})
    const [buttonsAreLoading, setButtonsAreLoading] = useState(true)
    const [transactionHasChanged, setTransactionHasChanged] = useState(false)

    const getData = async () => {
        setButtonsAreLoading(true)
        try {
            return {accounts: await getAllAccounts()}
        } catch (e) {
            setErrorMsg(`${e?.response?.data?.detail || e}`)
        }
    }

    useEffect(() => {
        getData().then(data => {
                if (data) {
                    setButtonsAreLoading(false)
                    setData(data)
                }
            }
        )
    }, [])

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
            }
        })
    }, [month, transactionHasChanged])

    return (
        <>
            <Container>
                <MonthSelection
                    month={month}
                    setMonth={setMonth}
                />
                <Card className="mt-3 p-2 d-flex justify-content-center align-items-center" style={{minHeight: "50px"}}>
                    {
                        isLoading ?
                            <Spinner animation="border"/>
                            :
                            <div className="d-flex flex-column p-1 gap-1 w-100">
                                {transactions.map((t, index) =>
                                    <Transaction
                                        key={`operation-${index}`}
                                        transaction={t}
                                        amountInAccountCurrency={t["amount_in_account_currency_at_creation"]}
                                        type={t["receipt_account"] ? "spending" : "income"}
                                        category={t["receipt_account"] ? SPENDING_CATEGORIES[t["category"]].name : INCOME_CATEGORIES[t["category"]].name}
                                        icon={t["receipt_account"] ? SPENDING_CATEGORIES[t["category"]].icon : INCOME_CATEGORIES[t["category"]].icon}
                                        account={t["receipt_account"] ? t["receipt_account"] : t["replenishment_account"]}
                                        hasChanged={transactionHasChanged}
                                        setHasChanged={setTransactionHasChanged}
                                    />)}
                            </div>
                    }
                </Card>
            </Container>
            {buttonsAreLoading ? null :
            <AddTransactionButtons
                hasChanged={transactionHasChanged}
                setHasChanged={setTransactionHasChanged}
                data={data}
            />
            }
            <ErrorComponent message={errorMsg} onClose={() => {setErrorMsg("")}}/>
        </>
    );
};

export default Transactions;