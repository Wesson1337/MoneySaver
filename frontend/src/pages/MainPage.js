import React, {useEffect, useState} from 'react';
import {useAuth} from "../context/Auth";
import {getAllAccounts} from "../http/accountsAPI";
import {Container, Spinner} from "react-bootstrap";
import {ErrorComponent} from "../components/ErrorComponent";
import BudgetCard from "../components/main_page/BudgetCard";
import MonthOperationsCard from "../components/main_page/MonthOperationsCard";
import {getAllOperations} from "../http/operationsAPI";

const MainPage = () => {
    const {user} = useAuth()
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState(null)
    const [accountData, setAccountData] = useState(null)
    const [errorMsg, setErrorMsg] = useState(null)

    const getData = async () => {
        const accounts = await getAllAccounts()
        let currentDate = new Date()
        const firstDayOfPreviousMonth = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth() - 1,
            1, 3).toISOString().replace("Z", "")
        currentDate = currentDate.toISOString().replace("Z", "")
        const operations = await getAllOperations(
            null,
            firstDayOfPreviousMonth,
            currentDate
        )
        return {operations: operations, accounts: accounts}
    }

    useEffect(() => {
        getData().then(data => {
            setData(data)
        }).finally(() => setIsLoading(false))
    }, [])

    return (<>
            {isLoading
                ?
                <Spinner
                    variant="border"
                    style={{position: 'absolute', top: window.innerHeight / 2 - 56, left: '50%'}}
                />
                :
                <Container>
                    <ErrorComponent message={errorMsg} onClose={() => setErrorMsg(null)}/>
                    <h1>{user}</h1>
                    <BudgetCard data={data} setErrorMsg={setErrorMsg}/>
                    <MonthOperationsCard month="this-month" data={data} setErrorMsg={setErrorMsg}/>
                    <MonthOperationsCard month="previous-month" data={data} setErrorMsg={setErrorMsg}/>
                </Container>}
        </>
    );
};

export default MainPage;