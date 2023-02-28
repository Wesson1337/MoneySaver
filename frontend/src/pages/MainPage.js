import React, {useEffect, useState} from 'react';
import {useAuth} from "../context/Auth";
import BudgetCard from "../components/BudgetCard";
import {getAllAccounts} from "../http/accountsAPI";
import {Button, Form} from "react-bootstrap";

const MainPage = () => {
    const {user} = useAuth()
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState(null)
    const [accountData, setAccountData] = useState(null)

    const getData = async () => {
        const accounts = await getAllAccounts()
        const operations = await getAllOperations()
        return {accounts: accounts, operations: operations}
    }

    useEffect(() => {
        getData().then(accounts => setData(accounts)).finally(() => setIsLoading(false))
    }, [])

    return (
        <div>
            <h1>{user}</h1>
            <BudgetCard/>
            {data ? data.map((x) => (<div>{x.balance}</div>)) : null}
            <Form>
                <Form.Control/>

                <Button>Create account</Button>
            </Form>
        </div>
    );
};

export default MainPage;