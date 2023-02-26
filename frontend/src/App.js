import React, {useContext, useEffect, useState} from 'react';
import {Route, Routes} from "react-router-dom";
import MainPage from "./pages/MainPage";
import Auth from "./pages/Auth";
import PrivateRoutes from "./utils/PrivateRoutes";
import {ACCOUNTS_ROUTE, LOGIN_ROUTE, MAIN_PAGE_ROUTE, OPERATIONS_ROUTE, REGISTRATION_ROUTE} from "./utils/consts";
import Accounts from "./pages/Accounts";
import Operations from "./pages/Operations";
import {useAuth} from "./context/Auth";
import {check} from "./http/userAPI";
import {Spinner} from "react-bootstrap";
import NavBar from "./components/NavBar";
import AppRouter from "./components/AppRouter";

function App() {
    const {setUser} = useAuth()
    const [loading, setLoading] = useState(true)
    useEffect(() => {
        check().then(email => {
            setUser(email)
        }).finally(() => setLoading(false))
    }, [setUser])

    return (
        loading ? <Spinner animation='border' style={{position: 'absolute', top: '50%', left: '50%'}}/> :
            <div>
                <NavBar/>
                <AppRouter/>
            </div>
  );
}

export default App;