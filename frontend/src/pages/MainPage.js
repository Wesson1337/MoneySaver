import React, {useEffect, useState} from 'react';
import {useAuth} from "../context/Auth";
import {getAllAccounts} from "../http/accountsAPI";
import {Container, Spinner} from "react-bootstrap";
import {ErrorComponent} from "../components/ErrorComponent";
import BudgetCard from "../components/BudgetCard";

const MainPage = () => {
    const {user} = useAuth()
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState(null)
    const [accountData, setAccountData] = useState(null)
    const [errorMsg, setErrorMsg] = useState(null)

    const getData = async () => {
        const accounts = await getAllAccounts()
        return {accounts: accounts}
    }

    useEffect(() => {
        getData().then(data => {console.log(data); setData(data)}).finally(() => setIsLoading(false))
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
            <BudgetCard data={data}/>
        </Container>}
        </>
    );
};

export default MainPage;